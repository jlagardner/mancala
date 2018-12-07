import Tkinter as tk
import math
from random import randint
import time


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 760
BLOCK_SIZE = 20

PLAYER_A = 0
PLAYER_B = 1
names={0:'Player A',1:'Player B'}


def draw_rectangle(centre_x,centre_y,width,height,colour):
    global canvas
    canvas.create_rectangle(centre_x - width/2, centre_y - height/2, centre_x + width/2, centre_y + height/2,fill=colour)

def draw_label(x,y,txt):
    label = tk.Text(root, height=1,width=1,bg='grey',highlightbackground='grey')
    label.place(x=x-BLOCK_SIZE/2.7,y=y-BLOCK_SIZE/1.5)
    label.insert('1.0', txt)

class Mancala_Board:
    def __init__(self, LENGTH=6, STARTING_STONES=4, current_player=PLAYER_B):
        self.LENGTH = LENGTH
        self.pots = [[STARTING_STONES] * LENGTH,[STARTING_STONES] * LENGTH]
        self.score = [0] * 2
        self.current_player = current_player
        self.passive_player = (current_player + 1)%2
        self.type_of_ = {PLAYER_A:'AI',PLAYER_B:'HUMAN'}

    def start_game(self):
        print('starting')
        self.draw()
        self.log()
        if self.type_of_[self.current_player] == "AI":
            self.get_AI_next_move(self)
            main_game.update_state_until_next_human_turn()

    def swap_players(self):
        print('swapping players')
        self.current_player = (self.current_player + 1)%2
        self.passive_player = (self.passive_player + 1)%2

    def log(self):
        print('logging')
        lines=['   ', '','     Player A']
        line = ' '
        for pot in reversed(self.pots[PLAYER_A]):
            line += ' ' + str(pot) + ' '
        lines.append(line)
        line = ''
        line = str(self.score[PLAYER_A]) + '   ' * self.LENGTH + str(self.score[PLAYER_B])
        lines.append(line)
        line = ' '
        for pot in self.pots[PLAYER_B]:
            line += ' ' + str(pot) + ' '
        lines.append(line)
        lines.append('     Player B')
        lines.append(' ')
        line = ' '

        lines.append(line)
        for l in lines:
            print(l)

    def draw(self):
        print('drawing')
        global canvas
        draw_rectangle(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,WINDOW_WIDTH+20,WINDOW_HEIGHT+20,'white')
        draw_rectangle(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,BLOCK_SIZE*self.LENGTH,3*BLOCK_SIZE,'grey')
        for a in range(self.LENGTH):
            a_x = WINDOW_WIDTH/2 + BLOCK_SIZE*(self.LENGTH - 1)/2 - a*BLOCK_SIZE
            a_y = WINDOW_HEIGHT/2 - 2*BLOCK_SIZE
            for counter in range(self.pots[PLAYER_A][a]):
                draw_rectangle(a_x,a_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'white')
                a_y -= BLOCK_SIZE
        for b in range(self.LENGTH):
            b_x = WINDOW_WIDTH/2 - BLOCK_SIZE*(self.LENGTH - 1)/2 + b*BLOCK_SIZE
            b_y = WINDOW_HEIGHT/2 + 2*BLOCK_SIZE
            for counter in range(self.pots[PLAYER_B][b]):
                draw_rectangle(b_x,b_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'white')
                b_y += BLOCK_SIZE
            t_y = WINDOW_HEIGHT/2 + BLOCK_SIZE
            draw_label(b_x, t_y, str(b))

        for i in range(self.score[PLAYER_B]):
            i_x = WINDOW_WIDTH/2 + BLOCK_SIZE*(self.LENGTH+1)/2 + math.floor(i/3)*BLOCK_SIZE
            i_y = WINDOW_HEIGHT/2 + BLOCK_SIZE - (i%3)*BLOCK_SIZE
            draw_rectangle(i_x,i_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'red')
        for j in range(self.score[PLAYER_A]):
            j_x = WINDOW_WIDTH/2 - BLOCK_SIZE*(self.LENGTH+1)/2 - math.floor(j/3)*BLOCK_SIZE
            j_y = WINDOW_HEIGHT/2 - BLOCK_SIZE + (j%3)*BLOCK_SIZE
            draw_rectangle(j_x,j_y,BLOCK_SIZE*0.8,BLOCK_SIZE*0.8,'red')

    def no_winner(self):
        side_a_empty = all(pot == 0 for pot in self.pots[PLAYER_A])
        side_b_empty = all(pot == 0 for pot in self.pots[PLAYER_B])
        print('determining if there is a winner : {}'.format(side_a_empty or side_b_empty))
        return not ( side_a_empty or side_b_empty )

    def valid_move(self,move):
        print('determining if valid move')
        if move >=0 and move < self.LENGTH and self.pots[self.current_player][move] > 0:
            self.move_from_pot = move
            return True
        return False

    def update_state_until_next_human_turn(self):
        print('updating state until next human turn')
        self.make_move()
        self.draw()
        self.log()
        if not self.no_winner():
            print('{} is the winner'.format(self.type_of_[self.current_player]))
        self.update_current_player()
        self.play_out_AI_turn()

    def play_out_AI_turn(self):
        print('playing out AI\'s turn : so far done nothing')
        while self.type_of_[self.current_player] == 'AI':
            print("AI turn again")
            get_AI_next_move(self)
            self.make_move()
            self.draw()
            self.log()
            if not self.no_winner():
                print('{} is the winner'.format(self.type_of_[self.current_player]))
            self.update_current_player()

    def update_current_player(self):
        print('checking if should swap players')
        turn_over = not self.last_pot_inserted_into == self.LENGTH
        if turn_over:
            self.swap_players()

    def make_move(self):
        print('making move of {} : {}'.format(self.type_of_[self.current_player],self.move_from_pot))
        self.last_pot_inserted_into = self.move_from_pot
        counters_to_distribute = self.pots[self.current_player][self.move_from_pot]
        self.pots[self.current_player][self.move_from_pot] = 0
        while counters_to_distribute > 0:
            self.log()
            self.last_pot_inserted_into = (self.last_pot_inserted_into + 1)%(self.LENGTH * 2 + 1)
            if self.last_pot_inserted_into < self.LENGTH:
                self.pots[self.current_player][self.last_pot_inserted_into] += 1
            elif self.last_pot_inserted_into == self.LENGTH:
                self.score[self.current_player] += 1
            elif self.last_pot_inserted_into > self.LENGTH:
                self.pots[self.passive_player][self.last_pot_inserted_into - self.LENGTH -1] += 1
            counters_to_distribute -= 1
        if self.last_pot_inserted_into < self.LENGTH:
            if self.pots[self.current_player][self.last_pot_inserted_into] == 1:
                self.score[self.current_player] += self.pots[self.passive_player][self.LENGTH-1-self.last_pot_inserted_into]
                self.pots[self.passive_player][self.LENGTH-1-self.last_pot_inserted_into] = 0



def get_AI_next_move(board):
    move = randint(0,board.LENGTH-1)
    while not board.valid_move(move):
        move = randint(0,board.LENGTH-1)

def valid_click(event,board):
    x = event.x
    y = event.y
    x_in_bounds = x > WINDOW_WIDTH/2 - board.LENGTH*BLOCK_SIZE/2 or x < WINDOW_WIDTH/2 + board.LENGTH*BLOCK_SIZE/2
    y_in_bounds = y > WINDOW_HEIGHT/2 + 1.5*BLOCK_SIZE
    if x_in_bounds and y_in_bounds:
        move = int(math.floor((x-WINDOW_WIDTH/2)/BLOCK_SIZE) + board.LENGTH/2)
        if board.valid_move(move):
            board.move_from_pot = move
            return True
    return False

def make_human_choice(event):
    global main_game
    if valid_click(event, main_game):
        main_game.update_state_until_next_human_turn()


root=tk.Tk()
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()
root.title("Mancala")
root.bind("<Button-1>", make_human_choice)

main_game = Mancala_Board()
main_game.start_game()


root.mainloop()
