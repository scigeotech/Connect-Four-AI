import numpy as np

#game settings (can change later)
ROW_COUNT = 6 #default 6
COLUMN_COUNT = 7 #default 7
#piece number
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
#for "windowing" the board
WINDOW_LENGTH = 4

#board functions
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int) #empty integer board (default is float; this is more convenient)
    return board

def valid_move(board, col):
    return board[ROW_COUNT - 1][col] == 0 #if the top row of the column is empty, then it's a valid location

def get_valid_moves(board):
    valid_moves = [] #possible moves
    for col in range(COLUMN_COUNT): #find columns with empty rows
        if valid_move(board, col):
            valid_moves.append(col) #this is a possible move, add to list
    return valid_moves

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0: #if the row is empty, return it
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece #drop the piece in the board

# board scanning
def evaluate_window(window, piece): #how useful is the scanned area?
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4: #if the window has 4 of the same piece, it wins
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1: #if the window has 3 of the same piece, it's a good move
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2: #if the window has 2 of the same piece, it's a decent move
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1: #if the opponent has 3 of the same piece, it must be blocked
        score -= 4
    #note that |score +=5| > |score -=4| because it's more important to win than to block the opponent from winning
    #in other cases, the opponent must be blocked first
    return score

def score_position(board, piece): #score the board based on how good the position is for the piece
    score = 0
    #score center column
    center_array = list(board[:, COLUMN_COUNT // 2]) #get the center column as a list
    #count how many of this piece are in the center column
    score += center_array.count(piece) * 3 #the more pieces in the center column, the better

    #divide board into windows for scanning and focus
    for r in range(ROW_COUNT): # horizontal
        row_array = list(board[r, :]) #get the row as a list
        for c in range(COLUMN_COUNT - 3): #divide the row into windows of 4 (note the -3 since it can't go over the side edge)
            window = row_array[c:c + WINDOW_LENGTH] #get the window
            score += evaluate_window(window, piece) #evaluate the window and add to score

    for c in range(COLUMN_COUNT): # vertical
        col_array = list(board[:, c]) #get the column as a list
        for r in range(ROW_COUNT - 3): #divide the column into windows of 4 (note the -3 since it can't go over the top edge)
            window = col_array[r:r + WINDOW_LENGTH] #get the window
            score += evaluate_window(window, piece) #evaluate the window and add to score

    for r in range(ROW_COUNT - 3): # (positive sloped diagonal)
        for c in range(COLUMN_COUNT - 3): #note both row/column are -3 since diagonal has both prior limitations
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)] #get the window as a list
            score += evaluate_window(window, piece) #evaluate the window and add to score

    for r in range(ROW_COUNT - 3): # (negative sloped diagonal)
        for c in range(COLUMN_COUNT - 3): #note both row/column are -3 since diagonal has both prior limitations
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)] #get the window as a list
            score += evaluate_window(window, piece) #evaluate the window and add to score

    return score

def winning_move(board, piece): #check from piece position
    for c in range(COLUMN_COUNT - 3): #check horizontal locations for win
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT): #check vertical locations for win
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    
    for c in range(COLUMN_COUNT - 3): #check positively sloped diagonals
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    
    for c in range(COLUMN_COUNT - 3): #check negatively sloped diagonals
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def is_terminal_node(board): #if either wins, or if no more valid moves (tie)
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_moves(board)) == 0
