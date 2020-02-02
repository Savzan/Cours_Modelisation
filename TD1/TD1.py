# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:03:30 2020

@author: Yoann Mollier
"""

import numpy as np
eps = np.spacing(1)

#%% Déclaration des fonctions 
def moy(x):
    m = sum(x)/len(x)
    return m

def sigma(x):
    s = np.sqrt( (1/( len(x)-1 )) * sum((x - moy(x))**2) )
    return s

#%% Corps du programme
#Mesures expérimentales
x0 = 0.5
x1 = np.array([10.3, 9.3, 8.8, 11.1, 9.7, 6.1])
x2 = np.array([3.4, 3.0, 2.9, 3.4, 3.0, 2.1])

#l'effectif des mesures
n = len(x1)

#Coefficient de Laplace, son incertitute et sa moyenne sur l'effectif
gamma = (x1-x0)/(x1-x2)
dGamma = 0.1 / (x1-x2)
moyGamma = moy(gamma)


#Défini la fonction de l'écart type
ecartType = sigma(gamma)

#Gère la création d'un tableau, chaque colonne est espacé d'une valeur minimum
#de la variable spacing qui représente le nombre d'espace.
#Les valeurs sont tronquées jusqu'à la 4ème valeur après la virgule

spacing = 8
print("gamma",' '*(spacing-len("gamma")), "dGamma")
for x,y in zip(gamma, dGamma) :
    print(str(x)[0:6],' '*(spacing-len(str(x)[0:6])),str(y)[0:6])

#print les valeurs de l'écart type Sigma et la valeur moyenne de gamma, agencée
print("\nmoyGamma",' '*(spacing-len("moyGamma")), "Sigma")
print(str(moyGamma)[0:6],' '*(spacing-len(str(moyGamma)[0:6])), str(ecartType)[0:6])
