'''
Eric H. Lee
erhlee.bird@gmail.com

Node.py
'''
import math

class Node:
    """The container class for each Node"""

    def __init__(self, id, name, numEdges):
        self.id = id
        self.name = name
        self.numEdges = numEdges
        self.color = "red"
        self.cID = 0
        self.loc = (None, None, None, None)
        self.center = (None, None)
        self.radius = None
        self.connections = {}

    def findDistBetween(self, nodeC):
        return ((nodeC[0] - self.center[0]) ** 2 + (nodeC[1] - self.center[1]) ** 2) ** .5

    def findCenter(self):
        return (self.loc[0] + self.radius, self.loc[1] + self.radius)

    def findRadius(self):
        return abs((self.loc[2] - self.loc[0]) / 2.0)

    def circleEdge(self, target):
        sC, tC = self.center, target.center
        sR, tR = self.radius, target.radius
        dX, dY = tC[0] - sC[0], tC[1] - sC[1]
        if not dX or not dY: return # Node links to itself
        angle = abs(math.atan(dY / dX))
        xMod, yMod = 1 and dX > 0 or -1, 1 and dY > 0 or -1
        sX, sY = sC[0] + xMod * (sR * math.cos(angle)), sC[1] + yMod * (sR * math.sin(angle))
        tX, tY = tC[0] - xMod * (tR * math.cos(angle)), tC[1] - yMod * (tR * math.sin(angle))
        return ((sX, sY), (tX, tY))

    def build(self, coords, cID):
        self.cID = cID
        self.loc = coords
        self.radius = self.findRadius()
        self.center = self.findCenter()

    def reDraw(self, canvas):
        canvas.delete(self.cID)
        canvas.create_oval(self.loc, fill=self.color)
