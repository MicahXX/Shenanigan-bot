import os


async def load_extensions(bot):

    for file in os.listdir("./commands"):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = os.path.splitext(file)[0]
            module = f"commands.{module_name}"
            print("Loading extension:", module)
            await bot.load_extension(module)

    from commands.tasks import setup_tasks
    setup_tasks(bot)
