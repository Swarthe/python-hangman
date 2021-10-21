#!/usr/bin/env python
#
# extra.py: Support functions for hangman
#
# Copyright (c) 2021 Emil Overbeck <https://github.com/Swarthe>
#
# Subject to the MIT License. See LICENSE.txt for more information.
#

# TODO: get a full dictionnary to randomly choose from, maybe with options
mot = list("priori")

def evalue(essai, mot_in):
    '''
    Retourne list de l'intersection mot <=> essai et valeur bool si cette
    intersection existe

    str, list -> list, bool
    '''
    mot_out = [ '-' ] * len(mot_in)
    success = False

    # TODO: make cap insensitive
    for i, c in enumerate(mot_in):
        if c == essai:
            mot_out[i] = essai
            success = True

    return mot_out, success

def convertit(char_list):
    '''
    Transform list en string
    list -> str
    '''
    return ''.join(char_list)
