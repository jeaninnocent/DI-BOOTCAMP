import time
import os

class GameOfLife:
    def __init__(self, rows=20, cols=20, initial_cells=None, infinite_borders=False):
        """
        Initialise le jeu.
        :param rows: Nombre de lignes (pour les bordures fixes ou l'affichage).
        :param cols: Nombre de colonnes (pour les bordures fixes ou l'affichage).
        :param initial_cells: Liste de tuples (r, c) représentant les cellules vivantes au départ.
        :param infinite_borders: Booléen. Si True, la grille n'a pas de limites (Bonus).
        """
        self.rows = rows
        self.cols = cols
        self.infinite_borders = infinite_borders
        
        # On utilise un set pour stocker uniquement les cellules vivantes.
        # Cela évite de stocker des milliers de cellules mortes en mémoire (parfait pour le bonus).
        self.live_cells = set(initial_cells) if initial_cells else set()

    def _get_neighbors(self, r, c):
        """Retourne les coordonnées des 8 voisins d'une cellule."""
        neighbors = [
            (r-1, c-1), (r-1, c), (r-1, c+1),
            (r, c-1),             (r, c+1),
            (r+1, c-1), (r+1, c), (r+1, c+1)
        ]
        
        if self.infinite_borders:
            return neighbors
        
        # Si bordures fixes, on filtre les voisins qui sortent du cadre
        valid_neighbors = []
        for nr, nc in neighbors:
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                valid_neighbors.append((nr, nc))
        return valid_neighbors

    def next_generation(self):
        """Calcule la génération suivante selon les 4 règles de Conway."""
        neighbor_counts = {}
        
        # 1. Compter les voisins pour chaque cellule vivante et ses voisines immédiates
        for r, c in self.live_cells:
            # S'assurer que la cellule vivante est dans le dictionnaire (même avec 0 voisin)
            if (r, c) not in neighbor_counts:
                neighbor_counts[(r, c)] = 0
                
            for nr, nc in self._get_neighbors(r, c):
                if (nr, nc) not in neighbor_counts:
                    neighbor_counts[(nr, nc)] = 0
                neighbor_counts[(nr, nc)] += 1

        new_live_cells = set()
        
        # 2. Appliquer les règles pour déterminer qui vit ou meurt
        for cell, count in neighbor_counts.items():
            if cell in self.live_cells:
                # Règle 2 : Une cellule vivante avec 2 ou 3 voisins survit.
                # (Les règles 1 et 3 sont implicitement gérées car on ne l'ajoute pas si < 2 ou > 3)
                if count in (2, 3):
                    new_live_cells.add(cell)
            else:
                # Règle 4 : Une cellule morte avec exactement 3 voisins naît par reproduction.
                if count == 3:
                    # Vérification de sécurité pour les bordures fixes
                    if self.infinite_borders or (0 <= cell[0] < self.rows and 0 <= cell[1] < self.cols):
                        new_live_cells.add(cell)

        self.live_cells = new_live_cells

    def display(self):
        """Affiche la grille dans la console."""
        # Nettoie la console pour créer une animation fluide (Windows ou Linux/Mac)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Si infini, la caméra "suit" les cellules. Sinon, la caméra reste fixe.
        if self.infinite_borders and self.live_cells:
            min_r = min(r for r, c in self.live_cells) - 1
            max_r = max(r for r, c in self.live_cells) + 1
            min_c = min(c for r, c in self.live_cells) - 1
            max_c = max(c for r, c in self.live_cells) + 1
        else:
            min_r, max_r = 0, self.rows - 1
            min_c, max_c = 0, self.cols - 1

        for r in range(min_r, max_r + 1):
            row_str = ""
            for c in range(min_c, max_c + 1):
                if (r, c) in self.live_cells:
                    row_str += "██ " # Cellule vivante
                else:
                    row_str += ".  "  # Cellule morte
            print(row_str)
        print("=" * (max_c - min_c + 1) * 3)

    def play(self, generations, delay=0.3):
        """Lance la simulation pour un nombre donné de générations."""
        for i in range(generations):
            print(f"--- Generation {i + 1} ---")
            self.display()
            
            if not self.live_cells:
                print("All cells died. Extinction.")
                break
                
            self.next_generation()
            time.sleep(delay)


# ==========================================
# TEST SCRIPT (Modèles initiaux intéressants)
# ==========================================
if __name__ == "__main__":
    # Motif 1 : Le "Blinker" (Clignotant) - Oscille entre deux états
    blinker_cells = [(5, 5), (5, 6), (5, 7)]
    
    # Motif 2 : Le "Glider" (Planeur) - Se déplace en diagonale
    glider_cells = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    
    print("Choisissez le mode de test :")
    print("1. Bordures Fixes avec un Blinker (Oscillateur)")
    print("2. Bordures Infinies (BONUS) avec un Glider (Vaisseau en mouvement)")
    
    choice = input("Votre choix (1 ou 2) : ")
    
    if choice == '1':
        game = GameOfLife(rows=10, cols=10, initial_cells=blinker_cells, infinite_borders=False)
        game.play(generations=10, delay=0.5)
    elif choice == '2':
        # Avec les bordures infinies, la caméra va suivre le Glider à l'infini !
        game = GameOfLife(initial_cells=glider_cells, infinite_borders=True)
        game.play(generations=30, delay=0.2)
    else:
        print("Choix invalide.")