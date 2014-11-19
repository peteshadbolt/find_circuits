import linear_optics as lo
import numpy as np
from numpy.random import randint
from collections import defaultdict
import itertools as it
import json
from time import clock
from pprint import pprint
import sys

generators = [lambda x,y: {"type":"crossing", "pos": posxy(x,y)}, lambda x,y: {"type":"coupler", "ratio":.5, "pos": posxy(x,y)}]

bp = lambda y: {"type": "bellpair", "pos": posxy(-1, y)}
sps = lambda y: {"type": "sps", "pos": posxy(-1, y)}
bucket = lambda y: {"type": "bucket", "pos": posxy(100, y)}

def sketch(circuit):
    s=json.dumps(circuit)
    f=open("viewer/scripts/mycircuit.js", "w")
    f.write(s)
    f.close()

def collision(a,b):
    if a["x"]!=b["x"]: return False
    if a["bottom"]<b["y"]: return False
    if b["bottom"]<a["y"]: return False
    return True

def mutate_add(circuit):
    """ Find an empty slot, and add a component """
    x=randint(0, depth); y=randint(0, width)
    a=generators[randint(len(generators))](x,y)
    for c in circuit:
        b=lo.fill_gaps(c)
        q=lo.fill_gaps(a)
        if collision(q,b): return
    circuit.append(a)

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
    compiled["patterns"]=[(2,3,4)]
    u=np.matrix(compiled["unitary"])
    if not np.allclose(u*u.H, np.eye(len(u))):
        print u.round(1)
        pprint(circuit)
        sketch(circuit)
        sys.exit(0)
    output_state = lo.simulate(**compiled)
    return abs(lo.dinner(output_state, target_state))**2


p2=np.pi/2.; p4=np.pi/4.
posxy = lambda x,y: {"x":x, "y":y}
depth=5
width=5
sources=[sps(0), sps(1), sps(4)]
target_state = defaultdict(complex, {(2,3,4):1})


# Start here
current=random_circuit(100)

for i in range(100000):
    alternative=list(current)
    mutate(alternative)
    mutate(alternative)
    f1=fitness(alternative)
    f2=fitness(current)
    p=(1+f1-f2)/2.
    if np.random.rand()<p:
        current=alternative

    if f2==1: 
        print "success"
        sketch(sources+current)
        sys.exit(0)

print "fail"

