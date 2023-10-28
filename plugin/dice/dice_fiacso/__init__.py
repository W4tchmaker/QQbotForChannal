from service import Service
from .fiscso import fiasco_sv

sv = Service("fiasco")


@sv.on_full_match("开始空前惨败")
async def start_fiasco(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        reply = await fiasco_sv.start_fiasco(message.channel_id, "")
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match("结束空前惨败")
async def end_fiasco(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        reply = await fiasco_sv.start_fiasco(message.channel_id)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match("加入空前惨败")
async def add_fiasco_player(bot, message):
    reply = await fiasco_sv.add_player(message.channel_id, message.author.username)
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_full_match("空前惨败投骰")
async def roll_fiasco_dice(bot, message):
    flag = await bot.get_priv(message.channel_id, message.author.id)
    if flag:
        reply = await fiasco_sv.rolling_dices(message.channel_id)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix("取骰")
async def add_fiasco_player(bot, message):
    reply = await fiasco_sv.picking_dices(message.channel_id, message.author.username, message.content.strip())
    await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)


@sv.on_prefix("重骰")
async def re_reroll_fiasco(bot, message):
    flag = (await bot.get_priv(message.channel_id, message.author.id) and
            message.content.strip().endswith("公共骰"))
    if flag:
        reply = await fiasco_sv.reroll(message.channel_id, public=True)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)
    else:
        reply = await fiasco_sv.reroll(message.channel_id, public=True)
        await bot.send(channel_id=message.channel_id, content=reply, reply_message=message.id)
