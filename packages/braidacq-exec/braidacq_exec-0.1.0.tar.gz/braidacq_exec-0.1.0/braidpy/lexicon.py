#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
from collections import defaultdict, Counter

import pandas as pd
import pdb
import numpy as np
import re
from Levenshtein import distance

from braidpy import _ROOT


def selectdf(df, lenMin, lenMax, maxItem, maxItemLen):
    """
    Filters the dataframe provided based on the provided parameters `lenMin`, `lenMax`, `maxItem`, and `maxItemLen`,

    :param df: The input dataframe
    :param lenMin: The minimum length of the 'len' column in the dataframe
    :param lenMax: The maximum length of the words to include in the dataframe
    :param maxItem: The maximum number of items to be selected from the dataframe based on the frequency column (most frequent words are kept)
    :param maxItemLen: The maximum number of items to keep for each length group.
    :return: a subset of the input dataframe `df` based on the provided conditions.
    """
    df['len'] = df['len'].astype(int)
    if 'phlen' in df.columns:
        df['phlen'] = df['phlen'].astype(int)
    if lenMin is not None and lenMax is not None:
        df = df[(df['len'] >= lenMin - 2) & (df['len'] <= lenMax + 2)].set_index('word')
    if maxItem is not None:
        df = df.nlargest(maxItem, 'freq')
    if maxItemLen is not None and (maxItem is None or maxItemLen < maxItem):
        df = df.groupby('len').apply(lambda x: x.sort_values(by='freq', ascending=False).head(maxItemLen)).reset_index(0, drop=True)
    # word as index
    return df.head(maxItem)


def extractLexicon(lexicon_name="BLP.csv", maxItem=None, maxItemLen=None, lenMin=None, lenMax=None,
                   fMin=0, fMinPhono=None, fMinOrtho=None, fMax=1000000, cat=None, phono=False, ortho=True, return_df=False):
    """
    Extracts the lexicon accoring to some selection criteria.

    :param lexicon_name: string. lexicon name.
    :param maxItem: The maximum number of items to be selected from the dataframe based on the frequency column (most frequent words are kept)
    :param maxItemLen: The maximum number of items to keep for each length group.
    :param lenMin: The minimum length of the 'len' column in the dataframe
    :param lenMax: The maximum length of the words to include in the dataframe
    :param fMin: float. minimum frequency for the words.
    :param fMinPhono: float. minimum phono frequency for the words to be included in the phono lexicon
    :param fMinOrtho: float. minimum ortho frequency for the words to be included in the ortho lexicon
    :param fMax: float. maximum frequency for the words.
    :param cat: string. grammatical category.
    :param phono: boolean. Modality extracted or not ?
    :param ortho: boolean. Modality extracted or not ?
    :param return_df: boolean. Must the df be returned instead of a list of word ?
    :return: A list of word or a dataframe.
    """
    # careful, if change lenMax, it changes the chosen words, this parameters cannot be progressively raised during expe.
    # MaxItemLen can be raised progressively
    df = pd.read_csv(os.path.join(_ROOT, 'resources/lexicon/', lexicon_name),
                     keep_default_na=False)
    # grammatical category
    if cat is not None and 'cat' in df.columns:
        df = df[df.cat == cat]
    df["word"] = df.word.str.replace("'", "").replace("-", "").replace(" ", "")
    if "pron" in df.columns:
        df["pron"] = df.pron.str.replace(" ", "")
        df["phlen"] = df.pron.str.len()
    col = ['len', 'word', 'freq'] + (['pron', 'phlen'] if phono and 'pron' in df.columns else [])
    # Homographs handling
    agg_fun = {key: 'first' for key in col}
    agg_fun['freq'] = 'sum'
    agg_fun['len'] = 'min'
    df = df.groupby('word').agg(agg_fun).reset_index(drop=True)
    df = df.assign(ortho=ortho).assign(phono=(phono & ('pron' in df.columns)))
    if fMin is not None:
        df = df[df['freq'] > fMin]
    if fMax is not None:
        df = df[df['freq'] < fMax]
    if fMinPhono is not None:
        df.loc[df['freq'] < fMinPhono, 'phono'] = False
    if fMinOrtho is not None:
        df.loc[df['freq'] < fMinOrtho, 'ortho'] = False
    df = selectdf(df, lenMin, lenMax, maxItem, maxItemLen)  # .to_dict()['freq']
    return df if return_df else list(df.reset_index().word)


