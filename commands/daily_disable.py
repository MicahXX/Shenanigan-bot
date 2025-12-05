import discord
from discord import app_commands
from discord.ext import commands
from tasks.daily_task import get_daily_task_manager
from utils.json_store import save_settings


class DailyDisable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_disable",
        description="Disable daily messages for"
    )
    async def daily_disable(self, interaction: discord.Interaction):
        manager = get_daily_task_manager(self.bot)
        gid = str(interaction.guild_id)

        if gid not in manager.settings:
            manager.settings[gid] = {}

        manager.settings[gid]["enabled"] = False
        save_settings(manager.settings)

        await interaction.response.send_message("Daily messages disabled for this server.")