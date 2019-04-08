import numpy as np
import cupy as cp
from random import uniform as rndfloat
from math import exp

def generateChain(l, T, total_steps, skip_first, jump_every):
    state = np.random.choice([+1,-1],(l,l))
    
    for i in range(total_steps):
        state = monteCarloStep(state,l,T)
        if i>=skip_first and i % jump_every == 0:
            evaluateState(state)


def monteCarloStep(state,l,T):
    dU_array = [-8,-4,0,4,8]
    w_dict = {dU:exp(-dU/T) for dU in dU_array}
    for i in range(l):
        for j in range(l):
            dU = 2 * state[i,j] * \
                (state[(i-1)%l, j] + state[(i+1)%l, j] + state[i, (j-1)%l] + state[i, (j+1)%l])
            if dU>=0:
                state[i,j] = -state[i,j]
            else:
                R = rndfloat(0.,1.)
                w = w_dict[dU]
                if R<=w:
                    state[i,j] = -state[i,j]
    return state



def evaluateState(state):
    avg_m = np.mean(state)
    print(avg_m)
    outputfile.write(f'avg_m\n')
##############################################################################
outputfile = open("termalizacja.out","w")
generateChain(50,1,1000000,0,100)
outputfile.close()