def simplify_letters(df):
    """
    Simplifies the lexicon by merging some letters of the dataframe.

    :param df: input dataframe (lexicon)
    :return: the filtered dataframe
    """
    def f(val):
        a = {k: 'a' for k in ['à', 'â', 'ä', 'ã', 'á']}
        o = {k: 'o' for k in ['ö', 'ô', 'ó']}
        u = {k: 'u' for k in ['ù', 'û', 'ü', 'ú']}
        i = {k: 'i' for k in ['î', 'í']}
        return dict(**{' ': '', ':': '', '?': ''}, **a, **o, **u, **i)[val[0]]
    # handle cases where word is in the index.
    index_name = df.index.name
    if index_name is not None:
        df = df.reset_index()
    for col in ['orthosyll', 'segm', 'gpmatch', 'word']:
        if col in df.columns:
            df[col] = df[col].str.replace('ã|à|â|ä|á|ö|ô|ó|ù|û|ü|ú|î|í| |:|\?', f, regex=True)
    df.set_index(index_name if index_name is not None else 'word')
    return df


def simplify_phonemes(df, langue="fr"):
    """
    Simplifies the lexicon by merging some phonemes of the dataframe.

    :param df: input dataframe (lexicon)
    :return: the filtered dataframe
    """
    def f_fr(val):
        return {'O': 'o', 'E': 'e', 'I': 'i', '9': '2', '1': '5', '8': 'y', ' ': '', 'A': 'a', '*': '°', '§': '&', 'U': 'u', 'r': 'R'}[val[0]]

    def f_en(val):
        return {'O': 'o', 'I': 'i', ' ': '', 'U': 'u', '$': 'o', 'Q': 'o', 'r': 'R'}[val[0]]
    df.reset_index(inplace=True)
    for col in ['pron', 'syll', 'pseg', 'phono', 'gpmatch', 'pron_x', 'pron_y', 'word']:
        if col in df.columns and not df[col].dtype == 'bool':
            if col in df.columns:
                if langue == "fr":
                    df[col] = df[col].str.replace('O|E|I|9|1| |\*|8|§|r', f_fr, regex=True)
                elif langue == "en":
                    df[col] = df[col].str.replace('O|I| |U|\$|Q|r', f_en, regex=True)
    return df


def extract_spanish_lexicon(path):
    """
    Extracts the spanish lexicon from txt file and stores it as a csv file.

    :param path: path to the lexicon
    :return:
    """
    df = pd.read_csv(os.path.join(path, 'resources/lexicon/lexique_espagnol.txt'), sep='\t', encoding='latin')
    freq = pd.read_csv(os.path.join(path, 'resources/lexicon/freq_espagnol.txt'), sep='\t', encoding='latin')
    lex = df[['word', 'pron']].merge(freq, on='word')
    lex['pron'] = lex['pron'].str.replace('-', '')
    lex = simplify_letters(simplify_phonemes(lex))
    lex['len'] = lex.word.str.len()
    lex['phlen'] = lex.pron.str.len()
    lex.to_csv(os.path.join(path, 'resources/lexicon/lexique_espagnol.csv'))


