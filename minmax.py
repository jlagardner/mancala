from random import randint

class random_evaluator():
    def evaluate(self,board):
        scores = [0]*board.LENGTH
        print(scores)
        move = randint(0,board.LENGTH - 1)
        while not board.valid_move(move):
            move = randint(0,board.LENGTH - 1)
        print(move)
        scores[move] = 1
        print("In evaluator : scores = ")
        print(scores)
        return scores


class min_max_evaluator():
    def __init__(self,win_reward,loss_reward,draw_reward,original_player_to_move):
        self.win_reward = win_reward
        self.loss_reward = loss_reward
        self.draw_reward = draw_reward
        self.original_player_to_move = original_player_to_move

    def evaluate(self,board, depth):
        scores = [0]*board.LENGTH
        if board.game_over():
            if board.winner == original_player_to_move:
                scores = [board.win_reward]
            elif board.winner != original_player_to_move:
                scores = [board.loss_reward]
            else:
                scores = [board.draw_reward]
        elif depth > 0:
            for move in range(board.LENGTH):
                new_board = board.__copy__()
                if new_board.valid_move(move) and not new_board.game_over():
                    new_board.set_move_to_make(move)
                    new_board.make_current_move()
                    new_board.update_current_player()
                    scores[move] = sum(self.evaluate(new_board, depth - 1))
        elif depth == 0:
            scores = [1]

        print(scores)
        return scores
