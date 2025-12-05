import discord
from discord import app_commands
from discord.ext import commands

from tasks.daily_task import get_daily_task_manager


class CustomPrompt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="customprompt",
        description="Set the custom daily prompt"
    )
    async def customprompt(self, interaction: discord.Interaction, prompt: str):
        manager = get_daily_task_manager(self.bot)
        manager.set_prompt(interaction.guild_id, prompt)

        await interaction.response.send_message(
            f"Custom daily prompt set to:\n{prompt}"
        )


async def setup(bot):
    await bot.add_cog(CustomPrompt(bot))