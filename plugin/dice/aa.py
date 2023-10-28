import random


async def random_choice(content):
    options = []
    line = content.split('\n')
    desc = line[0]
    for i in range(1, len(line)):
        if line[i].strip() == "":
            pass
        elif " " not in line[i]:
            return f" {str(line[i])} 的选项格式错误"
        else:
            line_content = line[i].lstrip().split(" ", maxsplit=1)
            try:
                options = options + int(line_content[0])*[line_content[1]]
            except ValueError:
                return f" {str(line_content[0])} 的选项格式错误"
    reply = f"安价 {desc}:\n"
    random.shuffle(options)
    crit_flag = False
    if len(options) == 9:
        crit_flag = True
        options.append("大成功/大失败")
    for i in range(len(options)):
        reply = reply + f"{i + 1}\t{options[i]}\n"
    dice = random.randint(0, len(options) - 1)
    reply = reply + f"  1d{len(options)}={dice + 1}:\n  {dice + 1}\t{options[dice]}"
    if dice == 9 and crit_flag:
        crit = random.randint(1, 2)
        crit_text = ["大成功", "大失败"]
        reply = reply + f"\n    1d2={crit}:{crit_text[crit - 1]}"
    return reply
