from Board import *
import math
import random





def random_playout(board, turn):
    board_copy = board.copy()

    while not is_terminal_node(board_copy):
        valid_moves = get_valid_moves(board_copy)
        col = random.choice(valid_moves)
        row = get_next_open_row(board_copy, col)

        if turn == AI_PIECE:
            drop_piece(board_copy, row, col, AI_PIECE)
            turn = PLAYER_PIECE
        else:
            drop_piece(board_copy, row, col, PLAYER_PIECE)
            turn = AI_PIECE

    if winning_move(board_copy, AI_PIECE):
        return 1
    elif winning_move(board_copy, PLAYER_PIECE):
        return -1
    else:
        return 0
# ---------- Monte Carlo algorithm ----------
def monte_carlo_move(board, simulations):
    valid_moves = get_valid_moves(board)
    best_score = -math.inf
    best_col = random.choice(valid_moves)

    for col in valid_moves:
        score = 0

        for _ in range(simulations):
            board_copy = board.copy()
            row = get_next_open_row(board_copy, col)
            drop_piece(board_copy, row, col, AI_PIECE)

            result = random_playout(board_copy, PLAYER_PIECE)
            score += result

        if score > best_score:
            best_score = score
            best_col = col

    return best_col, best_score