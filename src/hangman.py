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
import urllib.request
import extra

#
# Setup
#

# Choisit dictionnaire
if os.path.isfile(extra.fichier_dictionnaire):
    dictionnaire = open(extra.fichier_dictionnaire).read().splitlines()
    print('INFO:', 'Using local dictionary')
    print('INFO:', 'System language is', os.getenv('LANG'))
else:
    dictionnaire = urllib.request.urlopen(extra.page_dictionnaire) \
                                         .read().decode().splitlines()
    print('INFO:', 'Using remote dictionary')

# Choisit un mot du dictionnaire, qui doit être en majuscules pour fonctionner
mot = random.choice(dictionnaire).upper()
mot_affiche = '–' * len(mot)

gagne = False
run = True
lettre_tapee = ''
essais = 10

lettres_essayees = []

pygame.init()

window = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

# Défini polices
Police_Lettre = pygame.font.SysFont(None, 72)
Police_Consigne = pygame.font.SysFont(None, 54)
Police_Conseil = pygame.font.SysFont(None, 32)
Police_Mot_affiche = pygame.font.SysFont(None, 80)
Police_Annonce1 = pygame.font.SysFont(None, 100)
Police_Annonce2 = pygame.font.SysFont(None, 64)

#
# Fonctions
#
def victoire(statut):

    '''
    Cours séquence de fin de jeu
    bool -> void
    '''
    if statut:
        extra.render_text(window, Police_Annonce1,
                          'VICTORY / VICTOIRE', extra.c_vert, 250)
        extra.render_text(window, Police_Annonce2,
                          f'The word was {mot}', extra.c_blanc, 450)

    else:
        extra.render_text(window, Police_Annonce1,
                          'LOSS / PERTE', extra.c_rouge, 250)
        extra.render_text(window, Police_Annonce2,
                          f'The word was {mot}', extra.c_rouge, 450)

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
        # Lettre non essayée
        elif event.key == 13 and lettre_tapee not in lettres_essayees:
            return True
        # Lettre déjà essayée
        elif event.key == 13:
            extra.render_text(window, Police_Conseil,
                              'Already entered', extra.c_violet, 550)
            pygame.time.wait(250)
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
    window.fill(extra.c_gris)
    entrer = False

    for event in pygame.event.get():
        if interprete_touche():
            entrer = True
        else:
            continue

    if essais > 0 and not gagne:
        # Écrit la consigne
        extra.render_text(window, Police_Mot_affiche, mot_affiche, extra.c_blanc,
                          75)
        extra.render_text(window, Police_Consigne,
                      f'essais restants :  {essais}', extra.c_blanc, 450)

        # Vérifie si la lettre est dans le mot et a déjà été essayée
        if lettre_tapee in mot and lettre_tapee in lettres_essayees:
            couleur_lettre = extra.c_vert

        # Vérifie si la lettre a déjà été essayée mais n'est pas dans le mot
        elif lettre_tapee in lettres_essayees:
            couleur_lettre = extra.c_rouge

        # Sinon, si elle n'est pas une lettre essayée
        else:
            couleur_lettre = extra.c_bleu

        extra.render_text(window, Police_Lettre, lettre_tapee, couleur_lettre,
                          500)

        if entrer:
            lettres_essayees.append(lettre_tapee)

            if lettre_tapee in mot:
                mot_affiche = extra.convertit(extra.evalue(lettre_tapee, mot,
                                                           mot_affiche))
            else:
                essais -= 1

        if mot == mot_affiche:
            gagne = True

    else:
        victoire(gagne)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
