import discord
from discord import app_commands
from discord.ext import commands
import os
from openai import OpenAI
from io import BytesIO
import subprocess

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
            if not interaction.user.voice:
                await interaction.response.send_message(
                    "You must be in a voice channel to use this."
                )
                return

            voice_channel = interaction.user.voice.channel
            await interaction.response.send_message(f"Joining {voice_channel.name}...")

            # Connect bot to VC
            if interaction.guild.voice_client:
                vc = interaction.guild.voice_client
                await vc.move_to(voice_channel)
            else:
                vc = await voice_channel.connect()

            # Generate TTS MP3 using OpenAI
            audio = client_ai.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=text
            )

            # Stream MP3 bytes into FFmpeg directly, output PCM to Discord
            mp3_bytes = BytesIO()
            audio.stream_to_file(mp3_bytes)
            mp3_bytes.seek(0)

            ffmpeg_audio = discord.FFmpegPCMAudio(
                source=mp3_bytes,
                pipe=True,
                before_options="-nostdin",
                options="-ar 48000 -ac 2"
            )

            if not vc.is_playing():
                vc.play(ffmpeg_audio)
                print("Streaming audio to VC...")

        except Exception as e:
            await interaction.followup.send("Failed to speak in voice channel.")
            print("VC Error:", repr(e))


async def setup(bot):
    await bot.add_cog(SayVC(bot))