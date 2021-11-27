# Tic-Tac-Toe with Reinforcement Learning
This is a repository for training an AI agent to play Tic-tac-toe using
reinforcement learning. The SARSA, Q-learning RL, and DQN
algorithms are implemented. A user may teach the agent himself by
playing the game for a couple of rounds, or he may apply an automated
teacher agent. 

2/18/2020:  Modified by Nathan Larson.
2/29/2020:  Modified by Benson Mathew.
10/28/2021: Modified by Nathan Larson.
    Updated code for new version of keras
11/26/2021: Modified by Nathan Larson, added info on prototype of UI

## Dependencies
Python 3.8
TensorFlow-2.1.0
Keras-2.3.1

## Setup

1. Install Python
2. Install Python extensions
    TensorFlow-2.1.0 and Keras-2.3.1 are required to be installed before running `play.py`.
    These dependencies can be installed by running the following commands:

        pip install tensorflow
        pip install keras
        pip install matplotlib

## Code Structure

#### Source Code

The directory `tictactoe` contains the core source code for this project.
There are 3 main source code files:
1. game.py
2. agent.py
3. teacher.py

I have implemented three RL agents that learn to play the game of tic-tac-toe:
one follows the SARSA algorithm, one that follows Q-learning, and the other that 
follows a Deep Q-Learning Network Algorithm.
These agents are trained by a teacher agent that knows the optimal strategy;
however, the teacher only follows this strategy with a given probability
p at each turn. The rest of the time this teacher chooses randomly
from the moves that are available, so that the agents are able to win on
occasion and learn from these wins. To initialize the learning agent Q values,
I make use of default dictionaries with default values of 0 such that the
value for every state-action pair is initialized to 0.

The Q-learning, SARSA, and DQN agents are implemented in `agent.py`.
Each of the two learning agents inherit from a parent learner class; the key difference between the two is their Q-value update function. 

The Teacher agent is implemented in `teacher.py`. 
The teacher knows the optimal policy for each state presented; however, this agent only takes the optimal choice with a set probability.

In `game.py`, the main game class is found. 
The Game class holds the state of each particular game instance, and it contains the majority of the main game functionality. 
The main game loop can be found in the class's function playGame().

#### Game Script

To play the game (see "Running the Program" below for instructions) you will use the script called `play.py`. 
This script is organized as follows. 
The GameLearner class holds the state of the current game sequence, which will continue until the player choses to stop or the teacher has finished the designated number of episodes.

## Running the Program

1. If using Anaconda, launch Anaconda
2. activate a previously used environment or create a new one
   a.  conda activate <environment>
3. Install the dependencies (shown above)

#### Train a new agent manually
To initialize a new agent and begin a new game loop, simply run:

    python play.py -a q                (Q-learner)
    python play.py -a s                (Sarsa-learner)
    python play.py -a dqn              (Deep Q-Learning Network)

This will initialize the game and allow you to train the agent manually
by playing against the agent repeatedly. Be careful, however, as initializing
a new agent will delete the state of the previous agents that were stored for
the selected agent type. In the process of playing, you will be storing the
new agent state with each game iteration.

#### Train a new agent automatically (via teacher agent)
To initialize a new RL agent and train it automatically with a teacher agent,
use the flag '-t' followed by the number of game iterations you would like to
train for:

    python play.py -a q -t 5000        (Q-learner)
    python play.py -a s -t 5000        (Sarsa-learner)
    python play.py -a dqn -t 5000      (Deep Q-Learning Network)


Again, be careful as this will overwrite previously-existing agents.

#### Load a trained agent
To load existing agents and play against them, run:

    python play.py -a q -l             (Q-learner)
    python play.py -a s -l             (Sarsa-learner)
    python play.py -a dqn -l           (Deep Q-Learning Network)

I have trained an instance of each the Q-learner and Sarsa-learner agents
and pickled them into .pkl files that are included here. These agents were
trained by a teacher of level 0.9 for 100000 episodes, and they have learned
to play considerably well. You can make use of these if you like, but they
will be overwritten if you have initialized new agents.

#### Load a trained agent and train it further
You can train existing agents further by loading them and teaching them, via
a combination of '-t' and '-l':

    python play.py -a q -l -t 5000     (Q-learner)
    python play.py -a s -l -t 5000     (Sarsa-learner)
    python play.py -a dqn -l -t -5000  (Deep Q-Learning Network)

#### Load a trained agent and view reward history plot
Finally, to load a stored agent and view a plot of its cumulative reward
history, use '-l' in combination with '-p':

    python play.py -a q -l -p          (Q-learner)
    python play.py -a s -l -p          (Sarsa-learner)
    python play.py -a dqn -l -p        (Deep Q-Learning Network)
