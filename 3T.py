import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
GRID_SIZE = 3
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
X_COLOR = (255, 0, 0)  # Red for X
O_COLOR = (50, 50, 50)  # Dark Gray for O
LINE_COLOR = (0, 255, 0)  # Green for winning line
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
HASH_COLOR = (255, 255, 255)  # White
FONT_SIZE = 80
SCORE_FONT_SIZE = 40

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('3T - Tic Tac Toe')

# Fonts
font = pygame.font.Font(None, FONT_SIZE)
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

# Song
pygame.mixer.music.load('assets/KPOP6.0.wav')  # Replace with your music file
pygame.mixer.music.play(-1)  # Play the music in a loop

# Variables
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_1_symbol = 'X'
player_2_symbol = 'O'
turn = random.choice([player_1_symbol, player_2_symbol])
game_over = False
winner = None
scores = {player_1_symbol: 0, player_2_symbol: 0}
rounds_to_win = 3
current_round = 1
winning_cells = []

# Function to draw grid
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, HASH_COLOR, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), 5)
        pygame.draw.line(screen, HASH_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, SCREEN_WIDTH), 5)

# Function to draw X or O
def draw_symbol(symbol, x, y):
    text = font.render(symbol, True, X_COLOR if symbol == 'X' else O_COLOR)
    screen.blit(text, (x + (CELL_SIZE - FONT_SIZE) // 2, y + (CELL_SIZE - FONT_SIZE) // 2))

# Function to check if there's a winner
def check_winner():
    # Check rows, columns, and diagonals
    for row in range(GRID_SIZE):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '':
            return board[row][0], [(row, i) for i in range(GRID_SIZE)]

    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col], [(i, col) for i in range(GRID_SIZE)]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0], [(i, i) for i in range(GRID_SIZE)]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2], [(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)]

    return None, None

# Function to draw winning line
def draw_winning_line(cells):
    for cell in cells:
        x = cell[1] * CELL_SIZE + CELL_SIZE // 2
        y = cell[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, LINE_COLOR, (x, y), 20, 5)

# Function to reset the board
def reset_board():
    global board, turn, winner, game_over, winning_cells
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turn = random.choice([player_1_symbol, player_2_symbol])
    game_over = False
    winner = None
    winning_cells = []

# Function to check if the board is full (a tie)
def is_board_full():
    for row in board:
        if '' in row:
            return False
    return True

# Main game loop
while True:
    screen.fill(BACKGROUND_COLOR)

    # Draw grid
    draw_grid()

    # Draw symbols
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] != '':
                draw_symbol(board[row][col], col * CELL_SIZE, row * CELL_SIZE)

    # Display scores
    score_text = score_font.render(f"X: {scores['X']} | O: {scores['O']}", True, HASH_COLOR)
    screen.blit(score_text, (SCREEN_WIDTH - 200, 10))

    if game_over and winner:
        draw_winning_line(winning_cells)
        if scores[winner] == rounds_to_win:
            game_over_text = font.render(f"{winner} wins the game!", True, LINE_COLOR)
        else:
            game_over_text = font.render(f"{winner} wins the round!", True, LINE_COLOR)
        screen.blit(game_over_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
    elif game_over and winner is None:
        tie_text = font.render("It's a tie!", True, HASH_COLOR)
        screen.blit(tie_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    else:
        turn_text = font.render(f"Turn: {turn}", True, HASH_COLOR)
        screen.blit(turn_text, (SCREEN_WIDTH // 10, SCREEN_HEIGHT - 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE

            if row < GRID_SIZE and board[row][col] == '':
                board[row][col] = turn
                winner, winning_cells = check_winner()

                if winner:
                    scores[winner] += 1
                    game_over = True
                elif is_board_full():
                    game_over = True
                else:
                    turn = player_2_symbol if turn == player_1_symbol else player_1_symbol

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                if winner and scores[winner] == rounds_to_win:
                    # Reset scores if the game is over
                    scores = {player_1_symbol: 0, player_2_symbol: 0}
                    current_round = 1
                else:
                    current_round += 1
                reset_board()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

