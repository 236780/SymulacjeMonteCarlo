import numpy as np

#CONFIG

n_samples = 1000
n_steps = 1000
outputFileName = "output.dat"


positions = np.zeros(n_samples,int)
distribution = np.zeros(2*n_steps+1,int)

for n in range(n_steps):
    rand = np.random.random_integers(0,1,n_samples)
    rand = 2*rand-1
    positions = np.add(positions,rand)
    
for x in positions:
    distribution[x+n_steps] += 1

with open(outputFileName,"w") as fout:
    for i in range(-n_steps,n_steps+1):
        fout.write(f'{i}\t{distribution[i+n_steps]}\n')
