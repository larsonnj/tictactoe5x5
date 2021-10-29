import random
import os
import pickle
import logging

from tictactoe.agent import Qlearner


log = logging.getLogger(__name__)


class Teacher:
    """ 
    A class to implement a teacher that knows the optimal playing strategy.
    Teacher returns the best move at any time given the current state of the game.
    Note: things are a bit more hard-coded here, as this was not the main focus of
    the exercise so I did not spend as much time on design/style. Everything works
    properly when tested.

    Parameters
    ----------
    level : float 
        teacher ability level. This is a value between 0-1 that indicates the
        probability of making the optimal move at any given time.
    """

    def __init__(self, level=0.9):
        """
        Ability level determines the probability that the teacher will follow
        the optimal strategy as opposed to choosing a random available move.
        """
        self.ability_level = level
        self.wins = 0
        self.lifetime_wins = 0

    def win(self, board, key='X'):
        """ If any row or diag has only a key or keys, play on that to win. """

        board_range = 5

        for i in range(board_range):
            for j in range(board_range):
                # diagonal down to the right, 5 next to each other
                if i == 0 and j == 0:
                    a = [board[i][j], board[i + 1][j + 1], board[i + 2][j + 2], board[i + 3][j + 3], board[i + 4][j + 4]]
                    if a.count('-') + a.count(key) == 5 and a.count(key) > 1:
                        ind = a.index('-')
                        return i+ind, j+ind
                # diagonal down to the left, 5 next to each other
                if i == 0 and j == 4:
                    b = [board[i][j], board[i + 1][j - 1], board[i + 2][j - 2], board[i + 3][j - 3], board[i + 4][j - 4]]
                    if b.count('-') + b.count(key) == 5 and b.count(key) > 1:
                        ind = b.index('-')
                        return i+ind, j-ind
                # columns 5 next to each other
                if j == 0:
                    col = [board[i][j], board[i][j + 1], board[i][j + 2], board[i][j + 3], board[i][j + 4]]
                    if col.count('-') + col.count(key) == 5 and col.count(key) > 1:
                        ind = col.index('-')
                        return i, j+ind
                # rows, 5 next to each other
                if i ==0:
                    col = [board[i][j], board[i + 1][j], board[i + 2][j], board[i + 3][j], board[i + 4][j]]
                    if col.count('-') + col.count(key) == 5 and col.count(key) > 1:
                        ind = col.index('-')
                        return i+ind, ind
        return None

    def blockWin(self, board):
        """ Block the opponent if she has a win available. """
        return self.win(board, key='O')

    def fork(self, board):
        """ Create a fork opportunity such that we have 2 threats to win. """
        # Check all adjacent side middles
        if board[1][0] == 'X' and board[0][1] == 'X':
            if board[0][0] == '-' and board[2][0] == '-' and board[0][2] == '-':
                return 0, 0
            elif board[1][1] == '-' and board[2][1] == '-' and board[1][2] == '-':
                return 1, 1
        elif board[1][0] == 'X' and board[2][1] == 'X':
            if board[2][0] == '-' and board[0][0] == '-' and board[2][2] == '-':
                return 2, 0
            elif board[1][1] == '-' and board[0][1] == '-' and board[1][2] == '-':
                return 1, 1
        elif board[2][1] == 'X' and board[1][2] == 'X':
            if board[2][2] == '-' and board[2][0] == '-' and board[0][2] == '-':
                return 2, 2
            elif board[1][1] == '-' and board[1][0] == '-' and board[0][1] == '-':
                return 1, 1
        elif board[1][2] == 'X' and board[0][1] == 'X':
            if board[0][2] == '-' and board[0][0] == '-' and board[2][2] == '-':
                return 0, 2
            elif board[1][1] == '-' and board[1][0] == '-' and board[2][1] == '-':
                return 1, 1
        # Check all cross corners
        elif board[0][0] == 'X' and board[2][2] == 'X':
            if board[1][0] == '-' and board[2][1] == '-' and board[2][0] == '-':
                return 2, 0
            elif board[0][1] == '-' and board[1][2] == '-' and board[0][2] == '-':
                return 0, 2
        elif board[2][0] == 'X' and board[0][2] == 'X':
            if board[2][1] == '-' and board[1][2] == '-' and board[2][2] == '-':
                return 2, 2
            elif board[1][0] == '-' and board[0][1] == '-' and board[0][0] == '-':
                return 0, 0
        return None

    def blockFork(self, board):
        """ Block the opponents fork if she has one available. """
        corners = [board[0][0], board[2][0], board[0][2], board[2][2]]
        # Check all adjacent side middles
        if board[1][0] == 'O' and board[0][1] == 'O':
            if board[0][0] == '-' and board[2][0] == '-' and board[0][2] == '-':
                return 0, 0
            elif board[1][1] == '-' and board[2][1] == '-' and board[1][2] == '-':
                return 1, 1
        elif board[1][0] == 'O' and board[2][1] == 'O':
            if board[2][0] == '-' and board[0][0] == '-' and board[2][2] == '-':
                return 2, 0
            elif board[1][1] == '-' and board[0][1] == '-' and board[1][2] == '-':
                return 1, 1
        elif board[2][1] == 'O' and board[1][2] == 'O':
            if board[2][2] == '-' and board[2][0] == '-' and board[0][2] == '-':
                return 2, 2
            elif board[1][1] == '-' and board[1][0] == '-' and board[0][1] == '-':
                return 1, 1
        elif board[1][2] == 'O' and board[0][1] == 'O':
            if board[0][2] == '-' and board[0][0] == '-' and board[2][2] == '-':
                return 0, 2
            elif board[1][1] == '-' and board[1][0] == '-' and board[2][1] == '-':
                return 1, 1
        # Check all cross corners (first check for double fork opp using the corners array)
        elif corners.count('-') == 1 and corners.count('O') == 2:
            return 1, 2
        elif board[0][0] == 'O' and board[2][2] == 'O':
            if board[1][0] == '-' and board[2][1] == '-' and board[2][0] == '-':
                return 2, 0
            elif board[0][1] == '-' and board[1][2] == '-' and board[0][2] == '-':
                return 0, 2
        elif board[2][0] == 'O' and board[0][2] == 'O':
            if board[2][1] == '-' and board[1][2] == '-' and board[2][2] == '-':
                return 2, 2
            elif board[1][0] == '-' and board[0][1] == '-' and board[0][0] == '-':
                return 0, 0
        return None

    def center(self, board):
        """ Pick the center if it is available. """
        if board[4][4] == '-':
            return 4, 4
        return None

    def corner(self, board):
        """ Pick a corner move. """

        # Pick opposite corner of opponent if available
        if board[0][0] == 'O' and board[4][4] == '-':
            return 4, 4
        elif board[4][0] == 'O' and board[0][4] == '-':
            return 0, 4
        elif board[0][4] == 'O' and board[4][0] == '-':
            return 4, 0
        elif board[4][4] == 'O' and board[0][0] == '-':
            return 0, 0
        # Pick any corner if no opposites are available
        elif board[0][0] == '-':
            return 0, 0
        elif board[4][0] == '-':
            return 4, 0
        elif board[0][4] == '-':
            return 0, 4
        elif board[4][4] == '-':
            return 4, 4
        return None

    def sideEmpty(self, board):
        """ Pick an empty side. """
        if board[1][0] == '-':
            return 1, 0
        elif board[2][1] == '-':
            return 2, 1
        elif board[1][2] == '-':
            return 1, 2
        elif board[0][1] == '-':
            return 0, 1
        return None

    def randomMove(self, board):
        """ Chose a random move from the available options. """
        possibles = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == '-':
                    possibles += [(i, j)]
        return possibles[random.randint(0, len(possibles)-1)]

    def makeMove(self, board):
        """
        Trainer goes through a hierarchy of moves, making the best move that
        is currently available each time. A touple is returned that represents
        (row, col).
        """
        # Chose randomly with some probability so that the teacher does not always win
        if random.random() > self.ability_level:
            return self.randomMove(board)
        # Follow optimal strategy
        a = self.win(board)
        if a is not None:
            return a
        a = self.blockWin(board)
        if a is not None:
            return a
        a = self.fork(board)
        if a is not None:
            return a
        a = self.blockFork(board)
        if a is not None:
            return a
        a = self.center(board)
        if a is not None:
            return a
        a = self.corner(board)
        if a is not None:
            return a
        a = self.sideEmpty(board)
        if a is not None:
            return a
        return self.randomMove(board)

    def increment_wins(self):
        self.wins += 1
        self.lifetime_wins += 1

    def get_wins(self):
        return self.wins

    def reset_wins(self):
        self.wins = 0

    def get_lifetime_wins(self):
        return self.lifetime_wins


