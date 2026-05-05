from Board import *
import math
import random

def minimax(board, depth, maximizingPlayer):
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal: #can it be processed?
        if is_terminal:
            if winning_move(board, AI_PIECE): #high score for bot winning
                return (None, 123456789)
            elif winning_move(board, PLAYER_PIECE): #low score for human winning
                return (None, -123456789)
            else: #no more valid moves (tie)
                return (None, 0)
        else: #depth == zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        minimax_score = -math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            board_copy = board.copy()
            drop_piece(board_copy, get_next_open_row(board_copy, col), col, AI_PIECE) #simulate dropping a piece
            new_score = minimax(board_copy, depth - 1, False)[1]
            if new_score > minimax_score:
                minimax_score = new_score
                column = col
        return column, minimax_score

    else: #minimize player
        minimax_score = math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            board_copy = board.copy()
            drop_piece(board_copy, get_next_open_row(board, col), col, PLAYER_PIECE) #simulate dropping a piece
            new_score = minimax(board_copy, depth - 1, True)[1]
            if new_score < minimax_score:
                minimax_score = new_score
                column = col
        return column, minimax_score

#----------minimax with alpha-beta pruning ----------
#it's only a few extra lines but i thought i should separate this too
def minimax_pruned(board, depth, alpha, beta, maximizingPlayer):
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal: #can it be processed?
        if is_terminal:
            if winning_move(board, AI_PIECE): #high score for bot winning
                return (None, 123456789)
            elif winning_move(board, PLAYER_PIECE): #low score for human winning
                return (None, -123456789)
            else: #no more valid moves (tie)
                return (None, 0)
        else: #depth == zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        minimax_score = -math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            board_copy = board.copy()
            drop_piece(board_copy, get_next_open_row(board_copy, col), col, AI_PIECE) #simulate dropping a piece
            new_score = minimax_pruned(board_copy, depth - 1, alpha, beta, False)[1]
            if new_score > minimax_score:
                minimax_score = new_score
                column = col
            alpha = max(alpha, minimax_score)
            if alpha >= beta:
                break
        return column, minimax_score

    else: #minimize player
        minimax_score = math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            board_copy = board.copy()
            drop_piece(board_copy, get_next_open_row(board, col), col, PLAYER_PIECE) #simulate dropping a piece
            new_score = minimax_pruned(board_copy, depth - 1, alpha, beta, True)[1]
            if new_score < minimax_score:
                minimax_score = new_score
                column = col
            beta = min(beta, minimax_score)
            if alpha >= beta:
                break
        return column, minimax_score

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


# ---------- simulation helper for Monte Carlo ----------
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
            turn = AI_PIECEs

    if winning_move(board_copy, AI_PIECE):
        return 1
    elif winning_move(board_copy, PLAYER_PIECE):
        return -1
    else:
        return 0
# ---------- Monte Carlo algorithm ----------
def monte_carlo_move(board, simulations=50):
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


