def display_board(board):
    """
    Displays the current state of the Tic Tac Toe board.
    It expects a list of 9 elements representing the grid.
    """
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def player_input(board, player):
    """
    Asks the player for their move and updates the board.
    Validates that the input is a number, within 1-9, and the cell is empty.
    """
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): "))
            
            # Check if the number is between 1 and 9
            if 1 <= move <= 9:
                # Check if the chosen spot is empty (we subtract 1 because lists are 0-indexed)
                if board[move - 1] == " ":
                    board[move - 1] = player
                    break  # Valid move, exit the loop
                else:
                    print("That space is already taken. Try again.")
            else:
                print("Invalid input. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a valid number, not text.")

def check_win(board, player):
    """
    Checks if the specified player has won the game.
    Returns True if there is a win, False otherwise.
    """
    # All the 8 possible winning combinations (indices of the board list)
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for condition in win_conditions:
        # Check if all three spots in a win condition match the player's mark
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
            
    return False

def check_tie(board):
    """
    Checks if the board is completely full, resulting in a tie.
    """
    return " " not in board

def play():
    """
    The main game loop that coordinates all other functions.
    """
    # Initialize an empty board with 9 spaces
    board = [" "] * 9
    current_player = "X"
    game_over = False

    print("Welcome to Tic Tac Toe!")
    print("The board positions are numbered 1-9, starting from top-left:")
    
    # Show a reference board so players know which number corresponds to which square
    reference_board = [str(i) for i in range(1, 10)]
    display_board(reference_board)
    print("Let's begin!")

    # Main game loop
    while not game_over:
        display_board(board)
        
        # Get the move from the current player
        player_input(board, current_player)

        # Check if the current player won
        if check_win(board, current_player):
            display_board(board)
            print(f"🎉 Congratulations! Player {current_player} wins the game!")
            game_over = True
            
        # Check if the game is a tie
        elif check_tie(board):
            display_board(board)
            print("🤝 It's a tie! All squares are full.")
            game_over = True
            
        # If no win and no tie, switch players
        else:
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"

# This ensures the game runs when the script is executed directly
if __name__ == "__main__":
    play()