import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager

class DailyDisable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_disable",
        description="Disable the daily outrageous message"
    )
    async def daily_disable(self, interaction: discord.Interaction):
        manager = get_daily_task_manager(self.bot)
        if manager.is_running():
            manager.stop()
            await interaction.response.send_message("Daily messages disabled.")
        else:
            await interaction.response.send_message("Daily messages were already disabled.")

async def setup(bot):
    await bot.add_cog(DailyDisable(bot))