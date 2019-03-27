from tkinter import *
import numpy as np
from threading import Thread

import time

class draughtsboard:

    def __init__(self, window=None):

        self.window = Tk()
        self.boardframewidth = 400
        self.boardframeheight = 400
        self.colordark = "saddle brown"
        self.colorwhite = "burlywood3"
        self.pieces = []
        self.movedisplayframeheight = self.boardframeheight/10
        self.movedisplayframe = Frame(self.window, width=self.boardframewidth, height=self.movedisplayframeheight, bd=2, background="white")
        self.movedisplayframe.pack()
        self.movedisplaycanvas = Canvas(self.movedisplayframe, width=self.boardframewidth, height=self.movedisplayframeheight)
        self.movedisplaycanvas.pack()
        self.boardframe = Frame(self.window, width=self.boardframewidth, height=self.boardframeheight, bd=2, background="white") 
        self.boardframe.pack()
        self.boardcanvas = Canvas(self.boardframe, width=self.boardframewidth, height=self.boardframeheight)
        self.boardcanvas.pack()
        #self.window.event_add('<<virttest>>')
        self.window.bind('<<virttest>>', self.testhandler)
        self.initboard()
        self.initmovedisplay()
        #self.window.mainloop()

    def testhandler(self):
        
        print("Hallo")
        

    def initboard(self):

        Filling = self.colorwhite
        dx = int(self.boardframewidth/8)
        dy = int(self.boardframeheight/8)
        self.boardposcoordinates = []

        for x in range(0, self.boardframewidth, dx):

            columncoordinates = []

            for y in range(0, self.boardframeheight, dy):
                
                rectangle = self.boardcanvas.create_rectangle(x, y, x+dx, y+dy, fill=Filling)
                self.boardcanvas.tag_bind(rectangle, '<Button-1>', self.clickonfield)
                columncoordinates.append((x+int(dx/2), y+int(dy/2)))

                if y != int(self.boardframeheight*(7/8)):
                    if Filling == self.colorwhite:
                        Filling = self.colordark
                    else:
                        Filling = self.colorwhite

            self.boardposcoordinates.append(columncoordinates)

    def initmovedisplay(self):
        
        self.movedisplay_rectangle = self.movedisplaycanvas.create_rectangle(0, 0, self.boardframewidth, self.movedisplayframeheight, fill="black")
        self.movedisplay_text = self.movedisplaycanvas.create_text(int(self.boardframewidth/2), int(self.movedisplayframeheight/2), text="It is black's move", fill="white", font=("Times", 13))

    def changecurrentmove(self, nextmove):

        if nextmove=="black":
            self.movedisplaycanvas.itemconfig(self.movedisplay_rectangle, fill="black")
            self.movedisplaycanvas.itemconfig(self.movedisplay_text, text="It is black's move", fill="white")
        else:
            self.movedisplaycanvas.itemconfig(self.movedisplay_rectangle, fill="white")
            self.movedisplaycanvas.itemconfig(self.movedisplay_text, text="It is white's move", fill="black")
        self.window.update()

    def settostate(self, state):

        for piece in self.pieces:

            self.boardcanvas.delete(piece.piece)
            self.boardcanvas.delete(piece.text)

        for y, row in enumerate(state):
            for x, field in enumerate(row):

                if field[1] != 0:
                    
                    if field[1] == 1 or field[1] == 3:
                        color = "white"
                    else:
                        color = "black"

                    piece = draughtpiece(self.boardcanvas, color, int(self.boardframeheight/8), int(field[2]))
                    piece.place(self.boardposcoordinates[x][y])
                    self.pieces.append(piece)
        self.window.update()

    def clickonfield(self, event):
        print("Click")
        print(event.x, event.y)

class draughtpiece:

    def __init__(self, canvas, color, dim, ID):

        self.canvas = canvas
        self.color = color
        if color == "black":
            self.textcolor = "white"
        else:
            self.textcolor = "black"
        self.posx = None
        self.posy = None
        self.dim = dim
        self.id = ID
        

    def place(self, xytuple):

        x = xytuple[0]
        y = xytuple[1]

        if self.posx == None and self.posy == None:
            
            self.piece = self.canvas.create_oval(x-int(self.dim/2), y-int(self.dim/2), x+(self.dim/2), y+(self.dim/2), fill=self.color)
            self.text = self.canvas.create_text(x, y, text=str(self.id), fill=self.textcolor, font=("Times", 15))

        else:
            
            self.canvas.move(self.piece,x-self.posx, y-self.posy)
            self.canvas.move(self.text, x-self.posx, y-self.posy)

        self.posx = x
        self.posy = y

def startmainloop(boardobject):

    boardobject.event_generate('<<virttest>>')

if __name__=="__main__":

    window = Tk()
    db = draughtsboard(window)
    state = np.zeros([8, 8, 3])
    state[0, 0, 1] = 2
    state[0, 0, 2] = 1
    state[7, 7, 1] = 1
    state[7, 7, 2] = 2
   # db.settostate(state)
    #mainthread = Thread(target = startmainloop, args=([window]))
    #mainthread.start()
    #window.mainloop()
    print("HI")
    db.settostate(state)
    window.mainloop()
    #while True:
    #    print("WWWW")
    #    time.sleep(1)
    #mainthread.join()

    
