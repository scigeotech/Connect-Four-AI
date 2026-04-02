import pygame
from Board import * #get everything from board.py
#note: most board functions were separated into board.py
#so the AI algorithms can import from there instead of here
#otherwise they would be importing from each other
from Minimax import * 

DEPTH = 5 #how many moves ahead the minimax algorithm should look (default is 5)
#turn number
PLAYER = 0
AI = 1
#UI
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#board ui functions
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)) #draw blue background
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE * 3/2)), RADIUS) #draw empty circles

    for c in range(COLUMN_COUNT): # per column, then per row (climb up)
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE: #player is red
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE: #ai is yellow
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update() #new frame

def preview_move(event):
    column = int(event.pos[0] / SQUARESIZE) #get the column of the mouse
    xpos = int(column * SQUARESIZE + SQUARESIZE / 2) #x pos of the circle, with centering
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE)) #clear the top row
    pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE / 2)), RADIUS) #red circle at x pos of mouse
    pygame.display.update() #new frame

# pygame setup
board = create_board()
pygame.init()
#build screen
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
screen = pygame.display.set_mode((width, height))
draw_board(board)
#"start" game variables
clock = pygame.time.Clock()
finish = False
turn = PLAYER
move_record = [] #record the moves made (columns)

# main game process
while not finish:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

        if event.type == pygame.MOUSEMOTION and turn == PLAYER: #if the mouse moves, show the piece hovering above the board
            preview_move(event)

        if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER: #when lmb clicked, drop the piece
            column = int(event.pos[0] / SQUARESIZE)
            if valid_move(board, column):
                row = get_next_open_row(board, column) #top row of the column
                drop_piece(board, row, column, PLAYER_PIECE)
                print("Player dropped piece at row " + str(row) + ", column " + str(column))
                if winning_move(board, PLAYER_PIECE):
                    print("-----> Player wins!")
                    finish = True
                elif is_terminal_node(board):
                    print("It's a draw!")
                    finish = True
                else:
                    turn = AI 
                draw_board(board) #update game state
                move_record.append(column)

        if turn == AI and not finish:
            timer_start = pygame.time.get_ticks() #for timing the AI's move
            column, minimax_score = minimax_pruned(board, DEPTH, -math.inf, math.inf, True) #get the best move from the minimax algorithm
            timer_end = pygame.time.get_ticks()
            elapsed = timer_end - timer_start
            if valid_move(board, column):
                row = get_next_open_row(board, column) #top row of the column
                drop_piece(board, row, column, AI_PIECE)
                print("AI dropped piece at row " + str(row) + ", column " + str(column) + " (calculated in " + str(elapsed) + " ms" + " for depth " + str(DEPTH) + ")")
                if winning_move(board, AI_PIECE):
                    print("-----> AI wins!")
                    finish = True
                elif is_terminal_node(board):
                    print("It's a draw!")
                    finish = True
                else:
                    turn = PLAYER 
                draw_board(board) #update game state
                move_record.append(column)
        
        if finish:
            print("Game finished! Move record: " + str(move_record))
            pygame.time.wait(5000) #for staring at the screen
            

pygame.quit()