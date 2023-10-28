from service import Service
import os
import json

from .get_target import get_tar

sv = Service('uma_target')
sv.help_image = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')


@sv.on_full_match("育成目标帮助")
async def get_help(bot, message):
    img = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    await bot.send(channel_id=message.channel_id, image_path=img, reply_message=message.id)


@sv.on_prefix('查目标')
async def search_target(bot, message):
    uma_name_tmp = str(message.content).replace('-f', '')
    is_force = True if str(message.content).endswith('-f') else False
    current_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info\\config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info\\replace_dict.json'), 'r',
              encoding='UTF-8') as af:
        replace_data = json.load(af)
    uma_target = ''
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            other_name_list = list(replace_data[uma_name]) if uma_name in replace_data else []
            if f_data[uma_name]['cn_name']:
                cn_name = f_data[uma_name]['cn_name']
            else:
                continue
            if str(uma_name) == uma_name_tmp or str(cn_name) == uma_name_tmp or \
                    str(f_data[uma_name]['jp_name']) == uma_name_tmp or str(uma_name_tmp) in other_name_list:
                try:
                    uma_target = await get_tar(cn_name, is_force)
                except:
                    await bot.send(channel_id=message.channel_id, content=f'这只马娘不存在或暂时没有育成目标', reply_message=message.id)
                    return
    if not uma_target:
        await bot.send(channel_id=message.channel_id, content=f'这只马娘不存在或暂时没有育成目标', reply_message=message.id)
        return
    await bot.send(channel_id=message.channel_id, image_path=uma_target, reply_message=message.id)
