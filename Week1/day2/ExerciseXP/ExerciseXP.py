# ==========================================
#  Exercice 1 : Convertir des listes en dictionnaires
# ==========================================
print("--- Exercice 1 ---")
keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

# Utilisation de la fonction zip pour combiner les listes et dict() pour convertir
result_dict = dict(zip(keys, values))
print(result_dict)


# ==========================================
#  Exercice 2 : Cinemax #2
# ==========================================
print("\n--- Exercice 2 ---")
family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}
total_cost = 0

# Boucle à travers le dictionnaire pour calculer le prix selon l'âge
for name, age in family.items():
    if age < 3:
        price = 0
    elif 3 <= age <= 12:
        price = 10
    else:
        price = 15
    print(f"Ticket price for {name.capitalize()} (age {age}): ${price}")
    total_cost += price

print(f"Total cost for the family: ${total_cost}")

# Bonus (Commenté pour éviter de bloquer l'exécution du script avec input)
"""
custom_cost = 0
while True:
    name = input("Enter family member's name (or 'quit' to stop): ")
    if name.lower() == 'quit':
        break
    age = int(input(f"Enter {name}'s age: "))
    if age < 3:
        custom_cost += 0
    elif 3 <= age <= 12:
        custom_cost += 10
    else:
        custom_cost += 15
print(f"Total custom cost: ${custom_cost}")
"""


# ==========================================
#  Exercice 3 : Zara
# ==========================================
print("\n--- Exercice 3 ---")
brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": ["blue"],
        "Spain": ["red"],
        "US": ["pink", "green"]
    }
}

# 1. Modifier le nombre de magasins
brand["number_stores"] = 2

# 2. Imprimer une phrase décrivant les clients
clients = ", ".join(brand["type_of_clothes"])
print(f"Zara creates clothes for {clients}.")

# 3. Ajouter la clé country_creation
brand["country_creation"] = "Spain"

# 4. Vérifier si international_competitors existe et ajouter "Desigual"
if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")

# 5. Supprimer la date de création
brand.pop("creation_date", None)

# 6. Imprimer le dernier concurrent international
print("Last competitor:", brand["international_competitors"][-1])

# 7. Imprimer les couleurs principales aux US
print("Major colors in the US:", ", ".join(brand["major_color"]["US"]))

# 8. Imprimer le nombre de clés
print("Number of keys:", len(brand))

# 9. Imprimer toutes les clés
print("Keys in dictionary:", list(brand.keys()))

# Bonus : Fusionner un nouveau dictionnaire
more_on_zara = {
    "creation_date": 1975,
    "number_stores": 10000
}
brand.update(more_on_zara)
print("Updated brand dictionary:", brand)


# ==========================================
#  Exercice 4 : Un peu de géographie
# ==========================================
print("\n--- Exercice 4 ---")
def describe_city(city, country="Unknown"):
    print(f"{city} is in {country}.")

describe_city("Reykjavik", "Iceland")
describe_city("Paris")


# ==========================================
#  Exercice 5 : Aléatoire
# ==========================================
print("\n--- Exercice 5 ---")
import random

def guess_number(user_number):
    random_number = random.randint(1, 100)
    if user_number == random_number:
        print("Success!")
    else:
        print(f"Fail! Your number: {user_number}, Random number: {random_number}")

# Appel de la fonction avec un nombre
guess_number(50)


# ==========================================
#  Exercice 6 : Créons des t-shirts personnalisés !
# ==========================================
print("\n--- Exercice 6 ---")
def make_shirt(size="large", text="I love Python"):
    print(f"The size of the shirt is {size} and the text is {text}.")

# Appels multiples avec et sans valeurs par défaut
make_shirt()
make_shirt("medium")
make_shirt("small", "Custom message")
# Bonus : Arguments nommés
make_shirt(size="XL", text="Hello!")


# ==========================================
# Exercice 7 : Conseils de température
# ==========================================
print("\n--- Exercice 7 ---")
# Bonus inclus : Nombres flottants (random.uniform) et gestion des saisons
def get_random_temp(season):
    if season == "winter":
        return round(random.uniform(-10.0, 16.0), 1)
    elif season in ["spring", "autumn"]:
        return round(random.uniform(10.0, 23.0), 1)
    elif season == "summer":
        return round(random.uniform(24.0, 40.0), 1)
    else:
        return round(random.uniform(-10.0, 40.0), 1)

def main_temp():
    # Simulation du choix de l'utilisateur pour le mois (ex: mois 8 pour août)
    month = 8 
    
    if month in [12, 1, 2]:
        season = "winter"
    elif month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8]:
        season = "summer"
    elif month in [9, 10, 11]:
        season = "autumn"
    else:
        season = "unknown"

    temp = get_random_temp(season)
    print(f"The temperature right now is {temp} degrees Celsius.")

    if temp < 0:
        print("Brrr, that’s freezing! Wear some extra layers today.")
    elif 0 <= temp <= 16:
        print("Quite chilly! Don’t forget your coat.")
    elif 16 < temp <= 23:
        print("Nice weather.")
    elif 23 < temp <= 32:
        print("A bit warm, stay hydrated.")
    elif 32 < temp <= 40:
        print("It’s really hot! Stay cool.")

main_temp()


# ==========================================
# Exercice 8 : Garnitures de pizza
# ==========================================
print("\n--- Exercice 8 ---")
def order_pizza():
    toppings = []
    base_price = 10.0
    topping_price = 2.50
    
    # Simulation d'entrées utilisateur pour permettre l'exécution directe
    print("(Simulation de la boucle while utilisateur)")
    simulated_inputs = ["cheese", "mushrooms", "peppers", "quit"]
    
    for user_input in simulated_inputs:
        if user_input == 'quit':
            break
        print(f"Adding {user_input} to your pizza.")
        toppings.append(user_input)
        
    total_cost = base_price + (len(toppings) * topping_price)
    
    print(f"\nFinal Pizza Toppings: {', '.join(toppings)}")
    print(f"Total cost of the pizza: ${total_cost:.2f}")

order_pizza()