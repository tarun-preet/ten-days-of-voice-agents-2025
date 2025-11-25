import logging
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    RoomOutputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")



class Assistant(Agent):
    def __init__(self) -> None:
        # Get current date and time for the assistant
        current_date = datetime.now().strftime("%B %d, %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        day_of_week = datetime.now().strftime("%A")

        # Read the wellness log
        wellness_log_path = Path(os.getcwd()) / "wellness_log.json"
        past_sessions = []
        if wellness_log_path.exists():
            with open(wellness_log_path, "r", encoding="utf-8") as f:
                try:
                    past_sessions = json.load(f)
                except json.JSONDecodeError:
                    past_sessions = []

        super().__init__(
            instructions=f"""You are a friendly and supportive health and wellness companion. Your goal is to conduct a short daily check-in with the user.

            **Conversation Flow:**

            1.  **Welcome & Mood Check:** Start by asking the user how they're feeling today (mood, energy levels).
            2.  **Reference Past:** Briefly and gently reference their last session. For example: "Last time we talked, you mentioned feeling [past mood]. How does today compare?"
            3.  **Daily Intentions:** Ask what 1–3 simple, practical things they'd like to accomplish today.
            4.  **Grounded Advice:** Offer simple, non-medical advice. Examples:
                *   "That sounds like a great goal. Remember to take it one step at a time."
                *   "Don't forget to take short breaks to stretch or walk around."
                *   "A 5-minute walk can be a nice way to clear your head."
            5.  **Recap & Confirm:** At the end, summarize the user's mood and goals, and ask for confirmation.
            6.  **Save Data:** Call the `save_wellness_log` tool with the session data.

            **Data to Collect (State Object):**
            ```json
            {{
              "mood": "string",
              "energy": "string (e.g., 'low', 'medium', 'high')",
              "objectives": ["string"],
              "summary": "string"
            }}
            ```

            **Important:**
            *   Keep conversations brief and focused.
            *   **Do not** provide medical advice or diagnosis.
            *   Today is {day_of_week}, {current_date}. The current time is {current_time}.
            *   Here are the past sessions to reference: {json.dumps(past_sessions, indent=2)}
            """,
        )

    @function_tool
    async def save_wellness_log(self, context: RunContext, mood: str, energy: str, objectives: list[str], summary: str):
        """Saves the user's wellness check-in data to a JSON file.

        Args:
            mood: The user's self-reported mood.
            energy: The user's self-reported energy level.
            objectives: A list of the user's stated objectives for the day.
            summary: A short summary of the session.
        """
        try:
            log_path = Path(os.getcwd()) / "wellness_log.json"
            
            new_entry = {
                "date": datetime.utcnow().isoformat() + "Z",
                "mood": mood,
                "energy": energy,
                "objectives": objectives,
                "summary": summary,
            }
            
            # Read existing data and append the new entry
            all_entries = []
            if log_path.exists():
                with open(log_path, "r", encoding="utf-8") as f:
                    try:
                        all_entries = json.load(f)
                    except json.JSONDecodeError:
                        all_entries = [] # Start fresh if file is corrupted

            all_entries.append(new_entry)

            # Write data back to the file
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(all_entries, f, indent=2, ensure_ascii=False)
                
            return {"status": "ok", "path": str(log_path)}
        except Exception as e:
            logger.exception("Failed to save wellness log")
            return {"status": "error", "error": str(e)}



def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    logger.info("agent starting....")
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    #- Temporarily disabled to debug
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    agent = Assistant()
    await session.start(
        room=ctx.room,
        agent=agent,
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
