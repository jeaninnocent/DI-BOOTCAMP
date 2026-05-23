import random

class Game:
    def __init__(self):
        # The valid items for the game
        self.valid_items = ['rock', 'paper', 'scissors']

    def get_user_item(self):
        """Asks the user to select an item and validates the input."""
        while True:
            user_input = input("Select an item (rock/paper/scissors): ").strip().lower()
            if user_input in self.valid_items:
                return user_input
            print("Invalid input. Please choose rock, paper, or scissors.")

    def get_computer_item(self):
        """Selects a random item for the computer."""
        return random.choice(self.valid_items)

    def get_game_result(self, user_item, computer_item):
        """Determines the result of the game."""
        if user_item == computer_item:
            return "draw"
        
        # Determine if the user won
        if (user_item == 'rock' and computer_item == 'scissors') or \
           (user_item == 'paper' and computer_item == 'rock') or \
           (user_item == 'scissors' and computer_item == 'paper'):
            return "win"
        
        # If it's not a draw and the user didn't win, it's a loss
        return "loss"

    def play(self):
        """Plays a single round of the game and returns the result."""
        # 1. Get user item
        user_item = self.get_user_item()
        
        # 2. Get computer item
        computer_item = self.get_computer_item()
        
        # 3. Determine the result
        result = self.get_game_result(user_item, computer_item)
        
        # 4. Print the output
        if result == "win":
            message = "You won!"
        elif result == "loss":
            message = "You lose!"
        else:
            message = "You drew!"
            
        print(f"You selected {user_item}. The computer selected {computer_item}. {message}")
        
        # 5. Return the result
        return result