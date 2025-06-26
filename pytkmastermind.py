#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Créé par quertier2, le 20/06/2025 en Python
"""
Version du 26 juin à 22h48 par Flo. 
Reste à faire :
    - Rajouter un cache une fois que le codeur a rajouté son code.
    - Faire une remise à zéro du plateau pour pouvoir faire une nouvelle manche
    - Enlever le bouton "Quitter" et le remplacer par un bouton "Annuler" ?
    - Fait-on un message pour confirmer au codeur que son code secret est entré ?
    - Fait-on un message quand le décodeur valide en code sans mais qu'aucune couleur n'est présente ?
"""

#Bibliotheques
import tkinter as tk

#variables globales
nbparties=1 # Doit être modifiable
nbcouleurs=6 # Doit être modifiable DEFAUT=6 MAX=10
nblignes=10 # Doit être modifiable DEFAUT=10
nbcolonnes=4 # Doit être modifiable DEFAUT=4
pas=4
rpion=20
rmarqueur=(2*rpion-pas)/4
rtrou=rpion/4
rptrou=rmarqueur/4
hligne=2*(pas+rpion)
numpartie=1
listejoueur=["toto","tata"]
decodeur=False
dictcouleurs={-1:"light gray",-2:"gray64",0:"red",1:"green",2:"blue",3:"yellow",4:"orange",5:"cyan",6:"purple",7:"magenta",8:"black",9:"white"}
dictcouleursreponse={-2:"gray64",0:"black",1:"white"}
colonne=0
ligne=0
matjeu=[[-1]*nbcolonnes for i in range(nblignes+1)]
matreponse=[[-1]*nbcolonnes for i in range(nblignes)]
canvaslignes=[0]*(nblignes+1)
canvasreponses=[0]*(nblignes+1)

# Fonctions
def cercle(canva,x,y,r,couleur):
    """
    Fonction qui dessine un cercle
    Parameters
    ----------
    canva : Canvas
    x : int abscisse du centre 
    y : int ordonnee du centre
    r : int rayon du centre
    couleur : string correspondant à la couleur
    ----------
    Returns None.
    """
    canva.create_oval(x-r, y-r,x+r,y+r, fill=couleur)
    return None
    
def bouton_valider():
    """
    Action du bouton Valider
    ----------
    Returns None.
    """
    global decodeur
    global ligne
    global nblignes
    global colonne
    global nbcolonnes
    global canvaslignes
    global canvasreponses
    global matjeu
    global matreponse
    if colonne==nbcolonnes:
        if decodeur:
            if feedback(matjeu, matreponse):
                print("Victoire !")
                # Il reste à tout remettre à zéro pour recommencer une nouvelle partie
            elif ligne==nblignes-1:
                print("Perdu !")
            else:
                print("Ligne",ligne,"validée. Il faut continuer !")
                # On incrémente la ligne et on remet la colonne à zéro
                ligne+=1
                colonne=0
        else:
            # On passe au joueur decodeur
            print("Code secret validé. On passe au joueur décodeur !")
            ligne=0
            colonne=0
            decodeur=not decodeur
    return None

def choisircouleur(matJ,numerocouleur,canvasL,button):
    """
    Fonction qui permet d'afficher un pion de la couleur choisie'
    Parameters
    ----------
    matJ : int[nblignes+1][nbcolonnes]
    numerocouleur : int
    canvasL : le canvas permettant d'afficher les pions dans la partie coder ou décoder
    button : le bouton Valider
    ----------
    Returns None.
    """
    global ligne
    global colonne
    global nbcolonnes
    global dictcouleurs
    global decodeur
    global pas
    global rpion
    global hligne
    if decodeur:
        if colonne<nbcolonnes:
            #print("couleur bouton:",dictcouleurs[numerocouleur])
            cercle(canvasL[ligne],pas+rpion+colonne*(pas+2*rpion),hligne/2,rpion,dictcouleurs[numerocouleur])
            matJ[ligne][colonne]=numerocouleur
            #print(matJ,str(matJ))
            colonne+=1
    else:
        choisircode(matJ,numerocouleur,canvasL,button)
    return None

