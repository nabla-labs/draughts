from Env.Env import DraughtsEnv
from Env.gui.gui import draughtsboard

env = DraughtsEnv()
Gui = draughtsboard()
env.reset()
Gui.settostate(env.reset())
env.render()
actions = env.get_possible_actions()

while True:
    pass
