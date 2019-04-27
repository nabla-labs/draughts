from Env.Env import DraughtsEnv
from Env.gui.gui import draughtsboard
from Agent.search_lib.state_generator import StateGenerator
import copy
env = DraughtsEnv()
gui = draughtsboard()

#gui.settostate(env.reset())


env.move_indicator = 1
#env.state[2][1][1] = 0
#env.state[2][1][0] = 0
#env.state[4][1][1] = 1
#env.state[4][1][2] = 9
#env.state[1][4][1] = 0
#env.state[1][4][2] = 0
#env.state[1][0][1] = 0
#env.state[1][0][2] = 0
#env.state[2][1][1] = 1
#env.state[2][1][2] = 5
#env.state[5][2][1] = 0
#env.state[5][2][2] = 0
env.state[1][2][1] = 3
env.state[1][2][2] = 14
env.state[2][1][1] = 2
env.state[2][1][2] = 1
env.state[2][3][1] = 2
env.state[2][3][2] = 2
env.state[4][1][1] = 2
env.state[4][1][2] = 3
#env.state[4][3][1] = 1
#env.state[4][3][2] = 4
env.state[6][3][1] = 2
env.state[6][3][2] = 5
#act = env.get_possible_actions_piece(5, 0)
#act = env.get_possible_actions_piece(1, 2)
#act = env.get_possible_actions()
act = env.get_possible_actions()
gui.settostate(env.state, "white", act)
act = gui.get_user_move()
piece_id = act[0][0]
path = act[0][1]
applied_action = (piece_id, path)
#print(applied_action)
print("applied_action:{}".format((piece_id, path)))
temp_state = copy.deepcopy(env.state)
env.apply_action(applied_action)
#print(env.render())
#print(act)
#print(gui.boardposcoordinates)
print(applied_action)
states = StateGenerator.get_states_by_actions(temp_state, [applied_action])
#print(states)
gui.settostate(states[0], "black", env.get_possible_actions())
gui.get_user_move()
#[print(action) for action in act if action[1]]
while True:
    pass

