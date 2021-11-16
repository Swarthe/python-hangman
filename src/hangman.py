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
import pathlib
import random
import pygame
import extra

#
# Setup
#

# Variables fichier

# Liste de mots standard pour *nix
FICHIER_DICT = pathlib.Path('/usr/share/dict/words')
# Sinon, dictionnaire français de dernier recours
FICHIER_DICT_FALLBACK = pathlib.Path(os.path.dirname(os.getcwd()) \
                                     + '/data/dict-fr.txt')
# Directoire d'images de pendu
DIR_IMAGE = pathlib.Path(os.path.dirname(os.getcwd()) + '/data/image')

# Choisit dictionnaire
if os.path.isfile(FICHIER_DICT):
    # Dictionnaire *nix si possible
    langue = os.getenv('LANG')
    dictionnaire = open(FICHIER_DICT).read().splitlines()
    print('INFO:', "Using the system dictionary")
    print('INFO:', "The system language is", langue)
else:
    # Dictionnaire français sinon
    langue = 'fr'
    dictionnaire = open(FICHIER_DICT_FALLBACK).read().splitlines()
    print('INFO:', "Using the fallback dictionary (French only)")

# Choisit un mot du dictionnaire, et met toutes les lettres en majuscules
mot = random.choice(dictionnaire).upper()
mot_affiche = '–' * len(mot)

# Organiser les images du pendu dans une liste
images_hangman = []

for i in range(1, 12):
    images_hangman.append(pygame.transform.scale(pygame.image.load(
                          pathlib.Path( f'{DIR_IMAGE}/hangman-{i}.png')),
                          (200, 200)))

# Définir les variables concernant le mot
gagne = False
run = True
lettre_tapee = ''
essais = 10
lettres_essayees = []

# Montre lettres trop difficiles au début
for c in ["'", 'É', 'È', 'Ê', 'Ù', 'Ô', 'À', 'Ï', "Â"]:
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

#
# Main
#

while run:
    # Rempli l'écran en gris
    window.fill(extra.C_GRIS)
    entrer = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # Annule
            if event.key == pygame.K_BACKSPACE:
                lettre_tapee = ''
            # Lettre
            elif event.key == pygame.K_RETURN:
                entrer = True

            # Ne différencie pas les majuscules
            elif event.unicode.islower() or event.unicode.isupper():
                lettre_tapee = event.unicode.capitalize()

    if essais > 0 and not gagne:
        # Écrit la consigne
        render_text(window, POLICE_MOT_AFFICHE, mot_affiche, extra.C_BLANC, 75)
        render_text(window, POLICE_CONSIGNE, f'Essais restants: {essais}',
                    extra.C_BLANC, 475)
        # Dessine l'image du pendu
        window.blit(images_hangman[10 - essais], (300, 225))

        # Vérifie si la lettre est dans le mot et a déjà été essayée
        if lettre_tapee in mot and lettre_tapee in lettres_essayees:
            couleur_lettre = extra.C_VERT
        # Vérifie si la lettre a déjà été essayée mais n'est pas dans le mot
        elif lettre_tapee in lettres_essayees:
            couleur_lettre = extra.C_ROUGE
        # Sinon, si elle n'est pas une lettre essayée
        else:
            couleur_lettre = extra.C_BLEU

        # Évalue la lettre et l'affiche de façon appropriée
        if entrer:
            if lettre_tapee in mot and lettre_tapee not in lettres_essayees:
                mot_affiche = extra.convertit(extra.evalue(lettre_tapee, mot,
                                                           mot_affiche))
                pygame.display.update()
            elif lettre_tapee in lettres_essayees:
                render_text(window, POLICE_CONSEIL, 'Déjà entrée',
                            extra.C_VIOLET, 575)
                pygame.display.update()
                pygame.time.wait(500)
            else:
                essais -= 1

            lettres_essayees.append(lettre_tapee)

        if mot == mot_affiche:
            gagne = True

        render_text(window, POLICE_LETTRE, lettre_tapee, couleur_lettre, 540)
        pygame.display.update()

    # Fin du jeu
    else:
        if gagne:
            render_text(window, POLICE_ANNONCE1, 'VICTOIRE', extra.C_VERT, 150)
            # Montre image pendu courante
            window.blit(images_hangman[10-essais], (300,225))
            render_text(window, POLICE_ANNONCE2, f'Le mot était {mot}',
                        extra.C_BLANC, 500)
        else:
            render_text(window, POLICE_ANNONCE1, 'DÉFAITE', extra.C_ROUGE, 150)
            # Montre image pendu perte
            window.blit(images_hangman[10], (300,225))
            render_text(window, POLICE_ANNONCE2, f'Le mot était {mot}',
                        extra.C_ROUGE, 500)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
