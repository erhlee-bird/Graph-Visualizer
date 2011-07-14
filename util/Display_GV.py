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
        size = (self.minDist ** 2 + self.minSize * 2) + self.minDist ** 2 + self.minSize ** 2
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

    # Finished Methods
    def createGrid(self):
        self.builtNodes = {}
        self.builtEdges = []
        self.tempNodes = []
        self.createNodes()
        self.createEdges()
        self.drawNodes()

    def createNodes(self):
        for node in self.parser.graphData[1].itervalues():
            if node in self.builtNodes: continue
            node.numEdges = len(node.connections)
            nodeCoords = None
            while not nodeCoords or self.overlap(nodeCoords):
                nodeCoords = self.mapNode(node.numEdges)
            node.build(nodeCoords, self.create_oval(nodeCoords, fill=node.color))
            self.builtNodes[node.id] = node

    def createEdges(self):
        for edge in self.parser.graphData[2]:
            if self.intCheck(edge): continue # Self Linked Node
            edge.reDraw(self)
            if not edge.cID: continue
            self.builtEdges.append(edge)

    def intCheck(self, obj):
        return type(obj).__name__ == "int"

    def randLoc(self, num):
        if not num: num = 1
        diff = num / 5.0
        if diff < 1: diff = 1
        return random.randint(-(self.minDist ** 2), self.minDist ** 2) / diff

    def mapNode(self, num):
        newX, newY = self.centerPoint + self.randLoc(num), self.centerPoint + self.randLoc(num)
        modD = self.minSize + num
        return (newX, newY, newX + modD, newY + modD)

    def overlap(self, coords):
        nodeC = (coords[0] + (coords[2] - coords[0]) / 2, coords[1] + (coords[3] - coords[1]) / 2)
        for node in self.builtNodes.itervalues():
            if node.findDistBetween(nodeC) < self.minDist + node.radius + self.minSize:
                return True
        return False

    def drawNodes(self):
        for node in self.builtNodes.itervalues():
            node.reDraw(self)

    def drawEdges(self, collection):
        for edge in collection:
            if self.intCheck(edge): continue #Self Linked Node
            edge.reDraw(self)

    def reset(self):
        if self.activeNode:
            list = []
            for edges in self.activeNode.connections.itervalues():
                for edge in edges:
                    if self.intCheck(edge): continue
                    edge.color = "gray"
                    edge.source.color = "red"
                    edge.target.color = "red"
                    self.delete(edge.cID)
                    if self.showEdges:
                        list.append(edge)
            self.drawEdges(list)
            self.drawNodes()
        self.activeNode = None

    def toggleEdges(self, event):
        self.showEdges = not self.showEdges
        if self.showEdges:
            self.drawEdges(self.builtEdges)
        else:
            for edge in self.builtEdges:
                self.delete(edge.cID)
        self.drawNodes()

    # Optimizable Methods
    def interact(self, event):
        for node in self.builtNodes.itervalues():
            if node.findDistBetween((event.x, event.y)) <= node.radius:
                if not self.activeNode:
                    self.activeNode = node
                    self.analyzeConnections(node)
                return
        if self.activeNode:
            self.reset()

    def analyzeConnections(self, node):
        for edges in node.connections.itervalues():
            if len(edges) == 1:
                if self.intCheck(edges[0]): continue
                if edges[0].source == node:
                    edges[0].color = "green"
                    edges[0].target.color = "green"
                else:
                    edges[0].color = "yellow"
                    edges[0].source.color = "yellow"
                edges[0].reDraw(self)
            else:
                for edge in edges:
                    if self.intCheck(edge): continue
                    edge.color = "orange"
                    edge.target.color = "orange"
                    edge.source.color = "orange"
                    edge.reDraw(self)
        node.color = "blue"
        self.drawNodes()
