import cupy as cp
import numpy as np
import time
#CONFIG
n_samples = 100000 #sample size for one simulation
n_steps_min = 1    #simulations for number of steps from 10**n_steps_min to 10**n_steps_max
n_steps_max = 6
n_datapoints = 20  #number of simulations

outputFileName = "output.dat"



n_steps_array=np.logspace(n_steps_min,n_steps_max,n_datapoints,True).astype(np.int32)

fileOut=open(outputFileName,'w')

t0=time.time()
for n_steps in n_steps_array:
    fileOut.write(f'\n\n{n_steps}\n')
    positions = cp.zeros(int(n_samples),np.int32)
    distribution = cp.zeros(2*int(n_steps)+1,np.int32)

    for n in range(n_steps):
        rand = cp.random.random_integers(0,1,n_samples)
        rand = 2*rand-1
        positions = cp.add(positions,rand)


    for x in positions:
        distribution[x+n_steps] += 1
    for i in range(-n_steps,n_steps+1):
        if(distribution[i+n_steps]!=0):
            fileOut.write(f'{i} {distribution[i+n_steps]}\n')

fileOut.close()

t1 = time.time()
t=t1-t0
print(t)