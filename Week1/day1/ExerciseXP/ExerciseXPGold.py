##Exercise 1:
# Ask the user for a month
month = int(input("Enter a month (1 to 12): "))

# Check which season the month falls into
if month in (3, 4, 5):
    print("Spring")
elif month in (6, 7, 8):
    print("Summer")
elif month in (9, 10, 11):
    print("Autumn")
elif month in (12, 1, 2):
    print("Winter")
else:
    print("Invalid month. Please enter a number between 1 and 12.")

##Exercise 2:
# Print all numbers from 1 to 20 (inclusive)
print("Numbers 1 to 20:")
for num in range(1, 21):
    print(num)

print("-" * 15)

# Print numbers where the index is even
print("Numbers with an even index:")
numbers = list(range(1, 21))

for index, num in enumerate(numbers):
    if index % 2 == 0:
        print(f"Index {index}: {num}")

##Exercise 3:   
my_name = "Jean"

while True:
    user_input = input("Please enter your name: ")
    
    if user_input == my_name:
        print(f"Hello, {my_name}! Loop stopped.")
        break
    else:
        print("That's not it. Try again!")

##Exercise 4:   
names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']

user_name = input("Enter a name: ")

if user_name in names:
    # .index() finds the first occurrence automatically
    name_index = names.index(user_name)
    print(f"The index of the first occurrence is: {name_index}")
else:
    print(f"{user_name} is not in the list.")

##Exercise 5:
# Ask for 3 numbers
num1 = int(input("Input the 1st number: "))
num2 = int(input("Input the 2nd number: "))
num3 = int(input("Input the 3rd number: "))

# Find the greatest using the built-in max() function
greatest = max(num1, num2, num3)

print(f"The greatest number is: {greatest}")

#Exercise 6:
wins = 0
losses = 0

# Notre astuce : une liste de nombres prédéfinie pour remplacer le hasard
nombres_secrets = [7, 3, 8, 1, 5, 9, 2, 4, 6]
# On garde une trace du tour actuel pour avancer dans la liste
tour = 0

print("Welcome to the Number Guessing Game!")

user_input = ""

while user_input != "quit":
    
    user_input = input("\nGuess a number from 1 to 9 (or type 'quit' to exit): ")
    
    if user_input != "quit":
        
        guess = int(user_input)
        
        # On choisit le nombre de la liste qui correspond au tour actuel
        correct_number = nombres_secrets[tour]
        
        if guess == correct_number:
            print("Winner!")
            wins = wins + 1
        else:
            print("Better luck next time. The correct number was", correct_number)
            losses = losses + 1
            
        # On prépare le prochain tour en avançant d'une case dans la liste
        tour = tour + 1
        
        # Si on arrive à la fin de notre liste (qui contient 9 nombres), on recommence à 0
        if tour == 9:
            tour = 0

print("\n--- Game Over ---")
print("Total games won:", wins)
print("Total games lost:", losses)