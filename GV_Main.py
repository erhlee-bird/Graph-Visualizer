'''
Eric H. Lee
erhlee.bird@gmail.com

GV_Main.py
'''
import Tkinter
from util import Display_GV

class GV_Main:
    """Main class for the Graph-Visualizer Project"""

    minDist = 20
    minSize = 6

    def __init__(self):
        self.initGUI()

    def initGUI(self):
        root = Tkinter.Tk()
        root.title("Graph-Visualizer")

        frame = Tkinter.Frame(root)
        frame.pack(side=Tkinter.RIGHT)

        size = (self.minDist ** 2 + self.minSize * 2) + self.minDist ** 2 + self.minSize
        self.canvas = Display_GV.Display_GV(self.minDist, self.minSize, root, width=size, height=size)
        self.canvas.pack(side=Tkinter.LEFT)

        toggleButton = Tkinter.Button(frame)
        toggleButton.configure(text="Toggle Edges", background="orange")
        toggleButton.pack(side=Tkinter.TOP)
        toggleButton.bind("<Button-1>", self.canvas.toggleEdges)

        root.mainloop()

if __name__ == "__main__":
    GV_Main()
