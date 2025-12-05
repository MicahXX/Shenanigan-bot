import os
import asyncio
import discord
from discord.ext import commands
from extensions import load_extensions
from tasks.daily_task import get_daily_task_manager

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    manager = get_daily_task_manager(bot)
    manager.start()
    print("DailyTaskManager started.")

    try:
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(f"Slash sync error: {e}")


async def main():
    await load_extensions(bot)
    await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())