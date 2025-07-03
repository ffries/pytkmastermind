# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 09:33:15 2025

@author: eddyo
"""

from random import randint

couleurs=["vert","violet","rouge","bleu","jaune","orange","cyan","blanc"]
nb_couleurs=6
len_code=4
nb_tentatives=10

def nb_pions(t,c):
    # t est la tentative et c le code
    bien_placees=[] # va contenir les couleurs bien placées de la tentative
    mal_placees=[] # va contenir les couleurs mal placées de la tentative
    utilises=[]
    for i in range(len(t)):
        if t[i]==c[i]:
            bien_placees.append(i)
            utilises.append(i)
    for i in range(len(t)):
        for j in range(len(c)):
            if t[i]==c[j] and i not in mal_placees and i not in bien_placees and j not in utilises:
                mal_placees.append(i)
                utilises.append(j)
    return len(bien_placees),len(mal_placees)

def partie():
    print("Vous allez jouer au Mastermind contre l'ordinateur.")
    print("Les couleurs disponibles sont :",end=" ")
    for i in range(nb_couleurs-1):
        print(couleurs[i],end=", ")
    print(couleurs[nb_couleurs-1],end=".")
    print()
    print("L'ordinateur choisit une combinaison au hasard")
    code=[couleurs[randint(0,nb_couleurs-1)] for i in range(len_code)]
    print("L'ordinateur a choisi !")
    tentatives=[]
    pions=[]
    while len(tentatives)<nb_tentatives:
        print("Il vous reste "+str(nb_tentatives-len(tentatives))+" tentatives.")
        tentative=[]
        for i in range(len_code):
            couleur=input("Veuillez saisir votre couleur numéro "+str(len(tentative)+1)+" : ")
            while couleur not in couleurs:
                couleur=input("Veuillez ressaisir votre couleur numéro "+str(len(tentative)+1)+" : ")
            tentative.append(couleur)
        tentatives.append(tentative)
        pions.append(nb_pions(tentative,code))
        for i in range(len(tentatives)):
            print(tentatives[i],pions[i])
        if pions[-1][0]==len_code:
            return "Le décodeur a gagné !"
    return "Le codeur a gagné !"

def distance(liste,matrice1,matrice2,coef):
    for i in range(int(len(matrice1)*coef)):
        if nb_pions(matrice1[-i-1],liste)!=matrice2[-i-1]:
            return True
    return False

def coefficient(chaine):
    if chaine=="Intermédiaire":
        coef=(6.64*len_code+5.46*nb_couleurs-31.42)/100
    else:
        coef=(5.91*len_code+6.71*nb_couleurs-25.15)/100
    return max(0,min(1,coef))

def coup(matrice1,matrice2,matrice3,coef):
    # matrice1 est la liste des coupsjoués
    # matrice2 est la liste des pions
    # matrice3 est la liste des coups possibles
    indice=randint(0,len(matrice3)-1)
    L=matrice3[indice]
    if len(matrice3)==nb_couleurs**len_code:
        matrice3.pop(indice)
        return L
    while distance(L,matrice1,matrice2,coef):
        matrice3.pop(indice)
        indice=randint(0,len(matrice3)-1)
        L=matrice3[indice]
    matrice3.pop(indice)
    return L
    
def exhaustif(prefix, k, L, result):
    if k == 0:
        result.append(prefix)
    else:
        for x in L:
            exhaustif(prefix + [x], k - 1, L, result)

def partieCodeur(difficulte):
    print("Vous allez jouer au Mastermind contre l'ordinateur.")
    print("Les couleurs disponibles sont :",end=" ")
    for i in range(nb_couleurs-1):
        print(couleurs[i],end=", ")
    print(couleurs[nb_couleurs-1],end=".")
    print()
    code=[]
    for i in range(len_code):
        couleur=input("Veuillez saisir votre couleur numéro "+str(len(code)+1)+" : ")
        while couleur not in couleurs:
            couleur=input("Veuillez ressaisir votre couleur numéro "+str(len(code)+1)+" : ")
        code.append(couleur)
    print("Vous avez choisi !")
    tentatives=[]
    pions=[]
    coups_possibles=[]
    exhaustif([], len_code, couleurs[:nb_couleurs], coups_possibles)
    coef=coefficient(difficulte)
    while len(tentatives)<nb_tentatives:
        print("Il vous reste "+str(nb_tentatives-len(tentatives))+" tentatives.")
        tentative=coup(tentatives,pions,coups_possibles,coef)
        tentatives.append(tentative)
        pions.append(nb_pions(tentative,code))
        for i in range(len(tentatives)):
            print(tentatives[i],pions[i])
        if pions[-1][0]==len_code:
            return "Le décodeur a gagné !",len(tentatives)
    return "Le codeur a gagné !",len(tentatives)
        
def test(n,difficulte):
    compteur=0
    l=[]
    max=0
    for i in range(n):
        chaine,coups=partieCodeur(difficulte)
        if chaine=="Le décodeur a gagné !":
            compteur+=1
            l.append(coups)
            if coups>max:
                max=coups
    l.sort()
    return compteur,sum(l)/n,max
    
    
    
    
    