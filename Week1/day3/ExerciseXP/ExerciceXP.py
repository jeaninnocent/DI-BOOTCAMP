##EXERCICSE 1
class Cat:
    """Represents a cat with a name and an age."""
    
    def __init__(self, cat_name: str, cat_age: int) -> None:
        """Initializes the Cat instance."""
        self.name = cat_name
        self.age = cat_age

def find_oldest_cat(cat1: Cat, cat2: Cat, cat3: Cat) -> Cat:
    """
    Compares three Cat objects and returns the oldest one.
    Uses the built-in max() function with a lambda for clean comparison.
    """
    return max((cat1, cat2, cat3), key=lambda cat: cat.age)

# Step 1: Create cat objects
cat_a = Cat("Garfield", 7)
cat_b = Cat("Tom", 12)
cat_c = Cat("Sylvester", 5)

# Step 2: Create a function to find the oldest cat
oldest_cat = find_oldest_cat(cat_a, cat_b, cat_c)

# Step 3: Print the oldest cat's details
print(f"The oldest cat is {oldest_cat.name}, and is {oldest_cat.age} years old.")

##EXERCICSE 2
class Dog:
    """Represents a dog with a name and a height in centimeters."""
    
    def __init__(self, name: str, height: int) -> None:
        """Initializes the Dog instance."""
        self.name = name
        self.height = height

    def bark(self) -> None:
        """Prints a barking sound."""
        print(f"{self.name} goes woof!")

    def jump(self) -> None:
        """Prints the jump height (height * 2)."""
        jump_height = self.height * 2
        print(f"{self.name} jumps {jump_height} cm high!")

# Step 2: Create Dog Objects
davids_dog = Dog("Rex", 50)
sarahs_dog = Dog("Teacup", 20)

# Step 3: Print Dog Details and Call Methods
# David's dog
print(f"David's dog is {davids_dog.name} and is {davids_dog.height} cm tall.")
davids_dog.bark()
davids_dog.jump()

# Sarah's dog
print(f"Sarah's dog is {sarahs_dog.name} and is {sarahs_dog.height} cm tall.")
sarahs_dog.bark()
sarahs_dog.jump()

# Step 4: Compare Dog Sizes
if davids_dog.height > sarahs_dog.height:
    print(f"{davids_dog.name} is bigger than {sarahs_dog.name}.")
elif sarahs_dog.height > davids_dog.height:
    print(f"{sarahs_dog.name} is bigger than {davids_dog.name}.")
else:
    print(f"{davids_dog.name} and {sarahs_dog.name} are the same size.")


##EXERCICSE 3
from typing import List

class Song:
    """Represents a song containing a list of lyrics."""
    
    def __init__(self, lyrics: List[str]) -> None:
        """Initializes the Song instance with lyrics."""
        self.lyrics = lyrics

    def sing_me_a_song(self) -> None:
        """Prints each line of the lyrics on a new line."""
        for line in self.lyrics:
            print(line)

# Step 2 & 3: Instantiate and test
stairway_lyrics = [
    "There's a lady who's sure", 
    "all that glitters is gold", 
    "and she's buying a stairway to heaven"
]
stairway = Song(stairway_lyrics)
stairway.sing_me_a_song()

##EXERCICSE 4
from typing import List, Dict

class Zoo:
    """Manages a zoo, its animals, and operations like adding or selling."""
    
    def __init__(self, zoo_name: str) -> None:
        """Initializes the Zoo instance with a name and an empty animal list."""
        self.zoo_name = zoo_name
        self.animals: List[str] = []

    def add_animal(self, *new_animals: str) -> None:
        """
        Adds one or multiple animals to the zoo.
        Prevents adding duplicates.
        """
        for animal in new_animals:
            if animal not in self.animals:
                self.animals.append(animal)
            else:
                # Logging a warning if the animal is already there
                print(f"Notice: '{animal}' is already in the zoo.")

    def get_animals(self) -> None:
        """Prints the list of all animals in the zoo."""
        print(f"Animals in {self.zoo_name}: {', '.join(self.animals)}")

    def sell_animal(self, animal_sold: str) -> None:
        """
        Removes an animal from the zoo if it exists.
        Handles the edge case where the animal is not found.
        """
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)
            print(f"Success: '{animal_sold}' has been sold.")
        else:
            print(f"Error: Cannot sell '{animal_sold}', it is not in the zoo.")

    def sort_animals(self) -> Dict[str, List[str]]:
        """
        Sorts animals alphabetically and groups them by their first letter.
        Returns a dictionary representing the grouped animals.
        """
        sorted_animals = sorted(self.animals)
        grouped_animals: Dict[str, List[str]] = {}
        
        for animal in sorted_animals:
            # Get the first letter, capitalized
            first_letter = animal[0].upper() 
            if first_letter not in grouped_animals:
                grouped_animals[first_letter] = []
            grouped_animals[first_letter].append(animal)
            
        return grouped_animals

    def get_groups(self) -> None:
        """Prints the animals grouped by their first letter."""
        grouped = self.sort_animals()
        print("\n--- Grouped Animals ---")
        for letter, animal_group in grouped.items():
            print(f"{letter}: {animal_group}")


# Step 2: Create a Zoo instance
brooklyn_safari = Zoo("Brooklyn Safari")

# Step 3: Use the Zoo methods (Utilisation du *args pour le bonus)
brooklyn_safari.add_animal("Giraffe", "Bear", "Baboon", "Cougar", "Cat", "Lion", "Zebra")

# Test duplicate handling
brooklyn_safari.add_animal("Giraffe") 

# Display animals
brooklyn_safari.get_animals()

# Sell an animal
brooklyn_safari.sell_animal("Bear")

# Display animals again to verify sale
brooklyn_safari.get_animals()

# Display groups
brooklyn_safari.get_groups()
