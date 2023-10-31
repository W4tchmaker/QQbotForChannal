# -*- coding: utf-8 -*-

import asyncio
import os

import botpy
from log import _log, _mdlogger
from botpy.ext.cog_yaml import read
from botpy.message import Message

from message_handler import handle_message
from import_plugin import import_plugins

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_message_create(self, message: Message):
        if "sleep" in message.content:
            await asyncio.sleep(10)

        await asyncio.sleep(0.5)
        await handle_message(self, message)

    async def get_priv(self, channel_id, user_id):
        user_permission = await self.api.get_channel_user_permissions(channel_id, user_id)
        user_permission_in_channel = int(user_permission["permissions"])

        manage_channel_permission = 2

        return (manage_channel_permission & user_permission_in_channel) != 0

    async def send(self, channel_id, content=None, image_path=None, reply_message=None):
        if not (content or image_path):
            return False
        if content:
            _mdlogger.log(content)
        await self.api.post_message(channel_id=channel_id, content=content, file_image=image_path, msg_id=reply_message)
        pass


if __name__ == "__main__":
    intents = botpy.Intents(guild_messages=True)

    bot = MyClient(intents=intents)
    import_plugins()
    bot.run(appid=test_config["appid"], token=test_config["token"])
