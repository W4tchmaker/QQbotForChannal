import trigger
import datetime
import os
from log import _log

# 获取当前日期作为文件名
today = datetime.date.today()
markdown_filename = f"markdown/{today}.md"
log_mode = False


async def handle_message(bot, message):
    if log_mode is not True:
        for t in trigger.chain:
            for service_func in t.find_handler(message):

                _log.info(f'Message:{message.id}\'s message triggered {service_func.__name__}.')
                try:
                    await service_func.func(bot, message)
                except Exception as e:      # other general errors.
                    _log.error(f'{type(e)} occurred when {service_func.__name__} handling message {message.id}.')
                    _log.exception(e)
                # the func completed successfully, stop triggering. (1 message for 1 function at most.)
    else:
        # 检查消息是否以指定字符开头
        if not message.content.startswith("(") and not message.content.startswith("（"):
            # 如果消息不以括号开头，则将其写入Markdown文件中
            with open(markdown_filename, "a", encoding="utf-8") as file:
                print(f"把{message.content}写入了{markdown_filename}中")
                file.write(f"{message.content}\n")

