from tkinter import *

class draughtsboard:

    def __init__(self):

        self.window = Tk()
        self.boardframewidth = 400
        self.boardframeheight = 400
        self.colordark = "saddle brown"
        self.colorwhite = "burlywood3"
        self.movedisplayframeheight = self.boardframeheight/10
        self.movedisplayframe = Frame(self.window, width=self.boardframewidth, height=self.movedisplayframeheight, bd=2, background="white")
        self.movedisplayframe.pack()
        self.movedisplaycanvas = Canvas(self.movedisplayframe, width=self.boardframewidth, height=self.movedisplayframeheight)
        self.boardframe = Frame(self.window, width=self.boardframewidth, height=self.boardframeheight, bd=2, background="white") 
        self.boardframe.pack()
        self.boardcanvas = Canvas(self.boardframe, width=self.boardframewidth, height=self.boardframeheight)
        self.boardcanvas.pack()
        
        self.initboard()
        self.initmovedisplay()
        piece = draughtpiece(self.boardcanvas, "black", int(self.boardframeheight/8), 0)
    
        piece.place(self.boardposcoordinates[7][7])
        self.window.mainloop()

    def initboard(self):

        Filling = self.colorwhite
        dx = int(self.boardframewidth/8)
        dy = int(self.boardframeheight/8)
        self.boardposcoordinates = []

        for x in range(0, self.boardframewidth, dx):

            columncoordinates = []

            for y in range(0, self.boardframeheight, dy):
                
                self.boardcanvas.create_rectangle(x, y, x+dx, y+dy, fill=Filling)
                columncoordinates.append((x+int(dx/2), y+int(dy/2)))

                if y != int(self.boardframeheight*(7/8)):
                    if Filling == self.colorwhite:
                        Filling = self.colordark
                    else:
                        Filling = self.colorwhite

            self.boardposcoordinates.append(columncoordinates)

    def initmovedisplay(self):
        
        self.movedisplay = 


class draughtpiece:

    def __init__(self, canvas, color, dim, ID):

        self.canvas = canvas
        self.color = color
        self.posx = None
        self.posy = None
        self.dim = dim
        self.id = ID

    def place(self, xytuple):

        x = xytuple[0]
        y = xytuple[1]

        if self.posx == None and self.posy == None:
            
            self.piece = self.canvas.create_oval(x-int(self.dim/2), y-int(self.dim/2), x+(self.dim/2), y+(self.dim/2), fill=self.color)
            self.text = self.canvas.create_text(x, y, text=str(self.id), fill="white", font=("Times", 15))
        else:
            
            self.canvas.move(self.piece,x-self.posx, y-self.posy)
            self.canvas.move(self.text, x-self.posx, y-self.posy)

        self.posx = x
        self.posy = y

if __name__=="__main__":

    db = draughtsboard()
