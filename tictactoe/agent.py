from abc import ABC, abstractmethod
import os
import pickle
import collections
import numpy as np
import random
import logging

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

log = logging.getLogger(__name__)


class Learner(ABC):
    """
    Parent class for Q-learning and SARSA agents.

    Parameters
    ----------
    alpha : float 
        learning rate
    gamma : float
        temporal discounting rate
    eps : float 
        probability of random action vs. greedy action
    eps_decay : float
        epsilon decay rate. Larger value = more decay
    """

    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        # Agent parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay
        # Possible actions correspond to the set of all x,y coordinate pairs
        self.actions = []
        for i in range(5):
            for j in range(5):
                self.actions.append((i, j))
        # Initialize Q values to 0 for all state-action pairs.
        # Access value for action a, state s via Q[a][s]
        self.Q = {}
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)
        # Keep a list of reward received at each episode
        self.rewards = []

    def get_size(self):
        print("Q Dict object: ")
        for action in self.actions:
            print("action with length:" + str(action) + ":" + str(len(self.Q[action])))

    def get_action(self, s):
        """
        Select an action given the current game state.

        Parameters
        ----------
        s : string
            state
        """
        # Only consider the allowed actions (empty board spaces)
        # possible_actions = [a for a in self.actions if s[a[0] * 3 + a[1]] == '-']
        possible_actions = [a for a in self.actions if s[a[0] * 5 + a[1]] == '-']

        if random.random() < self.eps:
            # Random choose.
            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
        else:
            # Greedy choose.
            values = np.array([self.Q[a][s] for a in possible_actions])
            # Find location of max
            ix_max = np.where(values == np.max(values))[0]
            if len(ix_max) > 1:
                # If multiple actions were max, then sample from them
                ix_select = np.random.choice(ix_max, 1)[0]
            else:
                # If unique max action, select that one
                ix_select = ix_max[0]
            action = possible_actions[ix_select]

        # update epsilon; geometric decay
        self.eps *= (1. - self.eps_decay)

        return action

    @abstractmethod
    def update(self, s, s_, a, a_, r):
        pass

    def save(self, path):
        """ Pickle the agent object instance to save the agent's state. """
        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def load(self, path):
        pass


class Qlearner(Learner):
    """
    A class to implement the Q-learning agent.
    """

    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def get_size(self):
        print("Q Dict object: ")
        for action in self.actions:
            print("action with length:" + str(action) + ":" + str(len(self.Q[action])))

    def update(self, s, s_, a, a_, r):
        """
        Perform the Q-Learning update of Q values.

        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action. NOT used by Q-learner!
        r : int
            reward received after executing action "a" in state "s"
        """
        # Update Q(s,a)
        if s_ is not None:
            # hold list of Q values for all a_,s_ pairs. We will access the max later
            possible_actions = [action for action in self.actions if s_[action[0] * 5 + action[1]] == '-']

            Q_options = [self.Q[action][s_] for action in possible_actions]
            # if max(Q_options) > 0:
                # print("possible actions")
                # print(possible_actions)
                # print("max Q_options")
                # print(max(Q_options))
            # update
            self.Q[a][s] += self.alpha * (r + self.gamma * max(Q_options) - self.Q[a][s])
            # self.Q[a][s] += self.alpha * (r + self.gamma * max(Q_options))
        else:
            # terminal state update
            self.Q[a][s] += self.alpha * (r - self.Q[a][s])
            # self.Q[a][s] += self.alpha * r
            # print(self.Q[a][s])
            # add r to rewards list
            self.rewards.append(r)


