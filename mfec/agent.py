#!/usr/bin/env python2

import time
import numpy as np


# TODO use some common agent-interface
class MFECAgent(object):

    def __init__(self, qec, discount, actions, epsilon):
        self.actions = actions
        self.qec = qec
        self.memory = []

        self.current_state = None
        self.current_action = None
        self.current_time = None

        self.discount = discount
        self.epsilon = epsilon

    def act(self, observation):
        """Choose an action for the given observation."""
        self.current_state = self.qec.project(observation)
        self.current_time = time.clock()

        # Exploitation
        if np.random.rand() > self.epsilon:
            self.current_action = self._exploit()

        # Exploration
        else:
            self.current_action = np.random.choice(self.actions)
        return self.current_action

    def _exploit(self):
        """Determine the action with the highest Q-value. If multiple
        actions with the the highest value exist then choose from this set
        of actions randomly."""
        action_values = [
            self.qec.estimate(self.current_state, action, self.current_time)
            for action in self.actions]
        best_value = np.max(action_values)
        best_actions = np.argwhere(action_values == best_value).flatten()
        return np.random.choice(best_actions)  # TODO paper?

    def receive_reward(self, reward):
        """Store (state, action, reward) tuple in memory."""
        self.memory.append(
            {'state': self.current_state, 'action': self.current_action,
             'reward': reward, 'time_step': self.current_time})

    # TODO batch-update
    def train(self):
        """Update Q-Values via backward-replay."""
        value = .0
        for _ in range(len(self.memory)):
            experience = self.memory.pop()
            value = value * self.discount + experience['reward']
            self.qec.update(experience['state'], experience['action'], value,
                            experience['time_step'])
