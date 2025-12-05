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
        description="Check the daily message settings for this server"
    )
    async def daily_status(self, interaction: discord.Interaction):
        manager = get_daily_task_manager(self.bot)
        gid = str(interaction.guild_id)

        settings = manager.settings.get(gid, {})
        prompt = settings.get("prompt", "Default outrageous prompt")
        interval = settings.get("interval", 24)
        random_mode = settings.get("random", True)
        channel_id = settings.get("channel", None)

        if random_mode:
            channel_text = "Random channel"
        else:
            channel_obj = interaction.guild.get_channel(channel_id)
            channel_text = channel_obj.mention if channel_obj else "Unknown channel"

        status = "ON" if manager.is_running() else "OFF"

        await interaction.response.send_message(
            f"**Daily Message Status**\n"
            f"Status: {status}\n"
            f"Interval: Every **{interval} hours**\n"
            f"Prompt: `{prompt}`\n"
            f"Channel: {channel_text}"
        )


async def setup(bot):
    await bot.add_cog(DailyStatus(bot))