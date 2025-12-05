import os

async def load_extensions(bot):

    for file in os.listdir("./commands"):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = os.path.splitext(file)[0]

            if module_name == "daily_task":
                continue

            module = f"commands.{module_name}"
            print("Loading extension:", module)
            await bot.load_extension(module)