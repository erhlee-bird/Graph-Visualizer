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

    activeNode = None
    showEdges = False

    def __init__(self, parent):
        baseName ="Graph_Data/"
        #fileName = "yeast.gexf"
        fileName = "photoviz dynamic.gexf"
        #fileName = "example.gexf"
        self.parser = GraphParser.GraphParser(''.join([baseName,fileName]))
        self.assertConstants(self.parser.graphData)

        if self.size > parent.winfo_screenwidth() or self.size > parent.winfo_screenheight():
            sSize = min(parent.winfo_screenwidth(), parent.winfo_screenheight())
            Tkinter.Canvas.__init__(self, parent, width=sSize, height=sSize)
        else:
            Tkinter.Canvas.__init__(self, parent, width=self.size, height=self.size)

        self.bind("<Motion>", lambda(evt): self.interact(*self.convertCanvasCoords((evt.x, evt.y))))
        self.bind("<B1-Motion>", lambda(evt): self.selectedMove(*self.convertCanvasCoords((evt.x, evt.y))))
        self.bind("<Button-2>", lambda(evt): self.scan_mark(evt.x, evt.y))
        self.bind("<B2-Motion>", lambda(evt): self.scan_dragto(evt.x, evt.y, 1))

        self.createGrid()
        #self.generateMatrix()

    # Finished Methods
    def assertConstants(self, data):
        stat = 5, 1 # MinSize, Scale
        self.size = sum([(stat[1] + len(n.connections)) ** 2 * 3.14 for n in data[1].itervalues()]) ** .5 + len(data[1])
        self.AA = AA.Assortment_Algorithms(self.size, *stat)

    def generateMatrix(self):
        matrix = []
        for id, node in self.builtNodes.items():
            matrix.insert(id, [0] * len(self.builtNodes))
            for edges in node.connections.itervalues():
                if type(edges).__name__ == "int":
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
                nodeCoords = self.AA.mapNode(node.numEdges)
            node.build(nodeCoords, self.create_oval(nodeCoords, fill=node.color))
            self.builtNodes[node.id] = node

    def createEdges(self):
        for edge in self.parser.graphData[2]:
            if self.showEdges:
                edge.reDraw(self)
            self.builtEdges.append(edge)

    def centerScreen(self, event):
        cX, cY = self.convertCanvasCoords((self.size * .5,) * 2)
        self.scan_mark(*map(int, (self.size * .5, self.size * .5)))
        self.scan_dragto(*map(int, (cX - self.size * .5, cY - self.size * .5)), gain=1)

    def overlap(self, coords):
        x, y, dx, dy = coords
        overlaps = len(self.find_overlapping(x, y, dx, dy))
        if overlaps:
            self.failCounter += 1
        return overlaps

    def drawNodes(self):
        map(lambda(e): e.reDraw(self), self.builtNodes.itervalues())

    def drawEdges(self, collection):
        map(lambda(e): e.reDraw(self), collection)

    def reset(self):
        list = []
        for edges in self.activeNode.connections.itervalues():
            for edge in edges:
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
            map(lambda(e): self.delete(e.cID), self.builtEdges)

    def convertCanvasCoords(self, coords):
        return (self.canvasx(coords[0]), self.canvasy(coords[1]))

    def analyzeConnections(self, node):
        for edges in node.connections.itervalues():
            if len(edges) == 1:
                if edges[0].source == node:
                    edges[0].color = "green"
                    edges[0].target.color = "green"
                else:
                    edges[0].color = "yellow"
                    edges[0].source.color = "yellow"
                edges[0].reDraw(self)
            else:
                for edge in edges:
                    edge.color = "orange"
                    edge.target.color = "orange"
                    edge.source.color = "orange"
                    edge.reDraw(self)
        node.color = "blue"
        self.drawNodes()

    # Optimizable Methods
    def filterNode(self, obj):
        return filter(lambda(e): e.cID == obj, self.builtNodes.itervalues())

    def filterOverlaps(self, x, y):
        return filter(lambda(e): self.type(e) == "oval", self.find_overlapping(x, y, x, y))

    def interact(self, x, y):
        node = map(self.filterNode, self.filterOverlaps(x, y))
        if self.activeNode:
            self.reset()
        if node:
            self.activeNode = node[0][0]
            self.analyzeConnections(node[0][0])

    def selectedMove(self, x, y):
        if self.activeNode:
            radius = self.activeNode.radius
            self.activeNode.build((x - radius, y - radius, x + radius, y + radius), self.activeNode.cID)
            map(lambda(e): self.drawEdges(e), self.activeNode.connections.itervalues())
            self.activeNode.reDraw(self)

