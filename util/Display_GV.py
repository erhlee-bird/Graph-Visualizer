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
    """The Canvas in charge of all the visual graph effects"""

    minDist = 20
    minSize = 5
    activeNode = None
    showEdges = True

    def __init__(self, parent):
        size = (self.minDist ** 2 + self.minSize * 2) + self.minDist ** 2 + self.minSize
        Tkinter.Canvas.__init__(self, parent, width=size, height=size)

        baseName ="Graph_Data/"
        fileName = "photoviz dynamic.gexf"#"example.gexf"
        self.parser = GraphParser.GraphParser(''.join([baseName,fileName]))

        self.centerPoint = self.minDist ** 2 + self.minSize * 2
        self.scan_mark(self.centerPoint, self.centerPoint)
        self.scan_dragto(self.centerPoint, self.centerPoint)

        self.bind("<Motion>", self.interact)
        #self.bind("<Button-1>", lambda(evt): self.scan_mark(evt.x, evt.y))
        #self.bind("<B1-Motion>", lambda(evt): self.scan_dragto(evt.x, evt.y, 2))

        self.createGrid()

    def createGrid(self):
        self.builtNodes = {}
        self.builtEdges = []
        self.tempNodes = []
        self.tempEdges = []
        self.createNodes()
        self.createEdges()

    def interact(self, event):
        for node in self.builtNodes.itervalues():
            if node.findDistBetween((event.x, event.y)) <= node.radius:
                if not self.activeNode:
                    self.clearTemp()
                    self.findEdges(node)
                    self.analyzeEdges(node)
                    self.drawEdges(self.tempEdges)
                    self.activeNode = node
                    self.tempNodes.append(self.create_oval(node.loc, fill="blue"))
                return
        if self.tempNodes or self.tempEdges:
            self.clearTemp()

    def toggleEdges(self, event):
        self.showEdges = not self.showEdges
        self.clearTemp()
        for edge in self.builtEdges:
            self.reDraw(self) if self.showEdges else self.delete(edge.cID)

    def findEdges(self, node):
        for edge in self.parser.graphData[2]:
            if node in (edge.source, edge.target):
                self.tempEdges.append(edge)

    def analyzeEdges(self, node):
        # Green for one way outwards, Orange for mutual, Yellow for one way inwards
        unprocessed = list(self.tempEdges)
        while len(unprocessed) > 0:
            edge = unprocessed.pop(0)
            if self.intCheck(edge): continue
            edgeContents = (edge.source, edge.target)
            color = "green" if node == edge.source else "yellow"
            for next in unprocessed:
                if self.intCheck(next): continue
                nextContents = (next.source, next.target)
                if edgeContents == nextContents[::-1]:
                    next.color = color = "orange"
                    unprocessed.remove(next)
            self.tempNodes.append(self.create_oval(node == edge.source and edge.target.loc or edge.source.loc, fill=color))
            edge.color = color

    def clearTemp(self):
        self.activeNode = None
        for node in self.tempNodes:
            self.delete(node)
        self.tempNodes = []
        for edge in self.tempEdges:
            self.delete(edge.cID)
        self.tempEdges = []
        if self.showEdges:
            for edge in self.builtEdges:
                edge.color = "gray"
                edge.reDraw(self)
        self.drawNodes()

    def intCheck(self, obj):
        return type(next).__name__ == "int"

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

    def createNodes(self):
        for node in self.parser.graphData[1].itervalues():
            if node in self.builtNodes: continue
            self.findEdges(node)
            node.numEdges = len(self.tempEdges)
            self.tempEdges = []
            nodeCoords = None
            while not nodeCoords or self.overlap(nodeCoords):
                nodeCoords = self.mapNode(node.numEdges)
            node.build(nodeCoords, self.create_oval(nodeCoords, fill="red"))
            self.builtNodes[node.id] = node

    def drawNodes(self):
        for node in self.builtNodes.itervalues():
            node.reDraw(self)

    def createEdges(self):
        for edge in self.parser.graphData[2]:
            if self.intCheck(edge): continue # Self Linked Node
            edge.reDraw(self)
            if not edge.cID: continue
            self.builtEdges.append(edge)

    def drawEdges(self, container):
        for edge in container:
            if self.intCheck(edge): continue #Self Linked Node
            edge.reDraw(self)
#            if not edge.cID: continue
