#!/usr/bin/env python
#
# extra.py: Support functions for hangman
#
# Copyright (c) 2021 Emil Overbeck <https://github.com/Swarthe>
# Copyright (c) 2021 Zachary Mahboub <https://github.com/zaximlo>
#
# Subject to the MIT License. See LICENSE.txt for more information.
#

#
# Variables globales
#

# Défini couleurs
c_blanc = (255, 255, 255)
c_rouge = (255, 0, 0)
c_vert = (0, 255, 0)
c_jaune = (255, 204, 0)
c_vert_fonce = (85, 107, 47)

#
# Fonctions
#

def evalue(essai, mot_reponse, mot_affichage):
    '''
    Compare lettre essai au string mot_reponse, et retourne un string
    d'affichage avec la lettre sélectionnée et les lettres précédemment passé au
    choix avec mot_affichage
    str, str, str -> list
    '''
    retval = [x for x in mot_affichage]
    for i in range(len(mot_reponse)):
        if essai == mot_reponse[i]:
            retval[i] = essai
    return retval

def convertit(char_list):
    '''
    Transforme list en string
    list -> str
    '''
    return ''.join(char_list)

def render_text(window, Police, texte, couleur, y):
    '''
    Rendre le string_texte_ avec la police _Police_ en _couleur_ au centre de
    l'écran avec une hauteur _y_ dans la fenetre _window_
    pygame.Surface, pygame.font.Font, str, tuple, int -> void
    '''
    render_text = Police.render(texte, True, couleur)

    # coord est les coordonnées du texte si le texte est au centre de l'écran
    # avec une hauteur y
    coord = render_text.get_rect(center = (400, y))
    window.blit(render_text, coord)
