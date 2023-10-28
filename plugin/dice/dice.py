import random
import re
from log import _log


def replace_d_with_function(match):
    groups = match.groups()
    # print(groups)
    a = int(groups[0]) if groups[0] else 1
    b = int(groups[1]) if groups[1] else 20
    result = roll(a, b)
    return str(result)


def replace_k_with_function(match):
    groups = match.groups()
    # print(groups)
    a = int(groups[0]) if groups[0] else 1
    b = int(groups[1]) if groups[1] else 20
    k = int(groups[2]) if groups[2] else 1
    result = roll(a, b, symbol=",") + "k" + str(k)
    return result


def max_k_from_dice(match):
    groups = match.groups()
    a = groups[0]
    k = int(groups[1])
    nums = a.split(",")
    for i in range(len(nums)):
        nums[i] = int(nums[i])
    nums.sort()
    for i in range(len(nums)):
        nums[i] = str(nums[i])
    return "(" + "+".join(nums[-k:]) + ")"


async def process_string_with_d(input_string):
    pattern = r'(\d+)d(\d+)'
    replaced_string = re.sub(pattern, replace_d_with_function, input_string, count=0)
    return replaced_string


async def process_string_with_k(input_string):
    pattern = r'(\d+)d(\d+)k(\d+)'
    replaced_string = re.sub(pattern, replace_k_with_function, input_string, count=0)
    return replaced_string


async def process_string_with_max(input_string):
    pattern = r'\(([\d,]+)\)k(\d+)'
    replaced_string = re.sub(pattern, max_k_from_dice, input_string, count=0)
    return replaced_string


async def eval_string(string, username="Someone"):
    # print("字符串为:",string)
    i = 0
    eqa = string.lower()
    k_flag = False
    while i < len(eqa) and (eqa[i].isdigit() or eqa[i] in "+-*()dk"):
        i = i + 1
    eqa = eqa[:i]
    if "k" in eqa:
        k_flag = True
    while (len(eqa) > 0 and eqa[-1] == "(") or (len(eqa) > 1 and eqa[-1] in "dk" and "d" in eqa[:-1]):
        eqa = eqa[:-1]
        i = i - 1
    if len(eqa) == 0:
        return "请输入表达式"
    eqa = re.sub("(?<![0-9])d", "1d", eqa, count=0)
    eqa = re.sub("d(?![0-9])", "d100", eqa, count=0)
    eqa = re.sub("k(?![0-9])", "k1", eqa, count=0)
    dis_eqa = ""
    if k_flag:
        dis_eqa = await process_string_with_k(eqa)
        dis_eqa = await process_string_with_d(dis_eqa)
        cal_eqa = await process_string_with_max(dis_eqa)
    else:
        cal_eqa = await process_string_with_d(eqa)
    if string[i:] == "":
        reply = f"{username}: "
    else:
        while string[i] == " ":
            i = i + 1
        reply = f"{string[i:]}: "
    try:
        if cal_eqa.isdigit():
            reply = reply + eqa + "=" + cal_eqa
        elif k_flag:
            reply = reply + eqa + '=' + dis_eqa + '=' + cal_eqa + "=" + str(eval(cal_eqa))
        else:
            # print(cal_eqa)
            reply = reply + eqa + "=" + cal_eqa + "=" + str(eval(cal_eqa))
    except SyntaxError:
        _log.error("Error calculating cal_eqa")
        return "表达式错误，未成功计算表达式。"
    return reply


def roll(dice_num=1, dice_size=100, symbol="+"):
    result = []
    if dice_num > 1:
        for i in range(dice_num):
            result.append(str(random.randint(1, dice_size)))
        # print(dice_num,dice_size,"+".join(result))
        return "(" + symbol.join(result) + ")"
    else:
        return str(random.randint(1, dice_size))