def extractPM(path=_ROOT, lexicon_name="pwords.txt", lenMin=3, lenMax=8, maxItem=None, maxItemLen=None):
    """
    Reads a lexicon file and returns a list of words that meet certain length and frequency criteria.

    :param path: Directory path where the lexicon file is located. By default, it is set to "../".
    :param lexicon_name: Name of the lexicon file. By default, it is set to "pwords.txt", defaults to pwords.txt (optional)
    :param maxItem: The maximum number of items to be selected from the dataframe based on the frequency column (most frequent words are kept)
    :param maxItemLen: The maximum number of items to keep for each length group.
    :param lenMin: The minimum length of the 'len' column in the dataframe
    :param lenMax: The maximum length of the words to include in the dataframe
    :return: a list of indices from a DataFrame.
    """
    df = pd.read_csv(os.path.join(path, "resources/lexicon/PM/", lexicon_name), delimiter=' ', usecols=[1, 5])
    df.columns = ['freq', 'word']
    df['len'] = df['word'].str.len()
    return list(selectdf(df, lenMin, lenMax, maxItem, maxItemLen).index)


def extractPM_BLP(path=_ROOT, lexicon_name="pseudo-words-BLP.csv", lenMin=2, lenMax=8, maxItem=None, maxItemLen=None):
    """
    Reads a lexicon file and returns a list of words that meet certain length and frequency criteria. Should be the same format as the BLP format (some operations are needed to transform data).

    :param path: Directory path where the lexicon file is located. By default, it is set to "../".
    :param lexicon_name: Name of the lexicon file. By default, it is set to "pwords.txt", defaults to pwords.txt (optional)
    :param maxItem: The maximum number of items to be selected from the dataframe based on the frequency column (most frequent words are kept)
    :param maxItemLen: The maximum number of items to keep for each length group.
    :param lenMin: The minimum length of the 'len' column in the dataframe
    :param lenMax: The maximum length of the words to include in the dataframe
    :return: a list of indices from a DataFrame.
    """
    df = pd.read_csv(os.path.join(path, "resources/lexicon/PM/", lexicon_name), delimiter=',', usecols=[0, 1])
    df = df[df.lexicality == 'N']
    df.columns = ['word', 'lexicality']
    df['word'] = df['word'].str.replace('_', '')
    df['len'] = df['word'].str.len()
    return list(selectdf(df, lenMin, lenMax, maxItem, maxItemLen).index)


def extractLetterFreq(lexicon, letters):
    """
    Calculates letter frequency based on words frequency of all words in the lexicon.

    :param lexicon: lexicon dictionary (word,freq)
    :param letters: letters dictionary
    :return:
    """
    letterFreq = {key: 0 for key in letters.keys()}
    for word, f in lexicon.items():
        for letter in word:
            letterFreq[letter] += f
    s = sum(letterFreq.values())
    return {key: value / s for key, value in letterFreq.items()}


def del_index(s, i):
    """
    Removes index i from a string.

    :param s: string
    :param i: index
    :return:  the string without the index i
    """
    if i == len(s) - 1:
        return s[:-1]
    if i < len(s) - 1:
        return s[:i] + s[i + 1:]
    return None


def is_consistent(r1, r2):
    """
    TODO function in devlopment
    Calculates if 2 words are consistant with each other.
    definition consistance :
    MTM : A word is said to be consistent if its pronunciation agrees with those of similarly spelled words (its orthographic neighbors)
    Borleff2017 : consistency approach to measure transparency
    dichotomous approach : a word or smaller sized unit is regarded consistent when there is only one possible mapping and inconsistent when there are alternative mappings.
    gradual approach : the level of consistency is expressed as the proportion of dominant mappings over the total number of occurrences of the base unit analyzed.

    :param r1: first word
    :param r2: second word
    """
    # special case for words starting with a silent letter
    def h_begin(r):
        if r.segm[0] == 'h' and len(r.segm.split('.')[0]) > 0:
            r.segm = r.segm[0] + '.' + r.segm[1:]
            r.pseg = '#.' + r.pseg
        return r
    r1 = h_begin(r1)
    r2 = h_begin(r2)
    o1 = r1.segm
    o2 = r2.segm
    # pas de la même longueur : on ne calcule pas la consistance
    # absents / absente : on en fait quoi ??? règle contextuelle, mais c'est inconsistant ??
    # que faire avec longueur phono différente ?? a priori c'est non consistant non ??
    if o1 == o2 or len(o1.replace('.', '')) != len(o2.replace('.', '')):
        return True
    pos1 = [i for i, l in enumerate(o1) if l != '.']
    pos2 = [i for i, l in enumerate(o2) if l != '.']
    diff = [i for i, (oi, oj) in enumerate(zip(o1.replace('.', ''), o2.replace('.', ''))) if oi != oj]
    # pas voisin : on ne calcule pas la consistance
    if len(diff) != 1:
        return True
    # on "enlève" le graphème avec une lettre différente
    p1 = r1.pseg
    p2 = r2.pseg
    p1_l = del_index(p1.split('.'), o1[:pos1[diff[0]]].count('.'))
    p2_l = del_index(p2.split('.'), o2[:pos2[diff[0]]].count('.'))
    if len(p1_l) != len(p2_l):
        return False
    for i, (pi, pj) in enumerate(zip(r1.pseg.split('.'), r2.pseg.split('.'))):
        if i != diff[0] and pi != pj:
            return False
    return True


