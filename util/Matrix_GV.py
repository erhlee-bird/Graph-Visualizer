'''
Eric H. Lee
erhlee.bird@gmail.com

Matrix_GV.py
'''
import Tkinter

class Matrix_GV(Tkinter.Canvas):
    """This canvas generates an adjacency matrix image for the graph"""

    def __init__(self, parent, matrix):
        Tkinter.Canvas.__init__(self, parent, height=parent.winfo_screenheight() / 2, width=parent.winfo_screenheight() / 2)
        self.drawMatrix(parent.winfo_screenheight() /2, matrix)

    def plotSquare(self, squareSize, color, x, y):
        nY, nX = x * squareSize, y * squareSize
        self.create_rectangle(nX, nY, nX + squareSize, nY + squareSize, fill=color, outline='white')

    def drawMatrix(self, size, matrix):
        numNodes = len(matrix)
        squareSize = size / numNodes
        if squareSize == 1: squareSize = 2
        for x in range(numNodes):
            map(lambda(y): self.plotSquare(squareSize, 'black' if matrix[x][y] else 'white', x, y), range(numNodes))
