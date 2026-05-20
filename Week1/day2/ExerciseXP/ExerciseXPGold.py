import random

# ==========================================
# Exercise 1 & 2: Birthday Look-up & Advanced
# ==========================================
print("--- Exercises 1 & 2 ---")

# 1. Create and initialize the birthdays dictionary
birthdays = {
    "Alice": "1992/05/14",
    "Bob": "1985/11/23",
    "Charlie": "1999/08/02",
    "Diana": "1988/01/30",
    "Eve": "1995/12/11"
}

# 2. Print welcome message and available names (Exercise 2 feature)
print("Welcome to the birthday dictionary!")
print("You can look up the birthdays of the people in the list!")
print("Here are the available names:")
for name in birthdays.keys():
    print(f"- {name}")

# 3. Get the user's input (Simulated here)
# To make it interactive, change to: user_input = input("Enter a person's name: ")
user_input = "Charlie" 
print(f"\n[Simulated Input] Enter a person's name: {user_input}")

# 4. Look up the birthday and print the result with error handling (Exercise 2 feature)
if user_input in birthdays:
    print(f"{user_input}'s birthday is {birthdays[user_input]}.")
else:
    print(f"Sorry, we don’t have the birthday information for {user_input}.")


# ==========================================
# Exercise 3: Check the index
# ==========================================
print("\n--- Exercise 3 ---")

names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']

# Simulated input 
# To make it interactive, change to: search_name = input("Enter your name: ")
search_name = "Cortana"
print(f"[Simulated Input] Enter your name: {search_name}")

# Check if the name is in the list and print its first index
if search_name in names:
    first_index = names.index(search_name)
    print(f"The index of the first occurrence of '{search_name}' is {first_index}.")
else:
    print(f"'{search_name}' is not in the list.")


# ==========================================
# Exercise 4: Double Dice
# ==========================================
print("\n--- Exercise 4 ---")

def throw_dice():
    """Simulates rolling a 6-sided die and returns an integer between 1 and 6."""
    return random.randint(1, 6)

def throw_until_doubles():
    """Keeps throwing 2 dice until they match. Returns the number of total throws."""
    throws = 0
    while True:
        throws += 1
        die1 = throw_dice()
        die2 = throw_dice()
        
        # Stop throwing if we reach doubles
        if die1 == die2:
            break
            
    return throws

def main():
    """Throws doubles 100 times and calculates the statistics."""
    # We use a list to collect the results because we need to store multiple 
    # integers to calculate both the sum (total) and the average later.
    results_collection = []
    
    # Run the simulation 100 times
    for _ in range(100):
        throws_needed = throw_until_doubles()
        results_collection.append(throws_needed)
        
    # Calculate statistics
    total_throws = sum(results_collection)
    average_throws = total_throws / len(results_collection)
    
    # Print the final results
    print(f"Total throws: {total_throws}")
    print(f"Average throws to reach doubles: {average_throws:.2f}")

# Execute the main function for Exercise 4
main()