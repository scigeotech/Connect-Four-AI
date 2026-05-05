from Board import *
import math
import random

def negamax(board, depth, color): #instead of boolean, maximizingPlayer turns to 1 (max) or -1 (min)
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if color == 1:
        piece = AI_PIECE
    else:
        piece = PLAYER_PIECE
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE): #high score for bot winning
                return (None, color * 123456789)
            elif winning_move(board, PLAYER_PIECE): #low score for human winning
                return (None, color * -123456789)
            else: #no more valid moves (tie)
                return (None, 0)
        else: #depth == zero
            return (None, color * score_position(board, AI_PIECE))
    negamax_score = -math.inf
    column = random.choice(valid_moves)
    for col in valid_moves:
        board_copy = board.copy()
        drop_piece(board_copy, get_next_open_row(board_copy, col), col, piece)
        new_score = -negamax(board_copy, depth - 1, -(color))[1]
        if new_score > negamax_score:
            negamax_score = new_score
            column = col
    return column, negamax_score

def negamax_pruned(board, depth, alpha, beta, color): #instead of boolean, maximizingPlayer turns to 1 (max) or -1 (min)
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if color == 1:
        piece = AI_PIECE
    else:
        piece = PLAYER_PIECE
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE): #high score for bot winning
                return (None, color * 123456789)
            elif winning_move(board, PLAYER_PIECE): #low score for human winning
                return (None, color * -123456789)
            else: #no more valid moves (tie)
                return (None, 0)
        else: #depth == zero
            return (None, color * score_position(board, AI_PIECE))
    negamax_score = -math.inf
    column = random.choice(valid_moves)
    for col in valid_moves:
        board_copy = board.copy()
        drop_piece(board_copy, get_next_open_row(board_copy, col), col, piece)
        new_score = -negamax_pruned(board_copy, depth - 1, -beta, -alpha, -color)[1]
        if new_score > negamax_score:
            negamax_score = new_score
            column = col
        alpha = max(alpha, new_score)
        if alpha >= beta:
            break
    return column, negamax_score