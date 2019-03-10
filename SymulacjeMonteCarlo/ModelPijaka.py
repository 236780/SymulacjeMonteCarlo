
import numpy as np

import cupy as cp #comment this line to disable CUDA
#cp = np          #uncomment this line to disable CUDA

import time

#CONFIG
n_samples = 1000000 #sample size for one simulation
n_steps_min = 1    #simulations for number of steps from 10**n_steps_min to 10**n_steps_max
n_steps_max = 5
n_datapoints = 10  #number of simulations
outputFileName = "output.dat"

n_steps_array=np.logspace(n_steps_min,n_steps_max,n_datapoints,True).astype(np.int32)

fileOut=open(outputFileName,'w')

for n_steps in n_steps_array:
    t0=time.time()
    positions = cp.zeros(int(n_samples),np.int32)
   
    for n in range(n_steps):
        rand = cp.random.random_integers(0,1,n_samples)
        rand = 2*rand-1
        positions = cp.add(positions,rand)

    mean = positions.mean()
    std = positions.std()
    t1 = time.time()
    t=t1-t0
    print(f'{n_steps}\t{mean}\t{std}\t{t}')
    fileOut.write(f'{n_steps}\t{mean}\t{std}\t{t}\n')

fileOut.close()