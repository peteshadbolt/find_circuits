import linear_optics as lo
import numpy as np
from collections import defaultdict
import itertools as it
import json

p2=np.pi/2.; p4=np.pi/4.
posxy = lambda x,y: {"x":x, "y":y}
generators = [lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":0.5},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/3.},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/4.},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p2},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p4},
              lambda x,y: {"type":"crossing", "pos": posxy(x,y)}]

def sketch(circuit):
    s="var myCircuitJSON="+json.dumps(circuit)
    f=open("viewer/scripts/mycircuit.js", "w")
    f.write(s)
    f.close()

def get_output(sources, dna):
    circuit=lo.compile_circuit(sources+dna)
    circuit.patterns=patterns
    return lo.simulate(**circuit)

bp = lambda y: {"type": "bellpair", "pos": posxy(-1, y)}
sps = lambda y: {"type": "sps", "pos": posxy(-1, y)}
bucket = lambda y: {"type": "bucket", "pos": posxy(100, y)}
sources=[sps(y) for y in range(10)]
detectors=[bucket(y) for y in range(2)]

dna=[generators[0](2,2)]
sketch(sources+dna)

#print get_output(sources, dna, detectors)