def calculate_syllabic_consistency(name, df):
    """
    Calculates the syllabic consistency of a word.

    :param name: word we want the consistency
    :param df: lexicon
    :return: the syllabic consistency
    """
    df = df.groupby('word').first()

    def f(x1, x2):
        return '.'.join([i + '-' + j for i, j in zip(x1.split('-'), x2.split('-'))])
    df['gpmatch'] = df.apply(lambda x: f(x.ortho, x.phono), axis=1)
    return calculate_consistency(name, df)


def calculate_consistency(name, df):
    """
    Calculates consistency for the whole lexicon.

    :param name: name of the file to be generated.
    :param df: input dataframe
    :return: a dataframe with new columns
    """
    df = df.groupby('word').first()
    # create consistencies by graphemes
    dico = defaultdict(list)
    dico_g = {}
    CGP = [i.split('-') for i in '.'.join(df.gpmatch.values).split('.') if len(i) > 2]
    for i, j in CGP:
        dico[i].append(j)
    # the occurrences of each phoneme associated with a grapheme
    for grapheme in dico:
        dico[grapheme] = Counter(dico[grapheme])
        s = sum(dico[grapheme].values())
        dico[grapheme] = {key: dico[grapheme][key] / s for key in dico[grapheme]}
        dico_g[grapheme] = s
    # retrieve the frequency of each phoneme associated with a grapheme
    f = pd.DataFrame(list([[key1 + '-' + key2, value] for key1 in dico for key2, value in dico[key1].items()]),
                     columns=['gp', 'value'])
    # create consistencies for each word
    df['cons'] = df['gpmatch'].apply(lambda s: " ".join([str(round(f[f.gp == i].value.iloc[0], 5)) for i in s.split('.') if len(i) > 2]))
    # calculate the minimum consistency
    df['cons-min'] = df['cons'].apply(lambda s: min([float(i) for i in s.split(' ') if len(i) > 0]))
    df['occ'] = df['gpmatch'].apply(lambda s: " ".join([str(dico_g[i.split('-')[0]]) for i in s.split('.') if len(i) > 0]))
    df['occ-min'] = df['occ'].apply(lambda s: min([int(i) for i in s.split(' ') if len(i) > 0]))
    df.to_csv(name[:-4] + '_cons.csv')
    return df


