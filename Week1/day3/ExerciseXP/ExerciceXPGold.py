##Exercice1
import math

class Circle:
    """Represents a geometrical circle and computes its properties."""
    
    def __init__(self, radius: float = 1.0) -> None:
        """Initializes the Circle with a radius (default is 1.0)."""
        self.radius = radius

    def perimeter(self) -> float:
        """Computes and returns the perimeter (circumference) of the circle."""
        return 2 * math.pi * self.radius

    def area(self) -> float:
        """Computes and returns the area of the circle."""
        return math.pi * (self.radius ** 2)

    def print_definition(self) -> None:
        """Prints the geometrical definition of a circle."""
        definition = (
            "A circle is a shape consisting of all points in a plane "
            "that are at a given distance from a given point, the centre."
        )
        print(definition)

# --- Test de l'exercice 1 ---
my_circle = Circle(5.0)
print(f"Perimeter: {my_circle.perimeter():.2f}")
print(f"Area: {my_circle.area():.2f}")
my_circle.print_definition()

##Exercice2
import random
from typing import List

class MyList:
    """A custom class to manipulate a list of letters."""
    
    def __init__(self, letters: List[str]) -> None:
        """Initializes the MyList instance with a list of letters."""
        self.letters = letters

    def reverse_list(self) -> List[str]:
        """Returns a reversed copy of the list."""
        return self.letters[::-1]

    def sort_list(self) -> List[str]:
        """Returns a sorted copy of the list alphabetically."""
        return sorted(self.letters)

    def generate_random_list(self) -> List[int]:
        """
        Bonus: Generates a list of random numbers between 1 and 100 
        with the same length as the original list using list comprehension.
        """
        return [random.randint(1, 100) for _ in self.letters]

# --- Test de l'exercice 2 ---
my_letters = MyList(['z', 'a', 'x', 'b', 'm'])
print("Original:", my_letters.letters)
print("Reversed:", my_letters.reverse_list())
print("Sorted:", my_letters.sort_list())
print("Random numbers (Bonus):", my_letters.generate_random_list())

##Exercice3
from typing import List, Dict, Union

class MenuManager:
    """Manages a restaurant menu allowing to add, update, and remove dishes."""
    
    def __init__(self) -> None:
        """Initializes the MenuManager with a default list of dishes."""
        # Using Union[str, int, bool] to perfectly describe the dictionary values for the linter
        self.menu: List[Dict[str, Union[str, int, bool]]] = [
            {"name": "Soup", "price": 10, "spice_level": "B", "gluten_index": False},
            {"name": "Hamburger", "price": 15, "spice_level": "A", "gluten_index": True},
            {"name": "Salad", "price": 18, "spice_level": "A", "gluten_index": False},
            {"name": "French Fries", "price": 5, "spice_level": "C", "gluten_index": False},
            {"name": "Beef bourguignon", "price": 25, "spice_level": "B", "gluten_index": True}
        ]

    def add_item(self, name: str, price: int, spice: str, gluten: bool) -> None:
        """Adds a new dish to the menu."""
        new_dish = {
            "name": name,
            "price": price,
            "spice_level": spice,
            "gluten_index": gluten
        }
        self.menu.append(new_dish)
        print(f"Success: '{name}' has been added to the menu.")

    def update_item(self, name: str, price: int, spice: str, gluten: bool) -> None:
        """Updates an existing dish. Notifies if the dish is not found."""
        for dish in self.menu:
            if dish["name"] == name:
                dish["price"] = price
                dish["spice_level"] = spice
                dish["gluten_index"] = gluten
                print(f"Success: '{name}' has been updated.")
                return
        
        print(f"Notice: The dish '{name}' is not in the menu.")

    def remove_item(self, name: str) -> None:
        """Removes a dish from the menu and prints the updated menu. Notifies if not found."""
        for dish in self.menu:
            if dish["name"] == name:
                self.menu.remove(dish)
                print(f"Success: '{name}' has been deleted.")
                print("--- Updated Menu ---")
                for item in self.menu:
                    print(item)
                return
                
        print(f"Notice: The dish '{name}' is not in the menu.")

# --- Test de l'exercice 3 ---
manager = MenuManager()

# Ajout d'un plat
manager.add_item("Tacos", 12, "C", True)

# Mise à jour d'un plat existant
manager.update_item("Soup", 12, "A", False)

# Tentative de mise à jour d'un plat inexistant
manager.update_item("Pizza", 20, "A", True)

# Suppression d'un plat (affiche le dictionnaire mis à jour)
manager.remove_item("French Fries")

