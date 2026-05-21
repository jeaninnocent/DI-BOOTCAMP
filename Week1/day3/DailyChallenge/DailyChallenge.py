from typing import List, Dict

class Farm:
    """Represents a farm with animals, their counts, and provides formatted information."""
    
    def __init__(self, farm_name: str) -> None:
        """Initializes the Farm with a name and an empty dictionary of animals."""
        self.name = farm_name
        self.animals: Dict[str, int] = {}

    def add_animal(self, animal_type: str = "", count: int = 1, **kwargs: int) -> None:
        """
        Adds animals to the farm.
        Handles single additions (animal_type, count) and multiple additions via **kwargs.
        """
        # Step 3: Handle traditional positional arguments
        if animal_type:
            # If the animal exists, add to its count, otherwise set it
            self.animals[animal_type] = self.animals.get(animal_type, 0) + count
            
        # Step 8 (Bonus): Handle multiple animals via **kwargs
        for animal, quantity in kwargs.items():
            self.animals[animal] = self.animals.get(animal, 0) + quantity

    def get_info(self) -> str:
        """Formats and returns the farm's information and animal counts."""
        # Using \n for new lines to match the exact requested output
        info_string = f"{self.name}'s farm\n\n"
        
        for animal, count in self.animals.items():
            info_string += f"{animal} : {count}\n"
            
        info_string += "\n    E-I-E-I-0!"
        return info_string

    def get_animal_types(self) -> List[str]:
        """Returns a sorted list of the animal types (keys) present in the farm."""
        return sorted(self.animals.keys())

    def get_short_info(self) -> str:
        """
        Returns a human-readable sentence about the animals in the farm,
        pluralizing the names if there is more than one.
        """
        animal_types = self.get_animal_types()
        formatted_animals = []
        
        for animal in animal_types:
            # Pluralize by adding 's' if count is greater than 1
            if self.animals[animal] > 1:
                # Even if 'sheep' plural is usually 'sheep', we follow the exercise example ('sheeps')
                formatted_animal = f"{animal}s"
            else:
                formatted_animal = animal
            formatted_animals.append(formatted_animal)
            
        # Join the animals list grammatically
        if len(formatted_animals) > 1:
            joined_animals = ", ".join(formatted_animals[:-1]) + f" and {formatted_animals[-1]}"
        elif len(formatted_animals) == 1:
            joined_animals = formatted_animals[0]
        else:
            joined_animals = "no animals"
            
        return f"{self.name}'s farm has {joined_animals}."


# --- Test de l'exercice ---
if __name__ == "__main__":
    print("--- STEP 5: Testing original requirements ---")
    macdonald = Farm("McDonald")
    macdonald.add_animal('cow', 5)
    macdonald.add_animal('sheep')
    macdonald.add_animal('sheep')
    macdonald.add_animal('goat', 12)
    
    print(macdonald.get_info())
    
    print("\n--- STEP 6 & 7: Testing get_animal_types and get_short_info ---")
    print("Animal types:", macdonald.get_animal_types())
    print("Short info:", macdonald.get_short_info())
    
    print("\n--- STEP 8: Testing **kwargs upgrade ---")
    new_farm = Farm("Old Town")
    # Python syntax requires keywords without quotes: cow=5, not 'cow'=5
    new_farm.add_animal(cow=5, sheep=2, goat=12, chicken=1) 
    print(new_farm.get_short_info())