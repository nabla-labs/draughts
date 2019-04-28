#!/usr/bin/env python3
import gym
import numpy as np
import copy


class DraughtsEnv(gym.Env):
    """ """

    move_count = 0
    white = (1, 3)
    black = (2, 4)

    def __init__(self):
        self.state = np.zeros((8, 8, 3))
        #black = -1
        self.move_indicator = -1
        self.deleted_pieces = []
        self.game_state = None
        self.is_done = False
        pass

    def reset(self):
        """
        reset the draughts board to its starting position, where an empty field
        is represented as [0, 0, 0]

        the field type is a 1x3 vector with [field_color, field_type, piece_id]
            field_color: 0=white, 1=black
            piece_type:  0=empty, 1=white piece, 2=black piece, 3=white king, 4=black king
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

        self.possible_actions = self.get_possible_actions()
        self.game_state = "go"
        self.is_done = False
        return self.state

    def step(self, action):
        reward = (0, 0)
        if self.game_state[0:2] == "go" and action:
            self.apply_action(action)
            self.check_done()
        elif not action:
            if self.move_indicator == -1:
                if self.game_state == "go-wd":
                    self.game_state = "draw"
                else:
                    self.game_state = "go-bd"
            else:
                if self.game_state == "go-bd":
                    self.game_state = "draw"
                else:
                    self.game_state = "go-wd"

        if self.game_state == "draw":
            reward = (0.5, 0.5)
            self.is_done = True
        elif self.game_state == "bw":
            reward = (1, -1)
            self.is_done = True
        elif self.game_state == "ww":
            reward = (-1, 1)
            self.is_done = True
        return self.state, reward, self.is_done

    def verify_action(self, action):
        for act in self.possible_actions:

            if act[0] == action[0]:
                
                assert action[1] in act[1]

    def move_piece_to_pos(self, piece_id, pos):
        for row_id, row in enumerate(self.state):
            for field_id, field in enumerate(row):
                if int(field[2]) == piece_id:
                    self.state[pos[0]][pos[1]] = field
                    self.state[row_id][field_id] = [field[0], 0, 0]
                    break
            else:
                continue
            break

    def delete_piece_at_pos(self, pos):
        row, col = pos
        self.deleted_pieces.append(
            (self.state[row][col][1], self.state[row][col][2]))
        self.state[row][col] = [self.state[row][col][0], 0, 0]

    def check_for_kings(self):
        for row in self.state:
            for row_ind, piece in enumerate(row):
                if piece[1] == 1 and row_ind == 0:
                    piece[1] = 3
                if piece[1] == 2 and row_ind == 7:
                    piece[1] = 4

    def apply_action(self, action):
        current_piece_pos = self.get_piece_pos_by_id(action[0])
        self.verify_action(action)
        self.move_piece_to_pos(action[0], action[1][-1])
        positions_to_visit = [current_piece_pos] + action[1]
        pieces_to_delete = self.get_positions_between(positions_to_visit)

        for piece_pos in pieces_to_delete:

            self.delete_piece_at_pos(piece_pos)

        self.check_for_kings()
        self.move_indicator = self.move_indicator*(-1)
        self.possible_actions = self.get_possible_actions()

    def get_positions_between(self, positions):

        pos_between = []
        for i in range(len(positions)-1):
            vec_row = positions[i+1][0]-positions[i][0]
            print(vec_row)
            vec_col = positions[i+1][1]-positions[i][1]
            print(vec_col)
            pos_between.append((positions[i][0]+int(vec_row*0.5), positions[i][1]+int(vec_col*0.5)))
        
        return pos_between

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

    def check_done(self):
        if not self.possible_actions:
            if self.move_indicator == -1:
                self.game_state = "ww"
            else:
                self.game_state = "bw"

    def get_possible_actions(self):
        all_actions = []
        for row in range(self.state.shape[0]):
            for col in range(self.state.shape[1]):
                # if field is not empty and piece is dran
                if self.is_valid_draw(self.state[row][col][1]):

                    piece_id, piece_actions = self.get_possible_actions_piece(
                        row, col)
                    all_actions.append((piece_id, piece_actions))
        self.possible_actions = all_actions
        return all_actions

    def get_possible_actions_piece(self, row, col):
        action_paths = []
        possible_pos, jumped = self.check_first_possible_position(
            row, col, self.state[row][col][1])

        if jumped:
            [self.find_actions(pos[0], pos[1], [(
                row, col), pos], self.state[row][col][1], action_paths) for pos in possible_pos]
        else:
            action_paths = [[pos] for pos in possible_pos]
        return int(self.state[row][col][2]), action_paths

    def check_first_possible_position(self, row, col, piece_type):
        jumped = True
        # theoretical jump positions
        possible_pos = self.get_diagonal_fields(row, col, piece_type, 2)
        # checks if we can jump to the field in possible_pos, if not removes it
        possible_pos = [pos for pos in possible_pos if self.is_jump(
            pos, (row, col), piece_type)]

        # if no jump is possible, check the basic moves are possible
        if not possible_pos:
            possible_pos = self.get_diagonal_fields(row, col, piece_type, 1)
            jumped = False
            possible_pos = [pos for pos in possible_pos if self.is_empty(pos)]

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

    def find_actions(self, row, col, current_path, piece_type, action_paths):
        # get the possible fields for jumps from position row/col
        possible_pos = self.get_diagonal_fields(row, col, piece_type, 2)

        # remove the position we came from if it is in the list of possible positions
        try:
            possible_pos.remove(current_path[-2])
        except:
            pass
        terminal_state = True
        for pos in possible_pos:

            if self.is_jump(pos, (row, col), piece_type):
                terminal_state = False
                current_path.append(pos)
                self.find_actions(
                    pos[0], pos[1], current_path, piece_type, action_paths)
                current_path.pop()
        if terminal_state:
            action_paths.append(copy.deepcopy(current_path)[1:])

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
        else:
            return None

    def is_enemy_piece(self, row, col, piece_type):
        return not(self.get_color(self.state[row][col][1]) == self.get_color(piece_type)) and not self.is_empty((row, col))

    def is_valid_draw(self, p_type):
        if self.move_indicator == -1 and (p_type == 2 or p_type == 4):
            return True
        elif self.move_indicator == 1 and (p_type == 1 or p_type == 3):
            return True
        elif p_type is 0:
            return False

    def get_move_indicator(self):
        return self.move_indicator

    def get_piece_pos_by_id(self, piece_id):

        for row_id, row in enumerate(self.state):
            for col_id, field in enumerate(row):

                if int(field[2]) == piece_id:

                    return (row_id, col_id)