def handle_double_phoneme(ortho, phono, new_phoneme):
    # irregular words
    if 'zzl' in ortho and 'z2l' in phono:  # puzzle
        ortho = ortho.replace('zzl', 'z.z.l')
        phono = phono.replace('z2l', 'z.2.l')
    if 'en' in ortho and '5n' in phono:  # bienheureux
        phono = phono.replace('5n', '5')
    if 'mm' in ortho and 'mm' in phono:  # mamma
        ortho = ortho.replace('mm', 'm.m')
        phono = phono.replace('mm', 'm.m')
    if 'rr' in ortho and 'RR' in phono:  # acquerra
        ortho = ortho.replace('rr', 'r.r')
        phono = phono.replace('RR', 'R.R')
    if 'xc' in ortho and 'ksk' in phono:  # acquerra
        ortho = ortho.replace('xc', 'x.c')
        phono = phono.replace('ksk', 'ks.k')
    # afriquées = 1 sound
    word_new_phoneme = False
    if 'tS' in phono and new_phoneme:  # coach
        phono = phono.replace('tS', 'T')
        word_new_phoneme = True
    if 'dZ' in phono and new_phoneme:  # banjo / adagio
        phono = phono.replace('dZ', 'J')
        word_new_phoneme = True
    if 'z' in ortho and 'dz' in phono and new_phoneme:  # pizza
        phono = phono.replace('dz', 'D')
        word_new_phoneme = True
    # separate in 2 when it creates at least one "most frequent correspondance"
    if 'qu' in ortho and ('kw' in phono or 'ky' in phono):  # quoi ubiquité
        ortho = ortho.replace('qu', 'q.u')
        phono = phono.replace('kw', 'k.w')
        phono = phono.replace('ky', 'k.y')
    if 'gu' in ortho and ('gw' in phono or 'gy' in phono):  # guacamole aiguille
        ortho = ortho.replace('gu', 'g.u')
        phono = phono.replace('gw', 'g.w')
        phono = phono.replace('gy', 'g.y')
    if 'gg' in ortho and 'gZ' in phono:  # suggérer
        ortho = ortho.replace('gg', 'g.g')
        phono = phono.replace('gZ', 'g.Z')
    if 'cc' in ortho and 'ks' in phono:  # suggérer
        ortho = ortho.replace('cc', 'c.c')
        phono = phono.replace('ks', 'k.s')
    if 'ui' in ortho and 'yi' in phono:  # appui
        ortho = ortho.replace('ui', 'u.i')
        phono = phono.replace('yi', 'y.i')
    if 'ey' in ortho and 'ej' in phono:  # asseyait
        ortho = ortho.replace('ey', 'e.y')
        phono = phono.replace('ej', 'e.j')
    if 'oo' in ortho and 'oo' in phono:  # zoo
        ortho = ortho.replace('oo', 'o.o')
        phono = phono.replace('oo', 'o.o')
    if 'oy' in ortho and 'waj' in phono:  # voyance
        if new_phoneme:
            word_new_phoneme = True
            phono = phono.replace('waj', 'Y')
    if ('oi' in ortho or 'oy' in ortho or 'oê' in ortho) and 'wa' in phono and 'waj' not in phono:  # oiseau
        if new_phoneme:
            phono = phono.replace('wa', 'A')
            word_new_phoneme = True
        else:
            ortho = ortho.replace('oi', 'o.i')
            phono = phono.replace('wa', 'w.a')
    if 'oin' in ortho and 'w5' in phono:  # foin
        if new_phoneme:
            phono = phono.replace('w5', 'U')
            word_new_phoneme = True
        else:
            ortho = ortho.replace('oin', 'o.in')
            phono = phono.replace('w5', 'w.5')
    if 'x' in ortho and ('ks' in phono or 'gz' in phono):  # exagérer
        if new_phoneme:
            word_new_phoneme = True
            phono = phono.replace('ks', 'X')
            phono = phono.replace('gz', 'G')
    # english or foreign words
    if ('ou' in ortho or 'ow' in ortho) and 'aw' in phono:  # cow
        ortho = ortho.replace('ou', 'o.u').replace('ow', 'o.w')
        phono = phono.replace('aw', 'a.w')
    if ('ue' in ortho) and 'ju' in phono:  # new
        ortho = ortho.replace('ue', 'u.e')
        phono = phono.replace('ju', 'j.u')
    if 'ei' in ortho and 'ej' in phono:  # bienheureux
        ortho = ortho.replace('ei', 'e.i')
        phono = phono.replace('ej', 'e.j')
    if 'ew' in ortho and 'ju' in phono:  # new
        ortho = ortho.replace('ew', 'e.w')
        phono = phono.replace('ju', 'j.u')
    if 'an' in ortho and '@n' in phono:  # new
        phono = phono.replace('@n', 'n')
    if 'a' in ortho and 'ej' in phono:  # bienheureux
        ph_split = phono.split('.')
        idx_ej = ph_split.index('ej')
        if ortho.split('.')[idx_ej] == 'a':
            ph_split[idx_ej] = 'E'
            phono = '.'.join(ph_split)
    if ('i' in ortho or 'y' in ortho) and 'aj' in phono and 'waj' not in phono:  # bienheureux
        ph_split = phono.split('.')
        idx_aj = ph_split.index('aj')
        if ortho.split('.')[idx_aj] in ['i', 'y']:
            ph_split[idx_aj] = 'I'
            phono = '.'.join(ph_split)
    # keep those with "w" only if there is "oi", "oy", "qu", or "w"
    # separate "ill", "ij", etc., to create smaller graphemes
    if 'ill' in ortho and ('ij' in phono):  # grille
        ortho = ortho.replace('ill', 'i.ll')
        phono = phono.replace('ij', 'i.j').replace('il', 'i.l')
    if 'lli' in ortho and ('ji' in phono):
        ortho = ortho.replace('lli', 'll.i')
        phono = phono.replace('ji', 'j.i').replace('lj', 'l.j').replace('jj', 'j.i')
    if 'ay' in ortho and ('ej' in phono or 'aj' in phono):
        ortho = ortho.replace('ay', 'a.y')
        phono = phono.replace('ej', 'e.j').replace('ei', 'e.i').replace('aj', 'a.j')
    if ('en' in ortho) and ('@n' in phono):  # enivrer / ennui
        ortho = ortho.replace('en', 'e.n')
        phono = phono.replace('en', 'e.n').replace('@n', '@.n')
    if ('emm' in ortho or 'um' in ortho) and ('am' in phono or 'om' in phono or '@m' in phono):
        ortho = ortho.replace('emm', 'e.mm').replace('um', 'u.m')
        phono = phono.replace('am', 'a.m').replace('om', 'o.m').replace('@m', '@.m')
    return ortho, phono, word_new_phoneme


