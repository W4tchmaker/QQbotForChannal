import random


async def gen_dnd_character(name, n):
    string = f"{name}的角色生成: \n"
    dnd_attr = ["力量", "敏捷", "体质", "感知", "智力", "魅力"]
    for i in range(n):
        dices = 0
        for j in range(6):
            dice_list = [random.randint(1, 6) for _ in range(4)]
            dice_list.sort()
            dices = dices+sum(dice_list[1:])
            string = string + f"{dnd_attr[j]}: {sum(dice_list[1:])} "

        string = string + f"总计:{dices}\n"
    if n == 1:
        dnd_class = ["奇械师", "野蛮人", "野蛮人", "牧师", "德鲁伊", "战士", "武僧", "圣武士", "游侠", "游荡者", "术士",
                     "邪术师", "法师"]
        dnd_races = ["矮人", "精灵", "半身人", "人类", "龙裔", "侏儒", "半精灵", "半兽人"]
        string = string + f"对这个属性我不负责任建议你使用{random.choice(dnd_races)}{random.choice(dnd_class)}"
    return string
