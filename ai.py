import os
import asyncio
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_outrageous_message():
    return await _run_prompt("Generate one short, ridiculous, extremely outrageous statement.")

async def generate_christmas_message():
    return await _run_prompt("Generate a short, interesting Christmas fact."
                             " It should be accurate, easy to understand,"
                             " and related to Christmas traditions, history, culture,"
                             " or surprising trivia.")

async def generate_custom_prompt(user_prompt: str):
    return await _run_prompt(user_prompt)


async def _run_prompt(prompt: str):
    system_prompt = (
        "You are generating output for Discord. "
        "If the user asks for code, wrap ONLY the code in triple backticks. "
        "If the output is plain text, return plain text with NO code blocks. "
        "Do not add formatting unless necessary."
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

    contains_code = "```" in msg

    if not contains_code and looks_like_code(msg):
        msg = f"```\n{msg}\n```"

    chunks = []
    while len(msg) > 1900:
        split_point = msg.rfind("\n", 0, 1900)
        if split_point == -1:
            split_point = 1900
        chunks.append(msg[:split_point])
        msg = msg[split_point:].lstrip()
    chunks.append(msg)

    if len(chunks) == 1:
        return chunks[0]

    return chunks


def looks_like_code(text: str) -> bool:
    code_keywords = [
        "class ", "def ", "{", "}", ";",
        "public ", "function ", "return ",
        "import ", "const ", "let ", "var "
    ]
    return any(keyword in text for keyword in code_keywords)