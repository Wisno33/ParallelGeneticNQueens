import string
import math
import itertools
import random
import multiprocessing

# Get all printable ascii chars to and map them to a int in order.
# This is used to map multiple digit ints to a single char for encoding
# purposes.
chars = string.printable
char_encodeing = {c:e for e,c in enumerate(chars)}


# Encode the state of the board as a string.
# Where the position i in the string is the row and
# char at i is the encoded value for the column.
def string_encoder(n):

    s = ''

    # Chose from the first n possible chars.
    for x in range(n):
        s += random.choice(chars[0:n])

    return s

# Counts the number of attacking queen pairs. Max C(n,2)
def pairs_attacked_check(s, n):

    # Generate all possible queen pair combinations.
    queen_pairs = itertools.combinations(range(n), 2)
    pairs_attacked_map = {qp : False for qp in queen_pairs}

    # Simulates a look over a 2D chess board.
    for e,i in enumerate(s):
        for f,j in enumerate(s):
            if e == f: # Same queen or all ready checked pair.
                continue
            if i == j: # Same column.
                if (e,f) in pairs_attacked_map.keys():
                    pairs_attacked_map[(e,f)] = True
            elif abs(char_encodeing[i] - char_encodeing[j]) == f-e: # Diagonal.
                if (e,f) in pairs_attacked_map.keys():
                    pairs_attacked_map[(e,f)] = True

    attacked_pairs = 0

    # Count the number of attacked pairs.
    for a in pairs_attacked_map.values():
        if a:
            attacked_pairs += 1

    return attacked_pairs

# Returns the fitness of a given state.
def fitness(s, n, max_fitness):

    return max_fitness - pairs_attacked_check(s, n)

# Computes the probability of selection and normalizes it for the data set.
def compute_selection_probabilities(population_fitnesses):

    fitness_list = [pf[1] for pf in population_fitnesses]

    # Get the sum of the fitnesses to be the normalization constant.
    normalization_constant = sum(fitness_list)

    # If the sum of the fitnesses is 0 assign all an equal probability.
    if normalization_constant == 0:
        return [(pf[0], 1/len(population_fitnesses)) for pf in population_fitnesses]

    # Normalize data.
    return [(pf[0], pf[1]/normalization_constant) for pf in population_fitnesses]

# Select the parents that will present for the cross over via fitness based probabilities.
def selection(population_selection_chances):

    return random.choices(population_selection_chances, 
                            weights=tuple([p[1] for p in population_selection_chances]),
                            k=len(population_selection_chances))

# Cross over the "DNA" string state for each sequential pair in the population.
def cross_over(parents, n):

    # The next generation states.
    children = list()

    # Loop through all parents by 2 and create 2 children from the 2 parents.
    # Using a random index to split the "gene" or state the merge the 2 together.
    for i in range(0, len(parents), 2):

        split_index = random.randint(1, n-2)

        # Take i's first split_index section and append the section after the split_index of i+1.
        children.append(parents[i][0:split_index] + parents[i+1][split_index:n])
        # Reverse the above.
        children.append(parents[i+1][0:split_index] + parents[i][split_index:n])

    return children

# Mutate a state by changing at most one element.
def mutate(population, n):

    children = list()

    # For each individual in the population choose 0 or 1. If 1 mutate a random index. 
    # Else nothing.
    for p in population:

        if random.randint(0, 1) == 1:
            gene = list(p)
            gene[random.randint(0, n-1)] = random.choice(chars[0:n])
            children.append(''.join(gene))
        else:
            children.append(p)

    return children
             
# Genetic n_queens solver algorithm.
def n_queens(n, is_solved, solution, original_pop_size=4):

    # No solutions exist for 2 or 3 -queens.
    if n == 2 or n == 3:
        return

    population = list()

    # Generate a population with size = original_pop_size.
    for _ in range(original_pop_size):
        population.append(string_encoder(n)) # Encode the state as a string.and

    # Number of queen pairs. 
    queen_pairs = len(list(itertools.combinations(range(n), 2)))

    generation = 0 # Track the current generation.

    while is_solved.value == 0:

        # Check if a member of the population is a valid solution.
        for p in population:
            if pairs_attacked_check(p, n) == 0:
                print(p)
                for i,c in enumerate(p):
                    solution[i] = char_encodeing[c] # Set the valid solution.
                is_solved.value = 1

        # Compute the fitnesses for all members of the population.
        population_fitnesses = [(p, fitness(p, n, queen_pairs)) for p in population]
        fitnesses = [f[1] for f in population_fitnesses]

        '''print(f'Highest fitness for {multiprocessing.current_process().name}: ' +
                f'generation {generation} is {max(fitnesses)}')'''

        # Compute the normalized probabilities based on the fitnesses of the population.
        population_selection_chances = compute_selection_probabilities(
                            population_fitnesses)

        # Sort the population such that the best individuals cross.
        #population_selection_chances = sorted(population_selection_chances, 
                                       # key= lambda a: a[1])[::-1]

        # Chose the parents for the next generation.
        chosen = selection(population_selection_chances)

        # Sort the chosen by highest selection probability (i.e fitness) so that
        # the highest fitness individuals pair.
        chosen = sorted(chosen, key= lambda a: a[1])[::-1]

        parents = [c[0] for c in chosen]

        # Crossed pairs / children / generation current + 1.
        children = cross_over(parents, n)

        # Mutate by possibly changing 1 char of the state.

        population  = mutate(children, n)

        generation += 1




        





    

                
                

        



