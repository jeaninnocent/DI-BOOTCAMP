import random

# 1. Base Class (Inheritance & Polymorphism)
class BiologicalSequence:
    def __init__(self):
        self.components = []

    def mutate(self):
        """
        Polymorphic method: Iterates through its components and has a 
        50% chance to trigger their specific mutate() method.
        """
        for component in self.components:
            if random.random() <= 0.5:
                component.mutate()

    def is_perfect(self):
        """Checks if all components have reached the target state (all 1s)."""
        return all(component.is_perfect() for component in self.components)


# 2. Gene Class
class Gene:
    def __init__(self):
        # A gene starts as a random 0 or 1
        self.value = random.choice([0, 1])

    def mutate(self):
        """Flips the gene value."""
        self.value = 1 if self.value == 0 else 0

    def is_perfect(self):
        return self.value == 1


# 3. Chromosome Class (Inherits from BiologicalSequence)
class Chromosome(BiologicalSequence):
    def __init__(self):
        super().__init__()
        # A Chromosome is composed of 10 Genes
        self.components = [Gene() for _ in range(10)]


# 4. DNA Class (Inherits from BiologicalSequence)
class DNA(BiologicalSequence):
    def __init__(self):
        super().__init__()
        # A DNA is composed of 10 Chromosomes
        self.components = [Chromosome() for _ in range(10)]


# 5. Organism Class
class Organism:
    def __init__(self, environment_prob):
        self.dna = DNA()
        self.environment_prob = environment_prob
        self.generations = 0

    def live_and_mutate(self):
        self.generations += 1
        # The environment dictates the probability of the DNA mutating
        if random.random() <= self.environment_prob:
            self.dna.mutate()
        
        return self.dna.is_perfect()


# ==========================================
# TEST SCRIPT & SIMULATION
# ==========================================
if __name__ == "__main__":
    population_size = 50
    environment_mutation_rate = 0.8
    # Failsafe limit to prevent infinite loops (see conclusion below)
    max_generations = 500_000 
    
    # Instantiate a number of organisms
    population = [Organism(environment_mutation_rate) for _ in range(population_size)]
    
    print(f"Starting simulation with {population_size} organisms...")
    
    simulation_ended = False
    for generation in range(1, max_generations + 1):
        for i, organism in enumerate(population):
            if organism.live_and_mutate():
                print(f"🧬 SUCCESS! Organism {i} reached perfect DNA in {organism.generations} generations.")
                simulation_ended = True
                break
        
        if simulation_ended:
            break
            
        if generation % 100_000 == 0:
            print(f"Reached generation {generation}... no perfect DNA yet.")
            
    if not simulation_ended:
        print(f"Simulation stopped at {max_generations} generations. No perfect DNA achieved.")