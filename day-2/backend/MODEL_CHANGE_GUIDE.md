# How to Change the LLM Model

## Current Configuration

The model is configured in `backend/src/agent.py` at lines 84-86:

```python
llm=google.LLM(
    model="gemini-2.5-flash",
),
```

## Available Gemini Models

You can change the model by modifying the `model` parameter. Here are popular Gemini models:

### Fast Models (Good for real-time voice):
- `"gemini-2.5-flash"` - Current, fastest, good balance (recommended)
- `"gemini-2.0-flash-exp"` - Experimental fast model
- `"gemini-1.5-flash"` - Fast and efficient
- `"gemini-1.5-flash-8b"` - Even faster, smaller model

### More Capable Models (Better quality, slower):
- `"gemini-2.5-pro"` - Most capable, best quality
- `"gemini-1.5-pro"` - High quality, larger context window
- `"gemini-1.5-pro-latest"` - Latest version of Pro

## Examples

### Change to Gemini Pro (Better Quality)
```python
llm=google.LLM(
    model="gemini-2.5-pro",
),
```

### Change to Gemini 1.5 Flash (Faster)
```python
llm=google.LLM(
    model="gemini-1.5-flash",
),
```

## Switching to Other Providers

### Option 1: OpenAI (GPT-4, GPT-4o, etc.)

1. **Install OpenAI plugin** (already included in dependencies):
   ```bash
   # Already in pyproject.toml: livekit-agents[google]
   ```

2. **Add API key to `.env.local`**:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Update imports** in `backend/src/agent.py`:
   ```python
   from livekit.plugins import murf, silero, openai, deepgram, noise_cancellation
   ```

4. **Change LLM configuration**:
   ```python
   llm=openai.LLM(
       model="gpt-4o",  # or "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"
   ),
   ```

### Option 2: Other Providers

You can use any provider supported by LiveKit Agents:
- **Anthropic (Claude)**: `from livekit.plugins import anthropic`
- **Groq**: `from livekit.plugins import groq`
- **Together AI**: `from livekit.plugins import together`
- **Fireworks AI**: `from livekit.plugins import fireworks`
- **xAI (Grok)**: `from livekit.plugins import xai`
- **DeepSeek**: `from livekit.plugins import deepseek`

See full list: https://docs.livekit.io/agents/models/llm/

## Steps to Change Model

1. **Edit** `backend/src/agent.py`
2. **Find** the `llm=` line (around line 84)
3. **Change** the `model` parameter to your desired model
4. **Restart** the backend:
   ```bash
   # Stop current backend (Ctrl+C)
   # Then restart:
   cd backend
   uv run python src/agent.py dev
   ```

## Quick Reference

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `gemini-2.5-flash` | ⚡⚡⚡ | ⭐⭐⭐ | Real-time voice (current) |
| `gemini-1.5-flash` | ⚡⚡⚡ | ⭐⭐ | Fast responses |
| `gemini-2.5-pro` | ⚡⚡ | ⭐⭐⭐⭐⭐ | Complex tasks, best quality |
| `gemini-1.5-pro` | ⚡⚡ | ⭐⭐⭐⭐ | High quality, large context |

## Where to Get the Complete List of Models

### Official Sources

#### 1. **Google Gemini Models** (For your current setup)
- **Official Google Documentation**: https://ai.google.dev/gemini-api/docs/models/gemini
- Lists all available Gemini models with their capabilities
- Includes model versions, context windows, and features

#### 2. **LiveKit Agents Models**
- **LiveKit LLM Overview**: https://docs.livekit.io/agents/models/llm/
- **LiveKit Gemini Plugin**: https://docs.livekit.io/agents/models/llm/plugins/gemini
- Lists all models supported by LiveKit Agents framework

#### 3. **Other Provider Models**

Each provider has their own documentation:
- **OpenAI**: https://platform.openai.com/docs/models
- **Anthropic (Claude)**: https://docs.anthropic.com/claude/docs/models-overview
- **Groq**: https://console.groq.com/docs/models
- **Together AI**: https://docs.together.ai/docs/inference-models
- **DeepSeek**: https://api-docs.deepseek.com/models

### Quick Access Links

| Resource | URL | What You'll Find |
|----------|-----|------------------|
| **Gemini Models (Official)** | https://ai.google.dev/gemini-api/docs/models/gemini | Complete list of all Gemini models |
| **LiveKit LLM Docs** | https://docs.livekit.io/agents/models/llm/ | All supported LLM providers |
| **LiveKit Gemini Plugin** | https://docs.livekit.io/agents/models/llm/plugins/gemini | Gemini-specific configuration |

### Common Gemini Model Names (Reference)

Based on Google's documentation, here are commonly available models:
- `gemini-2.5-pro`
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`
- `gemini-2.0-flash-exp`
- `gemini-2.0-flash-lite`
- `gemini-1.5-pro`
- `gemini-1.5-flash`
- `gemini-1.5-flash-8b`

**Note**: Model availability may vary. Always check the official Google docs for the most current list.

## Notes

- After changing the model, **restart the backend** for changes to take effect
- Make sure you have the correct API key in `.env.local`
- Some models may have different pricing - check Google AI pricing
- For voice agents, faster models usually provide better user experience
- **Always refer to official docs** for the most up-to-date model list

