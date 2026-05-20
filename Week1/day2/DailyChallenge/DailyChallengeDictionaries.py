# ==========================================
# Challenge 1: Letter Index Dictionary
# ==========================================
print("## Challenge 1: Letter Index Dictionary\n")

def get_letter_indices(word):
    """
    Creates a dictionary mapping each letter in the word to a list of its indices.
    """
    letter_dict = {}
    
    # Iterate through the word using enumerate to get both the index and the character
    for index, char in enumerate(word):
        # Check if the character is already a key in the dictionary
        if char in letter_dict:
            # If it is, append the current index to the existing list
            letter_dict[char].append(index)
        else:
            # If it is not, create a new key-value pair with the index in a list
            letter_dict[char] = [index]
            
    return letter_dict

# Testing Challenge 1 with the provided examples
test_words = ["dodo", "froggy", "grapes"]

for word in test_words:
    print(f"[Simulated Input] Enter a word: {word}")
    result = get_letter_indices(word)
    print(f"Output: {result}\n")


# ==========================================
# Challenge 2: Affordable Items
# ==========================================
print("## Challenge 2: Affordable Items\n")

def get_affordable_items(items_purchase, wallet):
    """
    Returns an alphabetically sorted list of items that can be purchased 
    with the given wallet amount, respecting the dictionary's order of priority.
    """
    # Data Cleaning: Remove '$' and ',' from the wallet string, then convert to int
    clean_wallet = int(wallet.replace("$", "").replace(",", ""))
    
    basket = []
    
    # Iterate through the items and attempt to buy them in priority order
    for item, price_str in items_purchase.items():
        # Data Cleaning: Remove '$' and ',' from the price string, then convert to int
        clean_price = int(price_str.replace("$", "").replace(",", ""))
        
        # Check if we can afford the item
        if clean_price <= clean_wallet:
            basket.append(item)
            clean_wallet -= clean_price # Update the wallet after buying
            
    # Check if the basket is empty
    if not basket:
        return "Nothing"
    else:
        # Return the basket list in alphabetical order
        return sorted(basket)

# Testing Challenge 2 with the provided examples

# Test Case 1
items_1 = {"Water": "$1", "Bread": "$3", "TV": "$1,000", "Fertilizer": "$20"}
wallet_1 = "$300"
print(f"Items: {items_1} | Wallet: {wallet_1}")
print(f"Output: {get_affordable_items(items_1, wallet_1)}\n")

# Test Case 2
items_2 = {"Apple": "$4", "Honey": "$3", "Fan": "$14", "Bananas": "$4", "Pan": "$100", "Spoon": "$2"}
wallet_2 = "$100"
print(f"Items: {items_2} | Wallet: {wallet_2}")
print(f"Output: {get_affordable_items(items_2, wallet_2)}\n")

# Test Case 3
items_3 = {"Phone": "$999", "Speakers": "$300", "Laptop": "$5,000", "PC": "$1200"}
wallet_3 = "$1"
print(f"Items: {items_3} | Wallet: {wallet_3}")
print(f"Output: {get_affordable_items(items_3, wallet_3)}")