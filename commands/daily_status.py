import discord
from discord import app_commands
from discord.ext import commands
from tasks.daily_task import get_daily_task_manager


def format_interval(hours: float) -> str:
    total_seconds = int(hours * 3600)
    days = total_seconds // 86400
    total_seconds %= 86400
    h = total_seconds // 3600
    total_seconds %= 3600
    m = total_seconds // 60
    s = total_seconds % 60

    parts = []
    if days > 0: parts.append(f"{days}d")
    if h > 0: parts.append(f"{h}h")
    if m > 0: parts.append(f"{m}m")
    if s > 0: parts.append(f"{s}s")
    return " ".join(parts) if parts else "0s"


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
        enabled = settings.get("enabled", False)
        prompt = settings.get("prompt", "Default outrageous prompt")
        interval = settings.get("interval", 24)
        random_mode = settings.get("random", True)
        channel_id = settings.get("channel", None)

        interval_text = format_interval(interval)

        if random_mode:
            channel_text = "Random channel"
        else:
            ch = interaction.guild.get_channel(channel_id)
            channel_text = ch.mention if ch else "Unknown channel"

        await interaction.response.send_message(
            f"**Daily Message Status**\n"
            f"Enabled: {'ON' if enabled else 'OFF'}\n"
            f"Interval: **{interval_text}**\n"
            f"Prompt: `{prompt}`\n"
            f"Channel: {channel_text}"
        )


async def setup(bot):
    await bot.add_cog(DailyStatus(bot))