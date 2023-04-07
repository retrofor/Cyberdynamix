from ...Shinweb.plugin import Plugin
import random


class RollDicePlugin(Plugin):
    """
    插件：掷骰子
    """

    def __init__(self, num, sides):
        self.num = int(num)
        self.sides = int(sides)

    def run(self):
        # 创建一个列表来存储每次掷骰的点数
        rolls = []
        for i in range(self.num):
            # 在 1 和骰子面数之间选择一个随机整数
            roll = random.randint(1, self.sides)
            # 将随机整数添加到列表中
            rolls.append(roll)

        # 计算所有点数的总和
        total = sum(rolls)

        # 根据格式返回结果字符串
        return f'掷骰{self.num}d{self.sides}={"+".join(str(x) for x in rolls)}={total}'
