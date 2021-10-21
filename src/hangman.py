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
from extra import *

pygame.init()

surf = pygame.display.set_mode((800,600))
run = True
lettre = ''

Police_Lettre = pygame.font.SysFont(None, 72)
Police_Consigne = pygame.font.SysFont(None, 54)

clock = pygame.time.Clock()

essais = 10

lettres_essayees = []
while run:
    # remplir l'écran en bleu
    surf.fill((0, 51, 153))

    entrer = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        # si on tape sur le clavier
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                lettre = ''

            # if we press enter
            elif event.key == 13 and lettre.isupper() and lettre not in lettres_essayees:
                entrer = True
                lettres_essayees.append(lettre)

            # Si il s'agit d'une lettre
            elif event.unicode.islower():
                lettre = event.unicode.capitalize()

    if essai > 0 and not win:
        # ecrire la consigne
        consigne = Police_Consigne.render(f'essais restants :  {essais}', True, (255, 255, 255))
        surf.blit(consigne, (250, 450))

        # verifier si la lettre a deja ete essayee
        if lettre in lettres_essayees:
            # la lettre affichee serait violette
            couleur_lettre = (178, 48, 221)
        else:
            # la lettre affichee serait jaune
            couleur_lettre = (255, 204, 0)

        choix = Police_Lettre.render(lettre, True, couleur_lettre)
        surf.blit(choix, (400, 500))

        # debug
        if entrer:
            'the thing'
            print(lettre)

            # essais -= 1
    elif win:
        print('win')
    else:
        run = False       # zachary




    pygame.display.flip()
    clock.tick(60)
pygame.quit()
