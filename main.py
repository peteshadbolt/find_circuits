import linear_optics as lo
import numpy as np
from numpy.random import randint
from collections import defaultdict
import itertools as it
import json

p2=np.pi/2.; p4=np.pi/4.
posxy = lambda x,y: {"x":x, "y":y}
depth=10
width=10
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
    s="var myCircuitJSON="+json.dumps(circuit)
    f=open("viewer/scripts/mycircuit.js", "w")
    f.write(s)
    f.close()

def mutate_add(circuit):
    """ Find an empty slot, and add a component """
    x=randint(0, depth); y=randint(0, width)
    for c in circuit:
        q=c.copy()
        lo.fill_gaps(q)
        if q["x"]==x and q["y"]<=y<=q["bottom"]: return
    circuit.append(generators[randint(len(generators))](x,y))

def mutate_delete(circuit):
    """ Find an occupied slot, and delete a component """
    n=len(circuit)
    if n>0: del circuit[randint(len(circuit))]

def get_output(sources, dna, patterns):
    circuit=lo.compile_circuit(sources+dna)
    circuit.patterns=patterns
    return lo.simulate(**circuit)

def random_circuit(count):
    circuit=[]
    for i in range(count):
        mutate_add(circuit)

    for i in range(30):
        mutate_delete(circuit)
    return circuit

sources=[sps(y) for y in range(2)]
detectors=[bucket(y) for y in range(2)]
dna=random_circuit(100)

sketch(sources+dna)

#print get_output(sources, dna, detectors)
