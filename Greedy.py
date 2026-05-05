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
