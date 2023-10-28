import os
import httpx
from bs4 import BeautifulSoup
import json
from config import resources_path


async def get_cn_name(uma_name):

    # 检查 JSON 文件是否存在，如果不存在则创建
    json_file_path = os.path.join(resources_path, f'uma/uma_cn_wiki_name.json')
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w', encoding='utf-8') as new_json_file:
            json.dump({}, new_json_file)

    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 查找输入字符串是否在JSON数据中
    if uma_name in data:
        return data[uma_name]  # 返回属性值
    else:
        url = f'https://wiki.biligame.com/umamusume/{uma_name}'
        res = httpx.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        target_cn_link = soup.find_all('a')
        desired_links = [a for a in target_cn_link if a.get('title', '').startswith("简/")]

        if len(desired_links) == 0:
            return False
        cn_name = desired_links[0].get('title', '')

        # 将新数据添加到JSON文件中
        data[uma_name] = cn_name

        # 写入更新后的JSON文件
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

        # 返回新添加的属性值
        return cn_name
