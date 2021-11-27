"""
Original code for a 3x3 board game taken from https://www.pythonpool.com/tic-tac-toe-python/
and modified into a 5x5 grid game.

"""
import math
from tkinter import *
from tkinter.messagebox import showinfo
import warnings
 
#Removes all the warning from the output
warnings.filterwarnings('ignore')
 
root=Tk()
 
# List of all possible numbers on the board, 5x5 grid = 25 
numbers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
numbers_orig = numbers

# y='X' for player1 and 'O' for player2
y=""
# x is the counter to keep counting the number of chances
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
 
 
def define_sign(number):
    global x,y,numbers

    print(str(number))
    print(str(numbers))
    """ Checking which button has been clicked and checking if the button has been already clicked or not to avoid over-writing"""
    if number in numbers:
      #  numbers.remove(number)
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
            showinfo("Result","Player1 wins")
            return
            #destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            return
            #destroys()
            
    # If we have not got any winner, display the dialogbox stating the match has bee tied.
    if(x>24 and result(boards,'X')==False and result(boards,'O')==False):
        showinfo("Result","Match Tied")
        return
        #destroys()
         
 
 
label1=Label(root,text="player1 : X",font="times 15")
label1.grid(row=0,column=1)
 
 
l2=Label(root,text="player2 : O",font="times 15")
l2.grid(row=0,column=2)
 
 
def destroys():
    # destroys the window when called
    root.destroy()
 

# construct the 5x5 grid



# construct the 5x5 grid
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

for i in range(25):
    row=math.ceil((i+1)/num_cols)
    col=(i+1)%num_cols
    if (col == 0):
        col = num_cols
    button_grid_list.append('b'+str(i+1))
    button_grid_list[i].grid(row=row, column=col)

#  Add menu bar
def donothing():
    return

bNew=Button(root,width=15,height=1,command=lambda:newgame())
bNew.grid(row=0,column=3)
bNew.config(text="New Game")

#  methods for the menus
def about():
    showinfo("About","Machine Learning 5x5 Tic Toc Toe Game.\nLast Update:  Nov 2021.")
    return

def clear_board():
    numbers = numbers_orig
    x=0
    for i in range(25):
        boards[i] = ' '
        button_grid_list[i].config(text='')
    return



def newgame():
    clear_board()
    return

menubar = Menu(root)
actionmenu = Menu(menubar, tearoff=0)
actionmenu.add_command(label="New Game", command=newgame)
actionmenu.add_separator()
actionmenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Action", menu=actionmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)
root.title("Tic Tac Toe 5x5 ML")
# Run the loop
root.mainloop()