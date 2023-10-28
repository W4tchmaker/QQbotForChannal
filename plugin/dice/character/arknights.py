import json
import os.path
import random
from config import resources_path


async def arknights_character(username, flag=False):
    reply = f"{username}的明日方舟干员:"
    with open(os.path.join(resources_path, "arknights.json"), "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    stars = random.choices([1, 2, 3, 4, 5, 6], weights=[7, 5, 17, 54, 130, 80])[0]
    reply = reply + f"{stars * '★'}\n"
    selected_class = random.choice(list(data["职业"].keys()))
    sub_class = random.choice(data["职业"][selected_class])
    reply = reply + f"职业为 {selected_class} - {sub_class}"
    times = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])
    words = random.choices(data["词缀"], k=times[0])
    if selected_class == "医师" and "治疗" not in words:
        words[0] = "治疗"
    elif selected_class == "重装" and "防护" not in words:
        words[0] = "防护"
    elif selected_class == "先锋":
        words[0] = "费用回复"
    elif sub_class == "处决者":
        words[0] = "快速复活"
    elif sub_class in ["推击手", "钩索师"] and "位移" not in words:
        words[0] = "位移"
    reply = reply + f" 关键词为 {','.join(words)}\n"
    for i in range(6):
        reply = reply + f"【{data['六维'][i]}】{random.choice(data['六维评价'])}\n"
    reply = reply + f"\n势力:{random.choice(data['势力'])}"
    reply = reply + f"\n出身地:{random.choice(data['出身地'])}"
    reply = reply + f"\n种族:{random.choice(data['种族'])} {random.choice(['感染者', '非感染者'])}"
    reply = reply + f"\n立绘:{random.randint(1, 100)}  人气:{random.randint(1, 100)} "
    reply = reply + f"\n强度评价:{random.choices(data['强度'], weights=[0.05, 0.2, 0.4, 0.2, 0.1, 0.05])[0]}"

    if flag:
        reply = reply + "\n 什么，你想穿越到明日方舟世界，那，唔……"
        reply = reply + f"\n和罗德岛关系:{random.randint(1, 100)},\
        剧情强度:{random.randint(1, 100)},地位{random.randint(1, 100)}"
    return reply
