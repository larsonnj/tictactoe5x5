"""
Original code for a 3x3 board game taken from https://www.pythonpool.com/tic-tac-toe-python/
and modified into a 5x5 grid game.

Version 1:  Set up initial board
Version 2:  Added menus
Version 3:  Moved some menu actions to buttons
Version 4:  Simplified some code and added two new game buttons
Version 5:  Add computer play and friend play functionality in code
            Add score tracking functionality.

"""
import math
import tkinter.font as fnt
from tkinter import *
from tkinter.messagebox import showinfo
import warnings
import random
from game import Game
from agent import Qlearner, SARSAlearner, DQN
import pickle

#Removes all the warning from the output
warnings.filterwarnings('ignore')
 
root=Tk()



 
# List of all possible numbers on the board, 5x5 grid = 25 
numbers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
numbers_orig = list(numbers)

# Track wins
player1_wins = 0
player2_wins = 0

# Friend and Computer Play
computer_play = 0

# y='X' for player1 and 'O' for player2
y=""
# x is the counter to keep counting the number of chances
# Start at zero to start with first player of 'X'
x=0

#boards is a list to store the mark with respect to the cell number
boards=["board"]*26
 
def result(boards,mark):
    return (
        # horizontal
               (boards[1] == boards[2] == boards [3] == boards[4] == boards[5] ==  mark) 
            or (boards[6] == boards[7] == boards [8] == boards[9] == boards[10] == mark) 
            or (boards[11] == boards[12] == boards [13] == boards[14] == boards[15] == mark) 
            or (boards[16] == boards[17] == boards [18] == boards[19] == boards[20] == mark) 
            or (boards[21] == boards[22] == boards [23] == boards[24] == boards[25] == mark) 
        # verticle
            or (boards[1] == boards[6] == boards [11] == boards[16] == boards[21] ==  mark) 
            or (boards[2] == boards[7] == boards [12] == boards[17] == boards[22] == mark) 
            or (boards[3] == boards[8] == boards [13] == boards[18] == boards[23] == mark) 
            or (boards[4] == boards[9] == boards [14] == boards[19] == boards[24] == mark) 
            or (boards[5] == boards[10] == boards [25] == boards[20] == boards[25] == mark) 
        # diaganal
            or (boards[1] == boards[7] == boards [13] == boards[19] == boards[25] ==  mark) 
            or (boards[5] == boards[9] == boards [13] == boards[17] == boards[21] == mark) 

    )
 


helv36 = fnt.Font( weight=fnt.BOLD)

l1=Label(root,text="player1(0): X",font="times 15")
l1.grid(row=0,column=1)
 
 
l2=Label(root,text="player2(0): O",font="times 15")
l2.grid(row=0,column=2)

def update_wins():
    global l1,l2, player1_wins, player2_wins
    xVal = "player1(" + str(player1_wins) + "): X"
    yVal = "player2(" + str(player2_wins) + "): Y"
    l1.config(text=xVal)
    l2.config(text=yVal)
    return


def define_sign(number):
    global x,y,numbers, player2_wins, player1_wins

    """ Checking which button has been clicked and checking if the button has been already clicked or not to avoid over-writing"""
    if number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        button_grid_list[number-1].config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            player1_wins+=1
            update_wins()
            showinfo("Result","Player1 wins")

            return
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            player2_wins+=1
            update_wins()
            showinfo("Result","Player2 wins")

            return
            
        # If we have not got any winner, display the dialogbox stating the match has bee tied.
        if(x>24 and result(boards,'X')==False and result(boards,'O')==False):
            showinfo("Result","Match Tied")
            return

    # Execute play if computer player is active
    if (computer_play == 1):
        random_num = random.choice(numbers)
        if x%2==0:
            y='X'
            boards[random_num]=y
 
        elif x%2!=0:
            y='O'
            boards[random_num]=y
                
        button_grid_list[random_num-1].config(text=y)
        x=x+1
        mark=y

        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            player1_wins+=1
            showinfo("Result","Player1 wins")
            return
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            player2_wins+=1
            showinfo("Result","Player2 wins")
            return

        # If we have not got any winner, display the dialogbox stating the match has bee tied.
        if(x>24 and result(boards,'X')==False and result(boards,'O')==False):
            showinfo("Result","Match Tied")
            return
         
 
 

 

def destroys():
    # destroys the window when called
    root.destroy()

