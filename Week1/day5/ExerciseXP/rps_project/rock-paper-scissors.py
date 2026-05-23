from game import Game

def get_user_menu_choice():
    """Displays the menu, gets the user's choice, and returns it."""
    print("\n--- Main Menu ---")
    print("1. Play a new game")
    print("2. Show scores")
    print("3. Quit (or type 'q'/'x')")
    
    choice = input("Enter your choice: ").strip().lower()
    return choice

def print_results(results):
    """Prints the final summary of all games played."""
    print("\n" + "="*20)
    print("   GAME SUMMARY")
    print("="*20)
    print(f"Wins:   {results.get('win', 0)}")
    print(f"Losses: {results.get('loss', 0)}")
    print(f"Draws:  {results.get('draw', 0)}")
    print("="*20)
    print("Thank you for playing!")

def main():
    # Dictionary to keep track of the scores
    results = {'win': 0, 'loss': 0, 'draw': 0}
    
    while True:
        # Display menu and get choice
        choice = get_user_menu_choice()
        
        if choice == '1':
            # Create a new Game object and play
            current_game = Game()
            outcome = current_game.play()
            
            # Remember the result
            results[outcome] += 1
            
        elif choice == '2':
            # Show current scores
            print(f"\nCurrent Scores -> Wins: {results['win']} | Losses: {results['loss']} | Draws: {results['draw']}")
            
        elif choice in ['3', 'q', 'x']:
            # Print results summary and exit
            print_results(results)
            break
            
        else:
            print("Invalid choice. Please select a valid option from the menu.")

if __name__ == "__main__":
    main()