def handle_silent_letter(ortho, phono):
    cons_phono = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 'R', 's', 't', 'v', 'z', 'S', 'G', 'J', 'N', 'Z', 'j']
    # add the final schwa if necessary
    last_grapheme = ortho.split('.')[-1]
    if len(phono) > 0 and phono.replace('.#', '')[-1] in cons_phono and 'e' in last_grapheme:
        last_dz = phono.rfind('.#')
        phono = phono[:last_dz] + phono[last_dz + 2:] + '.°' if '.#' in phono else phono + '.°'
        # separate into 2 graphemes if not already done
        if last_grapheme.index('e') > 0:
            ortho = ortho[:ortho.rfind('e')] + '.e' + ortho[ortho.rfind('e') + 1:]
    # silent letter at the end of the word (no schwa)
    while phono.endswith('.#'):
        phono = phono[:-2]
        ortho = ortho[:ortho.rfind('.')] + ortho[ortho.rfind('.') + 1:]
    # silent letter at the beginning of the word
    while phono.startswith("#."):
        phono = phono[2:]
        ortho = ortho.replace('.', '', 1)
    # silent letter in the middle of the word
    # between 2 consonants -> add a schwa
    # between 1 consonant and a vowel -> group with the consonant
    # between 2 vowels -> group with the following vowel (syllabic boundary)
    while '#' in phono:
        dz_idx = phono.index('#')
        pt_idx = phono[:dz_idx].count('.')
        spl = ortho.split('.')
        cons_prec = phono[dz_idx + 2] in cons_phono
        cons_suiv = phono[dz_idx - 2] in cons_phono
        if cons_prec and cons_suiv and ortho.split('.')[pt_idx] in ['a', 'e', 'o', 'i', 'y']:
            phono = phono[:dz_idx] + '°' + phono[dz_idx + 1:]
        else:
            ortho = ".".join(spl[:pt_idx + (0 if cons_suiv else 1)]) + ".".join(spl[pt_idx + (0 if cons_suiv else 1):])
            phono = phono.replace('#.', '', 1)
    return ortho, phono


