##Challenge 1
#Ask the user for a number and a length
number = int(input("Enter a number: "))
length = int(input("Enter the list length: "))

# Initialize an empty list to store the multiples
multiples_list = []

#Loop from 1 up to length (inclusive) to generate the multiples
for i in range(1, length + 1):
    multiples_list.append(number * i)

# Print the final result
print(multiples_list)

##Challenge 2
# Ask the user for a string
user_word = input("Enter a word with consecutive duplicate letters: ")

# Initialize an empty string to store the clean result
result = ""

# Loop through each character in the user's word
for char in user_word:
    # If the result string is empty OR the current character is different 
    # from the very last character added to the result, we keep it.
    if len(result) == 0 or char != result[-1]:
        result += char

# Display the cleaned string
print(f"Cleaned word: {result}")