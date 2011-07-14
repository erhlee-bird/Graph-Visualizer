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

    sizer = 3
    minDist = 20
    minSize = 5
    activeNode = None
    showEdges = True

    def __init__(self, parent):
        self.size = ((self.minDist ** 2 + self.minSize * self.sizer) + self.minDist ** 2 + self.minSize ** 2)
        Tkinter.Canvas.__init__(self, parent, width=self.size, height=self.size)

        baseName ="Graph_Data/"
        fileName = "photoviz dynamic.gexf"#"yeast.gexf"#"photoviz dynamic.gexf"#"example.gexf"
        self.parser = GraphParser.GraphParser(''.join([baseName,fileName]))

        self.centerPoint = self.minDist ** 2 + self.minSize ** self.sizer

        self.bind("<Motion>", self.interact)
        self.bind("<Button-1>", self.select)
        self.bind("<B1-Motion>", self.selectedMove)
        self.bind("<Button-2>", lambda(evt): self.scan_mark(evt.x, evt.y))
        self.bind("<B2-Motion>", lambda(evt): self.scan_dragto(evt.x, evt.y, 1))

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
            self.failCounter = 0
            while not nodeCoords or self.overlap(nodeCoords):
                if self.failCounter > 25:
                    break
                nodeCoords = self.mapNode(node.numEdges)
            node.build(nodeCoords, self.create_oval(nodeCoords, fill=node.color))
            self.builtNodes[node.id] = node

    def createEdges(self):
        for edge in self.parser.graphData[2]:
            if self.intCheck(edge): continue # Self Linked Node
            edge.reDraw(self)
            if not edge.cID: continue
            self.builtEdges.append(edge)

    def centerScreen(self, event):
        cX, cY = map(int, self.convertCanvasCoords((self.centerPoint,) * 2))
        self.scan_mark(0, 0)
        self.scan_dragto(cX - self.centerPoint, cY - self.centerPoint, 1)

    def intCheck(self, obj):
        return type(obj).__name__ == "int"

    def randLocRandom(self, num):
        numBound = self.minDist ** 2 + self.minSize ** self.sizer
        return random.randint(-numBound, numBound)

    def randLocSize(self, num):
        if not num: num = 0.5
        diff = num / 5.0
        if diff < 1: diff = 1
        numBound = self.minDist ** 2 + self.minSize ** self.sizer
        return random.randint(-int(numBound / diff), int(numBound / diff))

    def randLocHyperbolic(self, num):
        if not num: num = 0.5
        diff = num / 5.0
        if diff < 1: diff = 1
        mod = self.minSize ** self.sizer
        startCheck = self.minSize * self.sizer ** 2 + self.minDist - num * 2
        endCheck = (self.minDist ** 2 + mod) / diff
        sign = -1 if random.randint(0,1) == 0 else 1
        return sign * random.randint(int(startCheck), int(endCheck))

    def mapNode(self, num):
        # Determine which Graph you want to appear
        # self.randLocRandom, self.randLocSize, self.randLocHyperbolic
        newX, newY = self.centerPoint + self.randLocSize(num), self.centerPoint + self.randLocSize(num)
        modD = self.minSize + num
        return (newX, newY, newX + modD, newY + modD)

    def overlap(self, coords):
        x, y, dx, dy = coords
        overlaps = len(self.find_overlapping(x, y, dx, dy))
        if overlaps:
            self.failCounter += 1
        return overlaps

    def drawNodes(self):
        for node in self.builtNodes.itervalues():
            node.reDraw(self)

    def drawEdges(self, collection):
        for edge in collection:
            if self.intCheck(edge): continue #Self Linked Node
            edge.reDraw(self)

    def reset(self):
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
        self.activeNode.color = "red"
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

    def convertCanvasCoords(self, coords):
        return (self.canvasx(coords[0]), self.canvasy(coords[1]))

    # Optimizable Methods
    def interact(self, event):
        x, y = self.convertCanvasCoords((event.x, event.y))
        overlaps = self.find_overlapping(x, y, x, y)
        if self.activeNode:
            if len(overlaps) == 0:
                self.reset()
        else:
            for obj in overlaps:
                if not self.type(obj) == "oval": continue
                for node in self.builtNodes.itervalues():
                    if obj == node.cID:
                        self.activeNode = node
                        self.analyzeConnections(node)
                        return

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

    def select(self, event):
        x, y = self.convertCanvasCoords((event.x, event.y))
        overlaps = self.find_overlapping(x, y, x, y)
        if len(overlaps) > 0:
            for obj in overlaps:
                if not self.type(obj) == "oval": continue
                for node in self.builtNodes.itervalues():
                    if obj == node.cID:
                        self.activeNode = node
                        return

    def selectedMove(self, event):
        if self.activeNode:
            x, y = self.convertCanvasCoords((event.x, event.y))
            radius = self.activeNode.radius
            self.activeNode.build((x - radius, y - radius, x + radius, y + radius), self.activeNode.cID)
            for edges in self.activeNode.connections.itervalues():
                for edge in edges:
                    edge.reDraw(self)
            self.activeNode.reDraw(self)
