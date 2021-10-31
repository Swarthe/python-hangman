#!/usr/bin/env python
#
# hangman: Play hangman
#
# Copyright (c) 2021 Zachary Mahboub <https://github.com/zaximlo>
# Copyright (c) 2021 Emil Overbeck <https://github.com/Swarthe>
#
# Subject to the EUPL-1.2 license or later. See LICENSE.txt for more
# information.
#

import os
import random
import pygame
import extra

#
# Setup
#

# Choisit dictionnaire
if os.path.isfile(extra.FICHIER_DICT):
    # Dictionnaire *nix si possible
    dictionnaire = open(extra.FICHIER_DICT).read().splitlines()
    print('INFO:', "Using the system dictionary")
    print('INFO:', "The system language is", os.getenv('LANG'))
else:
    # Dictionnaire français sinon
    dictionnaire = open(extra.FICHIER_DICT_FALLBACK).read().splitlines()
    print('INFO:', "Using the fallback dictionary (French only)")

# Choisit un mot du dictionnaire, qui doit être en majuscules pour fonctionner
mot = random.choice(dictionnaire).upper()
mot_affiche = '–' * len(mot)

gagne = False
run = True
lettre_tapee = ''
essais = 10

lettres_essayees = []

# Montre lettres trop difficiles au début
for c in ["'", 'É', 'È', 'Ê', 'Ù', 'Ô', 'À', 'Ï']:
    mot_affiche = extra.convertit(extra.evalue(c, mot, mot_affiche))
    lettres_essayees.append(c)

pygame.init()

window = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

# Défini polices
POLICE_LETTRE = pygame.font.SysFont(None, 72)
POLICE_CONSIGNE = pygame.font.SysFont(None, 54)
POLICE_CONSEIL = pygame.font.SysFont(None, 32)
POLICE_MOT_AFFICHE = pygame.font.SysFont(None, 80)
POLICE_ANNONCE1 = pygame.font.SysFont(None, 100)
POLICE_ANNONCE2 = pygame.font.SysFont(None, 64)

#
# Fonctions
#
def render_text(window, Police, texte, couleur, y):
    '''
    window          : fenêtre où rendre le texte
    texte           : string à rendre au centre de l'écran
    police, couleur : apparence
    y               : hauteur dans la fenêtre
    pygame.Surface, pygame.font.Font, str, tuple, int -> void
    '''
    render_text = Police.render(texte, True, couleur)
    # coord est les coordonnées du texte si le texte est au centre de l'écran
    # avec une hauteur y
    coord = render_text.get_rect(center = (400, y))
    window.blit(render_text, coord)


def annonce_fin(gagne, reponse):
    '''
    Cours séquence de fin de jeu
    bool -> void
    '''
    if gagne:
        render_text(window, POLICE_ANNONCE1, 'VICTORY', extra.C_VERT, 250)
        render_text(window, POLICE_ANNONCE2, f'The word was {reponse}',
                    extra.C_BLANC, 450)

    else:
        render_text(window, POLICE_ANNONCE1, 'DEFEAT', extra.C_ROUGE, 250)
        render_text(window, POLICE_ANNONCE2, f'The word was {reponse}',
                    extra.C_ROUGE, 450)

def interprete_touche():
    '''
    Interprète touches de clavier
    void -> bool
    '''
    global lettre_tapee
    global run

    # Quit
    if event.type == pygame.QUIT:
        run = False
        return False

    if event.type == pygame.KEYDOWN:
        # Annule
        if event.key == pygame.K_BACKSPACE:
            lettre_tapee = ''
            return False
        # Lettre
        elif event.key == 13:
            return True
        # Ne différencie pas les majuscules
        elif event.unicode.islower() or event.unicode.isupper():
            lettre_tapee = event.unicode.capitalize()
            return False

#
# Main
#

while run:
    # Rempli l'écran en gris
    window.fill(extra.C_GRIS)
    entrer = False

    for event in pygame.event.get():
        if interprete_touche():
            entrer = True
        else:
            continue

    if essais > 0 and not gagne:
        # Écrit la consigne
        render_text(window, POLICE_MOT_AFFICHE, mot_affiche, extra.C_BLANC, 75)
        render_text(window, POLICE_CONSIGNE, f'Tries left:  {essais}',
                    extra.C_BLANC, 450)

        # Vérifie si la lettre est dans le mot et a déjà été essayée
        if lettre_tapee in mot and lettre_tapee in lettres_essayees:
            couleur_lettre = extra.C_VERT

        # Vérifie si la lettre a déjà été essayée mais n'est pas dans le mot
        elif lettre_tapee in lettres_essayees:
            couleur_lettre = extra.C_ROUGE

        # Sinon, si elle n'est pas une lettre essayée
        else:
            couleur_lettre = extra.C_BLEU

        render_text(window, POLICE_LETTRE, lettre_tapee, couleur_lettre, 500)

        if entrer:
            if lettre_tapee in mot and lettre_tapee not in lettres_essayees:
                mot_affiche = extra.convertit(extra.evalue(lettre_tapee, mot,
                                                           mot_affiche))
            elif lettre_tapee in lettres_essayees:
                render_text(window, POLICE_CONSEIL, 'Already entered',
                            extra.C_VIOLET, 550)
                pygame.time.wait(250)

            else:
                essais -= 1

            lettres_essayees.append(lettre_tapee)

        if mot == mot_affiche:
            gagne = True

    else:
        annonce_fin(gagne, mot)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