class DQN(Learner):
    """
    A class to implement the Deep Q-Learning Network agent.
    """
    REPLAY_MEMORY_SIZE = 50000  # How many last steps to keep for model training
    MINIBATCH_SIZE = 20  # How many steps (samples) to use for training
    UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)
    ACTION_SPACE = 81
    MIN_EPSILON = 0.001

    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

        # Main model
        self.model = self.create_model()

        # An array with last n steps for training
        self.replay_memory = collections.deque(maxlen=self.REPLAY_MEMORY_SIZE)

    def get_size(self):
        print("Size of DQN model %i" % self.model.size())

    def create_model(self):
        """
        Creates the Neural Network

        Returns
        -------
        A Sequential Neural Network model
        """
        model = Sequential()
        model.add(Dense(units=120, activation='relu', input_dim=self.ACTION_SPACE))
        model.add(Dropout(0.15))
        model.add(Dense(units=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(units=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(units=self.ACTION_SPACE, activation='softmax'))
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model

    # Adds step's data to a memory replay array
    def update_replay_memory(self, transition):
        """
        Updates the current replay memory.

        Parameters
        ----------
        transition : (current_state, action, reward, new_current_state, done) Tuple
        """
        self.replay_memory.append(transition)

    def train(self, terminal_state):
        """
        Trains and updates the memory network at each step in the episode.

        Parameters
        ----------
        terminal_state : Boolean
            True if the step is the last step in the sequence.

        """
        if len(self.replay_memory) > self.MINIBATCH_SIZE:
            minibatch = random.sample(self.replay_memory, self.MINIBATCH_SIZE)
        else:
            minibatch = self.replay_memory

        for current_state, action, reward, new_current_state, done in minibatch:
            target = reward
            if not terminal_state and len(new_current_state) > 0:
                target = reward + self.gamma * np.amax(self.model.predict(new_current_state))
            target_f = self.model.predict(np.array(current_state))
            target_f[0][np.argmax(action)] = target
            self.model.fit(current_state, target_f, epochs=1, verbose=0)

    def get_qs(self, state):
        """
        Queries main network for Q values given current observation space (environment state).

        Parameters
        ----------
        state : List
            The state as a 1D List

        Returns
        -------
            The predicted values based on the current depiction of the model.
        """
        return self.model.predict(np.array(state))

    def update(self, s, s_, a, a_, r):
        """
        Perform the Q-Learning update of Q values.

        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action. NOT used by Q-learner!
        r : int
            reward received after executing action "a" in state "s"
        """
        if not s_:
            done = True
            # add r to rewards list
            self.rewards.append(r)
        else:
            done = False
        # current_state, action, reward, new_current_state, done
        self.update_replay_memory((self.get_states(s), a, r, self.get_states(s_), done))
        self.train(done)

    def get_action(self, s):
        """
        Returns the predicted action based on the given state

        Parameters
        ----------
        s : String
            The state as a string

        Returns
        -------
            An (x, y) tuple of the predicted action to take.
        """
        possible_actions = [a for a in self.actions if s[a[0] * 5 + a[1]] == '-']

        # This part stays mostly the same, the change is to query a model for Q values
        try:
            if np.random.random() > self.eps:
                # Get action from Q table
                pred_act = np.argmax(self.get_qs(self.get_states(s)))

                # Get the location of the action based on where it was located in the results
                action = (int(pred_act / 5), int(pred_act % 5))
                # print(possible_actions)
                # Check if the prediction gave us valid action, else use a random valid action
                if action not in possible_actions:
                    # print(len(possible_actions))
                    action = possible_actions[np.random.randint(0, len(possible_actions) - 1)]
            else:
                # Get random action
                action = possible_actions[np.random.randint(0, len(possible_actions) - 1)]
        except ValueError:
            log.error("Got a Value Error, ignoring.")
            action = possible_actions[0]

        # Decay epsilon
        if self.eps > self.MIN_EPSILON:
            self.eps *= self.eps_decay
            self.eps = max(self.MIN_EPSILON, self.eps)

        return action

    @staticmethod
    def get_states(state_str):
        """
        Translates a String state to an array of categorized Integers.

        Parameters
        ----------
        state_str : String
            The State as a string

        Returns
        -------
            An array of categorized Integers
        """
        if not state_str:
            return []
        state = []
        for s in state_str:
            if s == 'X':
                state.append(-1)
            elif s == 'O':
                state.append(1)
            else:
                state.append(0)
        return np.array([state])

    def save(self, path):
        """
        Saves the model's weights based on the provided path.

        Parameters
        ----------
        path : String
            The location to save the model's weights
        """
        self.model.save(path)

    def load(self, path):
        """
        Loads the model's weights based on the provided path.

        Parameters
        ----------
        path : String
            The location to load the model's weights
        """
        self.model.load_weights(path)


class SARSAlearner(Learner):
    """
    A class to implement the SARSA agent.
    """

    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, s_, a, a_, r):
        """
        Perform the SARSA update of Q values.

        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action
        r : int
            reward received after executing action "a" in state "s"
        """
        # Update Q(s,a)
        if s_ is not None:
            self.Q[a][s] += self.alpha * (r + self.gamma * self.Q[a_][s_] - self.Q[a][s])
        else:
            # terminal state update
            self.Q[a][s] += self.alpha * (r - self.Q[a][s])
            # add r to rewards list
            self.rewards.append(r)
