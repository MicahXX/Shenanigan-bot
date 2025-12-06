import random
import time
from discord.ext import tasks
from ai import generate_custom_prompt, generate_outrageous_message
from utils.json_store import load_settings, save_settings


class DailyTaskManager:
    def __init__(self, bot):
        self.bot = bot
        self.settings = load_settings()

        for gid, data in self.settings.items():
            data.setdefault("recent_messages", [])

        self.task = tasks.loop(seconds=30)(self._run)


    def _get_recent_messages(self, gid: str):
        return self.settings.get(gid, {}).get("recent_messages", [])

    def _save_recent_message(self, gid: str, msg: str):
        if gid not in self.settings:
            self.settings[gid] = {}

        lst = self.settings[gid].setdefault("recent_messages", [])
        lst.append(msg)

        if len(lst) > 100:
            lst[:] = lst[-100:]

        save_settings(self.settings)


    async def _run(self):
        await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            gid = str(guild.id)
            guild_settings = self.settings.get(gid, {})

            if not guild_settings.get("enabled", False):
                continue

            interval = guild_settings.get("interval", 24)
            prompt = guild_settings.get("prompt", None)
            last_sent = guild_settings.get("last_sent", 0)
            now = time.time()

            # Interval check
            if now - last_sent < interval * 3600:
                continue

            # Channel selection
            channel_mode = guild_settings.get("channel_mode", "random")
            fixed_channel_id = guild_settings.get("channel_id")
            channel = None

            if channel_mode == "fixed" and fixed_channel_id is not None:
                channel = guild.get_channel(fixed_channel_id)

            if channel is None:
                channels = [
                    ch for ch in guild.text_channels
                    if ch.permissions_for(guild.me).send_messages
                ]
                if not channels:
                    continue
                channel = random.choice(channels)


            recent = set(self._get_recent_messages(gid))
            msg = None

            # Try up to 10 times to avoid duplicates
            for _ in range(10):
                if prompt:
                    candidate = await generate_custom_prompt(prompt)
                else:
                    candidate = await generate_outrageous_message()

                if candidate not in recent:
                    msg = candidate
                    break

            if msg is None:
                msg = candidate


            try:
                await channel.send(msg)
            except Exception as e:
                print(f"Could not send message to {guild.name}: {e}")
                continue

            # Update timestamp
            guild_settings["last_sent"] = now
            self.settings[gid] = guild_settings

            # Save memory
            self._save_recent_message(gid, msg)

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

        if random_mode:
            self.settings[gid]["channel_mode"] = "random"
            self.settings[gid]["channel_id"] = None
        else:
            self.settings[gid]["channel_mode"] = "fixed"
            self.settings[gid]["channel_id"] = channel_id

        save_settings(self.settings)

_daily_task_manager = None

def get_daily_task_manager(bot):
    global _daily_task_manager
    if _daily_task_manager is None:
        _daily_task_manager = DailyTaskManager(bot)
    return _daily_task_manager
