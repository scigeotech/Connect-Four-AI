import pygame
import pygame_widgets
from pygame_widgets.dropdown import Dropdown #for the dropdown menu
from pygame_widgets.textbox import TextBox #for the optional textbox
from Board import * #get everything from board.py
#note: most board functions were separated into board.py
#so the AI algorithms can import from there instead of here
#otherwise they would be importing from each other
from Minimax import * 
from Negamax import *
from Greedy import *
from MonteCarlo import *

DEPTH = 5 #how many moves ahead the minimax algorithm should look (default is 5)
MONTE_CARLO_SIMULATIONS = 50 #how many random playouts the Monte Carlo algorithm should do per move (default is 50)
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
player_algorithm = "Human" #human or selected algorithm for player 1
ai_algorithm = str() #selected algorithm for AI
ai_versus_iterations = 1 #number of AI-vs-AI games when algorithm is not "human"
record = [0, 0, 0] #record of wins per adversary (player, ai, draw) in this session
player_decision_time_average = [0, 0] #total time and turns, so avg = time / turns
ai_decision_time_average = [0, 0] #total time and turns, so avg = time / turns

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
    global player_algorithm, ai_algorithm, ai_versus_iterations
    menu_running = True
    font_title = pygame.font.SysFont("monospace", 80)
    font_small = pygame.font.SysFont("monospace", 20)
    choices = [
        'Human',
        #'Minimax',
        'Minimax with Alpha-Beta Pruning',
        'Random',
        'Greedy',
        'Monte Carlo',
        #'Negamax',
        'Negamax with Alpha-Beta Pruning'
    ]
    
    textbox_iterations = TextBox(
        screen, width // 2 - 180, height // 2 + 20, 360, 50,
        borderThickness=3,
        borderColour=pygame.Color('white'),
        colour=pygame.Color('white'),
        textColour=BLACK,
        placeholderText='Number of games',
        placeholderTextColour=(100, 100, 100),
        fontSize=24
    )
    dropdown_player = Dropdown(
        screen, 50, height // 2 - 60, 320, 50,
        name='Player Algorithm',
        choices=choices,
        borderRadius=3, colour=pygame.Color('aquamarine'), direction='down',
        textHAlign='centre' #DO NOT MISSPELL AS "CENTER" OR IT WILL BREAKKK
    )
    dropdown_ai = Dropdown(
        screen, width - 370, height // 2 - 60, 320, 50,
        name='AI Algorithm',
        choices=choices[1:],
        borderRadius=3, colour=pygame.Color('aquamarine'), direction='down',
        textHAlign='centre'
    )
    textbox_iterations.hide() #only show if player selects AI for player algorithm

    while menu_running:
        events = pygame.event.get()
        screen.fill(BLACK)
        title = font_title.render("Connect Four", True, YELLOW)
        screen.blit(title, (width // 2 - title.get_width() // 2, 100))

        player_choice = dropdown_player.getSelected()
        prompt = "After selection, press Enter to start."
        if player_choice is not None and player_choice != 'Human':
            prompt = "Enter number of games for AI vs AI, then press Enter."
            textbox_iterations.show()
            label = font_small.render("Games:", True, YELLOW)
            screen.blit(label, (width // 2 - 260, height // 2 + 30))
            textbox_iterations.draw()
        else:
            textbox_iterations.hide()

        text = font_small.render(prompt, True, YELLOW)
        screen.blit(text, (width // 2 - text.get_width() // 2, height - 150))

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and dropdown_player.getSelected() is not None and dropdown_ai.getSelected() is not None:
                    player_algorithm = dropdown_player.getSelected()
                    ai_algorithm = dropdown_ai.getSelected()
                    if player_algorithm != 'Human':
                        entered = textbox_iterations.getText().strip()
                        if entered == "":
                            error_text = "Please enter number of games."
                        else:
                            try:
                                value = int(entered)
                                if value < 1:
                                    error_text = "Enter a positive integer."
                                else:
                                    ai_versus_iterations = value
                                    menu_running = False
                            except ValueError:
                                error_text = "Enter a valid integer."
                    else:
                        ai_versus_iterations = 1
                        menu_running = False
        dropdown_player.draw()
        dropdown_ai.draw()
        pygame_widgets.update(events) #update the dropdown and textbox state
        pygame.display.update()

def match_algorithm(insert_algorithm, maximizing, color):
    algorithm_score = 0
    timer_start = pygame.time.get_ticks() #for timing the AI's move
    match insert_algorithm:
        case "Minimax":
            column, algorithm_score = minimax(board, DEPTH, maximizing) #get the best move from the minimax algorithm
        case "Minimax with Alpha-Beta Pruning":
            column, algorithm_score = minimax_pruned(board, DEPTH, -math.inf, math.inf, maximizing) #get the best move from the minimax algorithm
        case "Greedy":
            column, algorithm_score = greedy_move(board, AI_PIECE)
        case "Random":
            valid_moves = get_valid_moves(board)
            column = random.choice(valid_moves)
        case "Monte Carlo":
            column, algorithm_score = monte_carlo_move(board, MONTE_CARLO_SIMULATIONS)
        case "Negamax":
            column, algorithm_score = negamax(board, DEPTH, color) #get the best move from the minimax algorithm
        case "Negamax with Alpha-Beta Pruning":
            column, algorithm_score = negamax_pruned(board, DEPTH, -math.inf, math.inf, color) #get the best move from the negamax algorithm
        case _: #default is alpha-beta for now
            column, algorithm_score = minimax_pruned(board, DEPTH, -math.inf, math.inf, maximizing) #get the best move from the minimax algorithm
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
iterations_remaining = ai_versus_iterations
draw_board(board)
# main game process
while not finish:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

        if event.type == pygame.MOUSEMOTION and turn == PLAYER and player_algorithm == "Human": #if the mouse moves, show the piece hovering above the board
            preview_move(event)

        if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER and player_algorithm == "Human": #when lmb clicked, drop the piece
            column = int(event.pos[0] / SQUARESIZE)
            if valid_move(board, column):
                row = get_next_open_row(board, column) #top row of the column
                drop_piece(board, row, column, PLAYER_PIECE)
                print("Player dropped piece at row " + str(row) + ", column " + str(column))
                if winning_move(board, PLAYER_PIECE):
                    record[0] += 1 #add 1 player win to the record
                    print("-----> Player wins!")
                    finish = True
                elif is_terminal_node(board):
                    record[2] += 1 #add 1 draw to the record
                    print("It's a draw!")
                    finish = True
                else:
                    turn = AI 
                draw_board(board) #update game state
                move_record.append(column)

        if turn == PLAYER and not finish and player_algorithm != "Human":
            column, algorithm_score, elapsed = match_algorithm(player_algorithm, True, 1)
            if valid_move(board, column):
                row = get_next_open_row(board, column)
                drop_piece(board, row, column, PLAYER_PIECE)
                player_decision_time_average[0] += elapsed
                player_decision_time_average[1] += 1
                print("Player algorithm dropped piece at row " + str(row) + ", column " + str(column) + " (calculated in " + str(elapsed) + " ms" + " for depth " + str(DEPTH) + ")")
                if winning_move(board, PLAYER_PIECE):
                    record[0] += 1 #add 1 player win to the record
                    print("-----> Player wins!")
                    finish = True
                elif is_terminal_node(board):
                    record[2] += 1 #add 1 draw to the record
                    print("It's a draw!")
                    finish = True
                else:
                    turn = AI
                draw_board(board)
                move_record.append(column)

        if turn == AI and not finish:
            column, algorithm_score, elapsed = match_algorithm(ai_algorithm, True, 1)
            if valid_move(board, column):
                row = get_next_open_row(board, column) #top row of the column
                drop_piece(board, row, column, AI_PIECE)
                ai_decision_time_average[0] += elapsed
                ai_decision_time_average[1] += 1
                print("AI dropped piece at row " + str(row) + ", column " + str(column) + " (calculated in " + str(elapsed) + " ms" + " for depth " + str(DEPTH) + ")")
                if winning_move(board, AI_PIECE):
                    record[1] += 1 #add 1 AI win to the record
                    print("-----> AI wins!")
                    finish = True
                elif is_terminal_node(board):
                    record[2] += 1 #add 1 draw to the record
                    print("It's a draw!")
                    finish = True
                else:
                    turn = PLAYER 
                draw_board(board) #update game state
                move_record.append(column)
        
        if finish:
            if player_algorithm != "Human" and iterations_remaining > 1:
                iterations_remaining -= 1
                board, move_record, turn, finish = reset_game()
                draw_board(board)
                print("Game finished! Move record: " + str(move_record))
                print(f"Starting next AI vs AI game! ({iterations_remaining} iterations remaining)")
            else:
                print("Game finished! Move record: " + str(move_record))
                print(f"[RECORD DATA:] Player wins: {record[0]} ({record[0]/sum(record)*100:.1f}%), AI wins: {record[1]} ({record[1]/sum(record)*100:.1f}%), Draws: {record[2]} ({record[2]/sum(record)*100:.1f}%)")
                if player_decision_time_average[1] > 0: #safety check but should be above 0 no matter what, anyway
                    print(f"Average player decision time: {player_decision_time_average[0] / player_decision_time_average[1]:.2f} ms")
                if ai_decision_time_average[1] > 0: #safety check but should be above 0 no matter what, anyway
                    print(f"Average AI decision time: {ai_decision_time_average[0] / ai_decision_time_average[1]:.2f} ms")
                print("Press enter to repeat, or any other key to quit (you can also just close the window).")
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
                                iterations_remaining = ai_versus_iterations if player_algorithm != "Human" else 1
                                draw_board(board) #update game state
                            else:
                                finish = True
            

pygame.quit()