import linear_optics as lo
import numpy as np
import itertools as it
import json
from time import clock
from pprint import pprint
import sys
from circuit import *
from multiprocessing import Pool, cpu_count

sources=[sps(0), sps(2), sps(5), sps(7)]

def fitness(circuit):
    bell_patterns = [[0,6],[1,7]]
    herald_patterns = map(list, it.combinations([2,3,4,5], 2))
    interesting_patterns=[sorted(a+b) for a,b in it.product(bell_patterns, herald_patterns)]
    interesting_patterns=map(tuple, interesting_patterns)

    compiled=lo.compile(sources+circuit.json)
    compiled["patterns"]=interesting_patterns
    output_state = lo.simulate(**compiled)

    left_patterns=[tuple(sorted(bell_patterns[0]+b)) for b in herald_patterns]
    right_patterns=[tuple(sorted(bell_patterns[1]+b)) for b in herald_patterns]
    left_probability = sum([output_state[x] for x in left_patterns])
    right_probability = sum([output_state[x] for x in right_patterns])
    #print left_probability, right_probability
    #return left_probability*right_probability
    circuit.fitness=left_probability*right_probability

def crossover(a, b):
    if a.fitness>b.fitness:
        return a.copy()
    else:
        return b.copy()

if __name__=="__main__":
    # Specify the problem
    width=8; depth=20

    # Configure the optimizer
    generation_size=500
    mutation_probability=.3
    keep_fraction=.5

    # Primordial soup
    generation=[Circuit(True, width, depth) for i in range(generation_size)]

    # Get four processes
    #p=Pool(cpu_count())
    t=clock()
    while generation[0].fitness<10:
        # Evaluate fitness of this generation. Uses all four cores
        map(fitness, generation)

        # Survival of the fittest
        generation.sort(key=lambda c: c.fitness, reverse=True)
        best = generation[0].fitness
        average = np.average([c.fitness for c in generation])
        size = np.average([len(c.json) for c in generation])
        print "best=%.8f\taverage=%.8f\tsize=%.3f" % (best, average, size)
        generation=generation[:int((len(generation)-1)*keep_fraction)]

        compiled=lo.compile(sources+generation[0].json)
        output_state = lo.simulate(**compiled)
        for key, value in output_state.items(): 
            if value>0: print key, value

        # Draw a figure
        if clock()-t>.5: 
            sketch(sources+generation[0].json)
            t=clock()

        # Repoulate
        while len(generation)<generation_size:
            a=random.choice(generation)
            b=random.choice(generation)
            generation.append(crossover(a,b))

        # Mutate
        for c in generation:
            if np.random.rand() < mutation_probability:
                for i in range(3): c.mutate()


sketch(sources+generation[0].json)


