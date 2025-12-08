import discord
from discord import app_commands
from discord.ext import commands
import os
from openai import OpenAI
import subprocess
import asyncio
import traceback

client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SayVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_vcs = {}  # track VC per guild

    async def auto_disconnect(self, vc: discord.VoiceClient):
        await asyncio.sleep(1)
        while vc.is_connected():
            non_bot_members = [m for m in vc.channel.members if not m.bot]
            if len(non_bot_members) == 0:
                await vc.disconnect()
                print(f"Left VC {vc.channel.name} in guild {vc.guild.name} because nobody is left.")
                self.guild_vcs.pop(vc.guild.id, None)
                break
            await asyncio.sleep(5)  # check every 5 seconds

    @app_commands.command(
        name="sayvc",
        description="Make the bot join your voice channel and speak"
    )
    @app_commands.describe(text="What do you want the AI to say?")
    async def sayvc(self, interaction: discord.Interaction, text: str):
        try:
            if not interaction.user.voice or not interaction.user.voice.channel:
                await interaction.response.send_message(
                    "You must be in a voice channel to use this."
                )
                return

            voice_channel = interaction.user.voice.channel
            vc = interaction.guild.voice_client

            if vc is None:
                await interaction.response.send_message(f"Joining {voice_channel.name}...")
                vc = await voice_channel.connect()
                self.guild_vcs[interaction.guild.id] = vc
            else:
                if vc.channel != voice_channel:
                    await vc.move_to(voice_channel)
                else:
                    await interaction.response.send_message(
                        "Already connected, speaking now...", ephemeral=True
                    )

            mp3_file = "temp_tts.mp3"
            wav_file = "temp_tts.wav"

            # Stream TTS from OpenAI
            with client_ai.audio.speech.with_streaming_response.create(
                    model="gpt-4o-mini-tts",
                    voice="alloy",
                    input=text
            ) as audio_stream:
                audio_stream.stream_to_file(mp3_file)

            subprocess.run(
                ["ffmpeg", "-y", "-i", mp3_file, "-ar", "48000", "-ac", "2", wav_file],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            await asyncio.sleep(0.1)  # ensure VC is ready

            # Play in VC
            if not vc.is_playing():
                vc.play(discord.FFmpegPCMAudio(wav_file))

                while vc.is_playing():
                    await asyncio.sleep(0.1)

            os.remove(mp3_file)
            os.remove(wav_file)

            if vc.guild.id not in self.guild_vcs:
                self.bot.loop.create_task(self.auto_disconnect(vc))
                self.guild_vcs[vc.guild.id] = vc

        except Exception:
            await interaction.followup.send("Failed to speak in voice channel.")
            traceback.print_exc()


async def setup(bot):
    await bot.add_cog(SayVC(bot))