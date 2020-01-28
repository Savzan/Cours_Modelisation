# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:36:26 2020

@author: MOLLIER Yoann
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#Definition des fonctions utilisées
#Fonction de la loi de malus
def malus(angle, amplitude, phase, shift):
    Intensité = amplitude * np.cos((angle + phase)*np.pi/180)**2 + shift
    return Intensité

#TODO définir la fonction de regression linéaire des moindres carrés
 

#Charge le fichier avec les données loi de Malus
#Imprime les données dans la console
data = np.loadtxt('exp_loi_Malus1py.txt')
#print(data)

angle = data[:,0]
R = data[:,1]

#Determine une valeur d'intensité à l'aide des valeurs de data
IntensiteRes=R**(-1.6)

#Création d'une courbe de valeurs théorique
angleTh = np.arange(-90, 140, 5)
Ith1 = malus(angleTh, 0.28, np.pi/2, 0.04)

#trace la courbe théorique
plt.plot(angleTh, Ith1)
#Trace les points experimentaux
plt.plot(angle, IntensiteRes, 'ro', ms = 2)
#Determine les variables par fitting de notre fonction Malus()
pfit, pcov = curve_fit(malus, angle, IntensiteRes)


#Trace la fonction Malus fittée et autres graphiques shenaningans
#TODO faire un graphique à peu prêt correct
Ith2 = malus(angleTh, *pfit)
plt.plot(angleTh, Ith2,'g--',label=str(pfit[0])[0:6])
plt.xlabel(r'${\rm angle}\ \varphi\ \rm[deg]$', fontsize = 14)
plt.ylabel('$Intensité$', fontsize = 14)

plt.legend(fontsize = 14)
S = np.sqrt(np.diag(pcov))

print('I0 = {:.3f}+-{:.3f}'.format(pfit[0],S[0]))

#TODO créer une fonction de tendance pour les fonctions linéaires
