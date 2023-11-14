from service import Service
from .dice import eval_string,get_relation
from .aa import random_choice
from .anjia import aj
from . import character
from . import dice_fiacso

sv = Service("dice")
sv.help = """
骰子：
本骰子暂时仅支持以下指令
.r[a]d[b] 投a个面投，a默认为1，b默认为100
.r[a]d[b]k[c] 投a个面投，取其中最高的c个值的和，a默认为1，b默认为100

安科：
安科 主题名
a 选项
.....
a为选项出现的次数

安价：
指令有结束安价、查看安价、暂停安价、重启安价、安价历史
安价删除 主题号 以删除指定号码的安价
安价 内容以增加指定内容的安价
开始安价 主题号 以开始指定主题的安价"""


@sv.on_rex(r'\.r[dk+\-()\d]+.*')
async def roll_from_message(bot, message):
    content = message.content
    if len(content) <= 2:
        reply = "表达式格式错误。"
    else:
        reply = await eval_string(message.content[2:], message.author.username)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix('安科')
async def anke_from_message(bot, message):
    content = message.content
    if "\n" not in content and len(content) > 3:
        reply = "请至少输入一个安科选项"
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)
    else:
        content = content.lstrip()
        reply = await random_choice(content)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match('.help')
async def anjia_help(bot, message):
    await bot.send(channel_id=message.channel_id, content=sv.help, reply_message=message.id)


@sv.on_prefix('开始安价 ')
async def anjia_start(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        theme = message.content.strip()
        reply = await aj.insert_theme(theme, message.channel_id)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match('结束安价')
async def anjia_end(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        reply = await aj.open_close_anke(message.channel_id)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match('暂停安价')
async def anjia_end(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        reply = await aj.open_close_anke(message.channel_id, reopen=2)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match('重启安价')
async def anjia_end(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        reply = await aj.open_close_anke(message.channel_id, reopen=1)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match('查看安价')
async def view_anjia(bot, message):
    reply = await aj.view_anke(message.channel_id)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match('安价历史')
async def view_anjia_history(bot, message):
    reply = await aj.view_theme(message.channel_id)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix('安价 ')
async def add_anjia(bot, message):
    reply = await aj.insert_anke(channel_id=message.channel_id, userid=message.author.id,
                                 content=message.content)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix('删除安价 ')
async def delete_anjia(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        reply = await aj.delete_anke(channel_id=message.channel_id, num=int(message.content),
                                     is_admin=message.author.is_admin)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix('.关系骰 ')
async def relation(bot, message):
    reply = get_relation(message.content)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)
