import discord
from discord import app_commands
from discord.ext import commands

from ai import generate_christmastree_message

class Christmastree(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="christmastree",
        description="Get a Christmas Tree"
    )
    async def christmastree(self, interaction: discord.Interaction):
        try:
            msg = await generate_christmastree_message()
            await interaction.response.send_message(msg)
        except Exception as e:
            await interaction.response.send_message("Failed to generate christmas tree message!")
            print("Error generating message:", e)


async def setup(bot):
    await bot.add_cog(Christmastree(bot))
