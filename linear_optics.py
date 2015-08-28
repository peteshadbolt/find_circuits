from numpy import *
import itertools as it
from collections import defaultdict
from permanent import permanent

nmodes = 12
nphotons = 6
factorial = (1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800)
ir2 = 1 / sqrt(2)

def dinner(a, b):
    """ Inner product of states represented as dicts """
    return sum([a[key] * b[key] for key in set(a.keys() + b.keys())])


def normalization(modes):
    """ Compute the normalization constant """
    table = defaultdict(int)
    for mode in modes:
        table[mode] += 1
    return prod([factorial[t] for t in table.values()])


def simulate(input_state, unitary, patterns, mode="probability", **kwargs):
    """ Simulates a given circuit, for a given input state, looking at certain terms in the output state """
    output_state = defaultdict(complex)
    for cols, amplitude in input_state.items():
        cols = list(cols)
        n1 = normalization(cols)
        for rows in patterns:
            n2 = normalization(rows)
            perm = permanent(unitary[list(rows)][:, cols])
            value = amplitude * perm / sqrt(n1 * n2)
            output_state[rows] += value
    return output_state


def mzi(theta, phi):
    """ A Mach-Zehnder on two modes """
    tt = exp(1j * theta)
    pp = exp(1j * phi)
    return 0.5 * matrix([[tt * pp - pp, 1j * (tt + 1)], [1j * (tt * pp + pp), 1 - tt]])


def get_u(r):
    """ Get a unitary matrix from a Reck scheme's phases """
    u = matrix(eye(nmodes), dtype=complex)
    positions = it.chain(*(reversed(range(n)) for n in range(nmodes)))
    for j, (theta, phi) in zip(positions, r):
        u[j:j + 2] = mzi(theta, phi) * u[j:j + 2]
    return u

