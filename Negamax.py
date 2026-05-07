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

#---------- optimized ----------
#it's only a few extra lines but i thought i should separate this too
def minimax_pruned_opt(board, depth, alpha, beta, piece): #just negamax
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    opp = get_opponent(piece)
    if depth == 0 or is_terminal: #can it be processed?
        if is_terminal:
            if winning_move(board, piece): #high score for winning
                return (None, 123456789)
            elif winning_move(board, opp): #low score for opponent winning
                return (None, -123456789)
            else: #no more valid moves (tie)
                return (None, 0)
        else: #depth == zero
            return (None, score_position(board, piece))
    
    minimax_score = -math.inf
    column = random.choice(valid_moves)
    for col in valid_moves:
        board_copy = board.copy()
        drop_piece(board_copy, get_next_open_row(board_copy, col), col, piece) #simulate dropping a piece
        new_score = -minimax_pruned_opt(board_copy, depth - 1, -beta, -alpha, opp)[1]
        if new_score > minimax_score:
            minimax_score = new_score
            column = col
        alpha = max(alpha, minimax_score)
        if alpha >= beta:
            break
    return column, minimax_score