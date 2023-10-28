from .dnd_character import gen_dnd_character
from service import Service
from .arknights import arknights_character
from .others import gen_motivation
from .dnd_character import gen_dnd_character
from .maid_trpg import gen_maid_character

sv = Service("gen_character")


@sv.on_prefix('.dnd')
async def gen_dnd(bot, message):
    content = message.content.strip()
    i = 0
    while i < len(content) and content[i].isdigit():
        i = i+1
    if i == 0:
        content = "1"
        i = 1
    if content.isdigit():
        reply = await gen_dnd_character(message.author.username, int(content[:i]))
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)
    else:
        await bot.send(channel_id=message.channel_id, content="请在.dnd 后加入你要生成的角色数", reply_message=message.id)


@sv.on_prefix('.明日方舟')
async def gen_arknights(bot, message):
    tmp = str(message.content).replace('穿越', '')
    is_there = True if str(message.content).endswith('穿越') else False
    reply = await arknights_character(message.author.username, is_there)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix('.共鸣动机 ')
async def motivation(bot, message):
    if message.content:
        reply = await gen_motivation(message.content)
    else:
        reply = await gen_motivation(message.author.username)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix('.女仆')
async def motivation(bot, message):
    if message.content:
        reply = await gen_maid_character(message.content)
    else:
        reply = await gen_maid_character(message.author.username)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)