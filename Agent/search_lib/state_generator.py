import copy


class StateGenerator:

    @classmethod
    def get_states_by_actions(cls, state, actions):
        generated_states = []
        print(actions)
        for action in actions:

            generated_states.append(cls._apply_action(
                copy.deepcopy(state), action))
        return generated_states

    @classmethod
    def _move_piece_to_pos(cls, state, piece_id, pos):
        for row_id, row in enumerate(state):
            for col_id, field in enumerate(row):
                if int(field[2]) == piece_id:
                    state[pos[0]][pos[1]] = field
                    state[row_id][col_id] = [field[0], 0, 0]
                    break
            else:
                continue
            break

    @classmethod
    def _delete_piece_at_pos(cls, state, pos):
        row, col = pos
        state[row][col] = [state[row][col][0], 0, 0]

    @classmethod
    def _check_for_kings(cls, state):
        for row in state:
            for row_ind, piece in enumerate(row):
                if piece[1] == 1 and row_ind == 0:
                    piece[1] = 3
                if piece[1] == 2 and row_ind == 7:
                    piece[1] = 4

    @classmethod
    def _apply_action(cls, state, action):
        print("HALLO")
        print(action)
        current_piece_pos = cls._get_piece_pos_by_id(state, action[0])
        cls._move_piece_to_pos(state, action[0], action[1][-1])
        positions_to_visit = [current_piece_pos] + action[1]
        print(positions_to_visit)
        pieces_to_delete = cls._get_positions_between(positions_to_visit)

        for piece_pos in pieces_to_delete:
            cls._delete_piece_at_pos(state, piece_pos)

        cls._check_for_kings(state)

        return state

    @classmethod
    def _get_piece_pos_by_id(cls, state, piece_id):
        for row_id, row in enumerate(state):
            for col_id, field in enumerate(row):
                if int(field[2]) == piece_id:
                    return (row_id, col_id)

    @classmethod
    def _get_positions_between(cls, positions):
        pos_between = []
        for i in range(len(positions)-1):
            vec_row = positions[i+1][0] - positions[i][0]
            vec_col = positions[i+1][1] - positions[i][1]
            pos_between.append((positions[i][0]+int(vec_row*0.5),
                                positions[i][1]+int(vec_col*0.5)))
        return pos_between
