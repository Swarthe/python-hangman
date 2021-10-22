#!/usr/bin/env python
#
# hangman: Play hangman
#
# Copyright (c) 2021 Zachary Mahboub <https://github.com/zaximlo>
# Copyright (c) 2021 Emil Overbeck <https://github.com/Swarthe>
#
# Subject to the MIT License. See LICENSE.txt for more information.
#

import pygame
import sys

sys.path.append("./gui.py")
import extra as e

#
# Setup
#

# TODO: get a full dictionnary to randomly choose from, maybe with options
mot = 'TABLE'
mot_affiche = '-' * len(mot)

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
Police_Mot_affiche = pygame.font.SysFont(None, 80)
Police_Annonce1 = pygame.font.SysFont(None, 100)
Police_Annonce2 = pygame.font.SysFont(None, 64)

#
# Main
#

while run:
    # Rempli l'écran en bleu
    window.fill((0, 51, 153))

    entrer = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        # Interpréte touches de clavier
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                lettre_tapee = ''

            # Si il s'agit d'une nouvelle lettre non essayé
            elif event.key == 13 and lettre_tapee not in lettres_essayees:
                entrer = True


            # Si il s'agit d'une lettre
            elif event.unicode.islower() or event.unicode.isupper():
                lettre_tapee = event.unicode.capitalize()


    if essais > 0 and not gagne:
        # Ecrit la consigne
        e.render_text(window, Police_Mot_affiche, mot_affiche, e.c_blanc, 75)
        e.render_text(window, Police_Consigne, f'essais restants :  {essais}', e.c_blanc, 450)

        # Vérifie si la lettre est dans le mot et a déjà été essayée
        if lettre_tapee in mot and lettre_tapee in lettres_essayees:
            #la lettre affichée serait en vert fonce
            couleur_lettre = e.c_vert_fonce

        # Vérifie si la lettre a déjà été essayée mais n'est pas dans le mot
        elif lettre_tapee in lettres_essayees:
            # La lettre affichée est en violet
            couleur_lettre = e.c_rouge

        # Sinon, si elle n'est pas une lettre essayée
        else:
            # La lettre affichée est en jaune
            couleur_lettre = e.c_jaune

        e.render_text(window, Police_Lettre, lettre_tapee, couleur_lettre, 500)


        if entrer:
            lettres_essayees.append(lettre_tapee)
            if lettre_tapee in mot:
                mot_affiche = e.convertit(e.evalue(lettre_tapee, mot, mot_affiche))
            else:
                essais -= 1

        if mot == mot_affiche:
            gagne = True

    elif gagne:
        e.render_text(window, Police_Annonce1, 'YOU WON', e.c_vert, 200)
        e.render_text(window, Police_Annonce2, f'The word was {mot}', e.c_blanc, 450)

    else:
        e.render_text(window, Police_Annonce1, 'YOU LOST', e.c_rouge, 300)
        e.render_text(window, Police_Annonce2, f'The word was {mot}', e.c_rouge, 450)



    pygame.display.flip()
    clock.tick(60)
pygame.quit()
