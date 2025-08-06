import sys
import numpy as np 

BOARD_ROWS = 3
BOARD_COLS = 3

board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=None):
    if check_board is None:
        check_board = board

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=None):
    if check_board is None:
        check_board = board

    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
        
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

def minmax(minmax_board, depth, is_maxmizing):
    # Player 2 Wins
    if check_win(2, minmax_board):
        return float('inf')
    # Player 1 Wins
    elif check_win(1, minmax_board):
        return float('-inf')
    # Draw
    elif is_board_full(minmax_board):
        return 0
    
    if is_maxmizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minmax_board[row][col] == 0:
                    minmax_board[row][col] = 2
                    score = minmax(minmax_board, depth + 1, is_maxmizing=False)
                    minmax_board[row][col] = 0 
                    best_score = max(score, best_score)
        return best_score

    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minmax_board[row][col] == 0:
                    minmax_board[row][col] = 1
                    score = minmax(minmax_board, depth + 1, is_maxmizing=True)
                    minmax_board[row][col] = 0 
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minmax(board, 0, False)
                board[row][col] = 0 
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)  
        return True
    return False

def restart_game():
    global board
    board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

def print_board():
    symbols = {0: '.', 1: 'X', 2: 'O'}
    print('\nBoard:')
    for row in board:
        print(" ".join(symbols[cell] for cell in row))
    print()

# Game loop
player = 1
game_over = False

print("Tic Tac Toe! You are Player 1 (X). AI is Player 2 (O).")
print_board()

while not game_over:
    # Human move
    while True:
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
            if row in range(3) and col in range(3) and available_square(row, col):
                mark_square(row, col, player)
                break
            else: 
                print("Invalid move. Try again")
        except ValueError:
            print("Please enter a valid integers")

    print_board()

    if check_win(player):
        print("You Win!")
        game_over = True
        break

    if is_board_full(): 
        print("Draw")
        game_over = True
        break

    # AI Move
    print("AI is making a move....")
    best_move()
    print_board()

    if check_win(2):
        print("AT Wins!")
        game_over = True
        break

    if is_board_full(): 
        print("Draw")
        game_over = True
        break

if input("Play Again? (y/n): ").lower() == 'y':
    restart_game()
    game_over = False
