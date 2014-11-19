import linear_optics as lo
import numpy as np
import itertools as it
import json
from time import clock
from pprint import pprint
import sys
from circuit import *

def fitness(circuit):
    sources=[sps(0), sps(1), sps(4)]
    target_state = defaultdict(complex, {(2,3,4):1})
    compiled=lo.compile(sources+circuit.json)
    compiled["patterns"]=[(2,3,4)]

    output_state = lo.simulate(**compiled)
    return abs(lo.dinner(output_state, target_state))**2


# Start here
current=Circuit(True, 5, 5)
sources=[sps(0), sps(1), sps(4)]
sketch(sources+current.json)


for i in range(10000):
    alternative=current.copy()
    alternative.mutate()
    #alternative.mutate()
    current=alternative
    f1=fitness(alternative)
    f2=fitness(current)
    print f1, f2
    p=(1+f1-f2)/2.
    if np.random.rand()<p:
        current=alternative

    if f2==1: 
        print "success"
        sketch(sources+current)
        sys.exit(0)

print "fail"

