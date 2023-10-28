import random


class FiascoPlot:
    def __init__(self):
        self.plots = {}

    async def start_fiasco(self, channel_id, plot_name):
        self.plots[channel_id] = {}
        self.plots[channel_id]["name"] = [plot_name]
        self.plots[channel_id]["player_num"] = 0
        return f"已开始剧本{plot_name}"

    async def end_fiasco(self, channel_id):
        if channel_id in self.plots:
            del self.plots[channel_id]
            return f"已结束当前频道的游戏"
        else:
            return f"当前频道无游戏"

    async def add_player(self, channel_id, player_name):
        if player_name not in self.plots[channel_id]:
            self.plots[channel_id]["player_num"] = self.plots[channel_id]["player_num"] + 1
            self.plots[channel_id][player_name] = []
            return f"{player_name}加入当前空前惨败对局"
        else:
            return f"{player_name}已在游戏中"

    async def rolling_dices(self, channel_id):
        plot = self.plots[channel_id]
        reply = f"一把黑白骰子咕噜噜的在桌子上滚动\n"
        plot["white"] = []
        for i in range(2 * plot["player_num"]):
            plot["white"].append(str(random.randint(1, 6)))
        reply = reply + f"白色骰子: {' '.join(plot['white'])}\n"
        plot["black"] = []
        for i in range(2 * plot["player_num"]):
            plot["black"].append(str(random.randint(1, 6)))
        reply = reply + f"黑色骰子: {' '.join(plot['black'])}\n"
        return reply

    async def picking_dices(self, channel_id, player_name, string):
        plot = self.plots[channel_id]
        if player_name not in plot:
            return "你没有加入游戏"
        if string[0] == "白":
            color = "white"
        elif string[0] == "黑":
            color = "black"
        else:
            return "请输入正确颜色"

        dice_num = string[1]
        if dice_num in plot[color]:
            plot[color].remove(dice_num)
            plot[player_name].append(string)
            reply = f"{player_name}拿走了 {string}\n"
            reply = reply + f"{player_name}现有的骰子为 {' '.join(plot[player_name])}\n"
            reply = reply + f"现有的白色骰子为 {' '.join(plot['white'])}\n"
            reply = reply + f"现有的黑色骰子为 {' '.join(plot['black'])}\n"
            return reply
        else:
            return f"{player_name}试图拿走 {string}，但无该骰子"

    async def reroll(self, channal_id, player_name=None, public=False):
        plot = self.plots[channal_id]
        if public:
            for i in range(len(plot["white"])):
                plot["white"][i] = str(random.randint(1, 6))
            for i in range(len(plot["black"])):
                plot["black"][i] = str(random.randint(1, 6))
            reply = "剩下的骰子经过了一次重骰\n"
            reply = reply + f"现有的白色骰子为 {' '.join(plot['white'])}\n"
            reply = reply + f"现有的黑色骰子为 {' '.join(plot['black'])}\n"
            return reply
        elif player_name:
            if player_name not in plot:
                return "你没有加入游戏"
            for i in range(len(plot[player_name])):
                plot[player_name][i] = plot[player_name][i][0] + str(random.randint(1, 6))
            reply = f"{player_name}经过了一次重骰\n"
            reply = reply + f"现有的白色骰子为 {' '.join(plot[player_name])}\n"
            return reply


fiasco_sv = FiascoPlot()


