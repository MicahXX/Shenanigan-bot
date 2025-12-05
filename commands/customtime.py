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
        description="Set how often the daily message runs (in hours, default: 24)"
    )
    async def customtime(self, interaction: discord.Interaction, hours: int):
        if hours < 1:
            await interaction.response.send_message("❌ Hours must be at least 1.")
            return

        manager = get_daily_task_manager(self.bot)
        manager.set_interval(interaction.guild_id, hours)

        await interaction.response.send_message(
            f"Daily interval set to {hours} hours."
        )


async def setup(bot):
    await bot.add_cog(CustomTime(bot))