# construct the 5x5 grid:  I tried to put this into a loop, but ran into problems.  Should revisit later.
# Got every button added in a loop with the same command iwth value of the max button number (i.e. 25 for a 5x5 grid)
b1=Button(root,width=20,height=10,command=lambda:define_sign(1))
b2=Button(root,width=20,height=10,command=lambda:define_sign(2))
b3=Button(root,width=20,height=10,command=lambda: define_sign(3))
b4=Button(root,width=20,height=10,command=lambda: define_sign(4))
b5=Button(root,width=20,height=10,command=lambda: define_sign(5))
b6=Button(root,width=20,height=10,command=lambda: define_sign(6))
b7=Button(root,width=20,height=10,command=lambda: define_sign(7))
b8=Button(root,width=20,height=10,command=lambda: define_sign(8))
b9=Button(root,width=20,height=10,command=lambda: define_sign(9))
b10=Button(root,width=20,height=10,command=lambda: define_sign(10))
b11=Button(root,width=20,height=10,command=lambda: define_sign(11))
b12=Button(root,width=20,height=10,command=lambda: define_sign(12))
b13=Button(root,width=20,height=10,command=lambda: define_sign(13))
b14=Button(root,width=20,height=10,command=lambda: define_sign(14))
b15=Button(root,width=20,height=10,command=lambda: define_sign(15))
b16=Button(root,width=20,height=10,command=lambda: define_sign(16))
b17=Button(root,width=20,height=10,command=lambda: define_sign(17))
b18=Button(root,width=20,height=10,command=lambda: define_sign(18))
b19=Button(root,width=20,height=10,command=lambda: define_sign(19))
b20=Button(root,width=20,height=10,command=lambda: define_sign(20))
b21=Button(root,width=20,height=10,command=lambda: define_sign(21))
b22=Button(root,width=20,height=10,command=lambda: define_sign(22))
b23=Button(root,width=20,height=10,command=lambda: define_sign(23))
b24=Button(root,width=20,height=10,command=lambda: define_sign(24))
b25=Button(root,width=20,height=10,command=lambda: define_sign(25))

button_grid_list = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25]
num_rows=5
num_cols=5
# place the buttons onto the grid
for i in range(25):
    row=math.ceil((i+1)/num_cols)
    col=(i+1)%num_cols
    if (col == 0):
        col = num_cols
    button_grid_list.append('b'+str(i+1))
    button_grid_list[i].grid(row=row, column=col)

#  Add menu bar, menus and action buttons
bNewSingle=Button(root,width=15,height=1,command=lambda:play_computer())
bNewSingle.grid(row=0,column=3)
bNewSingle.config(text="Play Computer")

bNewFriend=Button(root,width=15,height=1,command=lambda:play_friend())
bNewFriend.grid(row=0,column=4)
bNewFriend.config(text="Play Friend")

#  methods for the menus
def donothing():
    return

def about():
    showinfo("About","Machine Learning 5x5 Tic Toc Toe Game.\nLast Update:  Nov 2021.")
    return

def clear_board():
    global numbers, x, numbers_orig
    numbers = list(numbers_orig)
    x=0
    y=''
    for i in range(25):
        boards[i] = ' '
        button_grid_list[i].config(text='')
    return

agent = ""
def load_agent():
    global agent
    try:
        f = open('../qlearner_agent.pkl', 'rb')
        agent = pickle.load(f)
        f.close() 
    except IOError:
        print("The agent file does not exist. Quitting.")
        exit(1)

def play_computer():
    global computer_play
    computer_play = 1
    clear_board()
    return

def play_friend():
    global computer_play
    computer_play = 0
    clear_board()
    return

menubar = Menu(root)
actionmenu = Menu(menubar, tearoff=0)
actionmenu.add_command(label="Play Computer", command=play_computer)
actionmenu.add_command(label="Play Friend", command=play_friend)
actionmenu.add_separator()
actionmenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Action", menu=actionmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.title("Tic Tac Toe 5x5 ML")

def ask_player():
   global player
   player = Toplevel(root)
   player.title("Choose play mode:");
   player.geometry("200x100")
   player.grab_set()
   Button(player, text="Single Player", command= lambda:player_mode(1)).pack(pady=5, side=TOP)
   Button(player, text="Two Player", command= lambda:player_mode(0)).pack(pady=5, side=TOP)
   return

def player_mode(player_mode):
    player.destroy()
    return

#ask_player()

# load the agent
load_agent()

# Run the loop
root.mainloop()