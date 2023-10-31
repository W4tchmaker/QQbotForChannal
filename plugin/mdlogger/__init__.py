from service import Service
import time
from log import _mdlogger

sv = Service("markdownlogger")
sv.help = """以markdown格式记录。
开始记录 日志名 以开始记录
结束记录 以结束记录并返回md文件
如果没有日志名，则日志名为当前子频道ID+日期"""


@sv.on_prefix("开始记录")
async def start_md_recording(bot, message):
    if message.content.isspace() or not message.content:
        filename = str(time.time())+message.channel_id
    else:
        filename = message.content
    _mdlogger.set_file_name(filename)
    reply = f"已创建名为{filename}的log。"

    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix("结束记录")
async def end_md_recording(bot, message):
    md_file_path = _mdlogger.return_md_file()
    if md_file_path:
        reply = f"日志已结束记录。"
    else:
        reply = "未开始记录日志或已结束记录。"
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)

