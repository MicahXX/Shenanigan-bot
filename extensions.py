import os
import importlib

async def load_extensions(bot):

    # Load slash commands
    for file in os.listdir("./commands"):
        if file.endswith(".py") and not file.startswith("__"):
            module = f"commands.{file[:-4]}"
            await bot.load_extension(module)

    # Load tasks
    from tasks import setup_tasks
    setup_tasks(bot)
