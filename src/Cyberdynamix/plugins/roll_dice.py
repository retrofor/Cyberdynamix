import random

from Cyberdynamix.plugin import Plugin

class roll_dice(Plugin):
    def __init__(self, num, sides) -> None:
        self.num = int(num)
        self.sides = int(sides)


    def run(self):
        total = 0
        for _ in range(self.num):
            roll = random.randint(1, self.sides)
            total += roll
        return total
 