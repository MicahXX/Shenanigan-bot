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
        description="Check the daily message settings"
    )
    async def daily_status(self, interaction: discord.Interaction):
        manager = get_daily_task_manager(self.bot)
        gid = str(interaction.guild_id)

        settings = manager.settings.get(gid, {})
        prompt = settings.get("prompt", "Default outrageous prompt")
        interval = settings.get("interval", 24)
        status = "ON" if manager.is_running() else "OFF"

        await interaction.response.send_message(
            f"**Daily Message Status for {interaction.guild.name}**\n"
            f"Status: {status}\n"
            f"Interval: Every **{interval} hours**\n"
            f"Prompt: `{prompt}`"
        )


async def setup(bot):
    await bot.add_cog(DailyStatus(bot))