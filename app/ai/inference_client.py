import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.ai.prompt_builder import build_system_prompt, build_user_prompt

# Initialize the OpenAI client pointing to OpenRouter
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

from typing import AsyncGenerator
import json

async def generate_repurposed_content(source_text: str, platforms: list[str], tone: str, brand_voice_description: str | None = None) -> dict:
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(source_text, platforms, tone, brand_voice_description)

    try:
        response = await client.chat.completions.create(
            model="google/gemma-4-31b-it", # Fallback to standard if unavailable, e.g. "google/gemma-7b-it:free"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        # Sometimes models wrap in markdown even when instructed not to
        if content.startswith("```json"):
            content = content.strip("`").replace("json\n", "", 1)
            
        return json.loads(content)
    except Exception as e:
        raise Exception(f"AI Generation Failed: {str(e)}")

async def stream_repurposed_content(source_text: str, platforms: list[str], tone: str, brand_voice_description: str | None = None) -> AsyncGenerator[str, None]:
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(source_text, platforms, tone, brand_voice_description)

    try:
        response = await client.chat.completions.create(
            model="google/gemma-4-31b-it", # Fallback to standard if unavailable
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        raise Exception(f"AI Streaming Generation Failed: {str(e)}")

