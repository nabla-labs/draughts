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
        self.submit_button = Button(self.boardframe, text="Submit action", command=self.submit_action_callback)
        self.submit_button.pack()
        self.initboard()
        self.initmovedisplay()
        self.disable_submit_button()
        self.marked_piece = None    
        self.piece_marker = None
        self.action_markers = None
        self.endpos_markers = None
        self.endpositions = None
        self.highlighted_endpos = None
        self.submitted_action_path = None

    def get_user_move(self):

        self.window.mainloop()
        return self.submitted_action_path

    def initboard(self):

        Filling = self.colorwhite
        dx = int(self.boardframewidth/8)
        dy = int(self.boardframeheight/8)
        #coordiantes are in (col, row) / (x, y)
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
        self.current_move = "black"
        self.movedisplay_rectangle = self.movedisplaycanvas.create_rectangle(0, 0, self.boardframewidth, self.movedisplayframeheight, fill="black")
        self.movedisplay_text = self.movedisplaycanvas.create_text(int(self.boardframewidth/2), int(self.movedisplayframeheight/2), text="It is black's move", fill="white", font=("Times", 13))

    def changecurrentmove(self, nextmove):

        self.current_move = nextmove
        if nextmove == "black":
            self.movedisplaycanvas.itemconfig(self.movedisplay_rectangle, fill="black")
            self.movedisplaycanvas.itemconfig(self.movedisplay_text, text="It is black's move", fill="white")
        elif nextmove == "white":
            self.movedisplaycanvas.itemconfig(self.movedisplay_rectangle, fill="white")
            self.movedisplaycanvas.itemconfig(self.movedisplay_text, text="It is white's move", fill="black")
        self.window.update()

    def settostate(self, state, current_move, actions):

        self.changecurrentmove(current_move)
        self.actions = actions

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

                    piece = draughtpiece(self.boardcanvas, color, int(self.boardframeheight/8), int(field[2]), self.click_on_piece)
                    piece.place(self.boardposcoordinates[x][y])
                    self.pieces.append(piece)
        self.window.update()

    def convert_coord_to_colrow(self, x, y):

        col0 = self.boardposcoordinates[0]
        coordinate_scale = []
        for tup in col0:
            coordinate_scale.append(tup[1])

        yboard = min(coordinate_scale, key=lambda rowel:abs(rowel-y))
        xboard = min(coordinate_scale, key=lambda colel:abs(colel-x))
        row = coordinate_scale.index(yboard)
        col = coordinate_scale.index(xboard)
        
        return col, row

    def enable_submit_button(self):
        self.submit_button.configure(state=NORMAL)

    def disable_submit_button(self):
        self.submit_button.configure(state=DISABLED)

    def clickonfield(self, event):
        print("Click")
        print(event.x, event.y)
        clicked_field = self.convert_coord_to_colrow(event.x, event.y)
        print(clicked_field)

        if self.endpositions is not None and (clicked_field[1], clicked_field[0]) in self.endpositions:

            endpos_index = self.endpositions.index((clicked_field[1], clicked_field[0]))
            self.enable_submit_button()
            if self.highlighted_endpos != endpos_index:

                if self.highlighted_endpos != None:
                    self.unhighlight_endpos(self.highlighted_endpos)
                self.highlight_endpos(endpos_index)
                self.highlighted_endpos = endpos_index

        else:
            self.disable_submit_button()
            self.unmark_piece()
            self.unmark_actions_of_piece()

    def highlight_endpos(self, endpos_index):
        
        self.boardcanvas.itemconfig(self.endpos_markers[endpos_index], width=4, )

    def unhighlight_endpos(self, endpos_index):

        self.boardcanvas.itemconfig(self.endpos_markers[endpos_index], width=2)

    def click_on_piece(self, event):

        print("Click on piece")
        print(event.x, event.y)
        piece_coord = self.convert_coord_to_colrow(event.x, event.y)
        piece = self.get_piece_by_colrow(piece_coord[0], piece_coord[1])

        if piece != None and self.is_piece_valid_move(piece):
            self.mark_piece(piece)
            self.mark_actions_of_piece(piece)
        else:
            self.unmark_piece()
            self.unmark_actions_of_piece()
    
    def submit_action_callback(self):
        submitted_endpos = self.endpositions[self.highlighted_endpos]
        piece_actions = self.get_actions_by_id(self.marked_piece.id)
        path = self.get_path_by_endpos(piece_actions, submitted_endpos)
        self.submitted_action_path = [(self.marked_piece.id, path)]
        self.window.quit()

    def get_path_by_endpos(self, action_paths, endpos):

        for path in action_paths:

            if path[-1] == endpos:

                return path

    def mark_piece(self, piece):
        
        if self.marked_piece == None or self.marked_piece != piece:
            self.marked_piece = piece
            self.boardcanvas.delete(self.piece_marker)
            edge_offset = int(piece.dim/2)-1
            x = piece.posx
            y = piece.posy
            self.piece_marker = self.boardcanvas.create_rectangle(x-edge_offset, y-edge_offset, x+edge_offset, y+edge_offset, outline="grey", dash=(3, 3), width = 2)

    def unmark_piece(self):
        
        self.marked_piece = None
        self.boardcanvas.delete(self.piece_marker)
        self.piece_marker = None


    def get_actions_by_id(self, piece_id):

        for act in self.actions:

            if act[0] == piece_id:
                return act[1]

    def mark_actions_of_piece(self, piece):
        
        self.unmark_actions_of_piece()
        action_paths = self.get_actions_by_id(piece.id)
        self.action_markers = []
        self.endpos_markers = []
        self.endpositions = []
        edge_offset = int(piece.dim/2)-1
        for path in action_paths:
            
            endpos = path[-1]
            for pos in path:
                x, y = self.boardposcoordinates[pos[1]][pos[0]]
                self.action_markers.append(self.boardcanvas.create_rectangle(x-edge_offset, y-edge_offset, x+edge_offset, y+edge_offset, outline="green", width=2))
            
            #create endpos marker
            self.endpositions.append((endpos[0], endpos[1]))
            x, y = self.boardposcoordinates[endpos[1]][endpos[0]]
            self.endpos_markers.append(self.boardcanvas.create_rectangle(x-edge_offset, y-edge_offset, x+edge_offset, y+edge_offset, outline="red", width=2))

    def unmark_actions_of_piece(self):
       
        if self.action_markers != None:
            for marker in self.action_markers:
                
                self.boardcanvas.delete(marker)
        
        if self.endpos_markers != None:
            for marker in self.endpos_markers:

                self.boardcanvas.delete(marker)

        self.endpos_markers = None
        self.action_markers = None
        self.end_positions = None
        self.highlighted_endpos = None

        
    def get_piece_by_colrow(self, col, row):

        for piece in self.pieces:
            piece_colrow = self.convert_coord_to_colrow(piece.posx, piece.posy)
            if piece_colrow == (col, row):
                
                return piece
        
        return None

    def is_piece_valid_move(self, piece):

        if piece.color == self.current_move:

            return True
        else:

            return False

