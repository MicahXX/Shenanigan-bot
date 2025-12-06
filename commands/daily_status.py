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
    return "0s" if not parts else " ".join(parts)


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

        enabled = settings.get("enabled", False)
        prompt = settings.get("prompt", "Default outrageous prompt")
        interval = settings.get("interval", 24)

        channel_mode = settings.get("channel_mode", "random")
        channel_id = settings.get("channel_id", None)

        uniqueness = settings.get("uniqueness_threshold", 0.6)

        interval_text = format_interval(interval)

        if channel_mode == "random":
            channel_text = "Random channel"
        else:
            ch = interaction.guild.get_channel(channel_id)
            channel_text = ch.mention if ch else "Unknown channel"

        await interaction.response.send_message(
            f"**Daily Message Status for this Server**\n"
            f"**Enabled:** {'ON' if enabled else 'OFF'}\n"
            f"**Interval:** `{interval_text}`\n"
            f"**Prompt:** `{prompt}`\n"
            f"**Channel Mode:** `{channel_mode}`\n"
            f"**Channel:** {channel_text}\n"
            f"**Uniqueness Threshold:** `{uniqueness}`"
        )


async def setup(bot):
    await bot.add_cog(DailyStatus(bot))
