import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager


class CustomTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="customtime",
        description="Set how often the daily message runs (in hours, can be decimal)"
    )
    @app_commands.describe(hours="Example: 0.5 = 30 minutes, 2.5 = 2h 30m")
    async def customtime(self, interaction: discord.Interaction, hours: float):
        if hours <= 0:
            await interaction.response.send_message("Time must be greater than 0.")
            return

        manager = get_daily_task_manager(self.bot)
        manager.set_interval(interaction.guild_id, hours)

        await interaction.response.send_message(
            f"Daily interval set to **{hours} hour(s)**."
        )


async def setup(bot):
    await bot.add_cog(CustomTime(bot))