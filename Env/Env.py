#!/usr/bin/env python3
import gym
import numpy as np


class DraughtsEnv(gym.Env):
    """ """

    move_count = 0
    white = (1, 3)
    black = (2, 4)

    def __init__(self):
        self.state = np.zeros((8, 8, 3))
        #black = -1
        self.move_indicator = -1
        self.is_done = False
        pass

    def reset(self):
        """
        reset the draughts board to its starting position, where an empty field
        is represented as [0, 0, 0]

        the field type is a 1x3 vector with [field_color, field_type, piece_id]
            field_color: 0=white, 1=black
            field_type:  0=empty, 1=white piece, 2=black piece, 3=white king, 4=black king
            piece_id:    0=empty, 1-12=white, 13-24=black
        """
        piece_id = 1
        for row in range(self.state.shape[0]):
            for col in range(self.state.shape[1]):
                if row < 3:
                    if row % 2:
                        if col % 2:
                            self.state[row][col] = [0, 0, 0]
                        else:
                            self.state[row][col] = [1, 1, piece_id]
                            piece_id += 1
                    else:
                        if col % 2:
                            self.state[row][col] = [1, 1, piece_id]
                            piece_id += 1
                        else:
                            self.state[row][col] = [0, 0, 0]
                elif row > 4:
                    if row % 2:
                        if col % 2:
                            self.state[row][col] = [0, 0, 0]
                        else:
                            self.state[row][col] = [1, 2, piece_id]
                            piece_id += 1
                    else:
                        if col % 2:
                            self.state[row][col] = [1, 2, piece_id]
                            piece_id += 1
                        else:
                            self.state[row][col] = [0, 0, 0]
                else:
                    if row % 2:
                        if col % 2:
                            self.state[row][col] = [0, 0, 0]
                        else:
                            self.state[row][col] = [1, 0, 0]
                    else:
                        if col % 2:
                            self.state[row][col] = [1, 0, 0]
                        else:
                            self.state[row][col] = [0, 0, 0]

        return self.state

    def step(self):
        pass

    def render(self):
        string = ''
        for row in range(8):
            string += '\n{}: '.format(row)
            for col in range(8):
                if self.state[row][col][1] == 0.0:
                    if self.state[row][col][0] == 0.0:
                        string += '□ '
                    else:
                        string += '■ '
                if self.state[row][col][1] == 1.0:
                    string += '○ '
                if self.state[row][col][1] == 2.0:
                    string += '● '
                if self.state[row][col][1] == 3.0:
                    string += '♔ '
                if self.state[row][col][1] == 4.0:
                    string += '♚ '
        string += '\n   A B C D E F G H'
        print(string)

    def is_done(self):
        return self.is_done

    def get_possible_actions(self):
        all_actions = np.zeros([12])
        for row in range(self.state.shape[0]):
            for col in range(self.state.shape[1]):
                # if field is not empty and piece is dran
                if self.is_valid_draw(self.state[row][col][1]):
                    piece_action_paths = []
                    possible_pos, jumped = self.check_first_possible_position(
                        row, col, self.state[row][col][1])
                    action_arr, piece_id = self.find_actions(
                        row, col, possible_pos, self.state[row][col][1], piece_action_paths)
                    all_actions[piece_id] = np.array(piece_action_paths)
        return all_actions

    def check_first_possible_position(self, row, col, piece_type):
        jumped = True
        # theoretical jump positions
        possible_pos = self.get_diagonal_fields(row, col, piece_type, 2)

        # checks if we can jump to the field in possible_pos, if not removes it
        for pos in possible_pos:
            if not self.is_jump(pos, (row, col), piece_type):
                possible_pos.remove(pos)

        # if no jump is possible, check the basic moves are possible
        if not possible_pos:
            possible_pos = self.get_diagonal_fields(row, col, piece_type, 1)
            jumped = False
            for pos in possible_pos:
                if not self.is_empty(pos):
                    possible_pos.remove(pos)
        return possible_pos, jumped

    def get_diagonal_fields(self, row, col, piece_type, rad):
        if piece_type == 1 or piece_type == 2:
            i = self.move_indicator
            possible_pos = [(row+rad*i, col+rad), (row+rad*i, col-rad)]
        elif piece_type == 3 or piece_type == 4:
            possible_pos = [(row + rad, col+rad), (row+rad, col-rad),
                            (row-rad, col + rad), (row-rad, col-rad)]
        possible_pos = [pos for pos in possible_pos if self.is_in_board(pos)]
        return possible_pos

    def is_in_board(self, pos):
        return (pos[0] >= 0 and pos[0] <= 7) and (pos[1] >= 0 and pos[1] <= 7)

    def find_actions(self, row, col, current_path, piece_type, piece_action_paths):
        #piece_type check for +-1 seems to be missing. And some kind of logic to change the move-direction of non-king pieces needs to be added.
        if self.is_enemy_piece((row+1*self.move_indicator, col+1)) and self.is_empty((row+2*self.move_indicator, col+2)) and not (row+2*self.move_indicator, col+2) in current_path:
            current_path.append((row+2*self.move_indicator, col+2))
            self.find_actions(row+2*self.move_indicator, col+2, current_path, piece_type)
            current_path.pop()
        if self.is_enemy_piece((row+1*self.move_indicator, col-1)) and self.is_empty((row+2*self.move_indicator, col-2)) and not (row+2*self.move_indicator, col-2) in current_path:
            current_path.append((row+2*self.move_indicator, col-2))
            self.find_actions(row+2*self.move_indicator, col-2, current_path, piece_type)
            current_path.pop()
        if piece_type == 3 or piece_type == 4:
            if  self.is_enemy_piece((row-1*self.move_indicator, col+1)) and self.is_empty((row-2*self.move_indicator, col+2)) and not (row-2*self.move_indicator, col+2) in current_path:
                current_path.append((row-2*self.move_indicator, col+2))
                self.find_actions(row-2*self.move_indicator, col+2, current_path, piece_type)
                current_path.pop()
            if  self.is_enemy_piece((row-1*self.move_indicator, col-1)) and self.is_empty((row-2*self.move_indicator, col-2)) and not row(-2*self.move_indicator, col-2) in current_path:
                current_path.append((row-2*self.move_indicator, col-2))
                self.find_actions(row-2*self.move_indicator, col-2, current_path, piece_type)
                current_path.pop()
        #Shouldnt it be sth like global possible actions.append(current_path)
        piece_action_paths.append(current_path)

        pass

    def is_empty(self, pos):
        return self.state[pos[0]][pos[1]][1] == 0

    def is_jump(self, pos, rowcol, piece_type):

        row, col = rowcol
        x = pos[1]-col
        y = pos[0]-row

        pos_between = (int(row+y/2), int(col+x/2))
        
        return self.is_enemy_piece(pos_between[0], pos_between[1], piece_type) and self.is_empty(pos)
    
    def get_color(self, piece_type):
        if piece_type in self.black:
            return self.black
        elif piece_type in self.white:
            return self.white

    def is_enemy_piece(self, row, col, piece_type):
        return not(self.get_color(self.state[row][col][1]) == self.get_color(piece_type))

    def is_valid_draw(self, p_type):
        if self.move_indicator == -1 and (p_type ==  2 or p_type == 4):
            return True
        elif self.move_indicator == 1 and (p_type == 1 or p_type == 3):
            return True
        elif p_type is 0:
            return False
