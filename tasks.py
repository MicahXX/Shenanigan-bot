import random
from discord.ext import tasks
from ai import generate_outrageous_message


class DailyTaskManager:
    def __init__(self, bot):
        self.bot = bot
        self.task = tasks.loop(hours=24)(self._run)

    async def _run(self):
        await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            channels = [
                ch for ch in guild.text_channels
                if ch.permissions_for(guild.me).send_messages
            ]

            if not channels:
                continue

            channel = random.choice(channels)
            msg = await generate_outrageous_message()

            try:
                await channel.send(msg)
            except Exception as e:
                print(f"Could not send message to {guild.name}: {e}")

    def start(self):
        if not self.task.is_running():
            self.task.start()

    def stop(self):
        if self.task.is_running():
            self.task.cancel()

    def is_running(self):
        return self.task.is_running()


daily_task_manager: DailyTaskManager | None = None


def init_daily_task(bot):
    global daily_task_manager
    if daily_task_manager is None:
        daily_task_manager = DailyTaskManager(bot)
        daily_task_manager.start()