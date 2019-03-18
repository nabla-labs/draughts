#!/usr/bin/env python3
import gym
import numpy as np


class DraughtsEnv(gym.Env):
    """ """

    move_count = 0

    def __init__(self):
        self.state = np.zeros((8, 8, 3))
        self.move_indicator = 1
        pass

    def reset(self):
        """
        reset the draughts board to its starting position, where an empty field
        is represented as [0, 0, 0]

        the field type is a 1x3 vector with [field_color, field_type, piece_id]
            field_color: 0=white, 1=black
            field_type: 0=empty, 1=white piece, 2=black piece, 3=white king, 4=black king
            piece_id: 0=empty, 1-12=white, 13-24=black
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

        return self.state

    def step(self):
        pass

    def render(self):
        pass

    def is_done(self):
        pass

    def get_possible_actions(self):
        all_actions = np.zeros([12])
        for row in range(self.state.shape[0]):
            for col in range(self.state.shape[1]):
                if (self.state[row][col][1] is not 0) and self.state[row][col][2] == self.move_indicator:
                    action_arr, id = find_actions(
                        row, col, self.state[row][col][1], self. move_indicator, True)
                    all_actions[id] = action_arr

    def find_actions(self, row, col, piece_type, move_indicator, recursive=False):
        nodes_to_visit = [(row, col)]
        pass
