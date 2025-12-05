import discord
from discord import app_commands
from discord.ext import commands

from .daily_task import daily_task_manager, init_daily_task


class DailyStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        init_daily_task(bot)

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_status",
        description="Check if the daily task is running (Admins only)"
    )
    async def daily_status(self, interaction: discord.Interaction):
        if daily_task_manager.is_running():
            await interaction.response.send_message("Daily messages are ON.")
        else:
            await interaction.response.send_message("Daily messages are OFF.")


async def setup(bot):
    await bot.add_cog(DailyStatus(bot))