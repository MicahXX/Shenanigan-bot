import os
import asyncio
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_outrageous_message():
    prompt = "Generate one short, ridiculous, extremely outrageous statement."
    return await _run_prompt(prompt)


async def generate_custom_prompt(user_prompt: str):
    return await _run_prompt(user_prompt)


async def _run_prompt(prompt: str):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
    )
    return response.choices[0].message.content