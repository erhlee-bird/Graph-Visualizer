'''
Eric H. Lee
erhlee.bird@gmail.com

Assortment_Algorithms.py
'''
import random

class Assortment_Algorithms:
    """A class in charge of calculating node placements"""

    def __init__(self, size, min, sizer):
        self.cSize, self.minSize, self.scale = size, min, sizer

    def mapNode(self, num):
        # Determine which Graph you want to appear
        # self.randLocRandom, self.randLocSize, self.randLocHyperbolic
        newX, newY = self.cSize * .5 + self.randLocSize(num), self.cSize * .5 + self.randLocSize(num)
        modD = self.minSize + num * self.scale
        return (newX, newY, newX + modD, newY + modD)

    def randLocRandom(self):
        return random.randint(-(self.cSize / 2), (self.cSize / 2))

    def randLocSize(self, nodeSize):
        if not nodeSize: nodeSize = 0.5
        diff = nodeSize / 5.0
        if diff < 1: diff = 1
        numBound = self.cSize / 2
        return random.randint(-int(numBound / diff), int(numBound / diff))

    def randLocHyperbolic(self, nodeSize):
        if not nodeSize: nodeSize = 0.5
        diff = nodeSize / 5.0
        if diff < 1: diff = 1
        mod = self.minSize ** self.scale
        startCheck =  self.minSize * self.scale ** 2 + self.minDist - nodeSize * 2
        endCheck = (self.minDist ** 2 + mod) / diff
        sign = -1 if random.randint(0,1) == 0 else 1
        return sign * random.randint(int(startCheck), int(endCheck))
