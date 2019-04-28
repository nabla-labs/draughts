#import Agent
from Env.Env import DraughtsEnv
import numpy as np
from Agent.search_lib.state_storage import StateStorage

sample_size = 300
episodes = 20
epochs = 200
storage_size = 3000

if __name__ == "__main__":

    env = DraughtsEnv()
    state_storage = StateStorage(storage_size)
    
    for epoch_num in range(epochs):
        env.reset()
        
        # run several episodes 
        for episode_num in range(episodes):
            is_done = False
            reward = 0
            temp_state_storage_black = []
            temp_state_storage_white = []
            reward_storage_black = 0
            reward_storage_white = 0

            while is_done == False:
                possible_actions = env.get_possible_actions()
                #action = Agent(state, possible_actions)
                state, reward, is_done = env.step(action)
                
                # black made a move, now it is white's turn
                if env.get_move_indicator() == 1:
                    temp_state_storage_black.append(state[:, :, :2])

                # white made a move, now it is black's turn
                elif env.get_move_indicator() == -1:
                    temp_state_storage_white.append(state[:, :, :2])

                if is_done:
                    reward_storage_black, reward_storage_white = reward
                    state_storage.add_states(temp_state_storage_black, reward_storage_black)
                    state_storage.add-states(temp_state_storage_white, reward_storage_white)

        sampled_states, sampled_rewards = state_storage.sample(sample_size)
        #train the agent


