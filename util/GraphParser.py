'''
Eric H. Lee
erhlee.bird@gmail.com

GraphParser.py
'''
import sys
import os
import Node
import Edge

class GraphParser:
    """Class used to parse graph files in formats like .gexf"""

    def __init__(self, fileName):
        try:
            file = open(fileName, 'r')
            self.parse(file, os.path.splitext(fileName)[1])
            file.close()
        except IOError as e:
            print("({}))".format(e))
            sys.exit(1)

    def parse(self, file, extension):
        self.graphData = ['',{},[]]
        if extension == '.gexf':
            self.gexfParser(file)

    def gexfParser(self, file):
        for line in file:
            line = line.rstrip().lstrip()
            if line.startswith("<description>"):
                line.replace('<description>', '')
                line.replace('</description>', '')
                self.graphData[0] = line
            elif line.startswith('<node '):
                info = line.split(' ')

                name = info[2][7:].replace('"', '')
                id = int(info[1][4:].replace('"', ''))
                self.graphData[1][id] = Node.Node(id, name, 0)
            elif line.startswith('<edge '):
                info = line.split(' ')

                for data in info:
                    if data.startswith('source'):
                        cutPoint = data[8:].index('"')
                        source = int(data[8:][:cutPoint])
                    elif data.startswith('target'):
                        cutPoint = data[8:].index('"')
                        target = int(data[8:][:cutPoint])
                edge = Edge.Edge(self.graphData[1][source], self.graphData[1][target])
                if not target in self.graphData[1][source].connections:
                    self.graphData[1][source].connections[target] = []
                if not source in self.graphData[1][target].connections:
                    self.graphData[1][target].connections[source] = []
                self.graphData[1][source].connections[target].append(edge)
                self.graphData[1][target].connections[source].append(edge)
                self.graphData[2].append(edge)
