import numpy as np
import random

#Konfiguracja
n = 30       #liczba atomów
l = 20      #rozmiar układu
kmax = 100  #liczba kroków
outputFileName = "DiffusionCoefficient.out"
#------------------------------------------

box = np.zeros((l,l),bool)          #macierz przechowuje informacje o tym czy miejsce jest zajęte
r0_array = np.ndarray((n,2),int)    #macierz położeń początkowych

#losowanie położeń początkowych
for r0 in r0_array:
    [x,y] = np.random.randint(0,l,(2))
    while (box[x,y]==True):
        [x,y] = np.random.randint(0,l,(2))
    box[x,y]=True
#-----------------------------------------

r_array = r0_array  #macierz położeń atomów
outputFile = open(outputFileName,"w")

for k in range(1,kmax+1):

    for atom_r in r_array:
        dr = random.choice([[1,0],[-1,0],[0,1],[0,-1]]) #losowanie kierunku przemieszczenia
        if (atom_r[0]>=0 and atom_r[0]<l and atom_r[1]>=0 and atom_r[1]<l \
         and box[atom_r+dr] == False):
            box[atom_r] = False
            atom_r = atom_r + dr
            box[atom_r] = True

    delta_r_array = r_array - r0_array
    delta_r2 = [float(x)**2+float(y)**2 for [x,y] in delta_r_array]
    delta_r2_mean = np.mean(delta_r2)
    diffusion_coefficient = delta_r2_mean / (4*k)

    outputFile.write(f'{k}\t{delta_r2_mean}\t{diffusion_coefficient}')
