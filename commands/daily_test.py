import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager
from ai import generate_custom_prompt, generate_outrageous_message


class DailyTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="daily_test",
        description="Send the daily message immediately (for testing)"
    )
    async def daily_test(self, interaction: discord.Interaction):
        manager = get_daily_task_manager(self.bot)
        gid = str(interaction.guild_id)

        settings = manager.settings.get(gid, {})
        prompt = settings.get("prompt", None)

        if prompt:
            msg = await generate_custom_prompt(prompt)
        else:
            msg = await generate_outrageous_message()

        await interaction.response.send_message("Test message sent below:")
        await interaction.followup.send(msg)


async def setup(bot):
    await bot.add_cog(DailyTest(bot))