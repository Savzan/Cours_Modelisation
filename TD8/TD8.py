# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:34:45 2020

@author: MOLLIER Yoann
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint
from scipy.optimize import curve_fit

#%% Déclaration des fonctions 

def EqKepler(u, t):
    x =  u[0]
    y =  u[1]
    vx = u[2]
    vy = u[3]
    
    ax = - x / (x**2+y**2)**(3./2)
    ay = - y / (x**2+y**2)**(3./2)
    

    return [vx, vy, ax, ay]

def ellipse(phi, p, e):
    ''' Équation de l'éllipse en coordonnée sphérique'''
    return p/(1 + e*np.cos(phi))

#%% KEPLER
u = [1,0,0,np.sqrt(0.25)]             # Paramètres initiaux [x,y,vx,vy]
t = np.linspace(0, 50, 5000)

#Résolution de l'équation différentielle
sol = odeint(EqKepler, u, t)
x = sol[:,0]
y = sol[:,1]
vx = sol[:,2]
vy = sol[:,3]


r = np.sqrt(x**2+y**2)
phi = np.arccos(x/r)

pfit, pcov = curve_fit(ellipse, phi, r)# Détermine les paramètres par curve_fit
phith = np.linspace(-1,1,50)*np.pi
pt = ellipse(phith, *pfit)             # Approximation à l'éllipse

xt = pt*np.cos(phith)
yt = pt*np.sin(phith)

# Partie hodographe et conservation du moment cinétique
vr = u[3] / (1+pfit[1])
a = - 2 * pfit[0] / (1-pfit[1]**2)

an = (max(x)-min(x))/2
fx = -pfit[1]*2*an

#Initialise les graphs pour une meilleure présentation
fig,ax = plt.subplots(1,2,gridspec_kw = {"width_ratios":(3, 2)}, figsize = (13.5, 5.5))

# Orbite de la planète autour de l'étoile
ax[0].set_title('Orbite de la planète autour du soleil')
ax[0].set_aspect('equal')
ax[0].plot(x,y, '--', color = 'gray' ,lw = 0.5)
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')

ax[0].plot(xt, yt, 'om', ms= 3)         # Trace l'orbite de la planète
ax[0].plot(0,0, '*r', ms = 12)          # Position du soleil
ax[0].plot(pfit[1]*a, 0, '^b')          # Position du second Foyer

txt2 = ax[0].text(1 + 0.03, 0.03, r"$planète$", fontsize = 10, color = "dimgray")
Planete, = ax[0].plot(1, 0, "og", ms = 15)
ligne1, = ax[0].plot([0, 1], [0, 0], '--k')
ligne2, = ax[0].plot([fx, 1], [0, 0], '--k')
vec2, = ax[0].plot([ u[0], u[0]+u[2]], [u[1] ,u[1]+u[3]], '-^r')

# Hodographe de la planète
ax[1].set_title('Hodographe de la planète en orbite')
ax[1].set_aspect('equal')
ax[1].set_xlabel(r'$v_x$')
ax[1].set_ylabel(r'$v_y$')

ax[1].plot(vx, vy, lw = 0.5)            # Trace l'Hodographe
ax[1].plot(0, pfit[1]*vr, 'xr')         # Centre de l'hodographe
ax[1].plot(0, 0, 'xr')                  # Origine de l'hodographe
 
vec,  = ax[1].plot([0,u[2]], [0,u[3]], '-^r')
ray, = ax[1].plot([0,u[2]], [pfit[1]*vr,u[3]], '--', color = 'dimgray')

factor = 0.1
def step(n):
    '''
    Animation de l'orbite de la planète autour du soleil
    Animation de l'hodomètre en fonction du temps
    '''
    # ANIMATION DE L'ORBITE
    # Anime la planète autour du soleil
    Planete.set_data(x[n], y[n])              
    txt2.set_position([x[n]-0.07, y[n]+0.04])
    # Trace une ligne allant du soleil à la planète, puis de la planète au second foyer
    ligne1.set_data([0, x[n]], [0, y[n]])
    ligne2.set_data([fx, x[n]], [0, y[n]])
    # Trace le vecteur sur le premier graph
    vec2.set_data([x[n], x[n]+vx[n]*factor], [y[n] ,y[n]+vy[n]*factor])
    
    # ANIMATION SUR L'HODOGRAPHE
    # Trace le vecteur (0,0) a (vx, vy)
    vec.set_data([0,vx[n]], [0,vy[n]])
    # Trace le rayon avec le centre de l'hodographe
    ray.set_data([0, vx[n]], [pfit[1]*vr ,vy[n]])
    
    
an = animation.FuncAnimation(fig, step, interval = 30, frames = len(t))




