class draughtpiece:

    def __init__(self, canvas, color, dim, ID, click_handler):

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
        self.click_handler = click_handler
        

    def place(self, xytuple):

        x = xytuple[0]
        y = xytuple[1]

        if self.posx == None and self.posy == None:
            
            self.piece = self.canvas.create_oval(x-int(self.dim/2), y-int(self.dim/2), x+(self.dim/2), y+(self.dim/2), fill=self.color)
            self.text = self.canvas.create_text(x, y, text=str(self.id), fill=self.textcolor, font=("Times", 15))
            self.canvas.tag_bind(self.piece, '<Button-1>', self.click_handler)
            self.canvas.tag_bind(self.text, '<Button-1>', self.click_handler)

        else:
            
            self.canvas.move(self.piece,x-self.posx, y-self.posy)
            self.canvas.move(self.text, x-self.posx, y-self.posy)

        self.posx = x
        self.posy = y


if __name__=="__main__":

    db = draughtsboard()
    #print(db.get_nearest_field(1, 1))
    #print(db.boardposcoordinates[0][0])
    #print(db.boardposcoordinates[1][0])
    state = np.zeros([8, 8, 3])
    state[0, 0, 1] = 2
    state[0, 0, 2] = 1
    state[7, 7, 1] = 1
    state[7, 7, 2] = 2
    state[0, 2, 1] = 2
    state[0, 2, 2] = 3
   # db.settostate(state)
    #mainthread = Thread(target = startmainloop, args=([window]))
    #mainthread.start()
    #window.mainloop()
    print("HI")
    db.settostate(state, "white", None)
    db.window.mainloop()
    #while True:
    #    print("WWWW")
    #    time.sleep(1)
    #mainthread.join()

    
