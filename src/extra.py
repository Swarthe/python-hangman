#!/usr/bin/env python
#
# extra.py: Support functions for hangman
#
# Copyright (c) 2021 Emil Overbeck <https://github.com/Swarthe>
# Copyright (c) 2021 Zachary Mahboub <https://github.com/zaximlo>
#
# Subject to the EUPL-1.2 license or later. See LICENSE.txt for more
# information.
#

#
# Variables globales
#

# Liste de mots standard pour Unix
fichier_dictionnaire = '/usr/share/dict/words'
# Sinon, ressource web de mots standard (uniquement en anglais)
page_dictionnaire = 'https://www.mit.edu/~ecprice/wordlist.10000'

# Défini couleurs <https://www.color-hex.com/color-palette/36646>
c_gris = (64, 69, 82)
c_blanc = (238, 238, 238)
c_rouge = (227, 0, 0)
c_vert = (0, 207, 0)
c_bleu = (102, 168, 246)
c_violet = (138, 103, 226)

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