# mathewb: Created a AgentTeacher that inherits from the base Teacher class to allow an Agent to become a Teacher
class AgentTeacher(Teacher):
    """
    A class that allows an Agent to become a Teacher (Player). This class adds update and save functions which are
    specific to how an Agent learns.

    Parameters
    ----------
    agent : Learner (see agent.py)
        The specific Agent.
    level : float   (Inherited from super class)
        teacher ability level. This is a value between 0-1 that indicates the
        probability of making the optimal move at any given time.
    """
    def __init__(self, agent, level=0.9):
        super().__init__(level)
        self.agent = agent

    def makeMove(self, board):
        """
        Overrides the makeMove functionality from the Teacher class.
        This class returns its calculated action (location on the board) as an (x, y) tuple.

        Parameters
        ----------
        board : 2D List
            The current state of the board

        Returns
        -------
            The location on the board as an (x, y) tuple.
        """
        return self.agent.get_action(self.get_state_key(board))

    def update(self, prev_state, new_state, prev_action, new_action, reward):
        """
        Updates the Agent's state to allow the Agent to learn.

        Parameters
        ----------
        prev_state : String
            The previous state
        new_state : String
            The current state
        prev_action : (x, y) Tuple
            The previous action
        new_action : (x, y) Tuple
            The new action
        reward : Integer
            The reward
        """
        self.agent.update(prev_state, new_state, prev_action, new_action, reward)

    def save(self):
        """ Saves the state of the agent """
        path = './teacher.pkl'
        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'wb') as f:
            print("saving teacher.")
            pickle.dump(self, f)

    @staticmethod
    def get_state_key(board):
        """
        Converts 2D list representing the board state into a string key
        for that state. Keys are used for Q-value hashing.
        NOTE: Copied from game.py

        Parameters
        ----------
        board : list of lists
            the current game board
        """
        key = ''
        for row in board:
            for elt in row:
                key += elt
        return key


class QLearnerTeacher(AgentTeacher):
    """
    Q-Learner that is also a Teacher (Player)

    Parameters
    ----------
    level : float   (Inherited from super class)
        teacher ability level. This is a value between 0-1 that indicates the
        probability of making the optimal move at any given time.
    """
    def __init__(self, level=0.9):
        super().__init__(Qlearner(.5, .9, .1), level)

    def save(self):
        """ Saves the state of the agent """
        path = './teacher.pkl'
        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'wb') as f:
            print("saving teacher.")
            pickle.dump(self, f)
