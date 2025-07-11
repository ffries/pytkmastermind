#Créé par quertier2, le 20/06/2025 en Python
#Bibliotheques
import tkinter as tk

#variables globales
pas=4
rpion=20
rmarqueur=(2*rpion-pas)/4
rtrou=rpion/4
rptrou=rmarqueur/4
hligne=2*(pas+rpion)
#Rajouter numéro de la partie
nbparties=1
listejoueur=["toto","tata"]
decodeur=0
codeur=1
nbcouleurs=6
dictcouleurs={-1:"light gray",-2:"gray64",0:"red",1:"green",2:"blue",3:"yellow",4:"orange",5:"cyan",6:"purple",7:"magenta",8:"black",9:"white"}
dictcouleursreponse={-2:"gray64",0:"black",1:"white"}
nbcolonnes=5
nblignes=10
colonne=0
ligne=0
matjeu=[[-1]*nbcolonnes for i in range(nblignes+1)]
matjeu[nblignes]=[i for i in range(nbcolonnes)]
matreponse=[[-1]*nbcolonnes for i in range(nblignes)]

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
    Returns
    -------
    None.
    """
    canva.create_oval(x-r, y-r,x+r,y+r, fill=couleur)
    
def rectangle(canva,x,y,largeur,hauteur,couleur):
    canva.create_rectangle(x-largeur/2,y-hauteur/2,x+largeur/2,y+hauteur/2,fill=couleur)


def ligne_jeu(canva,listecercle,dictcouleurs,positionligne):
    """
    Fonction qui dessine une ligne de cercle dans l'espace jeu ou dans l'espace réponse
    Parameters
    ----------
    canva : Canva
    listecercle : liste d'int correspondant au code couleur des cercles à dessiner
    dictcouleurs : dictionnaire de string contenant les couleurs utilisées
    positionligne : int correpondant à l'ordonnée de  la ligne à dessiner'
    Returns
    -------
    None.
    """
    global largeurfenetre
    global pasx
    global nbcolonnes
    for i in range(nbcolonnes):
        couleur=dictcouleurs[listecercle[i]]
        cercle(canva,pasx*(i+1),positionligne,pasx/4,couleur)
        
def ligne_reponse(canva,listecercle,dictcouleurs,positionligne):
    global largeurfenetre
    global pasx
    global nbcolonnes
    for i in range(nbcolonnes):
        couleur=dictcouleurs[listecercle[i]]
        rectangle(canva,pasx*(i+1),positionligne,pasx/4,pasy/4,couleur)
    
def bouton_clique():
    print("coucou") 

def jouer():
    global hauteurfenetre
    global nblignes
    coup=[1,2,4,3,5,6,2]
    ligne_jeu(cnv,coup, dictcouleurs, ((4*hauteurfenetre)/5)/((nblignes+1)))

def choisircouleur(matrice,numerocouleur):
   
    global ligne
    global colonne
    global dictcouleurs
    
    print("couleur bouton:",dictcouleurs[numerocouleur])
    cercle(canvaslignes[ligne],pas+rpion+colonne*(pas+2*rpion),hligne/2,rpion,dictcouleurs[numerocouleur])
    matrice[ligne][colonne]=numerocouleur
    print(matrice,str(matrice))
    if(colonne<nbcolonnes-1):
        colonne+=1
    else:
        button.config(command=lambda :feedback(matjeu,matreponse))
    return None

def choisircode(matrice,numerocouleur):
    global ligne
    global colonne
    global dictcouleurs
    cercle(canvaslignes[nblignes],pas+rpion+colonne*(pas+2*rpion),hligne/2,rpion,dictcouleurs[numerocouleur])
    matrice[nblignes][colonne]=numerocouleur
    #Reste à gérer le cache
    

def feedback(matjeu, matreponse):
    #reste à traiter la victoire
    global nbcolonnes
    global nblignes
    global ligne
    global colonne
    
    # Le secret est le dernière ligne de la matrice de jeu
    tupSecret=matjeu[nblignes]
    
    # La liste réponse est la ligne en cours
    ListeReponse=matjeu[ligne]

    black = sum(s==g for s,g in zip(tupSecret,ListeReponse))
    white = sum(min(tupSecret.count(c), ListeReponse.count(c)) for c in set(ListeReponse)) - black
    
    # On remplit la matrice réponse avec les blacks et les white
    for i in range(black):
        matreponse[ligne][i]=0
    
    for j in range(white):
        matreponse[ligne][black+j]=1
        
    # On dessine les pions
    for i in range(nbcolonnes):
        if matreponse[ligne][i]!=-1:
            xcercle=pas+rmarqueur+i%(nbcolonnes//2++nbcolonnes%2)*(pas+2*rmarqueur)
            ycercle=pas+rmarqueur+i//(nbcolonnes//2+nbcolonnes%2)*(pas+2*rmarqueur)
            cercle(canvasreponses[ligne],xcercle,ycercle,rmarqueur,dictcouleursreponse[matreponse[ligne][i]])
        
    # On incrémente la ligne et on remet la colonne à zéro
    ligne+=1
    colonne=0
    
    if black==nbcolonnes :
        return True
    return False

# Création de la fenêtre principale
root = tk.Tk()
root.title("Mastermind")
#chaine de caractère pour definir la surface de la fenetre en fonction de la largeur et de la hauteur définies
#Création des Label frame poour séparer l'espace de jeu du panneau de commande
espacecommande = tk.LabelFrame(root,text="Espace commande",relief='groove')
espacecommande.pack(side="bottom",padx=10,pady=10,fill="x")

espaceaffichage=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
espaceaffichage.pack(side="left",padx=0, pady=10, fill="y", expand=0.5)

espacejeu=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
espacejeu.pack(side="left",padx=0, pady=10)

espacereponse=tk.Frame(root, bd=4, relief="raised", padx=pas, pady=pas)
espacereponse.pack(side="left",padx=0, pady=10)

#espace affichage
labelnbparties = tk.Label(espaceaffichage, text="Partie sur "+str(nbparties))
labelnbparties.pack(side="top")
labeljoueur1=tk.Label(espaceaffichage,text="Codeur :"+listejoueur[codeur])
labeljoueur1.pack(side="top")
labelscore1=tk.Label(espaceaffichage,text="Score :")
labelscore1.pack(side="top")
labeljoueur2=tk.Label(espaceaffichage,text="Decodeur :"+listejoueur[decodeur])
labeljoueur2.pack(side="top")
labelscore2=tk.Label(espaceaffichage,text="Score :")
labelscore2.pack(side="top")

# Lignes complétées par le décodeur, plus la ligne réponse
canvaslignes=[0]*(nblignes+1)
for i in range(nblignes+1):
    canvaslignes[i] = tk.Canvas(espacejeu, width=pas+(2*rpion+pas)*nbcolonnes, height=hligne,bg=dictcouleurs[-1])
    for j in range(nbcolonnes):
        cercle(canvaslignes[i],pas+rpion+j*(pas+2*rpion),hligne/2,rtrou,dictcouleurs[-2])
    canvaslignes[i].pack()

# Lignes de 
canvasreponses=[0]*(nblignes+1)
for i in range(nblignes):
    canvasreponses[i]=tk.Canvas(espacereponse,width=pas+(nbcolonnes//2+nbcolonnes%2)*(2*rmarqueur+pas),height=hligne,bg=dictcouleurs[-1])
    for j in range(nbcolonnes):
        cercle(canvasreponses[i],pas+rmarqueur+j//2*(pas+2*rmarqueur),pas+rmarqueur+j%2*(pas+2*rmarqueur),rptrou,dictcouleurs[-2])
    canvasreponses[i].pack()

canvasreponses[nblignes]=tk.Canvas(espacereponse,width=pas+(nbcolonnes//2+nbcolonnes%2)*(2*rmarqueur+pas),height=hligne,bg=dictcouleurs[-1])
canvasreponses[nblignes].pack()

# Espace commande
buttonquit=tk.Button(espacecommande, text = 'Quitter', command = root.destroy)
buttonquit.pack(side="bottom")
#Initialisation de la liste qui va contenir les boutons de couleurs
boutons_couleur=[0]*nbcouleurs 
#Création du bouton annuler qui correspond à la couleur d'initialisation couleurs[0]
#boutons_annuler=tk.Button(espacecommande,text="Annuler", command=lambda : cercle(cnv,20,20,10,"red") )
#boutons_annuler.pack(side="left", fill="x", expand=1)
#Parcours de la liste de couleurs pour créer les boutons de couleurs sauf la couleur d'initialisation
for i in range(nbcouleurs):
    print("dictionnaire de couleurs",dictcouleurs[i], "i=", i)
    #i=i permet de garder la valeur actuelle de i sinon on capteur la référence à la variable i qui continue d'évoluer et vaut 5 quand on clique sur le bouton
    boutons_couleur[i]=tk.Button(espacecommande,text=dictcouleurs[i],command=lambda ifixe=i:choisircouleur(matjeu,ifixe))
    boutons_couleur[i].pack(side="left", fill="x", expand=1)
# boutons_couleur[0]=tk.Button(espacecommande,text=dictcouleurs[0],command=lambda:choisircouleur(matjeu,0))
# boutons_couleur[0].pack(side="left", fill="x", expand=1)
# boutons_couleur[1]=tk.Button(espacecommande,text=dictcouleurs[1],command=lambda:choisircouleur(matjeu,1))
# boutons_couleur[1].pack(side="left", fill="x", expand=1)

button = tk.Button(espacecommande,text="Valider", command=bouton_clique)
button.pack(side="left")

#Boucle principale


#initialisation_plateau()
positionligne=40
# coul=(couleurs[2])
# #cercle(cnv,20,20,10,"red")

# coup=[0,1,2,4,5,6,0]
# ligne_jeu(cnv,coup, couleurs, 80)
# res=[7,6,5,7,7]
# ligne_jeu(cnv2,res, couleurs, 40)


root.mainloop()

