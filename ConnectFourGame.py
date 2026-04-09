import pygame
import pygame_widgets
from pygame_widgets.dropdown import Dropdown #for the dropdown menu
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
algorithm = str() #empty for now, picked in start menu

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

def start_menu():
    global algorithm
    menu_running = True
    font_title = pygame.font.SysFont("monospace", 80)
    font_small = pygame.font.SysFont("monospace", 40)
    dropdown = Dropdown(
    screen, 120, height // 2, 250, 50,
    name='Select Algorithm',
    choices=[
        'Minimax',
        'Minimax with Alpha-Beta Pruning',
        'Random'
    ],
    borderRadius=3, colour=pygame.Color('aquamarine'), direction='down',
    textHAlign='centre' #breaks if you spell it as "center", watch out!
    )

    while menu_running:
        screen.fill(BLACK)
        title = font_title.render("Connect Four", True, YELLOW)
        screen.blit(title, (width // 2 - title.get_width() // 2, 100))
        text = font_small.render("Press ENTER to Start", True, YELLOW)
        screen.blit(text, (width // 2 - text.get_width() // 2, height - 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and dropdown.getSelected() is not None: #only start if an algorithm is selected
                    algorithm = dropdown.getSelected()
                    menu_running = False
        dropdown.draw()
        pygame_widgets.update(pygame.event.get()) #update the dropdown state
        pygame.display.update()

def match_algorithm(insert_algorithm):
    algorithm_score = 0
    match insert_algorithm:
        case "Minimax":
            timer_start = pygame.time.get_ticks() #for timing the AI's move
            column, algorithm_score = minimax(board, DEPTH, True) #get the best move from the minimax algorithm
            timer_end = pygame.time.get_ticks()
            elapsed = timer_end - timer_start
        case "Minimax with Alpha-Beta Pruning":
            timer_start = pygame.time.get_ticks() #for timing the AI's move
            column, algorithm_score = minimax_pruned(board, DEPTH, -math.inf, math.inf, True) #get the best move from the minimax algorithm
            timer_end = pygame.time.get_ticks()
            elapsed = timer_end - timer_start
        case _: #default is alpha-beta for now
            timer_start = pygame.time.get_ticks() #for timing the AI's move
            column, algorithm_score = minimax_pruned(board, DEPTH, -math.inf, math.inf, True) #get the best move from the minimax algorithm
            timer_end = pygame.time.get_ticks()
            elapsed = timer_end - timer_start
    return column, algorithm_score, elapsed

def reset_game():
    board_clear = create_board()
    move_record_clear = [] #record the moves made (columns)
    turn_clear = PLAYER
    finish_clear = False
    return board_clear, move_record_clear, turn_clear, finish_clear

# pygame setup
pygame.init()
#build screen
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
screen = pygame.display.set_mode((width, height))
#"start" game variables
clock = pygame.time.Clock()

start_menu() #show the start menu before starting the game
board, move_record, turn, finish = reset_game() #initialize with a reset
draw_board(board)
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
            column, algorithm_score, elapsed = match_algorithm(algorithm)
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
            print("Press enter to play again, or any other key to quit (you can also just close the window).")
            waiting_for_input = True #NOTE: put a win/loss indicator so user doesn't have to check console
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting_for_input = False
                        finish = True
                    if event.type == pygame.KEYDOWN:
                        waiting_for_input = False
                        if event.key == pygame.K_RETURN:
                            board, move_record, turn, finish = reset_game() #reset game variables
                            draw_board(board) #update game state
                        else:
                            finish = True
            

pygame.quit()