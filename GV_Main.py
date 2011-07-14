'''
Eric H. Lee
erhlee.bird@gmail.com

GV_Main.py
'''
import Tkinter
from util import Display_GV

class GV_Main:
    """Main class for the Graph-Visualizer Project"""

    def __init__(self):
        self.initGUI()

    def initGUI(self):
        root = Tkinter.Tk()
        root.title("Graph-Visualizer")

        frame = Tkinter.Frame(root)
        frame.pack(side=Tkinter.RIGHT)

        canvas = Display_GV.Display_GV(root)
        canvas.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)

        toggleButton = Tkinter.Button(frame)
        toggleButton.configure(text="Toggle Edges", background="orange")
        toggleButton.pack(side=Tkinter.TOP)
        toggleButton.bind("<Button-1>", canvas.toggleEdges)

        recenterButton = Tkinter.Button(frame)
        recenterButton.configure(text="Recenter Canvas", background="red")
        recenterButton.pack(side=Tkinter.BOTTOM)
        recenterButton.bind("<Button-1>", canvas.centerScreen)

        root.mainloop()

if __name__ == "__main__":
    GV_Main()
