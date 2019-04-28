import numpy as np


class StateStorage:

    def __init__(self, size):

        self.state_storage = None
        self.reward_storage = None
        self.size = size


    def add_states(self, state_list, reward):

        states = np.array(state_list, dtype=np.float32)
        rewards = np.full((states.shape[0]), reward)
        if not self.state_storage:
            self.state_storage = states
            self.reward_storage = rewards

        else:
            self.state_storage = np.concatenate((states, self.state_storage), axis=0)
            self.reward_storage = np.concatenate((rewards, self.reward_storage), axis=0)
            size_diff = self.size - self.state_storage.shape[0]

            if size_diff < 0:
                self.state_storage = self.state_storage[:self.size]
                self.reward_storage = self.reward_storage[:self.size]
        
        assert self.state_storage.shape[0] == self.reward_storage.shape[0]


    def sample(self, sample_size):

        sampled_states = []
        sampled_rewards = []
        for i in range(sample_size):
            rand_indx = np.random.random_integers(self.size)
            sampled_states.append(self.state_storage[rand_indx])
            sampled_rewards.append(self.reward_storage[rand_indx])

        return np.array(sampled_states, dtype=np.float32), np.array(sampled_rewards, dtype=np.float32)