def other_transformations(ortho, phono, word):
    # simplify the "jj"
    if 'jj' in phono:
        phono = phono.replace('jj', 'j')
    # remove diphthongs with "j"
    l = [['ij', 'i'], ['i.j', 'i'], ['ji', 'i'], ['j.i', 'i']] + [['j.' + string, 'i.' + string] for string in
                                                                  ['a', 'e', 'o', 'y', '@', '&', '5', '2']]
    for i in l:
        if 'ill' not in ortho and i[0] in phono:
            phono = phono.replace(i[0], i[1])
    w = [['w.' + string, 'u.' + string] for string in ['a', 'e', 'o', 'y', '@', '&', '5', '2', 'i']]
    for i in w:
        if not re.search('oi|oy|w|qu|gu', word) and i[0] in phono:
            phono = phono.replace(i[0], i[1])
    # bs becomes ps even if it starts with p: articulatory constraint
    if 'p.s' in phono and 'b' in ortho:
        phono = phono.replace('p.s', 'b.s')
    if 'p.t' in phono and 'b' in ortho:
        phono = phono.replace('p.t', 'b.t')
    return ortho, phono


def correct_graphemic_segmentation(df, new_phoneme=True, calc_complexity=False):
    """
    Corrects errors in the graphemic segmentation given by Manulex.

    :param df: dataframe with graphemic segmentation
    :param new_phoneme: True if for the graphemes corresponding to multiple phonemes, a "new phoneme" is defined
    :param calc_complexity: True if the objective is not to have 1 grapheme=1 phoneme, i.e. no separation of double phonemes
    :return: a new dataframe
    """
    nb = {"pb_longueur_finale": 0, "ok": 0, "dz": 0, "phoneme_mult": 0, "dz_deb": 0, "dz_fin": 0, "tot": 0}

    def transfo(x):
        # transformation to obtain more basic graphemes
        # doesn't work very well for "joyeux" and other complicated words in waj
        ortho = str(x.segm)
        phono = str(x.pseg).replace('*', '°')
        nb['tot'] += 1
        if max([len(i) for i in phono.split('.')]) > 1:
            nb['phoneme_mult'] += 1
        if '#' in phono:
            nb['dz'] += 1
            if phono.endswith('.#'):
                nb['dz_fin'] += 1
            if phono.startswith("#."):
                nb['dz_deb'] += 1
        if not calc_complexity:
            ortho, phono, word_new_phoneme = handle_double_phoneme(ortho, phono, new_phoneme)
        else:
            word_new_phoneme = False
        ortho, phono = handle_silent_letter(ortho, phono)
        ortho, phono = other_transformations(ortho, phono, x.word)
        x.pseg = phono
        x.segm = ortho
        x.word = ortho.replace('.', '')
        x.pron = phono.replace('.', '')
        x.gpmatch = '.'.join(['-'.join(i) for i in list(zip(ortho.split('.'), phono.split('.')))])
        x.new_phoneme = word_new_phoneme
        if len(x.pron) != x.gpmatch.count('-'):
            nb['pb_longueur_finale'] += 1
            x.pb_longueur = True
        return x
    df['new_phoneme'] = False
    df['pb_longueur'] = False
    df = simplify_letters(simplify_phonemes(df)).apply(transfo, axis=1)
    # 118478 2239 59781 62464 9830 5
    print("nombre de mots :", nb['tot'], "\n phonèmes silencieux en début de mot : ", nb['dz_deb'], "\n phonèmes silencieux en fin de mot : ", nb['dz_fin'], "\n phonèmes silencieux : ", nb['dz'], "\n phonèmes multiples : ", nb['phoneme_mult'], "\n problèmes de longueur à la fin : ", nb['pb_longueur_finale'])
    return df.set_index('word')


