import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_outrageous_message():
    prompt = (
        "Generate one short, ridiculous, outrageous, funny statement."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
    )

    return response.choices[0].message.content
