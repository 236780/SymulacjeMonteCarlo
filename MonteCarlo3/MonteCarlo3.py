import numpy as np

#CONFIG

l = 10      #rozmiar układu
Tr = 1.0    #temperatura zredukowana (J/kBT)


conf = np.random.choice([-1,+1],(l,l))
#conf = np.zeros((l,l),bool)

#WAR. BRZEGOWE

def deltaU(i,j):
    deltaU = 2*conf[i,j]*(#suma sąsiadów)