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
    global nbcouleurs
    global decodeur
    global ligne
    global nblignes
    global colonne
    global nbcolonnes
    global canvaslignes
    global canvasreponses
    global matjeu
    global matreponse
    global numpartie
    global nbparties
    global score1
    global score2
    global listejoueur
    
    # Toutes les variables tkInter d'affichage dynamique doivent être passées en variables globales
    global sv_nbparties
    global sv_codeur
    global sv_decodeur
    global sv_score1
    global sv_score2
    global sv_zoneinfo
    
    global bouton_validerligne
    global bouton_partiesuivante
    global boutons_couleur
    
    # Désactiver le bouton valider pour empêcher de le cliquer
    bouton_validerligne.config(state="disabled")
    
    # Désactiver le bouton Partie suivante
    bouton_partiesuivante.config(state="disabled")
    
    if colonne==nbcolonnes:
        if decodeur:
            if feedback(matjeu, matreponse):
               
                sv_zoneinfo.set(f"Combinaison secrète découverte ! Partie {numpartie} gagnée par le décodeur.")
                
                # Incrémenter le score
                score1+=int(numpartie%2)
                score2+=int((numpartie+1)%2)
                
                # Désactiver les boutons d'ajout de couleur pour empêcher de les cliquer
                for i in range(nbcouleurs):
                    boutons_couleur[i].config(state="disabled")
                
                # Activer le bouton Partie suivante si ce n'est pas la dernière partie
                if numpartie < nbparties :
                    bouton_partiesuivante.config(state="normal")
                else :
                    # Si c'est la dernière partie, on affiche le résultat final
                    if score1>score2 :
                        sv_zoneinfo.set(f"Partie terminée. Victoire finale de {listejoueur[0]}")
                    elif score1<score2 :
                        sv_zoneinfo.set(f"Partie terminée. Victoire finale de {listejoueur[1]}")
                    else :
                        sv_zoneinfo.set(f"Partie terminée. Egalité entre les deux joueurs")
                        
            elif ligne==nblignes-1:
                sv_zoneinfo.set(f"Combinaison secrète non découverte ! Partie {numpartie} gagnée par le codeur.")
                
                # Incrémenter le score
                score1+=int((numpartie+1)%2)
                score2+=int(numpartie%2)
                
                # Désactiver les boutons d'ajout de couleur pour empêcher de les cliquer
                for i in range(nbcouleurs):
                    boutons_couleur[i].config(state="disabled")
                    
                # Activer le bouton Partie suivante si ce n'est pas la dernière partie
                if numpartie < nbparties :
                    bouton_partiesuivante.config(state="normal")
                else :
                    # Si c'est la dernière partie, on affiche le résultat final
                    if score1>score2 :
                        sv_zoneinfo.set(f"Partie terminée. Victoire finale de {listejoueur[0]}")
                    elif score1<score2 :
                        sv_zoneinfo.set(f"Partie terminée. Victoire finale de {listejoueur[1]}")
                    else :
                        sv_zoneinfo.set(f"Partie terminée. Egalité entre les deux joueurs")
            else:
                sv_zoneinfo.set(f"Ligne {ligne+1} validée. Sélectionnez la ligne {ligne+2} !")
                # On incrémente la ligne et on remet la colonne à zéro
                ligne+=1
                colonne=0
                
            # Affichage du score
            sv_score1.set("Score "+listejoueur[0]+" : "+str(score1))
            sv_score2.set("Score "+listejoueur[1]+" : "+str(score2))
            
        else:
            # On passe au joueur decodeur
            sv_zoneinfo.set("Code secret validé. C'est au décodeur de jouer !")
            
            #Vidage du canvas de codage
            canvaslignes[nblignes].delete('all')
            ligne=0
            colonne=0
            
            #Intervertir codeur et décodeur
            decodeur=not decodeur
            
    return None

