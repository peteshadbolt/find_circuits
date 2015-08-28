#!/apps/python/2.7.3/bin/python

#PBS -l walltime=01:00:00
#PBS -l select=1:ncpus=20:mem=5gb
#PBS -o /work/pshadbol/logs/
#PBS -e /work/pshadbol/logs/

from numpy import *
import itertools as it
import multiprocessing
import signal
from scipy.optimize import fmin
from time import clock, time
import os
import json
import linear_optics as lo
from collections import defaultdict


def init_worker():
    """ Make sure we can Ctrl-c """
    signal.signal(signal.SIGINT, signal.SIG_IGN)



def fitness(r):
    """ Compute the fitness of a given R matrix """
    r = r.reshape((len(r) / 2, 2))
    input_state = {tuple(range(lo.nphotons)): 1}
    # target_state = defaultdict(complex, {(0, 0, 1, 1): 1})
    ts = {(0, 1, 2, 3, 4, 5): lo.ir2, (0, 1, 2, 6, 7, 8): lo.ir2}
    target_state = defaultdict(complex, ts)
    patterns = target_state.keys()
    output_state = lo.simulate(input_state, lo.get_u(r), patterns)
    return abs(lo.dinner(output_state, target_state)) ** 2


def cost(r):
    return 1 - fitness(r)


def crossover(a, b):
    """ Circuits have sex and produce offspring """
    return (a + b) / 2


def mutate(a):
    """ Mutate a candiate circuit """
    return a + random.uniform(-.01, .01, a.shape)


def run(i):
    """ Run the optimization """
    guess = random.uniform(0, pi * 2, lo.nmodes * (lo.nmodes - 1))
    best_guess = fmin(cost, guess, disp=False)
    return best_guess


if __name__ == '__main__':
    CPUs = multiprocessing.cpu_count()
    print "{} CPUs".format(CPUs)
    attempts = 50 if CPUs > 4 else 1
    pool = multiprocessing.Pool(CPUs, init_worker)

    # Actually run
    wins = pool.map(run, range(attempts))

    # Meditate on the outcome
    fitnesses = pool.map(fitness, wins)
    best_index = argmax(fitnesses)
    print "Best hit: {}".format(max(fitnesses))

    # Prepare to write to disk
    wins = map(list, wins)
    data = {"wins": wins, "best": wins[best_index], "best_fitness": max(fitnesses)}
    path = "/work/pshadbol/fc2/" if CPUs > 4 else "fc2"
    filename = os.path.join(path, "{}.json".format(int(time())))

    # Dump to disk
    f = open(filename, "wb")
    json.dump(data, f, indent=4)
    f.close()


