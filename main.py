import pygame
import sys
import random

# Définitions de la taille des cases , couleur des ligne , taille de la fenetre et la couleurs de celle ci
TAILLE_CASE = 100
COULEUR_LIGNE = (0, 0, 0)
HAUTEUR = 300
LARGEUR = 300
EPAISSEUR_LIGNE = 2
COULEUR_FOND = (255, 255, 255)

# Initialisation de la fenetre
pygame.init()
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Morpion TURNACO Jordan SN1')

# Class joueur avec un attribut qui prend son symbole X ou O
class Joueur:
    def __init__(self, symbole):
        self.symbole = symbole

# Class plateau avec une liste de liste qui represente la zone de jeu , et gere la condition de victoire
# affichages des assets un X et un O , dans le fichier assets
class Plateau:
    def __init__(self):
        self.plateau = [[' ' for _ in range(3)] for _ in range(3)]
        image_x = pygame.image.load(r'assets\x_image.png')
        image_o = pygame.image.load(r'assets\o_image.png')
        self.image_x = pygame.transform.scale(image_x, (TAILLE_CASE, TAILLE_CASE))
        self.image_o = pygame.transform.scale(image_o, (TAILLE_CASE, TAILLE_CASE))

    def dessiner_lignes(self):
        pygame.draw.line(ecran, COULEUR_LIGNE, (TAILLE_CASE, 0), (TAILLE_CASE, HAUTEUR), EPAISSEUR_LIGNE)
        pygame.draw.line(ecran, COULEUR_LIGNE, (2 * TAILLE_CASE, 0), (2 * TAILLE_CASE, HAUTEUR), EPAISSEUR_LIGNE)
        pygame.draw.line(ecran, COULEUR_LIGNE, (0, TAILLE_CASE), (LARGEUR, TAILLE_CASE), EPAISSEUR_LIGNE)
        pygame.draw.line(ecran, COULEUR_LIGNE, (0, 2 * TAILLE_CASE), (LARGEUR, 2 * TAILLE_CASE), EPAISSEUR_LIGNE)

    def dessiner_symboles(self):
        for ligne in range(3):
            for colonne in range(3):
                objet = self.plateau[ligne][colonne]
                if objet == 'X':
                    self.afficher_X(ligne, colonne)
        for ligne in range(3):
            for colonne in range(3):
                objet = self.plateau[ligne][colonne]
                if objet == 'O':
                    self.afficher_O(ligne, colonne)

    def afficher_X(self, ligne, colonne):
        x = colonne * TAILLE_CASE
        y = ligne * TAILLE_CASE
        if 0 <= x < LARGEUR and 0 <= y < HAUTEUR:
            ecran.blit(self.image_x, (x, y))

    def afficher_O(self, ligne, colonne):
        ecran.blit(self.image_o, (colonne * TAILLE_CASE, ligne * TAILLE_CASE))

    def verifier_victoire(self):
        for ligne in range(3):
            if self.plateau[ligne][0] == self.plateau[ligne][1] == self.plateau[ligne][2] != ' ':
                return True
        for colonne in range(3):
            if self.plateau[0][colonne] == self.plateau[1][colonne] == self.plateau[2][colonne] != ' ':
                return True
        if self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] != ' ':
            return True
        if self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] != ' ':
            return True
        return False

