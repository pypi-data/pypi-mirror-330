import pdb
import braidpy.utilities as utl
from itertools import combinations


### SUBSTITUTION ####

def subst(str_lex, str_perc, c1, c2):
    """
    Checks if the string str_lex can be transformed into str_perc by replacing one character c1 with another character c2

    :param str_lex: the first string
    :param str_perc: the string to be corrected
    :param c1: the character in str_lex that is being replaced
    :param c2: the character that is in the correct position in the second string
    :return: True or False
    """
    idx = [i for i, x in enumerate(str_lex) if x == c1]
    for i in idx:
        if str_lex[:i] + c2 + (str_lex[i + 1:] if i < len(str_lex) - 1 else "") == str_perc:
            return True
    return False


def detect_substitution_n_error(stim, str_lex, str_perc):
    """
    Checks whether the substitution of a phoneme in the stimulus is a substitution where both phonemes usually share a letter (like a/an etc)
"""
    """ substitution in an "on", "an" etc grapheme
    """
    # parfois rajoute une consonne qui n'est pasla bonne -> pas changement de voyelle
    # ou remplace un phonème par m/n -> mot correct
    str_perc = utl.str_transfo(str_perc)
    letters = {'a': 'a@', 'i': 'i5', 'o': 'o&u', 'u': '5y', 'e': '@e2°'}
    for l, ph in letters.items():
        if l + 'n' in stim[:-1] or l + 'm' in stim[:-1]:  # il faut qu'il y ait encore une lettre après
            if len(ph) > 2:
                for tuple in combinations(ph, 2):
                    if subst(str_lex, str_perc, tuple[0], tuple[1]) or subst(str_lex, str_perc, tuple[1], tuple[0]):
                        return True
            elif subst(str_lex, str_perc, ph[0], ph[1]) or subst(str_lex, str_perc, ph[1], ph[0]):
                if stim == 'coma':
                    print("coma")
                return True
    return False


def detect_substitution_schwa_error(str_lex, str_perc):
    """
    Checks if there is a schwa substitution
    """
    grapheme_list = ['i', '5', 'y', 'e', 'a', 'o', '@', '&', '2']
    for g in grapheme_list:
        if subst(str_lex, str_perc, g, '°') or subst(str_lex, str_perc, '°', g):
            return True
    return False


def detect_substitution_grapheme_error(str_lex, str_perc):
    """
    Checks if the two strings differ by a single phoneme, and if the difference is one of the grapheme errors

    """
    grapheme_list = ['i5', 'yu', 'ij', 'ie', 'ao', 'a@', 'e@', 'ae', 'o&', 'ks', 'sz', '°e', 'gZ', '2e', 'st']
    for g in grapheme_list:
        if subst(str_lex, str_perc, g[0], g[1]) or subst(str_lex, str_perc, g[1], g[0]):
            return True
    return False


def detect_substitution_semi_voyelles_error(str_lex, str_perc):
    """
    Checks if the two strings differ by a single phoneme, and if the difference is one of the grapheme errors

    """
    grapheme_list = ['ow', 'uw', 'ij']
    for g in grapheme_list:
        if subst(str_lex, str_perc, g[0], g[1]) or subst(str_lex, str_perc, g[1], g[0]):
            return True
    return False


def detect_end_substitution_error(str_lex, str_perc):
    """
    Detects substitution error at the last position

    """
    return str_perc[:-1] == str_lex[:-1]


def detect_generic_substitution_error(str_lex, str_perc):
    """ Detects substitution error
    """
    cpt = 0
    if len(str_lex) == len(str_perc):
        for i, j in zip(str_lex, str_perc):
            if i != j:
                cpt += 1
    return cpt == 1


def detect_substitution_error(stim, str_lex, str_perc):
    if detect_substitution_semi_voyelles_error(str_lex, str_perc):
        return "semi vowel substitution error"
    if detect_substitution_n_error(stim, str_lex, str_perc):
        return "xnx substitution error"
    if detect_substitution_schwa_error(str_lex, str_perc):
        return "schwa substitution error"
    if detect_substitution_grapheme_error(str_lex, str_perc):
        return "grapheme substitution error"
    if detect_end_substitution_error(str_lex, str_perc):
        return "end substitution error"
    if detect_generic_substitution_error(str_lex, str_perc):
        return "substitution error"
    return ""


##### INSERTION ######

def detect_generic_insertion_error(str_lex, str_perc):
    """ Detects insertion error
    """
    for i in range(len(str_perc)):
        str_perc_tmp = str_perc[:i] + (str_perc[i + 1:] if i < len(str_perc) - 1 else "")
        if str_perc_tmp == str_lex:
            return i, True
    return 0, False


def detect_insertion_error(str_lex, str_perc):
    i, val = detect_generic_insertion_error(str_lex, str_perc)
    if val:
        cons_phono = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 'R', 's', 't', 'v', 'z', 'S', 'G', 'J', 'N']
        if len(str_perc) == len(str_lex) + 1 and str_perc[:-1] == str_lex and str_perc[-1] == 's':
            return "silent S insertion error"
        if len(str_perc) == len(str_lex) + 1 and str_perc[:-1] == str_lex and str_perc[-1] in cons_phono:
            return "silent consonant insertion error"
        grapheme_list = ['i5', 'ij', 'ie', 'ao', 'a@', 'ae', 'o&', 'ow', 'ks', 'sz', '°e', 'gZ', '2e']
        for g in grapheme_list:
            if g in str_lex or g[::-1] in str_lex:
                return "grapheme insertion error"
        else:
            return "insertion error"
    return ""


##### DELETION ####

def detect_deletion_error(str_lex, str_perc):
    """ Detects deletion error
    """
    i, val = detect_generic_insertion_error(str_perc, str_lex)
    if val:
        cons_phono = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 'R', 's', 't', 'v', 'z', 'S', 'G', 'J', 'N']
        if len(str_lex) == len(str_perc) + 1 and str_perc == str_lex[:-1] and str_lex[-1] == 's':
            return "silent S deletion error"
        if len(str_lex) == len(str_perc) + 1 and str_perc == str_lex[:-1] and str_lex[-1] in cons_phono:
            return "silent consonant deletion error"
        if len(str_lex) == len(str_perc) + 1 and str_perc == str_lex[:-1]:
            return "end deletion error"
        elif (i > 0 and str_lex[i - 1] in cons_phono) or (i < len(str_lex) - 1 and str_lex[i + 1] in cons_phono):
            return "consonant cluster deletion error"
        else:
            return "deletion error"
    return ""
