import linear_optics as lo
import numpy as np
import itertools as it
import json
from time import clock
from pprint import pprint
import sys
from circuit import *

sources=[sps(0), sps(2), sps(5), sps(9)]
#detectors=[{"type":"bucket", "pos":posxy(5, y), "patterns":[y]} for y in (2,3,4)]

def fitness(circuit):
    target_state = defaultdict(complex, {(0,2,8,9):lo.ir2, (1,3,8,9):lo.ir2})
    compiled=lo.compile(sources+circuit.json)
    compiled["patterns"]=target_state.keys()
    #check_unitary(compiled["unitary"])
    output_state = lo.simulate(**compiled)
    return abs(lo.dinner(output_state, target_state))**2

def crossover(a, b):
    if a.fitness>b.fitness:
        return a.copy()
    else:
        return b.copy()

# Start here
width=10; depth=15
generation_size=500
mutation_probability=.3
keep_fraction=.5
generation=[Circuit(True, width, depth) for i in range(generation_size)]
t=clock()

while generation[0].fitness<1:
    # Evaluate - this should use four cores
    for c in generation:
        c.fitness=fitness(c)

    # Survival of the fittest
    generation.sort(key=lambda c: c.fitness, reverse=True)
    best = generation[0].fitness
    average = np.average([c.fitness for c in generation])
    size = np.average([len(c.json) for c in generation])
    print "best=%.3f\taverage=%.4f\tsize=%.3f" % (best, average, size)
    generation=generation[:int((len(generation)-1)*keep_fraction)]

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
            c.mutate()
            c.mutate()
            c.mutate()



