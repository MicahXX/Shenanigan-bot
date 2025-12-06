import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager


class DailyUniqueness(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="daily_uniqueness",
        description="Set how unique daily messages should be (0.0 – 1.0, higher = more strict uniqueness, default = 0.6)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def daily_uniqueness(self, interaction: discord.Interaction, threshold: float):
        if threshold < 0:
            threshold = 0.0
        if threshold > 1:
            threshold = 1.0

        manager = get_daily_task_manager(self.bot)
        manager.set_uniqueness_threshold(interaction.guild_id, threshold)

        await interaction.response.send_message(
            f"Daily uniqueness threshold set to **{threshold:.2f}**.\n"
        )


async def setup(bot):
    await bot.add_cog(DailyUniqueness(bot))
