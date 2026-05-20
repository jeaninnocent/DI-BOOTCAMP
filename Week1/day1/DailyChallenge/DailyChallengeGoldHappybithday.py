# 1. On demande la date
date_utilisateur = input("Enter your birthdate (DD/MM/YYYY): ")

# 2. On récupère juste les 4 derniers caractères tapés (l'année) et on le transforme en nombre
annee_naissance = int(date_utilisateur[-4:])

# 3. On calcule l'âge manuellement (on fixe l'année actuelle à 2026)
annee_actuelle = 2026
age = annee_actuelle - annee_naissance

# 4. Le dernier chiffre de l'âge donne le nombre de bougies
nb_bougies = age % 10

# 5. Calcul pour centrer les bougies sur les 11 espaces disponibles
tirets_restants = 11 - nb_bougies
t_gauche = "_" * (tirets_restants // 2)
t_droite = "_" * (tirets_restants - (tirets_restants // 2))

# On construit le "toit" du gâteau
ligne_bougies = t_gauche + ("i" * nb_bougies) + t_droite

# 6. On dessine notre gâteau dans un bloc de texte multi-lignes
gateau = f"""
      {ligne_bougies}
     |:H:a:p:p:y:|
   __|___________|__
  |^^^^^^^^^^^^^^^^^|
  |:B:i:r:t:h:d:a:y:|
  |                 |
  ~~~~~~~~~~~~~~~~~~~
"""

# 7. On affiche le résultat de base
print(f"\nYou are {age} years old!")
print(gateau)

# 8. Bonus : le calcul de l'année bissextile (divisible par 4, mais attention aux centaines)
if (annee_naissance % 4 == 0 and annee_naissance % 100 != 0) or (annee_naissance % 400 == 0):
    print("Bonus : You were born on a leap year! Here is a second cake:")
    print(gateau) # On réaffiche exactement le même dessin