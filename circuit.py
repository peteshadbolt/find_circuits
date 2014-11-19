import linear_optics as lo
import numpy as np
from numpy.random import randint
from collections import defaultdict
import itertools as it
import json, random

p2=np.pi/2.; p4=np.pi/4.
posxy = lambda x,y: {"x":x, "y":y}
building_blocks = [lambda x,y: {"type":"crossing", "pos": posxy(x,y)}, lambda x,y: {"type":"coupler", "ratio":.5, "pos": posxy(x,y)}]
bp = lambda y: {"type": "bellpair", "pos": posxy(-1, y)}
sps = lambda y: {"type": "sps", "pos": posxy(-1, y)}
bucket = lambda y: {"type": "bucket", "pos": posxy(100, y)}

def check_unitary(u):
    u=np.matrix(u)
    if not np.allclose(u*u.H, np.eye(len(u))):
        print "not unitary!"; raw_input()

def collision(a,b):
    c=lo.fill_gaps(a); d=lo.fill_gaps(b)
    if c["x"]!=d["x"]: return False
    if c["bottom"]<d["y"]: return False
    if d["bottom"]<c["y"]: return False
    return True

def sketch(data):
    """ Dump to a file for drawing in the browser """
    s=json.dumps(data)
    f=open("viewer/scripts/mycircuit.js", "w")
    f.write(s); f.close()


class Circuit(object):
    def __init__(self, initialize=False, width=5, depth=5):
        self.width, self.depth=width, depth
        self.json=[]
        if initialize: self.init_random()

    def init_random(self, count=10):
        """ Generate a new random circuit """
        self.json=[]
        for i in range(count):
            self.mutate_add()

    def copy(self):
        """ Get a copy """
        c=Circuit(False, self.width, self.depth)
        c.json=[x.copy() for x in self.json]
        return c

    def mutate_add(self):
        """ Find an empty slot, and add a component """
        x = randint(self.depth)
        y = randint(self.width)
        new_component = random.choice(building_blocks)(x,y)
        for c in self.json:
            if collision(c, new_component): return
        self.json.append(new_component)

    def mutate_delete(self):
        """ Find an occupied slot, and delete a component """
        n=len(self.json)
        if n>0: del self.json[randint(len(self.json))]

    def mutate(self):
        """ Either add or remove a component """
        if np.random.rand()>.3:
            self.mutate_add()
        else:
            self.mutate_delete()

