# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:43:20 2020

@author: Mollier Yoann
"""


import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import fsolve

#%% Déclaration des fonctions

def p(v,t):
    '''Résoud les équations de Van Der Waals '''
    a = 8./3 * t
    b = v - 1./3
    c = 3 / v**2
    return a / b - c

def comparaison(v,t, pi):
    ''' pour p(v, 0.88)'''
    return p(v,t)-pi

def ToBe0(pi, t):
    v1 = fsolve(comparaison, 0.5, args=(t, pi))[0]
    v2 = fsolve(comparaison, 4.0, args=(t, pi))[0]
    Mv = np.linspace(v1, v2, 201)
    
    return np.trapz(comparaison(Mv, t, pi), Mv) #Trouve les positions où l'aire est nulle

#%% Van der Waals

T = np.arange(0.3, 1.81, 0.02)
V = np.linspace(0.5, 4.0, 201)

plt.figure('Van der waals')
plt.clf()
plt.title('Van der waals')

for t in T :
    if abs(t-1) < 1e-6:
        plt.plot(V,p(V,t), '-r')
    else:
        plt.plot(V, p(V,t), '-b', linewidth=0.5)

plt.xlabel(r'$Volume, v = V/V_c$')
plt.ylabel(r'$Pression, p = P/P_c$')
plt.xlim(0.5, 3.2)
plt.ylim(0., 1.4)


plt.plot(1, 1, '*k', markersize = 11, label = 'Point Critique')

pinst = []
vinst = []

Ti = np.arange(0.3, 1.015, 0.005)
Vi = np.linspace(0.5, 4.0, 2001)

#Trace la courbe d'instabilité
for t in Ti[Ti<1.001]:
    i = np.argmin(p(Vi[Vi<1], t))
    pinst += [p(Vi[i], t)]
    vinst += [Vi[i]]
plt.plot(vinst, pinst, ':k', label = 'ligne d\'instabilité')

pinst = []
vinst = []
for t in Ti[Ti<1.001]:
    k = np.argmax(p(Vi[Vi>1], t))
    pinst += [p(Vi[Vi>1][k], t)]
    vinst += [Vi[Vi>1][k]]    
plt.plot(vinst, pinst, ':k') 
 

# Palier de maxwell pour T = 0.88
TEMP = 0.88
pisol = fsolve(ToBe0, p(1,TEMP), TEMP)[0]
v1 = fsolve(comparaison, 0.5, args=(TEMP, pisol,))[0]
v2 = fsolve(comparaison, 4.0, args=(TEMP, pisol,))[0]
plt.plot([v1, v2], [p(v1, TEMP), p(v2,TEMP)], '-k')
plt.plot(V, p(V, TEMP), '-k')

#Rempli l'aire sous la courbe entre l'isobare et l'isoterme à (T = 0.88)
bV = np.linspace(v1, v2, 181) # trace les points entre V1 et V2
plt.fill_between(bV, p(bV, TEMP), p(v1,TEMP), color ='yellow')
plt.legend(loc = 1)
