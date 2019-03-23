import numpy as np
import random
from os import system as sys
np.set_printoptions(formatter={'bool': lambda p: 'O' if p else ' '})




def diffusion(n,l,kmax,outputFileName):
    assert n<l**2, "Liczba miejsc musi być większa niż liczba atomów"

    box = np.zeros((l,l),bool)          #macierz przechowuje informacje o tym czy miejsce jest zajęte
    r0_array = np.empty((0,2),int)      #macierz położeń początkowych
    
    #losowanie położeń początkowych
    for i in range(n):
        r0 = np.random.randint(0,l,(2))     #losowanie wektora położenia
    
        while (box[r0[0],r0[1]]==True):     #jeśli miejsce już zajęte, powtórz losowanie
            r0 = np.random.randint(0,l,(2))
        
        box[r0[0],r0[1]]=True
        r0_array = np.vstack((r0_array,r0))
    
    print(box)
    print("Macierz położeń:")
    print(r0_array)
    #-----------------------------------------
    
    r_array = r0_array.copy()  #macierz położeń atomów
    outputFile = open(outputFileName,"w")
    
    
    for k in range(1,kmax+1):
    
        for i in range(n):
            r = r_array[i,:]    #i-ty wiersz macierzy r_array
            
            dr = random.choice([[1,0],[-1,0],[0,1],[0,-1]]) #losowanie kierunku przemieszczenia
            
            r_new = (r + dr) % l #przemieszczenie z zachowaniem period. war. brzeg.
            
            if box[r_new[0],r_new[1]] == False:
                box[r[0],r[1]] = False
                box[r_new[0],r_new[1]] = True
                r_array[i,:] = r_new.copy()
           
        #sys('cls')       
        #print(box)
        
        delta_r_array = r_array - r0_array
        
        delta_r2 = [float(x)**2+float(y)**2 for [x,y] in delta_r_array]
        delta_r2_mean = np.mean(delta_r2)
        diffusion_coefficient = delta_r2_mean / (4*k)
        
        outputFile.write(f'{k}\t\t{delta_r2_mean}\t\t{diffusion_coefficient}\n')
    