# Class jeu avec un plateau et deux joueurs , avec toute les methodes qui gere l'ia de l'adversaire , les affichages de fin de jeu
class Jeu:
    """
    Classe Jeu.

    Attributs:
        plateau (Plateau): Le plateau de jeu.
        joueur_courant (Joueur): Le joueur entrain de jouer.
        autre_joueur (Joueur): Le joueur qui ne joue pas.
        dernier_debutant (): Le symbole du dernier joueur à commencer.

    Methodes:
        joueur_IA(): Effectue le mouvement de l'IA.
        changer_joueur(): Change le joueur courant.
        recommencer(): Reintiallise le plateau de jeu -> nouvelle partie.
        afficher_message_fin(message): Affiche un message de fin de jeu.
        prompt_fin_jeu(): Affiche les boutons pour recommencer ou quitter le jeu.
        principal(): Fonction principale du jeu.
    """
    def __init__(self):
        self.plateau = Plateau()
        self.joueur_courant = Joueur('X')
        self.autre_joueur = Joueur('O')
        self.dernier_debutant = 'O'

    def joueur_IA(self):
        """
        Effectue le mouvement de l'IA.

        Returns:
            tuple: Les coordonnées de la case choisie par l'IA.
        """
        # Vérifie si l'IA peut gagner au prochain tour
        for ligne in range(3):
            for colonne in range(3):
                if self.plateau.plateau[ligne][colonne] == ' ':
                    self.plateau.plateau[ligne][colonne] = 'O'
                    if self.plateau.verifier_victoire():
                        return ligne, colonne
                    self.plateau.plateau[ligne][colonne] = ' '

        # Vérifie si l'IA doit bloquer le joueur pour qu'il ne gagne pas au prochain tour
        for ligne in range(3):
            for colonne in range(3):
                if self.plateau.plateau[ligne][colonne] == ' ':
                    self.plateau.plateau[ligne][colonne] = 'X'
                    if self.plateau.verifier_victoire():
                        self.plateau.plateau[ligne][colonne] = 'O'
                        return ligne, colonne
                    self.plateau.plateau[ligne][colonne] = ' '

        # Choisit une case libre au hasard
        while True:
            ligne = random.randint(0, 2)
            colonne = random.randint(0, 2)
            if self.plateau.plateau[ligne][colonne] == ' ':
                self.plateau.plateau[ligne][colonne] = 'O'
                return ligne, colonne

    def changer_joueur(self):
        """
        Change le joueur courant.
        """
        self.joueur_courant, self.autre_joueur = self.autre_joueur, self.joueur_courant

    def recommencer(self):
        """
        Réinitialise le jeu -> Nouvelle Partie.
        """
        self.plateau = Plateau()
        if self.dernier_debutant == 'X':
            self.joueur_courant = Joueur('O')
            self.autre_joueur = Joueur('X')
            self.dernier_debutant = 'O'
        else:
            self.joueur_courant = Joueur('X')
            self.autre_joueur = Joueur('O')
            self.dernier_debutant = 'X'

    def afficher_message_fin(self, message):
        """
        Affiche un message de fin de jeu.

        Args:
            message (str): Le message à afficher.
        """
        pygame.time.delay(500)
        ecran.fill(COULEUR_FOND)
        police = pygame.font.Font(None, 36)
        texte = police.render(message, True, COULEUR_LIGNE)
        ecran.blit(texte, (LARGEUR // 2 - texte.get_width() // 2, HAUTEUR // 2 - texte.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)

    def prompt_fin_jeu(self):
        """
        Affiche les boutons pour recommencer ou quitter le jeu.
        """
        bouton_recommencer = pygame.Rect(LARGEUR // 2 - 85, HAUTEUR // 2 + 50, 70, 40)
        bouton_quitter = pygame.Rect(LARGEUR // 2 + 15, HAUTEUR // 2 + 50, 70, 40)

        while True:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    position_souris = evenement.pos
                    if bouton_recommencer.collidepoint(position_souris):
                        self.recommencer()
                        return
                    elif bouton_quitter.collidepoint(position_souris):
                        pygame.quit()
                        sys.exit()

            pygame.draw.rect(ecran, (0, 255, 0), bouton_recommencer)
            pygame.draw.rect(ecran, (255, 0, 0), bouton_quitter)

            police = pygame.font.Font(None, 24)
            texte_recommencer = police.render('Relancer', True, (0, 0, 0))
            ecran.blit(texte_recommencer,
                        (LARGEUR // 2 - 85 + 35 - texte_recommencer.get_width() // 2,
                         HAUTEUR // 2 + 50 + 20 - texte_recommencer.get_height() // 2))
            texte_quitter = police.render('Quitter', True, (0, 0, 0))
            ecran.blit(texte_quitter,
                        (LARGEUR // 2 + 15 + 35 - texte_quitter.get_width() // 2,
                         HAUTEUR // 2 + 50 + 20 - texte_quitter.get_height() // 2))

            pygame.display.flip()

    def principal(self):
        """
        Fonction principale du jeu qui gère tout.
        """
        en_cours = True
        while en_cours:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evenement.type == pygame.MOUSEBUTTONDOWN and self.joueur_courant.symbole == 'X':
                    positionX_souris, positionY_souris = pygame.mouse.get_pos()
                    ligne_cliquee = positionY_souris // TAILLE_CASE
                    colonne_cliquee = positionX_souris // TAILLE_CASE
                    if self.plateau.plateau[ligne_cliquee][colonne_cliquee] == ' ':
                        self.plateau.plateau[ligne_cliquee][colonne_cliquee] = self.joueur_courant.symbole
                    if self.plateau.verifier_victoire():
                        pygame.time.delay(1000)
                        self.afficher_message_fin(f"le joueur :  {self.joueur_courant.symbole} a gagné!")
                        pygame.time.delay(200)
                        self.prompt_fin_jeu()
                    elif ' ' not in [cellule for ligne in self.plateau.plateau for cellule in ligne]:
                        self.afficher_message_fin("Égalité!")

                        pygame.time.delay(200)
                        self.prompt_fin_jeu()
                    self.changer_joueur()
                elif self.joueur_courant.symbole == 'O':
                    mouvement = self.joueur_IA()
                    if mouvement:
                        self.plateau.plateau[mouvement[0]][mouvement[1]] = 'O'
                        if self.plateau.verifier_victoire():
                            pygame.time.delay(1000)
                            self.afficher_message_fin(f"le joueur :  {self.joueur_courant.symbole} a gagné!")
                            pygame.time.delay(200)
                            self.prompt_fin_jeu()
                        elif ' ' not in [cellule for ligne in self.plateau.plateau for cellule in ligne]:
                            self.afficher_message_fin("Égalité !")
                            pygame.time.delay(200)
                            self.prompt_fin_jeu()
                        self.changer_joueur()

            ecran.fill(COULEUR_FOND)
            self.plateau.dessiner_lignes()
            self.plateau.dessiner_symboles()
            pygame.display.update()

if __name__ == "__main__":
    jeu = Jeu()
    jeu.principal()