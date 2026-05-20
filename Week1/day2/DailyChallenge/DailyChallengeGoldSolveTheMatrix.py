# 1. Define the Matrix as a 2D list
matrix = [
    ['7', 'i', 'i'],
    ['T', 's', 'x'],
    ['h', '%', '?'],
    ['i', ' ', '#'],
    ['s', 'M', ' '],
    ['$', 'a', ' '],
    ['#', 't', '%'],
    ['^', 'r', '!']
]

rows = len(matrix)
cols = len(matrix[0])

# 2. Extract the raw string by reading down each column
raw_string = ""
for col in range(cols):
    for row in range(rows):
        raw_string += matrix[row][col]

# At this point, raw_string is: "7This$#^is% Matrix?#  %!"

# 3. Apply Neo's decryption rules
decoded_message = ""
symbol_buffer = ""
found_first_letter = False

# Loop through our raw string
for char in raw_string:
    if char.isalnum(): # Checks if the character is a letter or number
        # If we have symbols stored, and we are between two words, replace with a space
        if found_first_letter and len(symbol_buffer) > 0:
            decoded_message += " "
            
        decoded_message += char
        symbol_buffer = "" # Reset the buffer
        found_first_letter = True
        
    else:
        # It's a symbol or space. Store it in the buffer if we are mid-sentence.
        if found_first_letter:
            symbol_buffer += char
        else:
            # If we haven't found any letters yet, keep leading symbols
            decoded_message += char

# Add any trailing symbols that weren't between alphanumeric characters
decoded_message += symbol_buffer

# 4. Output the final secret message
print(decoded_message)