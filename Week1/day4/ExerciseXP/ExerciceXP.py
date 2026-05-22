##Exercice1
class Pets:
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat:
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'

# Step 1: Create the Siamese class
class Siamese(Cat):
    pass # Le mot-clé 'pass' indique qu'on hérite de Cat sans ajouter de nouvelles méthodes

# Step 2: Create a list of cat instances
bengal_obj = Bengal("Simba", 3)
chartreux_obj = Chartreux("Luna", 5)
siamese_obj = Siamese("Nala", 2)

all_cats = [bengal_obj, chartreux_obj, siamese_obj]

# Step 3: Create a Pets instance
sara_pets = Pets(all_cats)

# Step 4: Take cats for a walk
sara_pets.walk()

##Exercice2
class Dog:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        return f"{self.name} is barking"

    def run_speed(self):
        return (self.weight / self.age) * 10

    def fight(self, other_dog):
        # Calcul de la puissance de chaque chien
        my_power = self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight
        
        if my_power > other_power:
            return f"{self.name} won the fight against {other_dog.name}!"
        elif my_power < other_power:
            return f"{other_dog.name} won the fight against {self.name}!"
        else:
            return f"The fight between {self.name} and {other_dog.name} is a draw!"

# Step 2: Create dog instances
dog1 = Dog("Rex", 4, 30)
dog2 = Dog("Max", 2, 20)
dog3 = Dog("Rocky", 5, 45)

# Step 3: Test dog methods
print(dog1.bark())
print(f"Speed of {dog2.name}: {dog2.run_speed()}")
print(dog1.fight(dog2))
print(dog3.fight(dog1))

##Exercice3
import random
# Dans un vrai projet, on utiliserait : from nom_du_fichier import Dog
# Pour tester ici, on assume que la classe Dog (ci-dessus) est déjà définie.

class PetDog(Dog):
    def __init__(self, name, age, weight):
        # super() appelle la méthode __init__ de la classe parente (Dog)
        super().__init__(name, age, weight)
        self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        # On gère le cas où l'utilisateur passe des objets Dog OU des chaînes de caractères (comme dans l'exemple)
        dog_names = [dog.name if hasattr(dog, 'name') else dog for dog in args]
        all_names = ", ".join(dog_names)
        print(f"{self.name}, {all_names} all play together")

    def do_a_trick(self):
        if self.trained:
            tricks = [
                "does a barrel roll", 
                "stands on his back legs", 
                "shakes your hand", 
                "plays dead"
            ]
            print(f"{self.name} {random.choice(tricks)}")
        else:
            print(f"{self.name} is not trained yet!")

# Test PetDog methods
my_dog = PetDog("Fido", 2, 10)

my_dog.train() # Affiche l'aboiement et entraîne le chien
my_dog.play("Buddy", "Max") # Test avec les arguments de l'énoncé
my_dog.do_a_trick() # Affiche un tour aléatoire

##Exercice4
class Person:
    def __init__(self, first_name, age, last_name=""):
        self.first_name = first_name
        self.age = age
        self.last_name = last_name

    def is_18(self):
        return self.age >= 18

class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = [] # Initialisé comme une liste vide

    def born(self, first_name, age):
        # Création de l'objet Person et ajout à la liste
        new_person = Person(first_name, age, self.last_name)
        self.members.append(new_person)
        print(f"Congratulations! {first_name} was born into the {self.last_name} family.")

    def check_majority(self, first_name):
        # Recherche du membre dans la famille
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print("You are over 18, your parents Jane and John accept that you will go out with your friends")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return # On arrête la recherche une fois la personne trouvée
        print(f"Person named {first_name} not found in this family.")

    def family_presentation(self):
        print(f"\n--- The {self.last_name} Family Presentation ---")
        for member in self.members:
            print(f"- {member.first_name} {member.last_name}, Age: {member.age}")


# Test du comportement attendu
smith_family = Family("Smith")

# Ajout de membres avec la méthode born()
smith_family.born("Michael", 45)
smith_family.born("Sarah", 15)
smith_family.born("David", 20)

print("\n--- Checking Majority ---")
# Vérification de la majorité
smith_family.check_majority("Sarah") # Devrait refuser
smith_family.check_majority("David") # Devrait accepter

# Affichage de la famille
smith_family.family_presentation()
