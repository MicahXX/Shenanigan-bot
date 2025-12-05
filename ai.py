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
    system_prompt = (
        "You are generating output for Discord. "
        "If the user asks for code, ALWAYS wrap it in triple backticks. "
        "Avoid broken markdown. Format cleanly."
    )

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
        )
    )

    msg = response.choices[0].message.content.strip()

    if "```" not in msg:
        msg = f"```\n{msg}\n```"

    chunks = []
    while len(msg) > 2900:
        split_point = msg.rfind("\n", 0, 2900)
        if split_point == -1:
            split_point = 2900
        chunks.append(msg[:split_point])
        msg = msg[split_point:].lstrip()
    chunks.append(msg)

    return chunks