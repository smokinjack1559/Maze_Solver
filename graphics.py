from tkinter import Tk, BOTH, Canvas


class Window:

    def __init__(self, width, height ):
        self._root = Tk()
        self._root.title("Maze Solver")
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self._root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
 #       self._root.mainloop()
        

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        self.close

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color = "black"):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def  draw(self, canvas, fill_color="black"):
        canvas.create_line(self.point1.x, 
                           self.point1.y, 
                           self.point2.x, 
                           self.point2.y, 
                           fill=fill_color, 
                           width=2
        )
        canvas.pack(fill=BOTH, expand=1)   




#w = Window(300,300)
#w.redraw()
#w.wait_for_close()
#w.close()



