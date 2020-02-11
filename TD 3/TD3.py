# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 13:53:46 2020
@author: Mollier Yoann
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint

#%% Déclaration des fonctions
def volterra(xy, t):
    '''
    Équation d'évolution de deux populations codépendantes
    '''
    x, y = xy
    dxdt = x*y*0.5 - x * 0.5
    dydt = -x*y + y
    return dxdt, dydt


def balistique(yv,t):
    '''
    Équations balistique d'un objet jeté sur une plage de temps donné
    '''
    y,v = yv
    dydt = v
    dvdt = -g
    return dydt, dvdt

def pendule(phib, t):
    '''
    Équations du mouvement d'un pendule
    '''
    phi,b = phib
    pos = b 
    accel = -np.sin(phi)
    return pos, accel   

def bernoulli(y, x):
    '''
    Équation de Bernoulli 
    '''
    dydx = x * y**2 - y
    return dydx

def newton(x):
    '''
    fonction 1/(1+x)
    '''
    s = 1 / (1 + x)
    return s
#%%
#Gestions des paramètres initiaux
#Évolutions des populations proies et prédateurs en fonction du temps
xy = [2,2] # Populations initiales
T = 25
t = np.linspace(0, T, 450) # plus de 100 points sont nécessaires pour éviter les artefacts

eqdiff = odeint(volterra, xy, t) #résolution de l'équation de Volterra

x = eqdiff[:,0]     # Population de prédateurs
y = eqdiff[:,1]     # Population de proies

plt.figure('Volterra')
#Premier graphique sur l'évolution des populations en fonction du temps
plt.subplot(211)
plt.title('Évolution des populations \n de proies et de prédateurs en fonction du temps')
plt.grid(True)
plt.xlabel('temps t')
plt.ylabel('densité de population')
plt.plot(t, x, label = 'Prédateurs')
plt.plot(t, y, label = 'Proies')
plt.legend()

#second graphique représentant l'évolution des population l'une en fonction de l'autre
plt.subplot(212)
plt.xlabel('densité de prédateurs')
plt.ylabel('densité de proies')
plt.grid(True)
plt.plot(x,y)
plt.subplots_adjust(hspace = 0.3)

#%% partie balistique
yv = [0, 10] # Conditions initiales de hauteurs et de vitesse
T = 3        # Temps de parcours de l'objet
g = 9.81     # Constante de pesanteur

t = np.linspace(0, T, 120) # plus de 100 points sont nécessaires pour éviter les artefacts
bal = odeint(balistique, yv, t)

y = bal[:,0]
v = bal[:,1]

fig = plt.figure('Balistique'); plt.clf()
plt.title('Évolution des populations')


plt.subplot(122)    # Emplacement dans la page du graphique
plt.title('v = f(t)')
plt.grid(True)
plt.plot(t, v)      # Trace l'évolution de la vitesse en fonction du temps
plt.xlabel('temps t (s)')
plt.ylabel('hauteur (m)')


plt.subplot(121)    # Emplacement dans la page du graphique
plt.subplots_adjust(wspace = 0.3)
plt.title('y = f(t)')
plt.grid(True)
plt.plot(t, y)      # Trace l'évolution de la hauteur en fonction du temps
plt.xlabel('temps t (s)')
plt.ylabel('vitesse (m/s)')



#Animation de la trajectoire de l'objet étudié
point, = plt.plot(t[0], y[0], 'o-r', lw = 1) #Position initiale

def step(n):
    '''
    Modifie à chaque frame la position de l'objet étudié
    '''
    point.set_data(t[n],y[n])
    
an = animation.FuncAnimation(fig, step, frames = 250, interval = 0.5)


#%% Pendule

ai = 50                       # Angle en degrés
phidphi = [ai * np.pi/180, 0]   # Paramètres initiaux d'angle(radian) et de vitesse

T = 8*np.pi                     # Période d'étude du pendule
t = np.linspace(0, T, 250)      # plus de 100 points sont nécessaires pour éviter les artefacts

#Résolution de l'équation du pendule
pend = odeint(pendule, phidphi, t)

phi = pend[:,0]
dphi = pend[:,1]

fig = plt.figure('Pendule');plt.clf()
plt.title('Évolution des paramètres du pendule')
plt.xlabel('temps t (s)')

plt.grid(True)
plt.plot(t,phi, label = r'$\varphi$')               # Trace la variation de phi en fonction du temps
plt.plot(t,dphi, label = r'$\frac{d\varphi}{dt} $') # Trace la vitesse angulaire en fonction du temps
plt.legend()

# Affiche dans une miniature la représentation de l'évolution du pendule au cours du temps
plt.axes([.75,.1,.2,.2], aspect = 'equal')
plt.xlim(-1,1)
plt.ylim(-1,1)

# Positions de la branche du pendule en fonction de phi
x = np.sin(phi)
y = -np.cos(phi)

#animation du pendule
line, = plt.plot([0,y[0]], [0,x[0]], 'o-r', lw = 1) #Initialisation des points du bras

def step(n):
    line.set_data([0,x[n]], [0,y[n]])
    
an = animation.FuncAnimation(fig, step, frames = 250, interval = 1)
plt.show()

#%% Bernoulli
T = 20      
x = np.linspace(0, T, 250) 

y0 = 1      #Conditions initiales

ber = odeint(bernoulli, y0, x)  #Eq de Bernoulli
new = newton(x)                 #Eq de f(x) = 1/(1+x)


#Initialisation du graphique
plt.figure('Bernoulli')
plt.title('Comparaison de l\'éq. Bernoulli et de sa solution analytique')
plt.xlabel('x')
plt.ylabel('y')

# Trace sur le graphique les deux fonctions pour les comparer
plt.plot(x, ber, label = 'Bernoulli')
plt.plot(x, new, label = r'f(x) = $\frac{1}{1+x}$')

plt.legend()
plt.show()


