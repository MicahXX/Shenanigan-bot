import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager


class DailyEnable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_enable",
        description="Enable the daily outrageous message"
    )
    async def daily_enable(self, interaction: discord.Interaction):
        manager = get_daily_task_manager(self.bot)

        if not manager.is_running():
            manager.start()
            await interaction.response.send_message("Daily messages enabled.")
        else:
            await interaction.response.send_message("Daily messages are already running.")


async def setup(bot):
    await bot.add_cog(DailyEnable(bot))