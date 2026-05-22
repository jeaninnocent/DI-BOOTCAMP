import math

class Pagination:
    def __init__(self, items=None, page_size=10):
        # Étape 2 : Initialisation avec gestion des paramètres par défaut
        self.items = items if items is not None else []
        self.page_size = int(page_size)  # Type casting (conversion en entier)
        self.current_idx = 0
        
        # Calcul du nombre total de pages à l'aide de math.ceil (arrondi au supérieur)
        if len(self.items) == 0:
            self.total_pages = 1
        else:
            self.total_pages = math.ceil(len(self.items) / self.page_size)

    def get_visible_items(self):
        # Étape 3 : Utilisation du "slicing" (découpage) de liste
        start_index = self.current_idx * self.page_size
        end_index = start_index + self.page_size
        return self.items[start_index:end_index]

    def go_to_page(self, page_num):
        # Étape 4 : Conversion de type et gestion d'erreurs (Exceptions)
        page_num = int(page_num)
        if page_num < 1 or page_num > self.total_pages:
            raise ValueError(f"Page {page_num} is out of bounds. Must be between 1 and {self.total_pages}.")
        
        # Les utilisateurs commencent à 1, mais notre index commence à 0
        self.current_idx = page_num - 1
        return self  # Permet le method chaining

    def first_page(self):
        self.current_idx = 0
        return self  # Permet le method chaining

    def last_page(self):
        self.current_idx = self.total_pages - 1
        return self  # Permet le method chaining

    def next_page(self):
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self  # Permet le method chaining

    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        return self  # Permet le method chaining

    def __str__(self):
        # Bonus Étape 5 : Méthode magique pour un affichage personnalisé
        visible_items = self.get_visible_items()
        # On convertit chaque élément en string pour être sûr que join() fonctionne
        return "\n".join(str(item) for item in visible_items)


# ==========================================
# TESTS SCRIPT (Vérification de l'énoncé)
# ==========================================
if __name__ == "__main__":
    alphabetList = list("abcdefghijklmnopqrstuvwxyz")
    p = Pagination(alphabetList, 4)

    print("--- Test Base ---")
    print(p.get_visible_items()) 
    # Output: ['a', 'b', 'c', 'd']

    p.next_page()
    print(p.get_visible_items()) 
    # Output: ['e', 'f', 'g', 'h']

    p.last_page()
    print(p.get_visible_items()) 
    # Output: ['y', 'z']

    print("\n--- Test __str__ Bonus ---")
    p.first_page()
    print(str(p))
    # Output: 
    # a
    # b
    # c
    # d

    print("\n--- Test Method Chaining Bonus ---")
    # Attention : L'énoncé bonus mentionne "nextPage()", mais la convention Python PEP 8 
    # et l'étape 4 exigent "next_page()". J'ai gardé "next_page()" pour te garantir
    # une syntaxe professionnelle parfaite.
    result = p.first_page().next_page().next_page().next_page().get_visible_items()
    print(result) 
    # Output: ['m', 'n', 'o', 'p']

    print("\n--- Test Exception ---")
    try:
        p.go_to_page(10)
    except ValueError as e:
        print(f"Erreur capturée avec succès : {e}")