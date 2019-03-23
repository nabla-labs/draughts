#!/usr/bin/env python3
import gym
import numpy as np


class DraughtsEnv(gym.Env):
    """ """

    move_count = 0

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
                        string += '■ '
                    else:
                        string += '□ '
                if self.state[row][col][1] == 1.0:
                    string += '● '
                if self.state[row][col][1] == 2.0:
                    string += '○ '
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
                    possible_pos, jumped = self.check_first_possible_position(
                        row, col, self.state[row][col][1])
                    action_arr, piece_id = self.find_actions(
                        row, col, possible_pos, self.state[row][col][1])
                    all_actions[piece_id] = action_arr

    def check_first_possible_position(self, row, col, piece_type):
        jumped = True
        # theoretical jump positions
        possible_pos = self.get_diagonal_fields(row, col, piece_type, 2)

        # checks if we can jump to the field in possible_pos, if not removes it
        for pos in possible_pos:
            if not self.is_jump(pos, (row, col)):
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
        if piece_type is 1 or 2:
            i = self.move_indicator
            possible_pos = [(row+rad*i, col+rad), (row+rad*i, col-rad)]
        elif piece_type is 3 or 4:
            possible_pos = [(row + rad, col+rad), (row+rad, col-rad),
                            (row-rad, col + rad), (row-rad, col-rad)]
        return possible_pos

    def find_actions(self, row, col, current_path, piece_type):
        if not self.is_empty((row+1, col+1)) and self.is_empty((row+2, col+2)):
            current_path.append((row+2, col+2))
            self.find_actions(row+2, col+2, current_path, piece_type)
            current_path.pop()
        if not self.is_empty((row+1, col-1)) and self.is_empty((row+2, col-2)):
            current_path.append((row+2, col-2))
            self.find_actions(row+2, col-2, current_path, piece_type)
            current_path.pop()
        if piece_type == 3 or piece_type == 4:
            if not self.is_empty((row-1, col+1)) and self.is_empty((row-2, col+2)):
                current_path.append((row-2, col+2))
                self.find_actions(row-2, col+2, current_path, piece_type)
                current_path.pop()
            if not self.is_empty((row-1, col-1)) and self.is_empty((row-2, col-2)):
                current_path.append((row-2, col-2))
                self.find_actions(row-2, col-2, current_path, piece_type)
                current_path.pop()
        return current_path

        pass

    def is_empty(self, pos):
        return self.state[pos[0]][pos[1]][1] is not 0

    def is_jump(self, pos):
        pass

    def is_valid_draw(self, p_type):
        if self.move_indicator is -1 and p_type is 2 or 4:
            return True
        elif self.move_indicator is 1 and p_type is 1 or 3:
            return True
        elif p_type is 0:
            return False
