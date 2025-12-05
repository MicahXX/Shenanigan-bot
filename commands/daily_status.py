import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager


class DailyStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_status",
        description="Check if the daily task is running"
    )
    async def daily_status(self, interaction: discord.Interaction):
        manager = get_daily_task_manager(self.bot)

        if manager.is_running():
            await interaction.response.send_message("Daily messages are ON.")
        else:
            await interaction.response.send_message("Daily messages are OFF.")


async def setup(bot):
    await bot.add_cog(DailyStatus(bot))