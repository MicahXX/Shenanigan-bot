import discord
from discord import app_commands
from discord.ext import commands

from ai import generate_outrageous_message

class Outrageous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="outrageous",
        description="Get a random outrageous statement",
    )
    async def outrageous(self, interaction: discord.Interaction):
        msg = await generate_outrageous_message()
        await interaction.response.send_message(msg)


async def setup(bot):
    await bot.add_cog(Outrageous(bot))
