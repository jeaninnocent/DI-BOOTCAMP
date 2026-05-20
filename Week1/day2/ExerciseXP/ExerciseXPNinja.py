# ==========================================
# Exercise 1: Cars
# ==========================================
print("--- Exercise 1: Cars ---")

# 1. Convert string to a list programmatically
cars_string = "Volkswagen, Toyota, Ford Motor, Honda, Chevrolet"
cars_list = cars_string.split(", ")

# 2. Print how many manufacturers are in the list
print(f"There are {len(cars_list)} manufacturers in the list.")

# 3. Print the list in reverse/descending order (Z-A)
# We sort it first, then reverse it to ensure strict Z-A alphabetical order
cars_descending = sorted(cars_list, reverse=True)
print(f"Manufacturers in descending order: {cars_descending}")

# 4. Find how many manufacturers' names have the letter 'o'
# We use a generator expression inside sum() which counts the True values
with_o = sum('o' in car.lower() for car in cars_list)
print(f"Manufacturers with the letter 'o': {with_o}")

# 5. Find how many manufacturers' names do NOT have the letter 'i'
without_i = sum('i' not in car.lower() for car in cars_list)
print(f"Manufacturers without the letter 'i': {without_i}")

# Bonus 1: Remove duplicates and print as comma-separated string
duplicates_list = ["Honda", "Volkswagen", "Toyota", "Ford Motor", "Honda", "Chevrolet", "Toyota"]
# Converting to a set automatically removes duplicates
unique_cars = list(set(duplicates_list))
joined_unique_cars = ", ".join(unique_cars)

print(f"\n[Bonus 1] Unique list: {joined_unique_cars}")
print(f"[Bonus 1] There are now {len(unique_cars)} companies in the unique list.")

# Bonus 2: Ascending order, but reverse the letters of each name
# First sort A-Z, then reverse the string characters using slicing [::-1]
ascending_cars = sorted(cars_list)
reversed_letters_cars = [car[::-1] for car in ascending_cars]
print(f"\n[Bonus 2] Ascending order with reversed letters: {reversed_letters_cars}")


# ==========================================
# Exercise 2: What’s your name?
# ==========================================
print("\n--- Exercise 2: What's your name? ---")

def get_full_name(first_name, last_name, middle_name=""):
    """
    Returns a properly capitalized full name. 
    middle_name is optional.
    """
    if middle_name:
        # title() ensures names like "lee" become "Lee"
        return f"{first_name.title()} {middle_name.title()} {last_name.title()}"
    else:
        return f"{first_name.title()} {last_name.title()}"

# Test cases provided in the prompt
name1 = get_full_name(first_name="john", middle_name="hooker", last_name="lee")
name2 = get_full_name(first_name="bruce", last_name="lee")

print(name1)
print(name2)


# ==========================================
# Exercise 3: From English to Morse
# ==========================================
print("\n--- Exercise 3: From English to Morse ---")

# Dictionary mapping letters/numbers to Morse code
MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.', '0': '-----', ',': '--..--', 
    '.': '.-.-.-', '?': '..--..', '!': '-.-.--'
}

# Create a reverse dictionary for decoding
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_DICT.items()}

def english_to_morse(text):
    """Converts English text to Morse code."""
    text = text.upper()
    morse_words = []
    
    # Split by spaces to isolate words
    words = text.split(" ")
    for word in words:
        morse_chars = []
        for char in word:
            if char in MORSE_DICT:
                morse_chars.append(MORSE_DICT[char])
        # Join characters of a word with a single space
        morse_words.append(" ".join(morse_chars))
        
    # Join words with a slash surrounded by spaces (as requested)
    return " / ".join(morse_words)

def morse_to_english(morse_code):
    """Converts Morse code to English text."""
    english_words = []
    
    # Split by the slash to isolate words
    words = morse_code.split(" / ")
    for word in words:
        english_chars = []
        # Split by space to isolate Morse characters
        chars = word.split(" ")
        for char in chars:
            if char in REVERSE_MORSE_DICT:
                english_chars.append(REVERSE_MORSE_DICT[char])
        # Join the letters back together
        english_words.append("".join(english_chars))
        
    # Join the words with a normal space
    return " ".join(english_words)

# Test the conversion functions
original_text = "HELLO PYTHON"
encoded_text = english_to_morse(original_text)
decoded_text = morse_to_english(encoded_text)

print(f"Original Text: {original_text}")
print(f"To Morse Code: {encoded_text}")
print(f"Back to English: {decoded_text}")