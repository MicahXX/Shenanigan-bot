import discord
from discord import app_commands
from discord.ext import commands

from ai import generate_custom_prompt


class Prompt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="prompt",
        description="Send a custom prompt to ChatGPT"
    )
    @app_commands.describe(text="The prompt you want to send to ChatGPT")
    async def prompt(self, interaction: discord.Interaction, text: str):
        try:
            msg = await generate_custom_prompt(text)
            await interaction.response.send_message(msg)
        except Exception as e:
            await interaction.response.send_message("Failed to generate response!")
            print("Error generating custom prompt:", e)



async def setup(bot):
    await bot.add_cog(Prompt(bot))
