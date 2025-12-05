import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import daily_task_manager, init_daily_task


class DailyDisable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        init_daily_task(bot)

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_disable",
        description="Disable the daily outrageous message task (Admins only)"
    )
    async def daily_disable(self, interaction: discord.Interaction):
        if daily_task_manager.is_running():
            daily_task_manager.stop()
            await interaction.response.send_message("Daily messages disabled.")
        else:
            await interaction.response.send_message("Daily messages were already disabled.")


async def setup(bot):
    await bot.add_cog(DailyDisable(bot))