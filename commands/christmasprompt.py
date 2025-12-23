import discord
from discord import app_commands
from discord.ext import commands

from ai import generate_christmas_message

class Christmas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="christmas",
        description="Get a random christmas fact"
    )
    async def christmas(self, interaction: discord.Interaction):
        try:
            msg = await generate_christmas_message()
            await interaction.response.send_message(msg)
        except Exception as e:
            await interaction.response.send_message("Failed to generate christmas message!")
            print("Error generating message:", e)


async def setup(bot):
    await bot.add_cog(Christmas(bot))
