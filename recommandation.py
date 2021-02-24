# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:15:10 2020

@author: Utilisateur

"""

from numpy import *
import matplotlib.pyplot as plt
import pandas as pd
from math import *
import time

db = pd.read_csv("toy_incomplet.csv",delimiter=' ')
tableau=db.to_numpy()

db = pd.read_csv("toy_complet.csv",delimiter=' ')
tableauReponse=db.to_numpy()

similariteMoyenneUtil1=[]
similariteMoyenneUtil2=[]

similariteCosinus=[]
similaritePearson=[]
tableauNotesExactes=array([[0.0 for i in range (1000)] for i in range(99)])

listeGraphiqueX = []
listeGraphiqueY = []

palierSimilaireListe = []

def calculSimilaritePearson(tableau,ligne): #On calcul la similarité entre la ligne "ligne" 
    for i in range (0,tableau.shape[0]): #On parcourt tous les utilisateurs
        utilisateur1=[]
        utilisateur2=[]
        for items in range (tableau[i].shape[0]): #On parcourt tous les items
            if (tableau[ligne][items]!=-1 and tableau[i][items]!=-1): 
            #On vérifie que l'item est noté par l'utilisateur avec qui on veut comparer et 
            #par l'utilisateur i
                utilisateur1.append(tableau[ligne][items]) #On prend en compte la note
                utilisateur2.append(tableau[i][items])     #On prend en compte la note
        
        #On applique l'algorithme de Pearson entre l'utilisateur "i" et l'utilisateur "ligne"
        sommeMoy1=0;
        sommeMoy2=0;
        
        for k in range (len(utilisateur1)):
            sommeMoy1+=utilisateur1[k]
            sommeMoy2+=utilisateur2[k]
            
        moyenneCoefUtil1 = sommeMoy1 / len(utilisateur1) #moyenne des coefs util 1
        moyenneCoefUtil2 = sommeMoy2 / len(utilisateur2) #moyenne des coefs util 2
        
        somme=0
        somme1=0
        somme2=0
        
        for k,j in zip(utilisateur1, utilisateur2):
            somme1 += (k - moyenneCoefUtil1) * (k - moyenneCoefUtil1)
            somme2 += (j - moyenneCoefUtil2) * (j - moyenneCoefUtil2)
            somme  += (k - moyenneCoefUtil1) * (j - moyenneCoefUtil2)
        
        pearson = somme / ((sqrt(somme1)) * (sqrt(somme2)))
        #On ajoute à la liste des similarite, celle entre "i" et "ligne"
        similaritePearson.append(pearson)
    
    return similaritePearson 
    #C'est une liste avec toutes les similarite entre "ligne" et les 10 premiers utilisateurs


def calculSimilariteCosinus(tableau,ligne): 
    for i in range (0,tableau.shape[0]): #Nombre de comparaisons avec l'utilisateur "ligne"
        utilisateur1=[]
        utilisateur2=[]
        for items in range (tableau[i].shape[0]): #On parcourt tous les items
            if (tableau[ligne][items]!=-1 and tableau[i][items]!=-1):
                utilisateur1.append(tableau[ligne][items])
                utilisateur2.append(tableau[i][items])
    
        somme=0
        somme1=0
        somme2=0
            
        for k,j in zip(utilisateur1, utilisateur2):
            somme1 += k * k
            somme2 += j * j 
            somme  += k * j
        
        similariteCos = somme / ((sqrt(somme1)) * (sqrt(somme2)))
        similariteCosinus.append(similariteCos)
        # print("la similarité avec le calcul du cosinus est de :",similariteCos)
        
    return similariteCosinus


# Méthode de la moyenne pour compléter les notes d'un utilisateur.
def methodeMoyenne (tableau,similarite,palierSimilaires,ligne) :
    for j in range (0,tableau[ligne].shape[0]): #On parcourt tous les items de l'utilisateur
        listePourMoyenneNotes=[]
        moyenneNotes=0
        if tableau[ligne][j] == -1: #Si l'item de l'utilisateur n'est pas rentré
            for k in range (0,tableau.shape[0]): #On parcourt tous les utilisateurs
                if tableau[k,j] != -1: #Si l'utilisateur k a noté l'item j
                    if similarite[k] > palierSimilaires:
                        #Si la similarite entre k et notre utilisateur est suffisante
                        #On ajoute la note de l'utilisateur k a une liste.
                        listePourMoyenneNotes.append(tableau[k][j])
            
            
            for l in range (len(listePourMoyenneNotes)):
                #On parcourt les notes retenues et on les sommes.
                moyenneNotes+=listePourMoyenneNotes[l]
            
            #On calcul la moyenne de ces notes : (somme des notes)/(nombre de notes)
            note=moyenneNotes/len(listePourMoyenneNotes)
            
            #print(note)
            
            #On remplit un tableau de 0 avec les notes obtenues (en valeur exacte)
            tableauNotesExactes[ligne,j]=float(note)
            #On ajoute un arrondi de la valeur exacte à un autre tableau
            tableau[ligne,j]=round(note)
                
    return tableau, tableauNotesExactes
    #On retournes les 2 tableaux obtenues


# Calcul des erreurs
def calculBiais(tableau,tableauNotesExactes):
    erreur=[]
    for i in range (tableau.shape[0]): #On ne compare que les 10 premiers utilisateurs
        for j in range (tableau[i].shape[0]): #On compare tous les items
            if (tableauNotesExactes[i,j]!=0.0):
                erreur.append(tableau[i,j]-tableauNotesExactes[i,j])
                
    somme=0
    for i in range (len(erreur)):
        somme+=erreur[i]
       
    biais=somme/len(erreur)
    return biais



def calculErreurMoyenne (tableau, tableauNotesExactes):
    erreur=[]
    for i in range (tableau.shape[0]): #On compare tous les utilisateurs
        for j in range (tableau[i].shape[0]): #On compare tous les items
            if (tableauNotesExactes[i,j]!=0.0):
                erreur.append(abs(tableau[i,j]-tableauNotesExactes[i,j]))    
        
    somme=0
    for i in range (len(erreur)):
        somme+=erreur[i]
     
    erreurMoyenne=somme/len(erreur)
    return erreurMoyenne


def scenarioPearson(tableau, tableauReponse,palierSimilaires):
    for i in range (0,tableau.shape[0]):
        #On calcul les similarite entre la ligne "i" et tous les autres
        similarite=calculSimilaritePearson(tableau,i) 
        """On va calculer les notes à rentrer dans le tableau.
        - tableau étant le tableau non complété, 
        - similarite est la liste de similarite entre l'utilisateur "i" et autres
        - palierSimilaire est le pallier que l'on choisit pour prendre en compte un utilisateur
            a partir de sa similarite avec l'utilisateur "i"
        - i est l'utilisateur
        """
        tableau, tableauNotesExactes=methodeMoyenne(tableau, similarite,palierSimilaires,i)
     
    #On va calculer le biais entre les notes du résultat obtenue et les notes exactes
    biais=calculBiais(tableau, tableauNotesExactes)
    #On va calculer l'erreur moyenne entre les notes du résultat obtenue et les notes exactes
    erreur=calculErreurMoyenne(tableau, tableauNotesExactes)
    print("Le biais est de : ",biais)
    print("L'erreur est de : ",erreur)
    
    return tableau,biais,erreur
    
def scenarioCosinus(tableau, tableauReponse,palierSimilaires):
    for i in range (0,tableau.shape[0]):
        #On calcul les similarite entre la ligne "i" et les 10 premières de tableau
        similarite=calculSimilariteCosinus(tableau,i) 
        """On va calculer les notes à rentrer dans le tableau.
        - tableau étant le tableau non complété, 
        - similarite est la liste de similarite entre l'utilisateur "i" et les 10 premiers
        - palierSimilaire est le pallier que l'on choisit pour prendre en compte un utilisateur
            a partir de sa similarite avec l'utilisateur "i"
        - i est l'utilisateur
        """
        tableau, tableauNotesExactes=methodeMoyenne(tableau, similarite,palierSimilaires,i)
        
    biais=calculBiais(tableau, tableauNotesExactes)
    erreur=calculErreurMoyenne(tableau, tableauNotesExactes)
    print("Le biais est de : ",biais)
    print("L'erreur moyenne est de : ",erreur)
    
    return tableau,biais,erreur



################################## Limite des similarité à prendre en compte
palierSimilaires = 0.75
##################################


for i in range (4):
    db = pd.read_csv("toy_incomplet.csv",delimiter=' ')
    tableau=db.to_numpy()
    t1=time.time()
    
    #tableau,biais,erreur=scenarioCosinus(tableau, tableauReponse, palierSimilaires)
    tableau,biais,erreur=scenarioPearson(tableau, tableauReponse, palierSimilaires)
    
    t2 = time.time()
    t = t2-t1
    print("Le programme tourne pendant ",t," secondes\n")
    
    listeGraphiqueX.append(t);
    listeGraphiqueY.append(erreur);
    
    palierSimilaireListe.append(palierSimilaires)
    palierSimilaires-=0.15
    

plt.plot(palierSimilaireListe,listeGraphiqueY)
plt.title("Méthode de Cosinus en User-based")
plt.xlabel("Palier de similarité")
plt.ylabel("Erreur moyen")

