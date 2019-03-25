import numpy as np
import random
from multiprocessing import Pool

def diffusion(n,l,kmax,seed):
    
    # funkcja przyjmuje parametry:
    #   n - liczba atomów
    #   l - rozmiar układu
    #   kmax - liczba kroków Monte Carlo
    #   seed - ziarno RNG 
    # funkcja zwraca tablicę z kwardatem przesunięcia (uśrednionym po atomach)
    #  dla każdego kroku Monte Carlo

    assert 0<=n<=l**2, "Liczba atomów nie mieści się w przedziale [0,l**2]"

    rng = np.random.RandomState(seed)   #inicjalizacja RNG

    box = np.zeros((l,l),bool)          #macierz przechowuje informacje o tym czy miejsce jest zajęte
    r0_array = np.empty((0,2),int)      #macierz położeń początkowych
    output_array = np.empty((0))      

    #losowanie położeń początkowych
    for i in range(n):
        r0 = rng.randint(0,l,(2))     #losowanie wektora położenia
    
        while (box[r0[0],r0[1]]==True):     #jeśli miejsce już zajęte, powtórz losowanie
            r0 = rng.randint(0,l,(2))
        
        box[r0[0],r0[1]]=True
        r0_array = np.vstack((r0_array,r0))
    
    r_array = r0_array.copy()  #macierz położeń atomów
    
    
    for k in range(kmax):
    
        for i in range(n):
            r = r_array[i,:]    #i-ty wiersz macierzy r_array
            r_periodic = r % l
            
           #losowanie kierunku przemieszczenia
            moves=[[1,0],[-1,0],[0,1],[0,-1]]
            randindex = rng.randint(4)
            dr = moves[randindex] 
            
            r_new = r + dr
            r_new_periodic  = r_new % l
            
            if box[r_new_periodic[0],r_new_periodic[1]] == False:
                box[r_periodic[0],r_periodic[1]] = False
                box[r_new_periodic[0],r_new_periodic[1]] = True
                r_array[i,:] = r_new.copy()
        
        delta_r_array = r_array - r0_array
     
        delta_r2 = [float(x)**2+float(y)**2 for [x,y] in delta_r_array]
        delta_r2_mean = np.mean(delta_r2)   #uśrednienie po atomach
        output_array= np.append(output_array,delta_r2_mean)

    return output_array




if __name__ == "__main__":
    def singleConcentration(n,l,kmax,isim):
    
        #   n - liczba atomów
        #   l - rozmiar układu
        #   kmax - liczba kroków Monte Carlo
        #   isim - liczba niezależnych symulacji
        #   funkcja zwraca tablicę współczynnika dyfuzji po kolejnych krokach MC
        
        parameters = [(n,l,kmax,np.random.randint(0,2**30)) for j in range(isim)]
        with Pool() as pool:
            delta_r2_array = np.array(pool.starmap(diffusion,parameters))
        mean_delta_r2 = np.mean(delta_r2_array,axis=0) #uśrednienie po niezal. symulacjach
        
        k=[4*i for i in range(1,kmax+1)]
        
        diff_coefficient = mean_delta_r2/k  #tablica współcz. dyfuzji w kolejnych krokach MC
        return diff_coefficient
    
    
    Nconc = 15       #liczba stężeń do sprawdzenia (rozł. równomiernie między 0 a 1)
    l = 20          #rozmiar układu
    isim = 100       #liczba niezal. symulacji dla każdego stężenia
    avgfrom = 400   #krok MC od którego będzie liczony średni wsp. dyfuzji
    kmax = 800      #liczba kroków MC
    
    outputFileName = "concentrations.out"
    
    concentrations =np.linspace(0.0, 1.0, Nconc)
    with open("concentrations.out","w") as out_file:
        for c in concentrations:
            n = int(c*l*l)
            D_array = np.array(singleConcentration(n,l,kmax,isim))
            D_mean = np.mean(D_array[avgfrom:])
            D_err = np.std(D_array[avgfrom:])
            out_file.write(f'{c}\t{D_mean}\t{D_err}\n')
            print(c)
    
