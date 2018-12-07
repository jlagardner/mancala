import Tkinter as tk
import math
from random import randint
import time


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 760
BLOCK_SIZE = 20
BOARD_LENGTH = 6
STARTING_STONES = 4
PLAYER_A = 0
PLAYER_B = 1
LOOP_SIZE = BOARD_LENGTH * 2 + 1
names={0:'Player A',1:'Player B'}
board = []
score = []
type_of_ = {0:'AI',1:'HUMAN'}



def draw_rectangle(centre_x,centre_y,width,height,colour):
    global canvas
    canvas.create_rectangle(centre_x - width/2, centre_y - height/2, centre_x + width/2, centre_y + height/2,fill=colour)

def setup_board():
    global board, score, current_player
    board = [[STARTING_STONES] * BOARD_LENGTH, [STARTING_STONES] * BOARD_LENGTH]
    score = [0,0]
    current_player = PLAYER_B
    draw_board()

def draw_label(x,y,txt):
    label = tk.Text(root, height=1,width=1,bg='grey',highlightbackground='grey')
    label.place(x=x-BLOCK_SIZE/2.7,y=y-BLOCK_SIZE/1.5)
    label.insert('1.0', txt)

def other_player():
    return (current_player+1)%2

def draw_board():
    global canvas, board
    draw_rectangle(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,WINDOW_WIDTH+20,WINDOW_HEIGHT+20,'white')
    draw_rectangle(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,BLOCK_SIZE*BOARD_LENGTH,3*BLOCK_SIZE,'grey')
    for a in range(BOARD_LENGTH):
        a_x = WINDOW_WIDTH/2 + BLOCK_SIZE*(BOARD_LENGTH - 1)/2 - a*BLOCK_SIZE
        a_y = WINDOW_HEIGHT/2 - 2*BLOCK_SIZE
        for counter in range(board[PLAYER_A][a]):
            draw_rectangle(a_x,a_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'white')
            a_y -= BLOCK_SIZE
    for b in range(BOARD_LENGTH):
        b_x = WINDOW_WIDTH/2 - BLOCK_SIZE*(BOARD_LENGTH - 1)/2 + b*BLOCK_SIZE
        b_y = WINDOW_HEIGHT/2 + 2*BLOCK_SIZE
        for counter in range(board[PLAYER_B][b]):
            draw_rectangle(b_x,b_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'white')
            b_y += BLOCK_SIZE
        t_y = WINDOW_HEIGHT/2 + BLOCK_SIZE
        draw_label(b_x, t_y, str(b))

    for i in range(score[PLAYER_B]):
        i_x = WINDOW_WIDTH/2 + BLOCK_SIZE*(BOARD_LENGTH+1)/2 + math.floor(i/3)*BLOCK_SIZE
        i_y = WINDOW_HEIGHT/2 + BLOCK_SIZE - (i%3)*BLOCK_SIZE
        draw_rectangle(i_x,i_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'red')
    for j in range(score[PLAYER_A]):
        j_x = WINDOW_WIDTH/2 - BLOCK_SIZE*(BOARD_LENGTH+1)/2 - math.floor(j/3)*BLOCK_SIZE
        j_y = WINDOW_HEIGHT/2 - BLOCK_SIZE + (j%3)*BLOCK_SIZE
        draw_rectangle(j_x,j_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'red')


def log_board():
    lines=['     Player A']
    line = ' '
    for pot in reversed(board[PLAYER_A]):
        line += ' ' + str(pot) + ' '
    lines.append(line)
    line = ''
    line = str(score[PLAYER_A]) + '   ' * BOARD_LENGTH + str(score[PLAYER_B])
    lines.append(line)
    line = ' '
    for pot in board[PLAYER_B]:
        line += ' ' + str(pot) + ' '
    lines.append(line)
    lines.append('     Player B')
    lines.append(' ')
    line = ' '
    if current_player == PLAYER_B:
        for i in range(BOARD_LENGTH):
            line += ' ' + str(i) + ' '
    else:
        for i in range(BOARD_LENGTH-1,-1,-1):
            line += ' ' + str(i) + ' '
    lines.append(line)
    for l in lines:
        print(l)

def no_winner():
    side_a_empty = all(pot == 0 for pot in board[PLAYER_A])
    side_b_empty = all(pot == 0 for pot in board[PLAYER_B])
    return not ( side_a_empty or side_b_empty )

def valid_move(move):
    return move >=0 and move < BOARD_LENGTH and board[current_player][move] > 0

def get_move():
    global move_from_pot, current_player
    print('--------------------')
    if type_of_[current_player] == 'HUMAN':
        pass
        #move_from_pot = int(input(names[current_player] + " to move: "))
        #while not valid_move(move_from_pot):
            #move_from_pot = int(input("[Inputs must be as above and non empty] : " +names[current_player] + " to move: "))
    else:
        move_from_pot = randint(0,BOARD_LENGTH-1)
        while not valid_move(move_from_pot):
            move_from_pot = randint(0,BOARD_LENGTH-1)
    print(names[current_player] + ' moves from: ' + str(move_from_pot))

def update_board():
    global into_pot
    into_pot = 0
    into_pot += move_from_pot
    counters_to_distribute = board[current_player][move_from_pot]
    board[current_player][move_from_pot] = 0
    while counters_to_distribute > 0:
        into_pot += 1
        if into_pot % LOOP_SIZE < BOARD_LENGTH:
            board[current_player][into_pot % LOOP_SIZE] += 1
        elif into_pot % LOOP_SIZE == BOARD_LENGTH:
            score[current_player] += 1
        elif into_pot % LOOP_SIZE > BOARD_LENGTH:
            board[other_player()][into_pot%LOOP_SIZE - BOARD_LENGTH -1] += 1
        counters_to_distribute -= 1
    if into_pot % LOOP_SIZE < BOARD_LENGTH:
        if board[current_player][into_pot%LOOP_SIZE] == 1:
            score[current_player] += board[other_player()][BOARD_LENGTH-1-into_pot % LOOP_SIZE]
            board[other_player()][BOARD_LENGTH-1-into_pot % LOOP_SIZE] = 0

def update_current_player():
    global current_player
    if turn_over():
        current_player = (current_player + 1)%2

def turn_over():
    return not into_pot % LOOP_SIZE == BOARD_LENGTH

def valid_click(event):
    global move_from_pot
    x = event.x
    y = event.y
    x_in_bounds = x > WINDOW_WIDTH/2 - BOARD_LENGTH*BLOCK_SIZE/2 or x < WINDOW_WIDTH/2 + BOARD_LENGTH*BLOCK_SIZE/2
    y_in_bounds = y > WINDOW_HEIGHT/2 + 1.5*BLOCK_SIZE
    if x_in_bounds and y_in_bounds:
        move = int(math.floor((x-WINDOW_WIDTH/2)/BLOCK_SIZE) + BOARD_LENGTH/2)
        if valid_move(move):
            move_from_pot = move
            return True
    return False

def choose_pot(event):
    if  no_winner() and valid_click(event):
        game_step()
        while type_of_[current_player] == 'AI':
            game_step()

def game_step():
    get_move()
    update_board()
    draw_board()
    log_board()
    update_current_player()




root=tk.Tk()
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()
root.title("Mancala")
setup_board()
draw_board()
log_board()
root.bind("<Button-1>", choose_pot)


root.mainloop()
