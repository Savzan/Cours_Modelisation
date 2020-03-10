# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:36:30 2020
@author: Mollier Yoann
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit

#%% Déclaration des fonctions

def amOsc(xv,t):
    """Fonction de résolution des équations caractéristiques de l'oscillateur ammorti"""
    x, dxdt = xv
    dvdt = -(pulsation0**2 * x)-(2*gamma * dxdt) + (amp0*np.sin(pulsation * t) )
    return dxdt, dvdt

def solAmp(pulsation, amp0, gamma, w0):
    """Fonction de résolution analytique en fonction des paramètres initiaux"""
    amplitude = amp0 / np.sqrt((w0**2 - pulsation**2)**2  + (2 * gamma * pulsation)**2)
    return amplitude

#%% Oscillateur forcé et diagramme de phase

#Déclaration des variables
xv = [0, 0]
pulsation0 = 1.0
pulsation = 0.9
gamma = 0.02
amp0 = 1.0

#faire comparaisons physiques avec w0 = w
#quand gamma = 0
t = np.linspace(0, 60*np.pi, num = 1501)

solution = odeint(amOsc, xv , t)

#titre, référence et légendes
plt.figure('Oscillateur amorti')
plt.title(r'$\frac{d^{2}x}{dt^{2}}+2\gamma \frac{dx}{dt}+\omega_{0}^{2}x = 0, \omega_{0} = 1, \gamma = 0.10 $')
plt.xlabel(r'$temps, t /  \pi$')
plt.ylabel('x, dx/dt')


#trace la courbe d'oscillation
plt.plot(t/np.pi, solution[:,0], label = 'x')
plt.plot(t/np.pi, solution[:,1], 'r' ,label = r'$\frac{dx}{dt}$',)


#trace le diagramme de phase
plt.legend()
plt.axes([.75,.1,.2,.2], aspect = 'equal')
plt.plot(solution[:,0], solution[:,1])

#%% 

#Déclaration du gamma, initialisation des pulsations et amplitudes
gamma = 0.15
puls = np.linspace(0.2,2.0,501)
allxamp = []
axAmp = []

#Initialisation du graphique
plt.figure('amplitude en fonction de la pulsation')
plt.title('Comparaison des fonctions de résonnance obtenues par \n méthode analytique et numérique')
plt.xlabel('pulsation')
plt.ylabel('amplitude')

#solution numérique
for pulsation in puls : 
    '''Méthode numérique de résolution de l'équation différentielle
    Effectue la résolution pour toutes les pulsations dans l'espace selectionné'''
    sol = odeint(amOsc, (1,0), t)
    x = sol[:,0]
    xamp = max(x [t > 0.9 * max(t)])
    allxamp += [xamp]
   
plt.plot(puls, allxamp, label = 'solution numérique') #Trace la solution numérique

#solution analytique
solA = solAmp(puls, amp0, gamma, pulsation0)
plt.plot(puls, solA, label ='solution analytique') #Trace la solution analytique

plt.legend()
#%% Résonance d'un circuit RLC

RLC = [350, 1, 0.1]
R = 350 #ohm
L = 1   #H
C = 0.1e-6 #micro F

data = np.loadtxt('resonanceRLC.txt')

#Initialisation des données du graphique de résonance
plt.figure('Résonance')
plt.title(r'LCR résonance $(1H, 0.1 \mu F, 350 \Omega )$')
plt.grid()
plt.xlabel('fréquence (Hz)')
plt.ylabel('amplitude (mV)')

#Trace la courbe de mesure issue des données du fichier resonanceRLC
plt.plot(data[:,0], data[:,1]*1000, label = 'Mesures')

#Détermination des
p0 = [1.6e6,189, 3167] 
pfit, pcov = curve_fit(solAmp, data[:,0]*2*np.pi, data[:,1], p0 = p0)

#trace la courbe d'approximation par la méthode curve_fit
ydata = solAmp(data[:,0]*2*np.pi, *pfit)
plt.plot(data[:,0], ydata*1000, '--r', label = 'Analytique')
plt.legend()

#Bruit associé aux mesures comparé à la solution analytique
plt.figure('Bruit associé aux mesures')
plt.title('Bruit associé à la mesure')
noise = data[:,1] - ydata
plt.plot(data[:,0], noise*1000)
plt.ylabel('amplitude (mV)')
plt.xlabel('Fréquence (Hz)')
