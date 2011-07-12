'''
Eric H. Lee
erhlee.bird@gmail.com

Edge.py
'''
import Node

class Edge:
    """The container class for each Edge"""

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.color = "orange"
        self.cID = 0

    def reDraw(self, canvas):
        canvas.delete(self.cID)
        edgePoints = self.source.circleEdge(self.target)
        if not edgePoints: return # Self Linked Node
        return canvas.create_line(edgePoints, fill=self.color)