def createManulexCP(path=_ROOT):
    """ Pre-processes Manulex data in a usable format.

    :param path: path to the file
     """
    df = pd.read_csv(os.path.join(path, "resources/lexicon/Manulex.csv"), usecols=["FORMES ORTHOGRAPHIQUES", "NLET", "CP F"]).dropna().rename(columns={"FORMES ORTHOGRAPHIQUES": "word", "NLET": "len", "CP F": "freq"})
    df['freq'].astype(float)  # considerate freq as float
    # remove words with space
    df = df.drop(df[df["word"].str.contains(" ")].index)
    df = df.drop(df[df["word"].str.contains("'")].index)
    df = df.drop(df[df["word"].str.contains("-")].index)
    df = df.drop(df[df["word"].str.contains("1")].index)
    df = df.drop(df[df["word"].str.contains("œ")].index)
    # remove accents
    df["word"] = df["word"].str.replace("à", "a")
    df["word"] = df["word"].str.replace("é", "e")
    df["word"] = df["word"].str.replace("è", "e")
    df["word"] = df["word"].str.replace("ê", "e")
    df["word"] = df["word"].str.replace("ë", "e")
    df["word"] = df["word"].str.replace("ï", "i")
    df["word"] = df["word"].str.replace("î", "i")
    df["word"] = df["word"].str.replace("ô", "o")
    df["word"] = df["word"].str.replace("û", "u")
    df["word"] = df["word"].str.replace("ù", "u")
    df["word"] = df["word"].str.replace("ç", "c")
    df["word"] = df["word"].str.replace("â", "a")
    # so we need to combine multiple words
    agg_fun = {'freq': np.sum, 'len': 'first'}
    df = df.groupby('word').agg(agg_fun).reset_index()  # add the frequencies of the homographs
    df.to_csv(os.path.join(path, "resources/lexicon/ManulexCP.csv"))


def neighbSize(df):
    """
    Calculates for each word of the dataframe the neighborhood size

    :param df: input dataframe
    :return: a dataframe with an added nb column
    """
    def nbNeigh(key):
        dfN = pd.DataFrame({"dist": df.word.apply(lambda x: distance(x, key))})
        return dfN.dist[dfN.dist == 1].count()
    df["nb"] = df.word.apply(nbNeigh)  # create a "dist" column in the dataframe
    return df


def neighbSizeLen(df):
    """
    Calculates for each word the neighborhood size, neighbors in the same length class

    :param df: input dataframe
    :return: a dataframe with an added nb column
    """
    def nbNeigh(key):
        dfa = df[df.len == len(key)]
        dfN = pd.DataFrame({"dist": dfa.word.apply(lambda x: distance(x, key))})
        return dfN.dist[dfN.dist == 1].count()
    df["len"] = df.word.str.len()
    df["nb"] = df.word.apply(nbNeigh)  # create a "dist" column in the dataframe
    return df


def neighbSizeLenList(df, l):
    """
    Calculate for each word in l the neighborhood size in the length class

    :param df: input dataframe
    :return: neighborhood size for one word.
    """
    def nbNeigh(key):
        dfa = df[df.len == len(key)]
        dfN = pd.DataFrame({"dist": dfa.word.apply(lambda x: distance(x, key))})
        return dfN.dist[dfN.dist == 1].count()
    df["len"] = df.word.str.len()
    nb = [nbNeigh(i) for i in l]
    dfRes = pd.DataFrame({"word": l, "nb": nb})
    return dfRes


def neighbSizeList(df, l):
    """
    Calculate for each word in l the neighborhood size

    :param df: input dataframe
    :return: neighborhood size for one word.
    """
    def nbNeigh(key):
        dfa = df[df.len == len(key)]
        dfN = pd.DataFrame({"dist": dfa.word.apply(lambda x: distance(x, key))})
        return dfN.dist[dfN.dist == 1].count()
    df["len"] = df.word.str.len()
    nb = [nbNeigh(i) for i in l]
    dfRes = pd.DataFrame({"word": l, "nb": nb})
    return dfRes


def removeNeigh(df, l):
    """
    Removes neighbors of the word l from the dataframe df.

    :param df: input dataframe
    :param l: word
    :return: the new dataframe
    """
    df = df.reset_index()
    for i in l:
        df["dist"] = df.word.apply(lambda x: distance(x, i))
        df = df[df.dist != 1]
    return df.drop("dist", axis=1)
