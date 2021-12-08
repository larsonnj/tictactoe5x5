import random
import os
import logging
from tictactoe.teacher import AgentTeacher


log = logging.getLogger(__name__)


class Game:
    """ The game class. New instance created for each new game. """

    def __init__(self, agent, teacher=None, gui=False, show_teaching_board=False):
        self.agent = agent
        self.teacher = teacher
        self.gui = gui
        self.show_teaching_board = show_teaching_board
        self.board_size = 5
        self.connect_length = 5

        # initialize the game board
        self.board = [['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-']]

    def playerMove(self):
        """
        Query player for a move and update the board accordingly.
        """
        if self.teacher is not None:
            action = self.teacher.makeMove(self.board)
            self.board[action[0]][action[1]] = 'X'
        else:
            printBoard(self)
            while True:
                move = input("Your move! Please select a row and column from 0-8 "
                             "in the format row,col: ")
                print('\n')
                try:
                    row, col = int(move[0]), int(move[2])
                except (ValueError, IndexError):
                    print("INVALID INPUT! Please use the correct format.")
                    continue
                if row not in range(self.board_size) or col not in range(self.board_size) or not self.board[row][col] == '-':
                    print("INVALID MOVE! Choose again.")
                    continue
                self.board[row][col] = 'X'
                break
    
    def setBoard(self,row,col,val):
        self.board[row][col] = val
        

    def agentMove(self, action):
        """
        Update board according to agent's move.
        """
        self.board[action[0]][action[1]] = 'O'
        if self.gui:
            print(str(action[0]) + "," + str(action[1]))

    def checkForWin(self, key):
        """
        Check to see whether the player/agent with token 'key' has won.
        Returns a boolean holding truth value.

        Parameters
        ----------
        key : string
            token of most recent player. Either 'O' or 'X'
        """

        # Loop through the board by rows
        #   Loop through the board on columns
        #       check for player win on diagonals
        # check for player win on rows/columns

        # Set the loop size = size of board
        board_range = self.board_size
        board_offset = self.board_size - self.connect_length
        board_edge_offset = board_range - board_offset

        for i in range(board_range):
            for j in range(board_range):
                # diagonal down to the right, 5 next to each other
                if i == 0 and j == 0:
                    a = [self.board[i][j], self.board[i + 1][j + 1], self.board[i + 2][j + 2], self.board[i + 3][j + 3], self.board[i + 4][j + 4]]
                    if a.count(key) == self.connect_length:
                        return True
                # diagonal down to the left, 5 next to each other
                if i == 0 and j == 4:
                    b = [self.board[i][j], self.board[i + 1][j - 1], self.board[i + 2][j - 2], self.board[i + 3][j - 3], self.board[i + 4][j - 4]]
                    if b.count(key) == self.connect_length:
                        return True
                # columns 5 next to each other
                if j == 0:
                    col = [self.board[i][j], self.board[i][j + 1], self.board[i][j + 2], self.board[i][j + 3], self.board[i][j + 4]]
                    if col.count(key) == self.connect_length:
                        return True
                # rows, 5 next to each other
                if i == 0:
                    col = [self.board[i][j], self.board[i + 1][j], self.board[i + 2][j], self.board[i + 3][j], self.board[i + 4][j]]
                    if col.count(key) == self.connect_length:
                        return True

        return False

    def checkForWin3(self, key):
        """
        Check to see whether the player/agent with token 'key' has won.
        Returns a boolean holding truth value.

        Parameters
        ----------
        key : string
            token of most recent player. Either 'O' or 'X'
        """

        # Loop through the board by rows
        #   Loop through the board on columns
        #       check for player win on diagonals
        # check for player win on rows/columns

        # Set the loop size = size of board
        board_range = 3

        for i in range(board_range):
            for j in range(board_range):
                # diagonal down to the right, n next to each other
                if i < (board_range - 2) and j < (board_range - 2):
                    a = [self.board[i][j], self.board[i + 1][j + 1], self.board[i + 2][j + 2]]
                    if a.count(key) == 3:
                        return True
                # diagonal down to the left, n next to each other
                if i < (board_range - 2) and (j > 1):
                    b = [self.board[i][j], self.board[i + 1][j - 1], self.board[i + 2][j - 2]]
                    if b.count(key) == 3:
                        return True
                # columns and rows, 3 next to each other
                if j < (board_range - 2):
                    col = [self.board[j][i], self.board[j + 1][i], self.board[j + 2][i]]
                    if col.count(key) == 3:
                        return True
                    row = [self.board[i][j], self.board[i][j + 1], self.board[i][j + 2]]
                    if row.count(key) == 3:
                        return True

        return False

    def checkForDraw(self):
        """
        Check to see whether the game has ended in a draw. Returns a
        boolean holding truth value.
        """
        draw = True
        for row in self.board:
            for elt in row:
                if elt == '-':
                    draw = False
        if self.teacher is None:
            log.debug("Draw = " + str(draw))
        return draw

    def checkForEnd(self, key):
        """
        Checks if player/agent with token 'key' has ended the game. Returns -1
        if the game is still going, 0 if it is a draw, and 1 if the player/agent
        has won.

        Parameters
        ----------
        key : string
            token of most recent player. Either 'O' or 'X'
        """
        if self.checkForWin(key):
            player_str = "Player"
            if self.teacher is not None:
                player_str = "Teacher"
                printBoard(self)
            else:
                printBoard(self)
                if key == 'X':
                    print("{} wins!".format(player_str))
                else:
                    print("RL agent wins!")
            return 1
        elif self.checkForDraw():
            if self.teacher is None:
                printBoard(self)
                print("It's a draw!")
            return 0
        return -1

    def playGame(self, player_first):
        """ 
        Begin the tic-tac-toe game loop. 

        Parameters
        ----------
        player_first : boolean
            Whether or not the player will move first. If False, the
            agent goes first.

        """
        counter = 0
        teacher_reward = 0
        # Initialize the agent's state and action
        if player_first:
            self.playerMove()
        prev_state = getStateKey(self.board)
        prev_action = self.agent.get_action(prev_state)

        # iterate until game is over
        while True:
            # execute oldAction, observe reward and state
            self.agentMove(prev_action)
            # Check for agent win
            agent_check = self.checkForEnd('O')
            if not agent_check == -1:
                # Agent wins
                # game is over. +1 reward if win, 0 if draw
                reward = agent_check
                teacher_reward = -1
                break
            self.playerMove()
            # Check for Player win
            check = self.checkForEnd('X')
            if not check == -1:
                # Player wins
                # game is over. No reward for agent, reward system changed from -1
                teacher_reward = check
                reward = -1
                # if self.teacher is not None and isinstance(self.teacher, AgentTeacher):
                if self.teacher is not None:
                    self.teacher.increment_wins()
                break
            else:
                # game continues. 0 reward
                reward = 0
            new_state = getStateKey(self.board)

            # determine new action (epsilon-greedy)
            new_action = self.agent.get_action(new_state)
            # update Q-values
            self.agent.update(prev_state, new_state, prev_action, new_action, reward)

            # Update Teacher's states:
            if self.teacher is not None and isinstance(self.teacher, AgentTeacher):
                self.teacher.update(prev_state, new_state, prev_action, new_action, teacher_reward)

            # reset "previous" values
            prev_state = new_state
            prev_action = new_action
            # append reward
            # nateJL: Add a break when the game is not ending.
            counter = counter + 1
            if counter > 25:
                # Break at this point, too many moves have been attempted.
                # 5x5 board has 81 moves
                log.error("The game is stuck after 25 turns!!!")
                log.error("Exiting this game as a Draw.")
                reward = 0
                teacher_reward = 0
                break

        # Update the states
        self.agent.update(prev_state, None, prev_action, None, reward)
        if self.teacher is not None and isinstance(self.teacher, AgentTeacher):
            self.teacher.update(prev_state, None, prev_action, None, teacher_reward)


    def resetBoard(self):
        # re-initialize the game board
        self.board = [['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-'],
                      ['-', '-', '-', '-', '-']]
        return
        
    def playAgent(self):
        """ 
        Used from GUI to make the agent move and
        calculate the reward and next move
        based on current board configuration
        """
        counter = 0
        teacher_reward = 0

        # Check for Player win
        # NJL:  This needs to be somewhere else, but is OK here for now
        check = self.checkForEnd('X')
        if not check == -1:
            # Player wins
            # game is over. No reward for agent, reward system changed from -1
            teacher_reward = check
            reward = -1
            # if self.teacher is not None and isinstance(self.teacher, AgentTeacher):
            if self.teacher is not None:
                self.teacher.increment_wins()
            return
        else:
            # game continues. 0 reward
            reward = 0

        # Initialize the agent's state and action
        prev_state = getStateKey(self.board)
        prev_action = self.agent.get_action(prev_state)

        # execute oldAction, observe reward and state
        self.agentMove(prev_action)
        # Check for agent win
        agent_check = self.checkForEnd('O')
        if not agent_check == -1:
            # Agent wins
            # game is over. +1 reward if win, 0 if draw
            reward = agent_check
            teacher_reward = -1
            return

        new_state = getStateKey(self.board)

        # determine new action (epsilon-greedy)
        new_action = self.agent.get_action(new_state)
        # update Q-values
        self.agent.update(prev_state, new_state, prev_action, new_action, reward)

        # Update Teacher's states:
        if self.teacher is not None and isinstance(self.teacher, AgentTeacher):
            self.teacher.update(prev_state, new_state, prev_action, new_action, teacher_reward)

        # reset "previous" values
        prev_state = new_state
        prev_action = new_action


    def start(self):
        """
        Function to determine who moves first, and subsequently, start the game.
        If a teacher is employed, first mover is selected at random.
        If a human is playing, the human is asked whether he/she would
        like to move fist. 
        """
        if self.teacher is not None:
            # During teaching, chose who goes first randomly with equal probability
            if random.random() < 0.5:
                self.playGame(player_first=False)
            else:
                self.playGame(player_first=True)
        else:
            while True:
                response = input("Would you like to go first? [y/n]: ")
                print('')
                if response == 'n' or response == 'no':
                    self.playGame(player_first=False)
                    break
                elif response == 'y' or response == 'yes':
                    self.show_teaching_board = True
                    self.playGame(player_first=True)
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def printBoard(self):

    """
    Prints the game board as text output to the terminal.

    Parameters
    ----------
    self:  Current game object
    """
    # Exit if gui being used
    if self.gui:
        return None


    if self.show_teaching_board is not True:
        return None

    # now, to clear the screen
    cls()

    print('    0   1   2   3   4\n')
    for i, row in enumerate(self.board):
        print('%i   ' % i, end='')
        for elt in row:
            print('%s   ' % elt, end='')
        print('\n')


def getStateKey(board):
    """
    Converts 2D list representing the board state into a string key
    for that state. Keys are used for Q-value hashing.

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
