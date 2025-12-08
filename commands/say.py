import discord
from discord import app_commands
from discord.ext import commands
import os
from openai import OpenAI

client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="say",
        description="Generate AI voice from text"
    )
    @app_commands.describe(text="What do you want the AI to say?")
    async def say(self, interaction: discord.Interaction, text: str):
        try:
            await interaction.response.send_message("Generating voice...")

            # Generate AI speech
            audio = client_ai.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=text
            )

            filename = "voice_output.mp3"
            audio.with_streaming_response.method(filename)

            # Upload MP3 to Discord
            await interaction.followup.send(
                content="🔊 Here's your AI voice:",
                file=discord.File(filename)
            )

        except Exception as e:
            await interaction.followup.send("Failed to generate voice.")
            print("TTS Error:", e)


async def setup(bot):
    await bot.add_cog(Say(bot))
