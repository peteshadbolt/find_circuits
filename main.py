import linear_optics as lo
import numpy as np
from collections import defaultdict

p2=np.pi/2.; p4=np.pi/4.
posxy = lambda x,y: {"x":x, "y":y}
generators = [lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":0.5},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/3.},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/4.},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p2},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p4},
              lambda x,y: {"type":"crossing", "pos": posxy(x,y)}]

def base_circuit():
    return [{"type": "bellpair", "pos": posxy(-1,0)}]

# TODO: ensure that we make valid circuits
def fitness(dna):
    circuit=base_circuit()
    target=defaultdict(complex, {(0,2):lo.ir2, (1,3):lo.ir2})
    h,w=dna.shape
    for i in range(w):
        for j in range(h):
            if dna[j,i]>=0: circuit.append(generators[dna[j,i]](i,j*2))
    circuit=lo.compile_circuit(circuit)
    output_state = lo.simulate(**circuit)
    return lo.dinner(output_state, target)


height=10
width=20
dna=np.random.randint(0, 5, (height, width))
dna=np.ones((height, width))*-1

print fitness(dna)
