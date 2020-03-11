# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 18:40:43 2020

@author: Mollier Yoann
"""

import numpy as np
from numpy import pi                 #importe pi, évite d'écrire np.pi
from matplotlib import pyplot as plt #importe les tableaux
from matplotlib import animation     #importe le module d'animation

#%% Déclaration des fonctions
def w(k):
    '''Évolution de la pulsation en fonction des différents
    paramètres, la vitesse de phase w(k0), 
    la vitesse de groupe (dw/dk) ainsi que
    la dispersion du paquet d'onde (d²w/dk²)'''
    return Vp*k0 + Vg*(k-k0) + 0.5*disp*(k-k0)**2 

def u(x,t):
    '''Fonction de représentation du paquet d'onde en fonction
    des paramètres de vitesse de groupe, du temps, et de sa dispersion'''
    uxt = 0
    for n in range (1, int(k0/pi)):
        kn = 2*pi*n
        B = 2*np.sqrt(pi)/dk
        varK= (kn-k0)
        uxt += B *np.exp(-(varK / dk)**2) * np.cos(kn*x - w(kn)*t)
    return uxt

def env(x, dk, t, disp):
    '''Définition de la fonction de représentation
    de l'enveloppe du paquet d'onde, en tenant
    également compte de la dispersion du paquet d'onde'''
    if disp == 0: #contrainte sur A dans le cas où la dispersion est nulle
        A = 1
    else :
        tau = 2 / ( abs(disp) * dk**2 )
        A = 1 / np.sqrt(1 + (t/tau)**2)
    dep = (x - Vg*t + 0.5)%1 - 0.5
    dx = 2/(A*dk)
    C = (dep / dx)**2
    return np.sqrt(A)*np.exp(-C)

#%% Mouvement et dispersion du paquet d'onde
#Initialisation des variables
dk =  2*2*pi
k0 = 30*2*pi

Vp = 0.5        # w(k0)  - la vitesse de phase
Vg = 0.4        # dw/dk  - la vitesse de groupe
disp = +0.001   #d²w/dk² - la valeur de dispersion

x = np.linspace(-0.5,0.5,1000)

# Mise en place du graphique, initialisation de l'enveloppe et du paquet d'onde
fig = plt.figure('Paquet')

#Titre ajusté en fonction des variables
title = r'Mouvement et dispersion du paquet d\'onde, '
var = r'$\frac{\delta_k}{2\pi}={}$'+str(dk/(2*pi))[0:1]+r', $\frac{d^2\omega}{dk^2} ={]$'+str(disp)
plt.title(title + var)
plt.xlabel(r'$x$', fontsize = 12)
plt.ylabel(r'$u$', fontsize = 12)

env1, = plt.plot(x,env(x, dk, 0, disp),'--r')  #trace le haut de l'enveloppe
env2, = plt.plot(x,-env(x, dk, 0, disp),'--r') #trace le bas de l'enveloppe
line,= plt.plot(x, u(x,0),'-b')                #trace l'enveloppe

#Animation
ind_t=plt.text(0.3,0.75,'t=0')

deltime = 0.1
def step(n):
    ''' Définie la fonction de l'animation sur une durée dt '''
    t = n*deltime
    uAnim = u(x,t)
    eAnim = env(x, dk, t, disp)
    line.set_ydata(uAnim)
    env1.set_ydata(+eAnim) 
    env2.set_ydata(-eAnim) 
    ind_t.set(text='t = '+str(t)[0:3])
an = animation.FuncAnimation(fig, step, frames=252, interval=50)

plt.show()