def choisircouleur(matJ,numerocouleur,canvasL,bouton_validerligne):
    """
    Fonction qui permet d'afficher un pion de la couleur choisie'
    Parameters
    ----------
    matJ : int[nblignes+1][nbcolonnes]
    numerocouleur : int
    canvasL : le canvas permettant d'afficher les pions dans la partie coder ou décoder
    bouton_validerligne : le bouton Valider
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
        choisircode(matJ,numerocouleur,canvasL,bouton_validerligne)
        
    if colonne<nbcolonnes:
        bouton_validerligne.config(state="disabled")
    else :
        bouton_validerligne.config(state="normal")
    return None
    
    return None

def choisircode(matJ,numerocouleur,canvasL,bouton_validerligne):
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
    
    #global bouton_validerligne
    
    if colonne<nbcolonnes:
        #print("couleur bouton:",dictcouleurs[numerocouleur])
        cercle(canvasL[nblignes],pas+rpion+colonne*(pas+2*rpion),hligne/2,rpion,dictcouleurs[numerocouleur])
        matJ[nblignes][colonne]=numerocouleur
       # print(matJ,str(matJ))
        colonne+=1
        
    if colonne<nbcolonnes:
        bouton_validerligne.config(state="disabled")
    else :
        bouton_validerligne.config(state="normal")
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



def jeu_fenetre_principale(canvasL,canvasR):
    """
    Fonction qui remplit les pions au fur et maesure du jeu dans la fenêtre principale

    Parameters
    ----------
    canvasL : Liste de Canvas conenant les lignes jouées par le codeur
    canvasR : Liste de Canvas contenant les lignes jouées par le décodeur

    Returns
    -------
    None.

    """
    #Il reste à retirer les variables globales inutiles
    global pas
    global nbparties
    global numpartie
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
    global root
    # global espacecommande
    # global espaceaffichage
    global espacejeu
    global espacereponse
    
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

def initialiser_fenetre_principale(canvasL,canvasR):
    """
    Fonction qui initialise l'espace de jeu en vidant chacun des Canvas de son contenu et en remplissant par les petits trous

    Parameters
    ----------
    canvasL : 
    canvasL : Liste de Canvas conenant les lignes jouées par le codeur
    canvasR : Liste de Canvas contenant les lignes jouées par le décodeur

    Returns
    -------
    None.

    """
    #Il reste à retire les variables globales inutiles
    global nbcouleurs
    global pas
    global nbparties
    global numpartie
    global nblignes
    global ligne
    global colonne
    global rpion
    global nbcolonnes
    global hligne
    global dictcouleurs
    global rtrou
    global rmarqueur
    global rptrou
    global root
    global decodeur
    
    # global espacecommande
    # global espaceaffichage
    global espacejeu
    global espacereponse
    global matjeu
    global matreponse
   
    # Toutes les variables tkInter d'affichage dynamique doivent être passées en variables globales
    global sv_nbparties
    global sv_codeur
    global sv_decodeur
    global sv_score1
    global sv_score2
    global sv_zoneinfo
    
    global bouton_validerligne
    global bouton_partiesuivante
    global boutons_couleur
    
    # On commence par incrémenter le numéro de partie
    numpartie+=1
    
    # Désactiver le bouton partie suivante
    bouton_partiesuivante.config(state="disabled")
    
    #Modifier l'affichage
    sv_nbparties.set(f"Partie {numpartie} sur {nbparties}") 
    sv_codeur.set("Codeur : "+listejoueur[int(not decodeur)])
    sv_decodeur.set("Décodeur : "+listejoueur[int(decodeur)])
    
    # On grise le bouton Valider ligne
    bouton_validerligne.config(state="disabled")
    # On rend les boutons d'ajout de couleur à nouveau cliquables
    for i in range(nbcouleurs):
        boutons_couleur[i].config(state="normal")

    # Lignes complétées par le décodeur, plus la ligne complétée par le codeur
    for i in range(nblignes+1):
        canvasL[i].delete('all')
        for j in range(nbcolonnes):
            cercle(canvasL[i],pas+rpion+j*(pas+2*rpion),hligne/2,rtrou,dictcouleurs[-2])
        canvasL[i].pack()

    # Lignes résultats
    for i in range(nblignes):
        canvasR[i].delete('all')     
        for j in range(nbcolonnes):
            cercle(canvasR[i],pas+rmarqueur+j//2*(pas+2*rmarqueur),pas+rmarqueur+j%2*(pas+2*rmarqueur),rptrou,dictcouleurs[-2])
        canvasR[i].pack()
    print("matjeu :",matjeu, "\n mat reponse",matreponse)
    matjeu=[[-1]*nbcolonnes for i in range(nblignes+1)]
    matreponse=[[-1]*nbcolonnes for i in range(nblignes)]
    canvaslignes=[0]*(nblignes+1)
    canvasreponses=[0]*(nblignes+1)
    print("matjeu :",matjeu, "\n mat reponse",matreponse)
    
    # On se place à la dernière ligne qui correspond au code secret
    ligne=nblignes
    colonne=0
    
    # Interversion codeur et décodeur
    decodeur=not decodeur
    sv_zoneinfo.set("Le codeur doit saisir une combinaison secrète")
    

def creation_fenetre_principale():
    """
    Création de la fenêtre principale, avec l'interface graphique Tkinter
    Les différents espaces sont créés, ainsi que les boutons
    Parameters
    ----------
    ----------
    Returns None.
    """
    global pas
    global nbparties
    global numpartie
    global listejoueur
    global score1
    global score2
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
    global root
    global espacecommande
    global espaceaffichage
    global espacejeu
    global espacereponse
    global canvaslignes
    global canvasreponses
    
    # Toutes les variables tkInter d'affichage dynamique doivent être passées en variables globales
    global sv_nbparties
    global sv_codeur
    global sv_decodeur
    global sv_score1
    global sv_score2
    global sv_zoneinfo
    
    global bouton_validerligne
    global bouton_partiesuivante
    global boutons_couleur
    
    root.title("Mastermind")
    
    # Création des Label frame pour séparer l'espace de jeu du panneau de commande
    
    espacecommande.pack(side="bottom",padx=10,pady=10,fill="x")
    espaceaffichage.pack(side="left",padx=0, pady=10, fill="y", expand=0.5)
    espacejeu.pack(side="left",padx=0, pady=10)   
    espacereponse.pack(side="left",padx=0, pady=10)

    # Espace affichage
    sv_nbparties = tk.StringVar()
    sv_nbparties.set(f"Partie {numpartie} sur {nbparties}")  # Valeur initiale
    labelnbparties = tk.Label(espaceaffichage, textvariable=sv_nbparties)
    labelnbparties.pack(side="top")
    
    sv_codeur = tk.StringVar()
    sv_codeur.set("Codeur : "+listejoueur[int(not decodeur)])
    labelcodeur=tk.Label(espaceaffichage,textvariable=sv_codeur)
    labelcodeur.pack(side="top")

    sv_decodeur = tk.StringVar()
    sv_decodeur.set("Décodeur : "+listejoueur[int(decodeur)])
    labeldecodeur=tk.Label(espaceaffichage,textvariable=sv_decodeur)
    labeldecodeur.pack(side="top")
    
    sv_score1 = tk.StringVar()
    sv_score1.set("Score "+listejoueur[0]+" : "+str(score1))
    labelscore1=tk.Label(espaceaffichage,textvariable=sv_score1)
    labelscore1.pack(side="top")
    
    sv_score2 = tk.StringVar()
    sv_score2.set("Score "+listejoueur[1]+" : "+str(score2))
    labelscore2=tk.Label(espaceaffichage,textvariable=sv_score2)
    labelscore2.pack(side="top")
    
    sv_zoneinfo = tk.StringVar()
    sv_zoneinfo.set("Le codeur doit saisir une combinaison secrète")
    labelzoneinfo=tk.Label(espaceaffichage,textvariable=sv_zoneinfo)
    labelzoneinfo.pack(side="top")
    
    jeu_fenetre_principale(canvaslignes, canvasreponses)

    # Espace commande
    
    bouton_partiesuivante=tk.Button(espacecommande, text = 'Partie suivante', command = lambda : initialiser_fenetre_principale(canvaslignes, canvasreponses))
    bouton_partiesuivante.pack(side="bottom")
    bouton_partiesuivante.config(state="disabled")
    
    #Initialisation de la liste qui va contenir les boutons de couleurs
    boutons_couleur=[0]*nbcouleurs 
    
    # BOUTON ANNULER À RAJOUTER ? On peut remplacer le bouton quitter par annuler.
    #Création du bouton annuler qui correspond à la couleur d'initialisation couleurs[0]
    #boutons_annuler=tk.Button(espacecommande,text="Annuler", command=lambda : cercle(cnv,20,20,10,"red") )
    #boutons_annuler.pack(side="left", fill="x", expand=1)
    
    #Parcours de la liste de couleurs pour créer les boutons de couleurs sauf la couleur d'initialisation
    for i in range(nbcouleurs):
        #print("dictionnaire de couleurs",dictcouleurs[i], "i=", i)
        boutons_couleur[i]=tk.Button(espacecommande,text=dictcouleurs[i],command=lambda ifixe=i:choisircouleur(matjeu,ifixe,canvaslignes,bouton_validerligne))
        boutons_couleur[i].pack(side="left", fill="x", expand=1)

    # Bouton Valider
    bouton_validerligne = tk.Button(espacecommande,text="Valider ligne", command=bouton_valider)
    bouton_validerligne.pack(side="left")
    bouton_validerligne.config(state="disabled")

    
# Fonctions
def lancer_application():
    # Lance la fenêtre de paramètres
    fenetre_parametres()
    root.mainloop()


def valider_parametres():
    """ Fonction qui valide les parametres du jeu
    """
    global nbcolonnes, nbcouleurs, nbparties, listejoueur
    global NBpions, NBcouleurs, NBparties, Enom1, Enom2
    
    # Récupérer les paramètres des widgets
    nbcolonnes = int(NBpions.get())  # Nombre de pions sélectionnés
    nbcouleurs = int(NBcouleurs.get())  # Nombre de couleurs sélectionnées
    nbparties = int(NBparties.get())  # Nombre de parties sélectionnées
    listejoueur = [Enom1.get(), Enom2.get()]  # Noms de joueurs

    startwindow.destroy()  # Ferme la fenêtre Toplevel
    root.deiconify()       # Réaffiche la fenêtre principale
    creation_fenetre_principale()

def fenetre_parametres():
    # Lancer la fenêtre de démarrage
    #startwindow.mainloop()  # La boucle principale de la fenêtre startwindow
    # Création de la fenêtre de démarrage
    global NBpions, NBcouleurs, NBparties, Enom1, Enom2, startwindow

    startwindow = tk.Toplevel(root)
    startwindow.title("Paramètres du jeu Mastermind")
    startwindow.geometry("450x400")

    # Données initiales
    choixpions = [2, 4, 6]
    choixcolor = [2, 4, 6, 8]
    choixparties = [2, 4, 6]

    # Marges
    PAD_X = 15 # valeur espacement horizontal 15 pixels à gauche et à droite
    PAD_Y = 10 # valeur espacement vertical 10 pixels en haut et en bas

    # Largeur uniforme pour les champs
    COMBO_WIDTH = 20  # largeur menu deroulant
    ENTRY_WIDTH = 23  # largeur saisie du nom

    # Ligne 1 - Nombre de pions
    tk.Label(startwindow, text="Nombre de pions :").grid(row=0, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
    NBpions = ttk.Combobox(startwindow, values=choixpions, width=COMBO_WIDTH)
    NBpions.current(0)  # valeur par défaut
    NBpions.grid(row=0, column=1, padx=PAD_X, pady=PAD_Y)

    # Ligne 2 - Nombre de couleurs
    tk.Label(startwindow, text="Nombre de couleurs :").grid(row=1, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
    NBcouleurs = ttk.Combobox(startwindow, values=choixcolor, width=COMBO_WIDTH)
    NBcouleurs.current(0)  # valeur par défaut
    NBcouleurs.grid(row=1, column=1, padx=PAD_X, pady=PAD_Y)

    # Ligne 3 - Nombre de parties
    tk.Label(startwindow, text="Nombre de parties :").grid(row=2, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
    NBparties = ttk.Combobox(startwindow, values=choixparties, width=COMBO_WIDTH)
    NBparties.current(0)  # valeur par défaut
    NBparties.grid(row=2, column=1, padx=PAD_X, pady=PAD_Y)

    # Ligne 4 - Nom du joueur qui code
    tk.Label(startwindow, text="Nom du joueur qui code :").grid(row=3, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
    Enom1 = tk.Entry(startwindow, width=ENTRY_WIDTH)
    Enom1.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y)

    # Ligne 5 - Nom du joueur qui devine
    tk.Label(startwindow, text="Nom du joueur qui devine :").grid(row=4, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
    Enom2 = tk.Entry(startwindow, width=ENTRY_WIDTH)
    Enom2.grid(row=4, column=1, padx=PAD_X, pady=PAD_Y)

    # Ligne 6 - Bouton validation des choix
    Bvalid = tk.Button(startwindow, text="VALIDER", width=20, command=valider_parametres)
    Bvalid.grid(row=5, column=0, columnspan=2, pady=30)
    
    root.mainloop()

#Bibliotheques
import tkinter as tk
from tkinter import ttk

#variables globales
nbparties=4 # Doit être modifiable
numpartie=1 # Partie en cours.
nbcouleurs=6 # Doit être modifiable DEFAUT=6 MAX=10
nblignes=10 # Doit être modifiable DEFAUT=10
nbcolonnes=4 # Doit être modifiable DEFAUT=4
pas=4
rpion=20
rmarqueur=(2*rpion-pas)/4
rtrou=rpion/4
rptrou=rmarqueur/4
hligne=2*(pas+rpion)
listejoueur=["toto","tata"]
score1=0 # Score du joueur 1
score2=0 # Score du joueur 2
decodeur=False
dictcouleurs={-1:"light gray",-2:"gray64",0:"red",1:"green",2:"blue",3:"yellow",4:"orange",5:"cyan",6:"purple",7:"magenta",8:"black",9:"white"}
dictcouleursreponse={-2:"gray64",0:"black",1:"white"}
colonne=0
ligne=0

root = tk.Tk()
root.withdraw() # Cache la fenêtre principale pour l'instant

espacecommande = tk.LabelFrame(root,text="Espace commande",relief='groove')
espaceaffichage=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
espacejeu=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
espacereponse=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)

matjeu=[[-1]*nbcolonnes for i in range(nblignes+1)]
matreponse=[[-1]*nbcolonnes for i in range(nblignes)]
canvaslignes=[0]*(nblignes+1)
canvasreponses=[0]*(nblignes+1)

# Lancement du programme
lancer_application()


    