def choisircode(matJ,numerocouleur,canvasL,button):
    """
    Fonction qui permet au coder de rentrer son code, et qui affiche le code
    Parameters
    ----------
    matJ : int[nblignes+1][nbcolonnes]
    numerocouleur : int
    canvasL : le canvas permettant d'afficher les pions dans la partie coder ou décoder
    button : le bouton Valider
    ----------
    Returns None.
    """
    global colonne
    global dictcouleurs
    global nblignes
    global nbcolonnes
    global pas
    global rpion
    global hligne
    if colonne<nbcolonnes:
        #print("couleur bouton:",dictcouleurs[numerocouleur])
        cercle(canvasL[nblignes],pas+rpion+colonne*(pas+2*rpion),hligne/2,rpion,dictcouleurs[numerocouleur])
        matJ[nblignes][colonne]=numerocouleur
       # print(matJ,str(matJ))
        colonne+=1
    return None
    # Il reste à gérer le cache

def feedback(matJ, matR):
    """
    Fonction permettant de compter les pions bien placé, de compter les pions dont la couleur est bonne mais mal placés, puis d'afficher les pions (respectivement noirs et blancs)
    Parameters
    ----------
    matJ : int[nblignes+1][nbcolonnes]
    matR : int[nblignes][nbcolonnes]
    ----------
   Returns bool : permet de savoir si la manche est terminée (True) ou non (False)
    """
    global nbcolonnes
    global nblignes
    global ligne
    global pas
    global rmarqueur
    global dictcouleursreponse
    global canvasreponses
    
    tupSecret=matJ[nblignes]  # tupSecret est le dernière ligne de la matrice de jeu
    ListeReponse=matJ[ligne]  # ListeReponse est la ligne en cours

    black = sum(s==g for s,g in zip(tupSecret,ListeReponse)) # Nombre de pions bien placés
    white = sum(min(tupSecret.count(c), ListeReponse.count(c)) for c in set(ListeReponse)) - black # Nombre de pions corrects mais mal placés
    
    # On remplit la matrice réponse avec les blacks et les white
    for i in range(black):
        matR[ligne][i]=0   
    for j in range(white):
        matR[ligne][black+j]=1
        
    # On dessine les pions
    for i in range(nbcolonnes):
        if matR[ligne][i]!=-1:
            xcercle=pas+rmarqueur+i%(nbcolonnes//2++nbcolonnes%2)*(pas+2*rmarqueur)
            ycercle=pas+rmarqueur+i//(nbcolonnes//2+nbcolonnes%2)*(pas+2*rmarqueur)
            cercle(canvasreponses[ligne],xcercle,ycercle,rmarqueur,dictcouleursreponse[matR[ligne][i]])
    
    if black==nbcolonnes :
        return True
    return False

def creation_fenetre_principale(canvasL,canvasR):
    """
    Création de la fenêtre principale, avec l'interface graphique Tkinter
    Parameters
    ----------
    canvasL : le canvas permettant d'afficher les pions dans la partie coder ou décoder
    canvasR : le canvas permettant d'afficher les pions dans la partie résultats
    ----------
    Returns None.
    """
    global pas
    global nbparties
    global listejoueur
    global decodeur
    global nblignes
    global rpion
    global nbcolonnes
    global hligne
    global dictcouleurs
    global rtrou
    global rmarqueur
    global rptrou
    global nbcouleurs
    
    root = tk.Tk()
    root.title("Mastermind")
    # Chaine de caractère pour definir la surface de la fenetre en fonction de la largeur et de la hauteur définies
    # Création des Label frame poour séparer l'espace de jeu du panneau de commande
    espacecommande = tk.LabelFrame(root,text="Espace commande",relief='groove')
    espacecommande.pack(side="bottom",padx=10,pady=10,fill="x")

    espaceaffichage=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
    espaceaffichage.pack(side="left",padx=0, pady=10, fill="y", expand=0.5)

    espacejeu=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
    espacejeu.pack(side="left",padx=0, pady=10)

    espacereponse=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
    espacereponse.pack(side="left",padx=0, pady=10)

    # Espace affichage
    labelnbparties = tk.Label(espaceaffichage, text="Partie sur "+str(nbparties))
    labelnbparties.pack(side="top")
    labeljoueur1=tk.Label(espaceaffichage,text="Codeur :"+listejoueur[int(not decodeur)])
    labeljoueur1.pack(side="top")
    labelscore1=tk.Label(espaceaffichage,text="Score :")
    labelscore1.pack(side="top")
    labeljoueur2=tk.Label(espaceaffichage,text="Decodeur :"+listejoueur[int(decodeur)])
    labeljoueur2.pack(side="top")
    labelscore2=tk.Label(espaceaffichage,text="Score :")
    labelscore2.pack(side="top")

    # Lignes complétées par le décodeur, plus la ligne complétée par le codeur
    for i in range(nblignes+1):
        canvasL[i] = tk.Canvas(espacejeu, width=pas+(2*rpion+pas)*nbcolonnes, height=hligne,bg=dictcouleurs[-1])
        for j in range(nbcolonnes):
            cercle(canvasL[i],pas+rpion+j*(pas+2*rpion),hligne/2,rtrou,dictcouleurs[-2])
        canvasL[i].pack()

    # Lignes résultats
    for i in range(nblignes):
        canvasR[i]=tk.Canvas(espacereponse,width=pas+(nbcolonnes//2+nbcolonnes%2)*(2*rmarqueur+pas),height=hligne,bg=dictcouleurs[-1])
        for j in range(nbcolonnes):
            cercle(canvasR[i],pas+rmarqueur+j//2*(pas+2*rmarqueur),pas+rmarqueur+j%2*(pas+2*rmarqueur),rptrou,dictcouleurs[-2])
        canvasR[i].pack()

    canvasR[nblignes]=tk.Canvas(espacereponse,width=pas+(nbcolonnes//2+nbcolonnes%2)*(2*rmarqueur+pas),height=hligne,bg=dictcouleurs[-1])
    canvasR[nblignes].pack()

    # Espace commande
    buttonquit=tk.Button(espacecommande, text = 'Quitter', command = root.destroy)
    buttonquit.pack(side="bottom")
    
    #Initialisation de la liste qui va contenir les boutons de couleurs
    boutons_couleur=[0]*nbcouleurs 
    
    # BOUTON ANNULER À RAJOUTER ? On peut remplacer le bouton quitter par annuler.
    #Création du bouton annuler qui correspond à la couleur d'initialisation couleurs[0]
    #boutons_annuler=tk.Button(espacecommande,text="Annuler", command=lambda : cercle(cnv,20,20,10,"red") )
    #boutons_annuler.pack(side="left", fill="x", expand=1)
    
    #Parcours de la liste de couleurs pour créer les boutons de couleurs sauf la couleur d'initialisation
    for i in range(nbcouleurs):
        #print("dictionnaire de couleurs",dictcouleurs[i], "i=", i)
        boutons_couleur[i]=tk.Button(espacecommande,text=dictcouleurs[i],command=lambda ifixe=i:choisircouleur(matjeu,ifixe,canvaslignes,button))
        boutons_couleur[i].pack(side="left", fill="x", expand=1)

    # Bouton Valider
    button = tk.Button(espacecommande,text="Valider", command=bouton_valider)
    button.pack(side="left")

    root.mainloop()

# Lancement du programme
creation_fenetre_principale(canvaslignes,canvasreponses)