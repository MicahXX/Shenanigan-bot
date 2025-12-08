import discord
from discord import app_commands
from discord.ext import commands
import os
from openai import OpenAI

client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SayVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="sayvc",
        description="Make the bot join your voice channel and speak"
    )
    @app_commands.describe(text="What do you want the AI to say?")
    async def sayvc(self, interaction: discord.Interaction, text: str):
        try:
            # User must be in a voice channel
            if not interaction.user.voice:
                await interaction.response.send_message("You must be in a voice channel to use this.")
                return

            voice_channel = interaction.user.voice.channel
            await interaction.response.send_message(f"Joining {voice_channel.name}...")

            # Connect bot to VC
            if interaction.guild.voice_client:
                vc = interaction.guild.voice_client
                await vc.move_to(voice_channel)
            else:
                vc = await voice_channel.connect()

            # Generate speech using OpenAI TTS
            audio = client_ai.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=text
            )

            filename = "voice_output_vc.mp3"
            audio.stream_to_file(filename)

            # Play the audio in VC
            if not vc.is_playing():
                vc.play(discord.FFmpegPCMAudio(filename))

        except Exception as e:
            await interaction.followup.send("Failed to speak in voice channel.")
            print("VC Error:", repr(e))


async def setup(bot):
    await bot.add_cog(SayVC(bot))
