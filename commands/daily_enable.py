import discord
from discord import app_commands
from discord.ext import commands

from .daily_task import daily_task_manager, init_daily_task


class DailyEnable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        init_daily_task(bot)

    @app_commands.command(
        name="daily_enable",
        description="Enable the daily outrageous message task"
    )
    async def daily_enable(self, interaction: discord.Interaction):
        if not daily_task_manager.is_running():
            daily_task_manager.start()
            await interaction.response.send_message("Daily messages enabled.")
        else:
            await interaction.response.send_message("Daily messages are already running.")


async def setup(bot):
    await bot.add_cog(DailyEnable(bot))