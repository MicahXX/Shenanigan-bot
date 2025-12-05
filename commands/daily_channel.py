import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager


class DailyChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_channel",
        description="Set the channel for daily messages or choose random mode"
    )
    @app_commands.describe(
        mode="Choose 'random' or 'fixed'",
        channel="Required if mode=fixed"
    )
    async def daily_channel(
            self,
            interaction: discord.Interaction,
            mode: str,
            channel: discord.TextChannel | None = None
    ):
        manager = get_daily_task_manager(self.bot)
        gid = interaction.guild_id

        mode = mode.lower()

        if mode == "random":
            manager.set_channel(gid, None, True)
            await interaction.response.send_message("Daily messages will now be sent to a **random channel**.")
            return

        if mode == "fixed":
            if channel is None:
                await interaction.response.send_message("You must specify a channel when using fixed mode.")
                return

            manager.set_channel(gid, channel.id, False)
            await interaction.response.send_message(
                f"Daily messages will now be sent to {channel.mention}."
            )
            return

        await interaction.response.send_message("Mode must be either `random` or `fixed`.")


async def setup(bot):
    await bot.add_cog(DailyChannel(bot))