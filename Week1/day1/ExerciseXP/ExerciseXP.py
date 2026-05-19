##Exercise 1:
print("Hello world\n" * 4) # Prints "Hello world" followed by a newline character (\n), repeated exactly 4 times


##Exercise 2:
print(f"le résultat est {(99**3)*8}") #Uses an f-string to embed a mathematical calculation (99 to the power of 3, multiplied by 8) directly into the text

##Exercise 3:
5 < 3 # False 
#(5 is not less than 3)

3 == 3 # True
#(3 is equal to 3)

3 == "3" #False 
#(An integer is not equal to a string data type)

"3" > 3 
# Error (Python cannot compare a string and an integer using >)

# "Hello" == "hello" #False 
#(Python is case-sensitive; 'H' and 'h' are different)

##Exercise 4:
computer_brand = "LENOVO"
print(f"I have a {computer_brand} computer.") # Injects the computer brand variable directly into the sentence

##Exercise 5:
name = "OUATTARA"
age = "19"
shoe_size = "41"
info = "My name is {name}, I am {age} years old and  my shoe size is {shoe_size}."
# Replaces the placeholders with the actual variables using .format() and prints it
print(info.format(name=name, age=age, shoe_size=shoe_size))

##Exercise 6:
a = 50
b = 19
if a > b: # Evaluates if 'a' is greater than 'b'. If true, it prints the message
    print("Hello World")

##Exercise 7:
number = int(input("Enter a number: ")) # Prompts the user for a number and immediately converts the string input into an integer (int)
if number % 2 == 0: #The '%' (modulo) operator calculates the remainder of the division by 2.
    print(f"{number} is an even number.") #If the remainder is 0, the number is even. 
else:  #Otherwise, it is odd. 
     print(f"{number} is an odd number.")

#Exercise 8:
user_name = input("What is your name? ") # Requests the user's name via input
my_name = "OUATTARA"
if user_name.upper() == my_name :  # Converts the user's input entirely to UPPERCASE using .upper()
# This ensures a successful match even if they typed it in lowercase
    print("Great! we have the same name!")
else:
    print("Oops! We don't have the same name.")

#Exercise 9:
# Ask the user for their height and convert the input to an integer
height = int(input("Enter your height in centimeters: "))

# Check if the height is over 145 cm
if height > 145:
    print("You are tall enough to ride!")
else:
    print("You need to grow some more to ride.")

