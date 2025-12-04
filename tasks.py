import random
from discord.ext import tasks
from ai import generate_outrageous_message


def setup_tasks(bot):

    @tasks.loop(seconds=10)
    async def daily_outburst():
        await bot.wait_until_ready()

        # Loop through every server the bot is in
        for guild in bot.guilds:

            # All text channels in this server
            channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages]

            if not channels:
                continue

            channel = random.choice(channels)
            msg = await generate_outrageous_message()

            try:
                await channel.send(msg)
            except Exception as e:
                print(f"Could not send message to {guild.name}: {e}")

    if not daily_outburst.is_running():
        daily_outburst.start()