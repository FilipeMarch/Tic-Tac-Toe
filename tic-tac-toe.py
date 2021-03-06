from Tkinter import *
import tkMessageBox
root = None
count = 0
sym = ""
frames = []
buttons = []
result = None

def create_frames(root):
    """
    This function creates the necessary structure of the game.
    """
    global buttons
    frame1=Frame(root)
    frame2=Frame(root)
    frame3=Frame(root)
    frame4=Frame(root)
    create_buttons(frame1)
    create_buttons(frame2)
    create_buttons(frame3)
    buttonExit = Button(frame4, height=1, width=2, text="Exit",command=lambda: exit_game(root))
    buttonExit.pack(side=LEFT)
    frame4.pack(side=BOTTOM)
    frame3.pack(side=BOTTOM)
    frame2.pack(side=BOTTOM)
    frame1.pack(side=BOTTOM)
    frames.append(frame1)
    frames.append(frame2)
    frames.append(frame3)  # Here is the frames array!
    for x in frames:
        buttons_in_frame=[]
        for y in x.winfo_children():
            buttons_in_frame.append(y)
        buttons.append(buttons_in_frame)    
    #print buttons    
    buttonReset = Button(frame4, height=1, width=2, text="Reset",command=lambda: reset_game())
    buttonReset.pack(side=LEFT)
    
def create_buttons(frame):
    """
    This function creates the buttons to be pressed/clicked during the game.
    """
    button0=Button(frame,height=2,width=2,text=" ",command=lambda:on_click(button0))
    button0.pack(side=LEFT)
    button1 = Button(frame, height=2, width=2, text=" ",command=lambda: on_click(button1))
    button1.pack(side=LEFT)
    button2 = Button(frame, height=2, width=2, text=" ",command=lambda: on_click(button2))
    button2.pack(side=LEFT)

def on_click(button):
    """
    This function determines the action of any button.
    """
    global count
    global sym
    global result
    if count%2==0:
        sym="X"       
    else:
        sym="O"
    count+=1
    button.config(text=sym,state='disabled',disabledforeground="red")

    board=calculate_board()
    #print board
    if board.count('X') != board.count('O') and board.count('X') + board.count('O') != 9:
        #import time
        #start=time.time()
        a,b = nextMove(board,"O")
        #print str(time.time()-start)
        button_to_change=get_button(b/3,b%3)
        if count%2==0:
            sym="X"
        else:
            sym="O"
        count+=1
        button_to_change.config(text=sym,state='disabled',disabledforeground="black")
    #print calculate_board()
    
    if check_victory(button) == True:
        result.set("You win :)")
        disable_game()
    elif board.count('X') + board.count('O') == 9:
        result.set("It's a draw :|")
        disable_game()
    elif check_victory(button_to_change) == True:
        result.set("You lose :(")
        disable_game()

def reset_game():
    """
    This function will reset all the tiles to the initial null value.
    """
    global frames
    global count
    count=0
    result.set("Your Turn First!")
    for x in frames:
        for y in x.winfo_children():
            y.config(text=" ",state='normal')

def disable_game():
    """
    This function deactivates the game after a win, loss or draw.
    """
    global frames
    for x in frames:
        for y in x.winfo_children():
            y.config(state='disabled')


def exit_game(root):
    """
    This function will exit the game by killing the root.
    """
    root.destroy()


