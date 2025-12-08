import discord
from discord import app_commands
from discord.ext import commands
import os
from openai import OpenAI
import subprocess
import asyncio

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

            mp3_file = "temp_tts.mp3"
            wav_file = "temp_tts.wav"

            with client_ai.audio.speech.with_streaming_response.create(
                    model="gpt-4o-mini-tts",
                    voice="alloy",
                    input=text
            ) as audio_stream:
                audio_stream.stream_to_file(mp3_file)

            subprocess.run([
                "ffmpeg", "-y", "-i", mp3_file,
                "-ar", "48000", "-ac", "2", wav_file
            ], check=True)

            # Play WAV in VC
            if not vc.is_playing():
                vc.play(discord.FFmpegPCMAudio(wav_file))
                print(f"Playing audio in VC: {wav_file}")

                # Wait until playback finishes
                while vc.is_playing():
                    await asyncio.sleep(0.1)

            # Cleanup temp files
            os.remove(mp3_file)
            os.remove(wav_file)

        except Exception as e:
            await interaction.followup.send("Failed to speak in voice channel.")
            print("VC Error:", repr(e))


async def setup(bot):
    await bot.add_cog(SayVC(bot))