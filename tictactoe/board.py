"""
Original code for a 3x3 board game taken from https://www.pythonpool.com/tic-tac-toe-python/
and modified into a 5x5 grid game.

"""
from tkinter import *
from tkinter.messagebox import showinfo
import warnings
 
#Removes all the warning from the output
warnings.filterwarnings('ignore')
 
root=Tk()
 
# List of all possible numbers on the board, 5x5 grid = 25 
numbers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] 
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
    """ Checking which button has been clicked and checking if the button has been already clicked or not to avoid over-writing"""
    if number==1 and number in numbers:
        numbers.remove(number)
        
        # If the value of x is even, Person1 will play and vivee versa
        if x%2==0:
            y='X'
            boards[number]=y
        elif x%2!=0:
            y='O'
            boards[number]=y
        #Using config, we write mark the button with appropriate value. 
        b1.config(text=y)
        x=x+1
        mark=y
        # Here we are calling the result() to decide whether we have got the winner or not
        if(result(boards,mark) and mark=='X' ):
            #If Player1 is the winner show a dialog box stating the winner
            showinfo("Result","Player1 wins")
            #Call the destroy function to close the GUI
            destroys()
        elif(result(boards,mark) and mark=='O'):
            showinfo("Result","Player2 wins")
            destroys()
         
    if number==2 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b2.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark)and mark=='X' ):
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark)and mark=='O' ):
            showinfo("Reuslt","Player2 wins")
            destroys()
         
    if number==3 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y    
        b3.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark)and mark=='X'):
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            showinfo("Result","Player2 wins")
            destroys()
         
    if number==4 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
         
        elif x%2!=0:
            y='O'
            boards[number]=y  
        b4.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark)and mark=='X'):
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            showinfo("Result","Player2 wins")
            destroys()
         
    if number==5 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
        elif x%2!=0:
            y='O'
            boards[number]=y
                        
        b5.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark)and mark=='X' ):
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,"O")and mark=='O'):
            showinfo("Result","Player2 wins")
            destroys()
         
    if number==6 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
        elif x%2!=0:
            y='O'
            boards[number]=y
 
        b6.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark)and mark=='O'):
            showinfo("Result","Player2 wins")
            destroys()
         
    if number==7 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
 
        b7.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X' ):
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()
         
    if number==8 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b8.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,"O")and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==9 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b9.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()      

    if number==10 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b10.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==11 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b11.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==12 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b12.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==13 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b13.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==14 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b14.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==15 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b15.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==16 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b16.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==17 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b17.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==18 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b18.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==19 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b19.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==20 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b20.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==21 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b21.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==22 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b22.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==23 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b23.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==24 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b24.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()

    if number==25 and number in numbers:
        numbers.remove(number)
        if x%2==0:
            y='X'
            boards[number]=y
 
        elif x%2!=0:
            y='O'
            boards[number]=y
             
        b25.config(text=y)
        x=x+1
        mark=y
        if(result(boards,mark) and mark=='X'):
            print("Player1 wins")
            showinfo("Result","Player1 wins")
            destroys()
        elif(result(boards,mark) and mark=='O'):
            print("Player2 wins")
            showinfo("Result","Player2 wins")
            destroys()
            
    # If we have not got any winner, display the dialogbox stating the match has bee tied.
    if(x>24 and result(boards,'X')==False and result(boards,'O')==False):
        showinfo("Result","Match Tied")
        destroys()
         
 
 
label1=Label(root,text="player1 : X",font="times 15")
label1.grid(row=0,column=1)
 
 
l2=Label(root,text="player2 : O",font="times 15")
l2.grid(row=0,column=2)
 
 
def destroys():
    # destroys the window when called
    root.destroy()
 

# construct the 5x5 grid
b1=Button(root,width=20,height=10,command=lambda:define_sign(1))
b1.grid(row=1,column=1)
b2=Button(root,width=20,height=10,command=lambda:define_sign(2))
b2.grid(row=1,column=2)
b3=Button(root,width=20,height=10,command=lambda: define_sign(3))
b3.grid(row=1,column=3)
b4=Button(root,width=20,height=10,command=lambda: define_sign(4))
b4.grid(row=1,column=4)
b5=Button(root,width=20,height=10,command=lambda: define_sign(5))
b5.grid(row=1,column=5)
b6=Button(root,width=20,height=10,command=lambda: define_sign(6))
b6.grid(row=2,column=1)
b7=Button(root,width=20,height=10,command=lambda: define_sign(7))
b7.grid(row=2,column=2)
b8=Button(root,width=20,height=10,command=lambda: define_sign(8))
b8.grid(row=2,column=3)
b9=Button(root,width=20,height=10,command=lambda: define_sign(9))
b9.grid(row=2,column=4)
b10=Button(root,width=20,height=10,command=lambda: define_sign(10))
b10.grid(row=2,column=5)
b11=Button(root,width=20,height=10,command=lambda: define_sign(11))
b11.grid(row=3,column=1)
b12=Button(root,width=20,height=10,command=lambda: define_sign(12))
b12.grid(row=3,column=2)
b13=Button(root,width=20,height=10,command=lambda: define_sign(13))
b13.grid(row=3,column=3)
b14=Button(root,width=20,height=10,command=lambda: define_sign(14))
b14.grid(row=3,column=4)
b15=Button(root,width=20,height=10,command=lambda: define_sign(15))
b15.grid(row=3,column=5)
b16=Button(root,width=20,height=10,command=lambda: define_sign(16))
b16.grid(row=4,column=1)
b17=Button(root,width=20,height=10,command=lambda: define_sign(17))
b17.grid(row=4,column=2)
b18=Button(root,width=20,height=10,command=lambda: define_sign(18))
b18.grid(row=4,column=3)
b19=Button(root,width=20,height=10,command=lambda: define_sign(19))
b19.grid(row=4,column=4)
b20=Button(root,width=20,height=10,command=lambda: define_sign(20))
b20.grid(row=4,column=5)
b21=Button(root,width=20,height=10,command=lambda: define_sign(21))
b21.grid(row=5,column=1)
b22=Button(root,width=20,height=10,command=lambda: define_sign(22))
b22.grid(row=5,column=2)
b23=Button(root,width=20,height=10,command=lambda: define_sign(23))
b23.grid(row=5,column=3)
b24=Button(root,width=20,height=10,command=lambda: define_sign(24))
b24.grid(row=5,column=4)
b25=Button(root,width=20,height=10,command=lambda: define_sign(25))
b25.grid(row=5,column=5)


#  Add menu bar
def donothing():
    return

#  Add menu bar
def about():
    showinfo("About","Machine Learning 5x5 Tic Toc Toe Game.\nLast Update:  Nov 2021.")
    return

menubar = Menu(root)
actionmenu = Menu(menubar, tearoff=0)
actionmenu.add_command(label="New Game", command=donothing)
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