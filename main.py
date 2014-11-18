import linear_optics as lo
import numpy as np
from numpy.random import randint
from collections import defaultdict
import itertools as it
import json
from time import clock
from pprint import pprint
import sys

generators = [lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":0.5},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/3.},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/4.},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p2},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p4},
              lambda x,y: {"type":"crossing", "pos": posxy(x,y)}]

bp = lambda y: {"type": "bellpair", "pos": posxy(-1, y)}
sps = lambda y: {"type": "sps", "pos": posxy(-1, y)}
bucket = lambda y: {"type": "bucket", "pos": posxy(100, y)}

def sketch(circuit):
    s=json.dumps(circuit)
    f=open("viewer/scripts/mycircuit.js", "w")
    f.write(s)
    f.close()

def mutate_add(circuit):
    """ Find an empty slot, and add a component """
    x=randint(0, depth); y=randint(0, width)
    for c in circuit:
        q=lo.fill_gaps(c)
        if q["x"]==x and q["y"]<=y<=q["bottom"]: return
    circuit.append(generators[randint(len(generators))](x,y))

def mutate_delete(circuit):
    """ Find an occupied slot, and delete a component """
    n=len(circuit)
    if n>0: del circuit[randint(len(circuit))]

def mutate(circuit):
    """ Either add or remove a component """
    if np.random.rand()>.3:
        mutate_add(circuit)
    else:
        mutate_delete(circuit)

def random_circuit(count):
    """ Generate a new random circuit """
    circuit=[]
    for i in range(count):
        mutate_add(circuit)
    return circuit

def fitness(circuit):
    compiled=lo.compile(sources+circuit)
    compiled["patterns"]=[(0,1)]
    u=np.matrix(compiled["unitary"])
    if not np.allclose(u*u.H, np.eye(len(u))):
        print u.round(1)
        sketch(circuit)
        sys.exit(0)
    output_state = lo.simulate(**compiled)
    return abs(lo.dinner(output_state, target_state))


p2=np.pi/2.; p4=np.pi/4.
posxy = lambda x,y: {"x":x, "y":y}
depth=5
width=5
sources=[sps(0), sps(2)]
target_state = defaultdict(complex, {(0,1):1})


# Start here
current=random_circuit(100)

t=clock()
for temperature in np.linspace(1, 0, 1000):
    alternative=list(current)
    mutate(alternative)
    f1=fitness(alternative)
    f2=fitness(current)
    if f1>f2:
        current=alternative
    print f2


    # Sketch twice per second
    if clock()-t>0.5:
        t=clock()
        sketch(sources+current)

