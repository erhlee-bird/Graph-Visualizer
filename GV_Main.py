'''
Eric H. Lee
erhlee.bird@gmail.com

GV_Main.py
'''
import sys
import Tkinter
from util import Display_GV, Matrix_GV

class GV_Main:
    """Main class for the Graph-Visualizer Project"""

    def __init__(self, fileName):
        self.initGUI(fileName)

    def initGUI(self, fileName):
        graphDsp = self.canvasScreen(fileName)
        #matrixDsp = self.matrixScreen()
        graphDsp.mainloop()

    def canvasScreen(self, fileName):
        graphScreen = Tkinter.Tk()
        graphScreen.title("Graph-Visualizer")

        frame = Tkinter.Frame(graphScreen)
        frame.pack(side=Tkinter.RIGHT)

        self.display = canvas = Display_GV.Display_GV(graphScreen, fileName)
        canvas.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)

        toggleButton = Tkinter.Button(frame)
        toggleButton.configure(text="Toggle Edges", background="orange")
        toggleButton.pack(side=Tkinter.TOP)
        toggleButton.bind("<Button-1>", canvas.toggleEdges)

        recenterButton = Tkinter.Button(frame)
        recenterButton.configure(text="Recenter Canvas", background="red")
        recenterButton.pack(side=Tkinter.BOTTOM)
        recenterButton.bind("<Button-1>", canvas.centerScreen)

        return graphScreen

    def matrixScreen(self):
        matrixScreen = Tkinter.Tk()
        matrixScreen.title("Graph Matrix")

        matrixFrame = Tkinter.Frame(matrixScreen)
        matrixFrame.pack()

        canvas = Matrix_GV.Matrix_GV(matrixScreen, self.display.generateMatrix())
        canvas.pack(expand=True, fill=Tkinter.BOTH)

        return matrixScreen

if __name__ == "__main__":
    fileName = ''
    if (len(sys.argv) > 1):
        fileName = sys.argv[1]
    GV_Main(fileName)
