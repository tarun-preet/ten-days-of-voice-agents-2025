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
        
        # Make this assistant a friendly barista persona for "Everbean Coffee"
        super().__init__(
            instructions=f"""You are a friendly barista for the coffee brand Everbean Coffee. The user is ordering a drink from you via voice.
            Your goal is to collect the full order by asking clarifying questions until all fields are filled. Maintain a small order state object with the following shape:
            {{
              "drinkType": "string",
              "size": "string",
              "milk": "string",
              "extras": ["string"],
              "name": "string"
            }}

            Ask short, clear clarifying questions (one question at a time) until the user provides values for every field. When a field can have multiple values (like extras), allow the user to add more than one item.

            Once the order is complete, call the tool `save_order` with the final order object (as JSON) so the order is saved. After saving, read back a brief summary in one or two friendly sentences.

            IMPORTANT: Current date and time information:
            - Today is {day_of_week}, {current_date}
            - Current time is approximately {current_time}
            - Always use this date when asked about the current date or today's date.
            """,
        )

    @function_tool
    async def save_order(self, context: RunContext, order: dict):
        """Save a completed order to a JSON file and return the saved path.

        Args:
            order: dict matching the order state schema.
        """
        try:
            orders_dir = Path(os.getcwd()) / "orders"
            orders_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            filename = f"order_{ts}_{order.get('name','guest').replace(' ','_')}.json"
            filepath = orders_dir / filename
            # Ensure extras is a list
            order_copy = {
                "drinkType": str(order.get("drinkType", "")).strip(),
                "size": str(order.get("size", "")).strip(),
                "milk": str(order.get("milk", "")).strip(),
                "extras": list(order.get("extras") or []),
                "name": str(order.get("name", "")).strip(),
                "saved_at": datetime.utcnow().isoformat() + "Z",
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(order_copy, f, indent=2, ensure_ascii=False)
            return {"status": "ok", "path": str(filepath), "order": order_copy}
        except Exception as e:
            logger.exception("Failed to save order")
            return {"status": "error", "error": str(e)}

    # To add tools, use the @function_tool decorator.
    # Here's an example that adds a simple weather tool.
    # You also have to add `from livekit.agents import function_tool, RunContext` to the top of this file
    # @function_tool
    # async def lookup_weather(self, context: RunContext, location: str):
    #     """Use this tool to look up current weather information in the given location.
    #
    #     If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.
    #
    #     Args:
    #         location: The location to look up weather information for (e.g. city name)
    #     """
    #
    #     logger.info(f"Looking up weather for {location}")
    #
    #     return "sunny with a temperature of 70 degrees."


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
