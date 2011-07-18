'''
Eric H. Lee
erhlee.bird@gmail.com

Display_GV.py
'''
import Tkinter
import GraphParser
import Assortment_Algorithms as AA
import Node
import Edge

class Display_GV(Tkinter.Canvas):
    """The Canvas in charge of all the visual graph effects"""

    sizer = 2
    activeNode = None
    showEdges = False

    def __init__(self, parent):
        baseName ="Graph_Data/"
        fileName = "yeast.gexf"
        #fileName = "photoviz dynamic.gexf"
        #fileName = "example.gexf"
        self.parser = GraphParser.GraphParser(''.join([baseName,fileName]))
        self.assertConstants(self.parser.graphData)

        Tkinter.Canvas.__init__(self, parent, width=self.size, height=self.size)

        self.bind("<Motion>", self.interact)
        self.bind("<Button-1>", self.select)
        self.bind("<B1-Motion>", self.selectedMove)
        self.bind("<Button-2>", lambda(evt): self.scan_mark(evt.x, evt.y))
        self.bind("<B2-Motion>", lambda(evt): self.scan_dragto(evt.x, evt.y, 1))

        self.createGrid()
        #self.generateMatrix()

    def assertConstants(self, data):
        self.minSize = 5
        self.scale = 1
        self.size = 0
        for node in data[1].itervalues():
            radius = self.minSize + len(node.connections)
            self.size += radius ** 2 * 3.14
        self.size = self.size ** .5 + len(data[1])
        self.AA = AA.Assortment_Algorithms((self.size, self.minSize, self.scale))

    # Finished Methods
    def generateMatrix(self):
        matrix = []
        for id, node in self.builtNodes.items():
            matrix.insert(id, [0] * len(self.builtNodes))
            for edges in node.connections.itervalues():
                if self.intCheck(edges):
                    matrix[id][id] = 1
                else:
                    for edge in edges:
                        target = edge.target if edge.source == node else edge.source
                        matrix[id][target.id] = 1
        print(matrix)

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
                if self.failCounter > 100:
                    break
                nodeCoords = self.mapNode(node.numEdges)
            node.build(nodeCoords, self.create_oval(nodeCoords, fill=node.color))
            self.builtNodes[node.id] = node

    def createEdges(self):
        for edge in self.parser.graphData[2]:
            if self.intCheck(edge): continue # Self Linked Node
            if self.showEdges:
                edge.reDraw(self)
            self.builtEdges.append(edge)

    def centerScreen(self, event):
        cX, cY = map(int, self.convertCanvasCoords((self.size * .5,) * 2))
        self.scan_mark(0, 0)
        self.scan_dragto(cX - self.size * .5, cY - self.size * .5, 1)

    def intCheck(self, obj):
        return type(obj).__name__ == "int"

    def mapNode(self, num):
        # Determine which Graph you want to appear
        # self.randLocRandom, self.randLocSize, self.randLocHyperbolic
        newX, newY = self.size * .5 + self.AA.randLocSize(num), self.size * .5 + self.AA.randLocSize(num)
        modD = self.minSize + num * self.scale
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

    def convertCanvasCoords(self, coords):
        return (self.canvasx(coords[0]), self.canvasy(coords[1]))

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

