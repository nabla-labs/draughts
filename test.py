from Env.Env import DraughtsEnv
from Env.gui.gui import draughtsboard

env = DraughtsEnv()
gui = draughtsboard()

#gui.settostate(env.reset())

#env.move_indicator = 1
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
act = env.get_possible_actions_piece(1, 2)
gui.settostate(env.state)
print(act)
#[print(action) for action in act if action[1]]
while True:
    pass

