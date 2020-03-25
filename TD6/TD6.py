# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 14:03:27 2020

@author: MOLLIER Yoann
"""

import numpy as np
from matplotlib import pyplot as plt
from pot1jFun import *

#%% Dipoles ponctuelles
q = 1
x = np.linspace(-2.0, 2.0, 250)
y = np.linspace(-1.5, 1.5, 250)

#Résolution par la méthode complexe
X,Y = np.meshgrid(x,y)
Z = X + 1j*Y

#Potentiels des charges
Uj1 = pot1j(Z, [-0.8,0],q) + pot1j(Z, [0.8,0], -q)
Uj2 = pot1j(Z, [-0.8,0],q) + pot1j(Z, [0.8,0], q)
Uj3 = pot1j(Z, [-0.8,0],-q) + pot1j(Z, [0.8,0], 2*q)

drawUandE(Z, Uj1, 'Dipôle q, -q', rangeU=(-6,6.1,0.5), rangeE=(8,2))
drawUandE(Z, Uj2, 'Dipole q, +q', rangeU=(-6,6.1,0.5), rangeE=(16,4))
drawUandE(Z, Uj3, 'Dipole -q, +2q', rangeU=(-6,6.1,0.5), rangeE=(16,8))
#%% Quadripole
q = 1
title = 'Quadripole'
x = np.linspace(-2.0, 2.0, 250)
y = np.linspace(-1.5, 1.5, 250)

X,Y = np.meshgrid(x,y)
Z = X + 1j*Y

Uj1 = pot1j(Z, [-0.8,0.5],q) + pot1j(Z, [0.8,0.5], -q) + pot1j(Z, [-0.8,-0.5],2*q) + pot1j(Z, [0.8,-0.5], -2*q)

drawUandE(Z, Uj1, title, rangeU=(-6,6.1,0.5), rangeE=(128,16))

#%% Condensateur diélectrique
title = 'Condensateur'
q = 1
#défini la position des plaques
position = np.linspace(-1.0,1.0,401)
#séparation sur l'axe Y entre les deux plaques
separation = 1

Uj = 0
for p in position:
    Uj += pot1j(Z, (p, +separation/2), q/ 401)
    Uj += pot1j(Z, (p, -separation/2), -q/ 401)
    
drawUandE(Z, Uj, title, rangeU=(-2.0,2.5,0.5), rangeE=(32,4))

#%%Condensateur métallique

data = np.loadtxt('LinAlgChargeDistributionForSeparation1.0.txt')
print(data)

title = 'Condensateur métallique'

position = data[:,0]
qall = data[:,1]
Uj = 0

for p,q in zip(position, qall):
    Uj += pot1j(Z, (p, +separation/2), q)
    Uj += pot1j(Z, (p, -separation/2), -q)

drawUandE(Z, Uj, title, rangeU=(-2.0,2.5,0.2), rangeE=(64,4))