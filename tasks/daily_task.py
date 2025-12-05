import random
import time
from discord.ext import tasks
from ai import generate_custom_prompt, generate_outrageous_message
from utils.json_store import load_settings, save_settings


class DailyTaskManager:
    def __init__(self, bot):
        self.bot = bot
        self.settings = load_settings()

        self.task = tasks.loop(seconds=20)(self._run)

    async def _run(self):
        await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            gid = str(guild.id)
            settings = self.settings.get(gid, {})

            interval = settings.get("interval", 24)
            prompt = settings.get("prompt", None)
            last_sent = settings.get("last_sent", 0)
            channel_id = settings.get("channel", None)
            random_mode = settings.get("random", True)
            history = settings.get("history", [])

            now = time.time()

            if now - last_sent < interval * 3600:
                continue

            if random_mode or not channel_id:
                channels = [
                    ch for ch in guild.text_channels
                    if ch.permissions_for(guild.me).send_messages
                ]
                if not channels:
                    continue
                channel = random.choice(channels)
            else:
                channel = guild.get_channel(channel_id)
                if not channel or not channel.permissions_for(guild.me).send_messages:
                    continue

            memory_block = (
                    "Below are your previous outputs. You MUST NOT repeat ANY of them.\n"
                    "You MUST generate something completely different in:\n"
                    "- topic\n"
                    "- structure\n"
                    "- logic\n"
                    "- answer\n"
                    "- style\n"
                    "\nPrevious outputs:\n"
                    + "\n".join(history[-50:])
                    + "\n\nHard rules:\n"
                      "- Do NOT use the same answer.\n"
                      "- Do NOT use the same riddle structure.\n"
                      "- Do NOT use the same logic.\n"
                      "- Do NOT use the same theme.\n"
                      "- Do NOT use classic riddles like 'echo', 'shadow', 'time', 'silence', etc.\n"
                      "- Create something NEW, UNIQUE, and DIFFERENT.\n"
            )

            if prompt:
                full_prompt = memory_block + f"\nNow respond to this prompt:\n{prompt}"
                msg = await generate_custom_prompt(full_prompt)
            else:
                full_prompt = memory_block + "Generate something new."
                msg = await generate_outrageous_message(full_prompt)

            try:
                await channel.send(msg)
            except Exception as e:
                print(f"Could not send message to {guild.name}: {e}")
                continue

            # Save infinite history
            history.append(msg)
            settings["history"] = history

            settings["last_sent"] = now

            self.settings[gid] = settings
            save_settings(self.settings)

    def start(self):
        if not self.task.is_running():
            self.task.start()

    def stop(self):
        if self.task.is_running():
            self.task.cancel()

    def is_running(self):
        return self.task.is_running()

    def set_prompt(self, guild_id: int, prompt: str):
        gid = str(guild_id)
        if gid not in self.settings:
            self.settings[gid] = {}
        self.settings[gid]["prompt"] = prompt
        save_settings(self.settings)

    def set_interval(self, guild_id: int, hours: float):
        gid = str(guild_id)
        if gid not in self.settings:
            self.settings[gid] = {}
        self.settings[gid]["interval"] = hours
        save_settings(self.settings)

    def set_channel(self, guild_id: int, channel_id: int | None, random_mode: bool):
        gid = str(guild_id)
        if gid not in self.settings:
            self.settings[gid] = {}
        self.settings[gid]["channel"] = channel_id
        self.settings[gid]["random"] = random_mode
        save_settings(self.settings)


_daily_task_manager = None


def get_daily_task_manager(bot):
    global _daily_task_manager
    if _daily_task_manager is None:
        _daily_task_manager = DailyTaskManager(bot)
    return _daily_task_manager