def check_victory(button):
    """
    This function checks various winning conditions of the game.
    """
    #check if previous move caused a win on vertical line
    global buttons
    x,y=get_coordinates(button)
    tt=button['text']
    if buttons[0][y]['text'] == buttons[1][y]['text'] == buttons[2][y]['text'] != " ":
        buttons[0][y].config(text="|"+tt+"|")
        buttons[1][y].config(text="|" + tt + "|")
        buttons[2][y].config(text="|" + tt + "|")
        return True

    #check if previous move caused a win on horizontal line
    if buttons[x][0]['text'] == buttons[x][1]['text'] == buttons[x][2]['text'] != " ":
        buttons[x][0].config(text="--" + tt + "--")
        buttons[x][1].config(text="--" + tt + "--")
        buttons[x][2].config(text="--" + tt + "--")
        return True

    #check if previous move was on the main diagonal and caused a win
    if x == y and buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != " ":
        buttons[0][0].config(text="\\" + tt + "\\")
        buttons[1][1].config(text="\\" + tt + "\\")
        buttons[2][2].config(text="\\" + tt + "\\")
        return True

    #check if previous move was on the secondary diagonal and caused a win
    if x + y == 2 and buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != " ":
        buttons[0][2].config(text="/" + tt + "/")
        buttons[1][1].config(text="/" + tt + "/")
        buttons[2][0].config(text="/" + tt + "/")
        return True

    return False

def get_coordinates(button):
    """
    This function returns the coordinates of the button clicked.
    """
    global buttons
    for x in range(len(buttons)):
        for y in range(len(buttons[x])):
            if buttons[x][y]==button:
                #print x,y
                return x,y

def get_button(x,y):
    """
    This function returns the button memory location corresponding to a coordinate.
    """
    global buttons
    return buttons[x][y]

def calculate_board():
   # global board
    global buttons
    board=[]
    for x in range(len(buttons)):
        for y in range(len(buttons[x])):
            if buttons[x][y]['text']!=" ":
                board.append(buttons[x][y]['text'])
            else:
                board.append("-")
    return board    



### modified minimax algorithm
def isWin(board):
    """
    Given a board checks if it is in a winning state.

    Arguments:
          board: a list containing X,O or -.

    Return Value:
           True if board in winning state. Else False
    """
    ### check if any of the rows has winning combination
    for i in range(3):
        if len(set(board[i * 3:i * 3 + 3])) is 1 and board[i * 3] is not '-':
            return True
    ### check if any of the Columns has winning combination
    for i in range(3):
       if (board[i] is board[i + 3]) and (board[i] is board[i + 6]) and board[i] is not '-':
           return True
    ### 2,4,6 and 0,4,8 cases
    if board[0] is board[4] and board[4] is board[8] and board[4] is not '-':
        return True
    if board[2] is board[4] and board[4] is board[6] and board[4] is not '-':
        return True
    return False


def nextMove(board, player):
    """
    Computes the next move for a player given the current board state and also
    computes if the player will win or not.

    Arguments:
        board: list containing X,- and O
        player: one character string 'X' or 'O'

    Return Value:
        willwin: 1 if 'X' is in winning state, 0 if the game is draw and -1 if 'O' is
                    winning
        nextmove: position where the player can play the next move so that the
                         player wins or draws or delays the loss
    """
    ### when board is '---------' evaluating next move takes some time since
    ### the tree has 9! nodes. But it is clear in that state, the result is a draw.

    if len(set(board)) == 1:
        #print "set board"
        return 0, 4

    nextplayer = 'X' if player == 'O' else 'O'
    if isWin(board):
        #print "iswin"
        if player is 'X':
            return -1, -1
        else:
            return 1, -1
    res_list = []  # list for appending the result
    c = board.count('-')
    if c is 0:
        return 0, -1
    _list = []  # list for storing the indexes where '-' appears
    for i in range(len(board)):
        if board[i] == '-':
            _list.append(i)
    #tempboardlist=list(board)
    for i in _list:
        board[i] = player
        ret, move = nextMove(board, nextplayer)
        res_list.append(ret)
        board[i] = '-'
    if player is 'X':
        maxele = max(res_list)
        return maxele, _list[res_list.index(maxele)]
    else:
        minele = min(res_list)
        return minele, _list[res_list.index(minele)]


def main():
    global result
    root=Tk()
    root.title("Tic-Tac-Toe")
    result=StringVar()
    result.set("Your Turn First!")
    w = Label(root, textvariable=result)
    w.pack(side=BOTTOM)
    create_frames(root)
    root.mainloop()

if __name__=='__main__':
    main()    
