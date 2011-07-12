'''
Eric H. Lee
erhlee.bird@gmail.com

Display_GV.py
'''
import Tkinter
import GraphParser
import Node
import Edge
import random

class Display_GV(Tkinter.Canvas):
    activeNode = [None, None]
    tempNodes = []
    showEdges = False

    def __init__(self, minDist, minSize, parent, width, height):
        Tkinter.Canvas.__init__(self, parent, width=width, height=height)
        self.minDist = minDist
        self.minSize = minSize

        fileName = "Graph_Data/example.gexf"#"photoviz dynamic.gexf"
        self.parser = GraphParser.GraphParser(fileName)

        self.centerPoint = self.minDist ** 2 + self.minSize * 2
        self.scan_mark(self.centerPoint, self.centerPoint)
        self.scan_dragto(self.centerPoint, self.centerPoint)

        self.bind("<Motion>", self.interact)
        #self.bind("<Button-1>", lambda(evt): self.scan_mark(evt.x, evt.y))
        #self.bind("<B1-Motion>", lambda(evt): self.scan_dragto(evt.x, evt.y, 2))

        self.createGrid()

    def interact(self, event):
        color = not self.showEdges and "orange" or "blue"
        for node in self.builtNodes.itervalues():
            coords = node.loc
            if node.findDistBetween((event.x, event.y)) <= node.radius:
                if not self.activeNode[0] == node:
                    self.clearTemp()
                    self.findEdges(node)
                    self.analyzeEdges(node)
                    self.drawEdges(self.builtEdges)
                    self.activeNode = [node, self.create_oval(coords, fill="blue")]
                return
        if self.activeNode[1]:
            self.clearTemp()

    def toggleEdges(self, event):
        self.showEdges = not self.showEdges
        self.clearEdges()
        if self.showEdges:
            for edge in self.parser.graphData[2]:
                edge.color = "gray"
            self.drawEdges(self.parser.graphData[2])

    def findEdges(self, node):
        for edge in self.parser.graphData[2]:
            if node in (edge.source, edge.target):
                self.builtEdges.append(edge)

    def analyzeEdges(self, node):
        unprocessed = list(self.builtEdges)
        while len(unprocessed) > 0:
            # Green for one way outwards, Orange for mutual, Yellow for one way inwards
            color = "green"
            edge = unprocessed.pop(0)
            if type(edge).__name__ == "int": continue
            if edge.source == node:
                color = "green"
                for next in unprocessed:
                    if type(next).__name__ == "int": continue
                    if next.source == edge.target:
                        color = next.color = "orange"
                        unprocessed.remove(next)
            if edge.target == node:
                color = "yellow"
                for next in unprocessed:
                    if type(next).__name__ == "int": continue
                    if next.target == edge.source:
                        color = next.color = "orange"
                        unprocessed.remove(next)
            edge.color = color

    def clearEdges(self):
        for edge in self.builtEdges:
            self.delete(edge)
        self.builtEdges = []

    def clearTemp(self):
        self.delete(self.activeNode[1])
        self.activeNode = [None, None]
        for node in self.tempNodes:
            self.delete(node.cID)
        self.clearEdges()
        for edge in self.parser.graphData[2]:
            edge.color = "gray"
        self.showEdges and self.drawEdges(self.parser.graphData[2])
#        if self.showEdges:
#            self.drawEdges(self.parser.graphData[2])

    def mapNode(self, num):
        randX = random.randint(-(self.minDist ** 2), self.minDist ** 2)
        randY = random.randint(-(self.minDist ** 2), self.minDist ** 2)
        newX, newY = self.centerPoint + randX, self.centerPoint + randY
        modD = self.minSize + num
        return (newX, newY, newX + modD, newY + modD)

    def overlap(self, coords):
        nodeC = (coords[0] + (coords[2] - coords[0]) / 2, coords[1] + (coords[3] - coords[1]) / 2)
        for node in self.builtNodes.itervalues():
            if node.findDistBetween(nodeC) < self.minDist + node.radius + self.minSize:
                return True
        return False

    def createGrid(self):
        self.builtNodes = {}
        self.builtEdges = []
        self.createNodes()

    def createNodes(self):
        for node in self.parser.graphData[1].itervalues():
            if node in self.builtNodes: continue
            self.findEdges(node)
            node.numEdges = len(self.builtEdges)
            self.builtEdges = []
            nodeCoords = None
            while not nodeCoords or self.overlap(nodeCoords):
                nodeCoords = self.mapNode(node.numEdges)
            node.build(nodeCoords, self.create_oval(nodeCoords, fill="gray"))
            self.builtNodes[node.id] = node

    def drawNodes(self):
        for node in self.builtNodes.itervalues():
            node.reDraw(self)

    def drawEdges(self, container):
        for edge in container:
            if type(edge).__name__ == "int": continue # Self Linked Node
            builtEdge = edge.reDraw(self)
            if not builtEdge: continue
            self.builtEdges.append(builtEdge)
        self.drawNodes()
