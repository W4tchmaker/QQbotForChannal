import random
from config import resources_path


async def gen_motivation(person):
    motivation = ["自傲", "占有", "本能", "破坏", "优越感", "怠惰", "逃避", "好奇心", "刺激", "喜悦", "愤怒",
                  "悲伤", "幸福", "不安", "厌恶", "恐怖", "嫉妒", "仇恨", "正义", "崇拜", "善恶", "野心", "理性",
                  "胜利", "秩序", "憧憬", "无私", "友情", "爱", "恋", "依存", "尊敬", "轻蔑", "庇护", "支配", "奉献",
                  "溺爱", "后悔", "孤独", "悲观", "绝望", "拒绝", "疑念", "罪恶感", "疯狂", "劣等感"]

    outer = random.choice(motivation)
    inner = random.choice(motivation)
    root = random.choice(motivation)

    return f"{person}的动机为 表现:{outer} 内里:{inner} 根源:{root}"
