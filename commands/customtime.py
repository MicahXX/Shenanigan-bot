import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager
import re


def parse_time_string(time_str: str) -> float:
    """
    Parse a time string like:
    30s, 5m, 2h, 1d, 2h30m, 1d4h20m10s, etc.
    Returns hours as float.
    """

    pattern = r"(\d+\.?\d*)([smhd])"
    matches = re.findall(pattern, time_str.lower())

    if not matches:
        raise ValueError("Invalid time format.")

    total_seconds = 0

    for value, unit in matches:
        value = float(value)

        if unit == "s":
            total_seconds += value
        elif unit == "m":
            total_seconds += value * 60
        elif unit == "h":
            total_seconds += value * 3600
        elif unit == "d":
            total_seconds += value * 86400

    return total_seconds / 3600  # convert to hours


def format_interval(hours: float) -> str:

    total_seconds = int(hours * 3600)

    d = total_seconds // 86400
    total_seconds %= 86400

    h = total_seconds // 3600
    total_seconds %= 3600

    m = total_seconds // 60
    s = total_seconds % 60

    parts = []
    if d > 0:
        parts.append(f"{d}d")
    if h > 0:
        parts.append(f"{h}h")
    if m > 0:
        parts.append(f"{m}m")
    if s > 0:
        parts.append(f"{s}s")

    if not parts:
        return "0s"

    return "".join(parts)


class CustomTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="customtime",
        description="Set how often the daily message runs (supports s/m/h/d)"
    )
    @app_commands.describe(
        time="Examples: 30s, 5m, 2h, 1d, 2h30m, 1d4h20m10s"
    )
    async def customtime(self, interaction: discord.Interaction, time: str):
        try:
            hours = parse_time_string(time)
        except ValueError:
            await interaction.response.send_message(
                "Invalid time format. Use formats like `30s`, `5m`, `2h`, `1d`, `2h30m`."
            )
            return

        if hours <= 0:
            await interaction.response.send_message("Time must be greater than 0.")
            return

        manager = get_daily_task_manager(self.bot)
        manager.set_interval(interaction.guild_id, hours)

        readable = format_interval(hours)

        await interaction.response.send_message(
            f"Daily interval set to **{readable}** (from `{time}`)."
        )


async def setup(bot):
    await bot.add_cog(CustomTime(bot))