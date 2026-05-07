from Board import *
import math
import random


def greedy_move(board, piece):
    valid_moves = get_valid_moves(board)
    best_score = -math.inf
    best_col = random.choice(valid_moves)

    for col in valid_moves:
        board_copy = board.copy()
        row = get_next_open_row(board_copy, col)
        drop_piece(board_copy, row, col, piece)

        score = score_position(board_copy, piece)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col, best_score

#----------las vegas algorithm----------
def las_vegas(board, piece): #similar but more unpredictable
    valid_moves = get_valid_moves(board)
    best_score = -math.inf
    best_columns = [] #list of highest columns

    for col in valid_moves:
        board_copy = board.copy()
        row = get_next_open_row(board_copy, col)
        drop_piece(board_copy, row, col, piece)

        if(winning_move(board_copy, piece)):
            return col, math.inf
        score = score_position(board_copy, piece)

        if score > best_score:
            best_score = score
            best_columns = [col] #new list of best columns
        elif score == best_score:
            best_columns.append(col)

    return random.choice(best_columns), best_score #return any best column to reduce predictability
