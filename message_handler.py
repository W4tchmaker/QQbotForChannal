import trigger
from log import _log
from log import _mdlogger


async def handle_message(bot, message):
    triggered = False
    for t in trigger.chain:
        for service_func in t.find_handler(message):
            _log.info(f'Message:{message.id}\'s message triggered {service_func.__name__}.')
            triggered = True
            try:
                await service_func.func(bot, message)
            except Exception as e:
                _log.error(f'{type(e)} occurred when {service_func.__name__} handling message {message.id}.')
                _log.exception(e)
    if not triggered:
        _mdlogger.log(message.content)