# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:36:26 2020
@author: MOLLIER Yoann
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#%% Definition des fonctions utilisées
#Fonction de la loi de malus
def malus(angle, amplitude, phase, shift):
    Intensité = amplitude * np.cos((angle + phase)*np.pi/180)**2 + shift
    return Intensité

#Fonction de droite ax+b
def lineaire(x, a, b):
    y = a*x + b
    return y 

#Fonction moyenne
def moy(x):
    moyenne = sum(x)/len(x)
    return moyenne

#Fonction déterminant le coefficient directeur (bx + a) : b
def coeff(x,y):
    b = sum( (x - moy(x)) * y ) / sum( (x-moy(x))**2 )
    return b

#Fonction déterminant l'ordonnée à l'origine (bx + a) : a
def origine(x,y):
    a = moy(y) - ( coeff(x,y) * moy(x) )
    return a
    
#Fonction de l'écart type du coefficient directeur
def sigmaCoeff(x,y):
    N = len(x)
    q = sum(( y  - coeff(x,y)*x - origine(x,y))**2)
    p = (N - 2)*sum((x-moy(x))**2)
    sb = np.sqrt(q/p)
    return sb

#Fonction de l'écart type (incertitude) de l'ordonnée à l'origine
def sigmaOrigine(x,y):
    N = len(x)
    q = (1 / (N-2)) * sum(( y  - coeff(x,y)*x - origine(x,y))**2)
    p = ((1 / N) + (moy(x)**2 / sum(( x-moy(x) )**2)))
    sa = np.sqrt(q*p)
    return sa
    

#%% Fitting, loi de Malus et construction de graphique

#Charge le fichier avec les données loi de Malus
#Imprime les données dans la console
data = np.loadtxt('exp_loi_Malus1py.txt')
print(data)

#gestion des données
angleExp = data[:,0]
R = data[:,1] 
IntensiteRes=R**(-1.6) #Determine une valeur d'intensité à l'aide des valeurs de data

#Création d'une courbe de valeurs théorique
angle = np.arange(-90, 140, 5) 
Ith1 = malus(angle, 0.28, np.pi/2, 0.04)

#Determine les variables par fitting de notre fonction Malus()
pfit, pcov = curve_fit(malus, angleExp, IntensiteRes)
Ith2 = malus(angle, *pfit)

#Etapes de constructions du graphique
plt.figure('Malus') #Référence du graphique

plt.xlabel(r'${\rm angle}\ \varphi\ $') # Légende axe X
plt.ylabel('$Intensité$') # Légende axe Y

#Trace les différentes courbes sur le graphique
plt.plot(angleExp, IntensiteRes, 'ro') #Courbe expérimentale
plt.plot(angle, Ith1, 'b' ,angle, Ith2,'g--') #Courbes théoriques

#Définie la légende du graphique
plt.legend((r'$I_{exp}$', r'$I_{th}$', r'$I_{fit}$'), shadow = True)# Les légendes
plt.title('Observation de l\'efficacité de l\'ajustement') # Titre du graphique
plt.show() # Affiche le graphique

#Tableau d'entrée des valeurs après ajustement
#Accompagnées de leurs incertitudes
#Méthode de détermination  des incertitudes par la diagonalisation de pcov
S = np.sqrt(np.diag(pcov))


print('\nValeurs obtenues par ajustement de la fonction malus aux valeurs experimentales')
print('I0 = {:.3f}+-{:.3f}'.format(pfit[0],S[0]))
print('Phase = {:.3f}+-{:.3f}'.format(pfit[1],S[1]))
print('I(offset) = {:.3f}+-{:.3f}'.format(pfit[2],S[2]))

#%% Deuxième partie, distribution aléatoire et fonction de tendance
#Gestion des données
N = 21 # Effectif
s = 0.2 # Valeur de l'écart aléatoire
a = 1.0 # Coefficient directeur

x = np.linspace(0,1,N)
distrib = a * x + s*(np.random.rand(N)-0.5) #Distribution aléatoire (-0.5) pour normaliser

pfit, pcov = curve_fit(lineaire, x, distrib) #Ajustement de la courbe de regression
S = np.sqrt(np.diag(pcov))
fit = lineaire(x, *pfit) #Approximation obtenue par la fonction curve_fit

analytique = x * coeff(x, distrib) + origine(x, distrib) #Méthode analytique

#Initialisation des données du Graphique
plt.figure('Distribution aléatoire')
plt.title('Distribution aléatoire sur fonction affine')

#Tracée des points et des courbes de regression
plt.plot(x, distrib, 'go', x, fit, 'b-', x, analytique, 'r-')
plt.legend((r'$Données  simulées$',r'$Curve Fit$', r'$Analytique$'))

plt.show()

print('\nValeurs de a et b obtenue par la méthode curve_fit')
print('a = {:.5f}+-{:.5f}'.format(pfit[0],S[0]))
print('b = {:.5f}+-{:.5f}'.format(pfit[1],S[1]))

print('Valeurs de a et b obtenue par la méthode analytique')
print('a = {:.5f}+-{:.5f}'.format(coeff(x,distrib),sigmaCoeff(x,distrib)))
print('b = {:.5f}+-{:.5f}'.format(origine(x, distrib),sigmaOrigine(x,distrib)))
