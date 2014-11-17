import linear_optics as lo
import numpy as np

p2=np.pi/2.; p4=np.pi/4.
posxy = lambda x,y: {"x":x, "y":y}
generators = [lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":0.5},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/3.},
              lambda x,y: {"type":"coupler", "pos": posxy(x,y), "ratio":1/4.},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p2},
              lambda x,y: {"type":"phaseshifter", "pos": posxy(x,y), "phase":p4},
              lambda x,y: {"type":"crossing", "pos": posxy(x,y)}]

def fitness(dna):
    #data=[{"type":"bellpair","pos":{"x":-8,"y":0}},{"type":"sps","pos":{"x":-8,"y":5}},{"type":"crossing","pos":{"x":-7,"y":0}},{"type":"coupler","pos":{"x":-5,"y":1},"ratio":0.5},{"type":"crossing","pos":{"x":-3,"y":2}},{"type":"crossing","pos":{"x":-1,"y":4}},{"type":"bucket","pos":{"x":0,"y":0}},{"type":"bucket","pos":{"x":0,"y":2}},{"type":"bucket","pos":{"x":0,"y":4}}] 
    circuit=[]
    h,w=dna.shape
    for i in range(w):
        for j in range(h):
            circuit.append(generators[dna[j,i]](i,j))
    circuit=lo.compile_circuit(circuit)
    print circuit

height=10
width=20
m=np.random.randint(0, 5, (height, width))

print fitness(m)
