##challenge1

def sort_csv_words():
    # 1. Ask the user for input
    user_input = input("Enter a comma-separated sequence of words: ")
    
    # 2. Use list comprehension to split and clean the words, then sort them
    sorted_words = sorted([word.strip() for word in user_input.split(',')])
    
    # 3. Join the sorted list back into a comma-separated string and print
    result = ",".join(sorted_words)
    print(result)

# Test the function (uncomment to run)
# sort_csv_words() 
# Input: without,hello,bag,world
# Output: bag,hello,without,world

##challenge2
def longest_word(sentence):
    """
    Finds the longest word in a sentence.
    Punctuation marks attached to words are counted as part of the word.
    """
    # Split the sentence into a list of words based on spaces
    words = sentence.split()
    
    # Find and return the longest word using max() with length as the key
    return max(words, key=len)

# ==========================================
# TEST CASES
# ==========================================
if __name__ == "__main__":
    print(longest_word("Margaret's toy is a pretty doll.")) 
    # Output: "Margaret's"
    
    print(longest_word("A thing of beauty is a joy forever.")) 
    # Output: "forever."
    
    print(longest_word("Forgetfulness is by all means powerless!")) 
    # Output: "Forgetfulness"