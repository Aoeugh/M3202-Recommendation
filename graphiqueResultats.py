# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:30:40 2020

@author: Utilisateur
"""

import matplotlib.pyplot as plt

# listeY = [0.6982552405137914,0.18885498925842517,0.632750235242101,0.17743620321381723]
# listeX = [16.390565156936646,64.68388557434082,178.58747601509094,736.8456604480743]

# plt.scatter(listeX,listeY)
# plt.title("Erreur moyenne des différentes méthodes en fonction de leur temps d'exécution")
# plt.xlabel("Temps d'exécution (en seconde)")
# plt.ylabel("Erreur moyenne")

listeX = [-1,0,1]
listeY = [0,0,0]
plt.grid()
plt.plot(listeX, listeY,color='blue')
plt.plot(listeY,listeX,color='blue')

