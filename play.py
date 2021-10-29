import argparse
import os
import pickle
import sys
import numpy as np
import matplotlib.pylab as plt
import logging

from tictactoe.agent import Qlearner, SARSAlearner, DQN
from tictactoe.teacher import Teacher, AgentTeacher, QLearnerTeacher
from tictactoe.game import Game

log = logging.getLogger(__name__)


def plot_agent_reward(rewards):
    """ Function to plot agent's accumulated reward vs. iteration """
    plt.plot(np.cumsum(rewards))
    plt.title('Agent Cumulative Reward vs. Iteration')
    plt.ylabel('Reward')
    plt.xlabel('Episode')
    plt.show()


class GameLearning(object):
    """
    A class that holds the state of the learning process. Learning
    agents are created/loaded here, and a count is kept of the
    games that have been played.
    """

    def __init__(self, args, alpha=0.5, gamma=0.8, epsilon=0.1):
        self.games_played = 0

        if args.agent_type == 'q':
            print("Using the QLearner Algorithm")
        elif args.agent_type == 's':
            print("Using the SARSA Learner Algorithm")
        elif args.agent_type == 'dqn':
            print("Using the DQN Algorithm")

        if args.run_with_gui:
            self.run_with_gui = 1
        else:
            self.run_with_gui = 0

        if args.display_board_during_teaching:
            print("Show the board!")
            self.show_teaching_board = True
        else:
            self.show_teaching_board = False

        if args.load:
            # load agent
            if args.agent_type == 'q':
                # QLearner
                try:
                    f = open('./qlearner_agent.pkl', 'rb')
                    self.agent = pickle.load(f)
                    f.close()
                except IOError:
                    print("The agent file does not exist. Quitting.")
                    sys.exit(1)
            elif args.agent_type == 's':
                # SarsaLearner
                try:
                    f = open('./sarsa_agent.pkl', 'rb')
                    self.agent = pickle.load(f)
                    f.close()
                except IOError:
                    print("The agent file does not exist. Quitting.")
                    sys.exit(1)
            elif args.agent_type == 'dqn':
                # DQN
                try:
                    self.agent = DQN(alpha, gamma, epsilon)
                    self.agent.load('./dqn.hdf5')
                except IOError:
                    print("The agent file does not exist. Quitting.")
                    sys.exit(1)
            else:
                print("UNSUPPORTED AGENT TYPE: {}".format(args.agent_type))
                sys.exit(1)

            # If plotting, show plot and quit
            if args.plot:
                plot_agent_reward(self.agent.rewards)
                sys.exit(0)
        else:
            # check if agent state file already exists, and ask user whether to overwrite if so
            if (not args.do_not_use_agent_files and
                    (args.agent_type == "q" and os.path.isfile('./qlearner_agent.pkl')) or
                    (args.agent_type == "s" and os.path.isfile('./sarsa_agent.pkl')) or
                    (args.agent_type == "dqn" and os.path.isfile('./dqn.hdf5'))):
                while True:
                    response = input("An agent state is already saved for this type. "
                                     "Are you sure you want to overwrite? [y/n]: ")
                    if response == 'y' or response == 'yes':
                        break
                    elif response == 'n' or response == 'no':
                        print("OK. Quitting.")
                        sys.exit(0)
                    else:
                        print("Invalid input. Please choose 'y' or 'n'.")
            if args.agent_type == "dqn":
                self.agent = DQN(alpha, gamma, epsilon)
            elif args.agent_type == "s":
                self.agent = SARSAlearner(alpha, gamma, epsilon)
            else:
                self.agent = Qlearner(alpha, gamma, epsilon)

    def beginPlaying(self):
        """ Loop through game iterations with a human player. """
        print("Welcome to Tic-Tac-Toe. You are 'X' and the computer is 'O'.")

        def play_again():
            print("Games played: %i" % self.games_played)
            while True:
                play = input("Do you want to play again? [y/n]: ")
                if play == 'y' or play == 'yes':
                    return True
                elif play == 'n' or play == 'no':
                    return False
                else:
                    print("Invalid input. Please choose 'y' or 'n'.")

        while True:
            game = Game(self.agent, None, self.run_with_gui, self.show_teaching_board)
            game.start()
            self.games_played += 1
            if not play_again():
                print("OK. Quitting.")
                break

        # nateltx: Add write_agent and plot at end of self play, remove from teaching play as called from here.
        self.write_agent()
        plot_agent_reward(self.agent.rewards)

    def write_agent(self):
        """Write out the agent to a file based on the learner type"""

        # nateltx:  Added the write function
        # should be able to write different files to allow for different levels of the tic tac toe
        if args.do_not_use_agent_files:
            return None

        print("Saving Agent Data")

        try:
            if args.agent_type == 'q':
                # QLearner
                self.agent.save('./qlearner_agent.pkl')
            elif args.agent_type == 's':
                # SarsaLearner
                self.agent.save('./sarsa_agent.pkl')
            elif args.agent_type == 'dqn':
                # DQN
                self.agent.save('./dqn.hdf5')
        except IOError:
            print("The agent file does not exist. Quitting.")
            sys.exit(1)

    def beginTeaching(self,  episodes, use_agent=False):
        """ Loop through game iterations with a teaching agent. """

        def play_ai():
            while True:
                play = input("Would you like to play the AI? [y/n]: ")
                if play == 'y' or play == 'yes':
                    self.show_teaching_board = True
                    return True
                elif play == 'n' or play == 'no':
                    return False
                else:
                    print("Invalid input. Please choose 'y' or 'n'.")

        def save_teacher_data():
            while True:
                play = input("Would you like to save the teacher's data: ")
                if play == 'y' or play == 'yes':
                    return True
                elif play == 'n' or play == 'no':
                    return False
                else:
                    print("Invalid input. Please choose 'y' or 'n'.")

        if use_agent:
            # attempt to make another agent be the teacher.
            print("Use a Teacher Agent to teach the AI.")
            teacher_file = './teacher.pkl'
            try:
                f = open(teacher_file, 'rb')
                teacher = pickle.load(f)
                f.close()
                teacher.reset_wins()
            except IOError:
                print("Could not load the teacher file.")
                teacher = QLearnerTeacher()
        else:
            print("Using basic teacher to train the AI.")
            teacher = Teacher()

        # Train for allotted number of episodes
        while self.games_played < episodes:
            game = Game(self.agent, teacher=teacher, gui=self.run_with_gui, show_teaching_board=self.show_teaching_board)

            game.start()
            self.games_played += 1
            # Monitor progress
            if episodes <= 1000:
                print("Games played: %i" % self.games_played)
            elif self.games_played % 1000 == 0:
                print("Games played: %i" % self.games_played)

        print("Teacher wins: ", teacher.get_wins())
        print("Teacher lifetime wins: ", teacher.get_lifetime_wins())
        print("Agent wins: ", self.games_played - teacher.get_wins())

        # nateltx: give option to play the computer
        if play_ai():
            self.beginPlaying()
        else:
            self.write_agent()
            plot_agent_reward(self.agent.rewards)

        # mathewb: give option to save the teacher's data
        if isinstance(teacher, AgentTeacher) and save_teacher_data():
            teacher.save()

        self.agent.get_size()


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe.")
    parser.add_argument('-a', "--agent_type", type=str, default="q",
                        help="Specify the computer agent learning algorithm. "
                             "AGENT_TYPE='q' for Q-learning and ='s' for Sarsa-learning")
    parser.add_argument("-l", "--load", action="store_true",
                        help="whether to load trained agent")
    parser.add_argument("-t", "--teacher_episodes", default=None, type=int,
                        help="employ teacher agent who knows the optimal "
                             "strategy and will play for TEACHER_EPISODES games")
    parser.add_argument("-ta", "--use_agent_to_teach", action="store_true",
                        help="employ a Q agent to play against the main agent "
                             "Can save progress of teacher agent")
    parser.add_argument("-db", "--display_board_during_teaching", action="store_true",
                        help="Display the playing board while agent being trained.")
    parser.add_argument("-p", "--plot", action="store_true",
                        help="whether to plot reward vs. episode of stored agent "
                             "and quit")
    parser.add_argument("-n", "--do_not_use_agent_files", action="store_true",
                        help="ignore saved agent files and do not write agent files.  Run as if new.")
    parser.add_argument("-g", "--run_with_gui", action="store_true",
                        help="Run program as a GUI engine.  Don't print board, only agent x,y selection values.")

    args = parser.parse_args()
    assert args.agent_type == 'q' or args.agent_type == 's' or args.agent_type == 'dqn', \
        "learner type must be either 'q' or 's' or 'dqn'."
    if args.plot:
        assert args.load, "Must load an agent to plot reward."
        assert args.teacher_episodes is None, \
            "Cannot plot and teach concurrently; must chose one or the other."

    gl = GameLearning(args)
    if args.teacher_episodes is not None:
        gl.beginTeaching(args.teacher_episodes, args.use_agent_to_teach)
    else:
        gl.beginPlaying()
