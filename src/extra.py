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
# Constantes globales
#

# Liste de mots standard pour *nix
FICHIER_DICT = '/usr/share/dict/words'
# Sinon, dictionnaire français de dernier recours
FICHIER_DICT_FALLBACK = '../data/dict-fr.txt'

# Défini couleurs <https://www.color-hex.com/color-palette/36646>
C_GRIS   = (64, 69, 82)
C_BLANC  = (238, 238, 238)
C_ROUGE  = (227, 0, 0)
C_VERT   = (0, 207, 0)
C_BLEU   = (102, 168, 246)
C_VIOLET = (138, 103, 226)

# Source des images
SOURCE_IMAGE = '<https://www.iconbros.com/icons/ib-g-hangman>'

#
# Fonctions
#

def evalue(essai, mot_reponse, mot_affichage):
    '''
    Compare lettre essai au string mot_reponse, et retourne un string
    d'affichage avec la lettre sélectionnée dans mot_affichage
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
