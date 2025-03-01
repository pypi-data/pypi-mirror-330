import pdb
import sys
import os
import unicodedata
from functools import partial
from time import time

import numpy as np
import pandas as pd
import logging
# BRAID utlities
import braidpy.utilities as utl
from braidpy import _ROOT
import pickle as pkl


class _Lexical:
    """
    The _Lexical class is an inner class of the modality class and represents the lexical submodel, either in the orthographic or phonological modality.

    :param chars_filename : string. name of the chars file
    :param eps : float. epsilon value for the lexical representations.
    :param learning : boolean. If True, learning happens in this modality at the end of the simulation.
    :param remove_stim : boolean. if True, remove stim from the lexicon before simulation (in the corresponding modality)
    :param forbid_list : list. list of words to exclude from lexicon
    :param force_app, force_update, force_word : booleans. force the new learning, the updating, or the correct identity of the stimulus.
    :param log_freq : boolean. if True, the lexical prior is the log frequency
    :param fMin, fMax : float, allowed frequency in the lexicon
    :param maxItem : int, max number of items in the lexicon
    :param maxItemLen : int, max number of items per length in the lexicon
    :param lenMin : int, minimum length in the lexicon
    :param lenMax : int, maximum length in the lexicon
    :param remove_neighbors : boolean. If True, neighbors of the stimulus are excluded from the lexicon
    :param remove_lemma : boolean. If True, words with the same lemma as the stimulus are excluded from the lexicon. (only in Franch or with a lemmatized lexicon)
    :param cat : string. if not None, the grammatical category to be selected in the lexicon
    :param store : boolean. if True, information of the modality is used during lexicon extraction.
    :param mixture_knowledge : boolean. if True, representations are mixed between good, bad, uniform
    :param shift : boolean. if True, comparison with +1/-1 length in the lexicon
    """

    def __init__(self, modality, chars_filename="", eps=0.001, learning=True, remove_stim=False, forbid_list=None,
                 force_app=False, force_update=False, force_word=False, log_freq=True,
                 fMin=0, fMax=sys.maxsize, maxItem=None, maxItemLen=None, lenMin=0, lenMax=13,
                 remove_neighbors=False, remove_lemma=False, cat=None, store=True, mixture_knowledge=False, shift=True):
        self.modality = modality
        self.chars_filename = chars_filename
        self.eps = eps
        self.learning = learning
        self.remove_stim = remove_stim
        self.removed = False
        self.removed_words = None
        self.restore = False
        self.old_repr = {}
        self.old_store = {}
        self.forbid_list = forbid_list if forbid_list else []
        self.force_app, self.force_update, self.force_word = force_app, force_update, force_word
        self.log_freq = log_freq
        self.leak = 12
        self.dist = {"word": None, "ld": None}
        # orthographic and phonological representations for all lengths (orthographic length)
        # attention: all_repr in both modalities is indexed by self.N
        self.all_repr = None
        # orthographic and phonological representations for current length
        self.repr = None
        self.lexicon_size = 0
        self.df = None
        self.chars = ""
        self.unknown = "null"
        # Lexical knowledge
        self.fMin, self.fMax, self.maxItem, self.maxItemLen = fMin, fMax, maxItem, maxItemLen
        self.lenMin, self.lenMax = lenMin, lenMax
        self.remove_neighbors, self.remove_lemma, self.cat, self.store = remove_neighbors, remove_lemma, cat, store
        self.mixture_knowledge = mixture_knowledge
        self.shift, self.shift_begin, self.all_shift_begin, self.shift_unif = shift, sys.maxsize, 0, False

        # frequency for words of current length
        self.freq = self.freq_shift = self.N_max = None
        self.extract_lexicon()
        self.handle_languages()
        self.set_char_dict()
        self.verify_chars()
        self.calculate_max_len()
        if self.shift:
            self.calculate_shift_begin()
            self.add_shift()
        self.calculate_max_len()
        self.build_all_repr()
        self.added_word = False

    ###################################
    ##### INIT LEXICON DATAFRAME ######
    ###################################

    def open_lexicon(self):
        """
        Reads a CSV file containing the lexicon to assign it to build the lexicon dataframe. Removes homophones from the same length class by selecting the most frequent one.
        """
        self.df = pd.read_csv(os.path.join(_ROOT, 'resources/lexicon/', self.modality.model.lexicon_name), keep_default_na=False)
        # TODO
        # self.df = self.df.loc[self.df.groupby(['len','pron'])['freq'].idxmax()].reset_index(drop=True)
        self.df = self.df.loc[self.df.groupby(['len', 'word'])['freq'].idxmax()].reset_index(drop=True)

    def extract_lexicon(self):
        """
        Extracts the lexicon dataframe based on various criteria such as word length, frequency, category, and a list of forbidden words.
        """
        self.df["word"] = self.df["word"].str.replace(r"['\-\s]", "", regex=True)
        self.df.len = self.df.word.str.len()
        if self.cat is not None and 'cat' in self.df.columns:
            self.df = self.df[self.df.cat == self.cat]
        self.df = self.df.assign(store=self.store)
        if self.forbid_list is not None:
            self.df.loc[self.df.word.isin(self.forbid_list), 'store'] = False
        if self.fMin is not None:
            self.df.loc[self.df['freq'] < self.fMin, 'store'] = False
        if self.fMax is not None:
            self.df.loc[self.df['freq'] > self.fMax, 'store'] = False
        # be careful: if you change lenMax, it changes the chosen words, so you can't gradually increase the len. but you can increase maxItemLen
        self.df['len'] = self.df['len'].astype(int)
        if self.lenMin is not None and self.lenMax is not None:
            self.df = self.df[(self.df['len_class'] >= self.lenMin) & (self.df['len_class'] <= self.lenMax)]
            self.df = self.df.set_index('word')
        if self.maxItem is not None:
            self.df = self.df.nlargest(self.maxItem, 'freq')
        if self.maxItemLen is not None and (self.maxItem is None or self.maxItemLen < self.maxItem):
            self.df = self.df.groupby('len').apply(lambda x: x.sort_values(by='freq', ascending=False).head(self.maxItemLen)).reset_index(0, drop=True)
        self.df = self.df.head(self.maxItem)
        self.modality.N_max = max(self.df.len_class)
        self.df = self.df[self.df.columns.intersection(['word', 'freq', 'len', 'idx', 'store', 'cat', 'len_class', 'other_modality'])]
        if self.modality.enabled and len(self.df[self.df.store]) == 0:
            raise ValueError('Incomplete lexicon in the ' + self.modality.mod + 'modality')
        if self.mixture_knowledge:
            np.random.seed(2021)
            self.df['repr_type'] = np.random.choice([0, 0, 0, 0, 0, 1, 1, 1, 2], size=len(self.df))

    @utl.abstractmethod
    def simplify_alphabet(self):
        pass

    def set_char_dict(self):
        """
        Reads a csv file to create the orthographic or phonological alphabet
        """
        col = ['idx', 'char']  # if mod == "ortho" else ['idx', 'char', 'ipa']
        dict_path = os.path.join(_ROOT, 'resources/chardicts/', self.chars_filename)
        df = pd.read_csv(dict_path, usecols=col)
        self.chars = "".join(df.char)  # it is simply a string
        self.modality.n = len(self.chars)

    @utl.abstractmethod
    def verify_chars(self):
        """
        Checks if all the characters in the lexicon are in the list of characters. If not, raises an error.
        """
        return

    def handle_languages(self):
        """
        The function handles language-specific operations during the lexicon extraction
        """
        if self.modality.model.langue in ["fr", "en"]:
            self.simplify_alphabet()
        if self.modality.model.langue == "ge":
            self.df.reset_index(inplace=True)
            self.df['word'] = self.df['word'].apply(lambda s: unicodedata.normalize('NFC', s))
            self.df['len'] = self.df.word.str.len()
        if self.df.index.name != "word":
            self.df.set_index('word', inplace=True)

    def extract_proba(self):
        """
        Extracts the prior probability for words.
        """
        f_type = "freq_log" if self.log_freq else "freq"
        if f_type == "freq_log":
            self.df["freq_log"] = np.log(self.df.freq + 1)
        self.freq = np.array(self.df[self.df.len_class == self.modality.N].sort_values(by='idx')[f_type])

    def change_freq(self, newF=1, string=""):
        """
        Artificially changes the frequency of a word (for the freq effect simulation)
        """
        string = string if len(string) > 0 else self.stim
        if len(string) > 0 and string in self.df.index and newF is not None:
            f = self.df.loc[string].freq
            self.old_freq = f
            self.df.loc[string, 'freq'] = float(newF)
            self.extract_proba()
            wd = self.df.loc[string]
            logging.braid(f"mot : {string}, brut freq= {wd.freq}, old freq= {f}")
        else:
            logging.warning("mot inconnu ou mauvaise fréquence, impossible de changer la fréquence")

    utl.abstractmethod

    def calculate_max_len(self):
        pass

    #####################################
    ##### INIT LEXICAL REPRESENTATIONS ##
    #####################################

    def normalize_repr(self, n=2):
        """
        Normalizes word representations according to the measure considered

        :param n: the LX measure to considere, defaults to 2, corresponding to the L2 measure (optional)
        """
        self.all_repr = {k: utl.norm3D(v, n=n) if len(v) > 0 else v for k, v in self.all_repr.items()}

    def build_all_repr(self):
        """
        Creates the list containing 3d matrix of phonological/orthographical representations for each word length
        """
        t = time()
        if self.modality.enabled:
            if self.modality.model.store_all_repr:
                print("extract")
                self.extract_all_repr()
            else:
                self.all_repr = {i: self.build_repr(i + 1) for i in range(int(self.modality.N_max))}
            # if L2 norm division in the similarity calculation, lexical representations are directly normed in memory (to avoid heavy calculations)
            if self.modality.model.L2_L_division and self.modality.enabled:
                self.normalize_repr()

    @utl.abstractmethod
    def extract_all_repr(self):
        pass

    @utl.abstractmethod
    def get_repr_indices_length(self, n, lex, forbid_idx=None):
        pass

    def get_repr_indices(self, wds, n):
        """
        Converts a list of words (string) into a numpy array of their corresponding indices in the alphabet.
        The indices will be used to create the arrays of lexical representations.

        :param wds: a list of words to be converted to indices
        :param n: int. The length of each word in the input "wds".
        :return: a numpy array `wds_idx` which contains the indices of the characters in the input words `wds`.
        If a character is not present in the character set `self.chars`, it is assigned an index of -1 if unknown characters are treated as uniform, -2 otherwise.
        """
        # -1 = uniform, -2 = null
        wds_idx = np.array([[self.chars.index(letter) if letter in self.chars else -1 for letter in wd]
                            if len(wd) > 0 else [-1 if self.unknown == "uniform" else -2] * n for wd in wds])
        return wds_idx

    def get_forbid_entries(self, string=None):
        """
        Returns the list of the forbidden entries (if there are some).

        :param string: The input string for which we want to find forbidden entries. If no string is provided, it uses the stimulus attribute.
        :return: a list of forbidden entries. If `self.model.remove_neighbors` is True, the function returns a list of words from the lexicon that differ from the
        input string by only one character. If `self.model.remove_lemma` is True, the function returns a list of words with same lemma as the input.
        """

        def isNeighb(w1, w2):
            return (len(w1) == len(w2)) & (sum([i != j for i, j in zip(w1, w2)]) == 1)

        if string is None:
            string = self.modality.model.ortho.stim if self.modality.model.ortho is not None else ''
        try:
            if self.modality.model.remove_neighbors:
                lx = self.modality.model.df.reset_index()
                df = pd.DataFrame({"dist": lx.word.apply(partial(isNeighb, string))})
                return list(lx[df.dist == True].word.values)
            if self.modality.model.remove_lemma:
                lemma = str(self.modality.model.df_lemma.loc[self.modality.model.ortho.stim].lemme)
                liste = list(self.modality.model.df_lemma[self.modality.model.df_lemma.lemme == lemma].index.values)
                liste = [i for i in liste if len(i) == len(self.modality.model.ortho.stim) and i in self.modality.model.df.index]
                return liste if self.remove_stim else [i for i in liste if i != self.modality.model.ortho.stim]
        except:
            return []
        return []

    def build_repr(self, n):
        """
        This function builds a 3D matrix of phonological/orthographical lexical representations for a specific word length.

        :param n: the specific word length
        :return: a 3D matrix of phonological/orthographical lexical representations.
        """
        if self.modality.enabled:
            lex = self.df[self.df.len_class == n].reset_index()
            if len(lex) == 0:  # empty lexicon for this length
                return []
            forbid_idx = list(lex[lex['store'] == False].idx) + self.get_forbid_entries()  # words that shouldn't be included
            wds_idx = self.get_repr_indices_length(n, lex, forbid_idx)
            if self.modality.model.mixture_knowledge:
                return utl.create_repr_mixt(wds_idx, self.modality.n, self.eps, np.array(lex.repr_type))
            else:
                try:
                    return utl.create_repr(wds_idx, self.modality.n, self.eps)
                except:
                    pdb.set_trace()

    def set_repr(self):
        """
        Sets the current orthographical/phonological knowledge to the length of the current stim
        """
        self.repr = self.all_repr[self.modality.N - 1] if self.all_repr is not None \
            else self.build_repr(self.modality.N)
        self.modality.exists = len(self.repr) > 0 and not np.all((self.repr == 0))
        if self.modality.enabled:
            self.repr_norm = utl.calculate_norm3D(utl.norm3D(self.repr, n=1))
            # to avoid problems when performing normalization with 0 distributions
            self.repr_norm = np.array([i if i > 0 else 1 for i in self.repr_norm])
        self.lexicon_size = len(self.repr)
        if self.shift:
            self.shift_begin = self.all_shift_begin[self.modality.N]
        self.extract_proba()

    def remove_stim_repr(self):
        """
        Removes the stimulus from the model's lexicon and from the model's representations
        """
        if self.modality.enabled and self.remove_stim and not self.removed and self.modality.stim in self.df.index:
            wds = list(set(self.forbid_list + [self.modality.stim] if self.remove_stim else []))
            self.removed_words = self.get_word_list_entry(wds)
            for key, raw in self.removed_words.iterrows():
                self.all_repr[self.modality.N - 1][raw.idx, :, :] = self.get_empty_percept(1 / self.modality.n if self.unknown == "uniform" else 0)
                self.df.loc[key, 'store'] = False
            self.removed = True
            try:
                self.df.loc[self.modality.stim, 'freq'] = 0
            except:
                pdb.set_trace()

    ############ INIT TOP DOWN #################
    def lex_shift(self, N, n, f):
        """
        The function adds shifted orthographies and pronunciations to the lexicon dataframe.

        :param N: the length of the original word in the lexicon
        :param n: the number of characters by which the words in the lexicon are shifted
        :param f: a list of tuples, where each tuple contains two functions taking a string as input and modifying it. The first function returns a string representing the shifted orthography. The second function returns the shifted pronunciation.
        """
        lexN = self.df[(self.df.len_class == N + n) & (~self.df.index.str.contains('#|~'))]
        tmpi = []
        for i in f:
            tmp = lexN.rename(index=i)
            tmpi.append(tmp)
        tmp2 = pd.concat(tmpi)
        tmp2["len"] = tmp2["len"] - n
        tmp2["len_class"] = tmp2["len_class"] - n
        tmp2["idx"] = tmp2.reset_index().index + len(self.df[self.df.len_class == N])
        self.df = pd.concat((self.df, tmp2))

    @utl.abstractmethod
    def add_shift(self):
        """
        Adds shifted words in the lexicon dataframe
        """
        pass

    def calculate_shift_begin(self):
        self.all_shift_begin = {i: len(self.df[self.df.len_class == i]) for i in range(1, int(self.modality.N_max) + 3)}

    #######################
    ##### LEARNING ########
    #######################

    @utl.abstractmethod
    def get_nb_mu_pre(self, len_ortho):
        pass

    @utl.abstractmethod
    def get_nb_mu_post(self, stim, len_ortho, nb_mu_pre):
        pass

    def learn_shift(self):
        # TODO
        def build_mu_repr(nb_mu):
            return utl.create_repr(np.array([[mu_idx for _ in range(nb_mu)]]), self.modality.n, self.eps)[0] if nb_mu > 0 \
                else np.empty((0, self.modality.n))
        stim_ortho = self.modality.model.ortho.stim
        stim = self.modality.stim
        # boucle sur la longueur du mot à ajouter
        # TODO je sais pas jusqu'à quelle longueur vous voulez ajoutez ces mots
        for len_word in range(len(stim_ortho), 10):
            # on initialise le gros array qu'on va ajouter à whole_repr à la fin du calcul
            # la taille c'est soit la taille ortho, soit la taille phono -> on a directement cette info en regardant la taille de self.repr
            all_mu_repr = np.empty((0, np.shape(self.all_repr[len_word - 1])[1], self.modality.n))
            # boucle sur le nombre de shifts vers la droite à considérer, en partant de 0 (ajouter simplement le mot)
            # on place la représentation phono en position nb_shift
            for nb_shift in range(0, len_word - len(stim_ortho) + 1):
                # calcul du nombre de mu à mettre avant et après la distribution P/Psi
                nb_mu_pre = self.get_nb_mu_pre(nb_shift)
                nb_mu_post = self.get_nb_mu_post(stim_ortho, len_word, nb_mu_pre)

                # on rajoute une ligne dans le dataframe
                name = 'µ' * nb_mu_pre + stim + 'µ' * nb_mu_post  # parce que je préfère avoir le vrai string, je trouve ça plus clair
                self.add_df_entry(name, len_word)

                # on crée la représentation du mot
                mu_idx = self.chars.index('#')
                mu_repr_pre = build_mu_repr(nb_mu_pre)
                mu_repr_post = build_mu_repr(nb_mu_post)
                mu_repr = np.concatenate((mu_repr_pre, self.modality.percept.dist["percept"], mu_repr_post), axis=0)
                all_mu_repr = np.concatenate((all_mu_repr, mu_repr[np.newaxis, :, :]))
            # on met à jour whole_repr avec le gros array créé
            self.all_repr[len_word - 1] = np.concatenate((self.all_repr[len_word - 1], all_mu_repr))
            self.repr = self.all_repr[self.modality.N - 1]

    def learn(self):
        """
        This function updates the lexicon and and the lexical representations (orthographic and phonological) after a simulation.
        """
        if self.learning:
            name = self.name_df()
            len_class = len(self.modality.model.ortho.stim)
            self.add_df_entry(name, len_class) if self.modality.model.PM else self.update_df_entry(name)
            if name is not None:
                self.create_trace() if self.modality.word.PM else self.update_trace(name)

    def name_df(self):
        """
        Calculates the name to use as index in the dataframe
        :return:
        """
        if not self.modality.model.PM:
            name = self.modality.word.chosen_word
        else:
            name = self.modality.stim
            if name is not None and len(name) == 0:
                name = self.modality.percept.decision().replace('#', '')
            if name in self.df.index:
                # handles the case with multiple lexical representations for the same word (add _i add the end)
                name += '_' + str(len(self.df[self.df.index.str.contains(name + '_') & (~self.df.index.str.contains('#|~'))]))
        return name

    def add_df_entry(self, name, len_class):
        """
        This function adds a new word to the lexicon dataframe.

        :param name: The word to be added to the lexicon
        :param len_class: The len_class (orthographic length) of the stimulus added to the lexicon
        """
        # calculation of the index of the word
        idx = int(self.all_shift_begin[len_class] if self.shift else int(self.df[self.df.len_class == len_class].count()['len']))
        dico = {"len": len(utl.str_transfo(name)), "freq": 1, "freq_log": np.log(1 + 1), "len_class": len_class,
                "store": True, "idx": int(idx)}
        if self.shift:  # shifted representations are pushed to the right to make room for the new representation that should be before the index 'shift_begin'
            self.df.loc[(self.df.len_class == self.modality.N) & (self.df.idx >= self.shift_begin), 'idx'] += 1
            self.all_shift_begin[len_class] += 1
            self.shift_begin = self.all_shift_begin[self.modality.N]
        # append row to the dataframe
        self.df = self.df.append(pd.Series(data=dico, name=name), ignore_index=False)
        self.added_word = True
        return name

    def update_df_entry(self, string):
        """
        This function updates the lexical entry according to the learning decision

        :param word: The word to be added to the lexicon
        """

        # according to selected word during the identification, updates the need to create or update the ortho/phono trace
        name = self.modality.word.chosen_word
        if name in self.df.index:
            self.df.loc[name, 'store'] = True
            self.df.loc[name, 'freq'] += 1
            self.added_word = False
        else:
            print("word could not be updated because the name is inknown")
        return name

    @utl.abstractmethod
    def handle_no_learning(self):
        pass

    def create_trace(self, alpha=0.9):
        """
        Creates a new trace in the current modality

        :param wd: the word that is being learned
        :param alpha: the learning rate
        """
        # Calculation
        if self.modality.enabled and self.learning:
            dist = self.modality.percept.dist["percept"]
            u = self.get_empty_percept()
            knowledge = utl.norm2D(alpha * dist + (1 - alpha) * u, 2 if self.modality.word.L2_L_division else 1)[np.newaxis]
        else:
            knowledge = self.handle_no_learning()
        if not self.modality.model.PM:
            wd = self.get_word_entry(self.modality.word.chosen_word)
            self.repr[int(wd.idx)] = knowledge
        elif self.modality.lexical.shift:
            # shift_begin -1 because it has already been updated
            self.repr = np.concatenate((self.repr[:self.modality.lexical.shift_begin - 1], knowledge, self.repr[self.modality.lexical.shift_begin - 1:]), 0) \
                if len(self.repr) > 0 and knowledge is not None else knowledge
        else:
            self.repr = np.concatenate((self.repr, knowledge), 0) \
                if len(self.repr) > 0 else knowledge
        # Print
        newTrace = [max(utl.norm1D(knowledge[0][j])) for j in range(np.shape(knowledge)[1])]
        logging.simu(f"New {self.mod} trace")
        logging.simu(f"Trace= {[round(i, 3) for i in newTrace]}\n")
        self.all_repr[self.modality.N - 1] = self.repr

    def update_trace(self, name, alpha=0.9):
        """
        Updates the trace of a word in the lexicon

        :param wd: the word to be updated
        :param alpha: the learning rate
        """
        if self.modality.enabled and self.modality.lexical.learning:
            wd = self.get_word_entry(name)
            p = self.modality.percept.dist["percept"]
            # Calculation
            learningRate = 1.0 / (5 * wd['freq'] + 1)
            u = self.get_empty_percept()
            newP = learningRate * alpha * p + (1 - learningRate * alpha) * u
            newTrace = utl.norm2D(self.repr[int(wd.idx)] * newP, 1)
            if self.modality.word.L2_L_division:  # on norme les L en L2
                newTrace = utl.norm2D(newTrace, 2)

            # Update
            self.repr[int(wd.idx)] = newTrace

            # Print
            logging.simu(f"Update {self.mod} trace : {(wd.name).replace('#', '')}")
            TraceValue = [max(utl.norm1D(self.repr[int(wd.idx), j, :])) for j in range(np.shape(self.repr)[1])]
            logging.simu(f"Trace= {[round(i, 3) for i in TraceValue]}")
            logging.simu(f"New freq = {wd['freq'] + 1}\n")

    #######################
    ##### INFO ############
    #######################

    def pseudodirac(self, word):
        """
        Given a word, returns its Pseudo Dirac distribution, which is a matrix of size $n \times n$ where $n$ is the length of the word, where the $i$th row is the probability distribution of the
        $i$th letter of the word

        :param word: the word we want to get the distribution
        :return: a 2d matrix corresponding to the lexical representation.
        """
        return np.array([[1 - (self.eps * (self.modality.n - 1)) if self.chars[i] == letter else self.eps for i in range(self.modality.n)] for letter in word])

    def get_word_list_entry(self, liste=None, check_store=False, check_len=True):
        """
        If the list is not empty, return the lexicon entries that contain any of the words in the list and have the same length as the current word

        :param liste: a list of words to search for
        :param check_store: boolean. If True, checks, that the word is stored in this modality, i.e. that the colum store is set at True for this word
        :param check_len: boolean. If True, checks, that the word has the same length as the stimulus.
        :return: A dataframe with the columns of the lexicon and the words that are in the list and have the same length as the word.
        """
        if liste is not None and len(liste) > 0:
            res = self.df[self.df.index.str.startswith(tuple([i + '_' for i in liste])) | self.df.index.isin(liste)]
            if check_len:
                res = res[res.len_class == self.modality.N] if check_len else res
            if check_store:
                res = res[res.store == True]
        return res

    def get_word_entries(self, string=None, check_store=False, check_len=True):
        """
        If the string is in the lexicon, returns the corresponding row. If not, return None

        :param string: the string to look up in the lexicon
        :param check_store: boolean. If True, the raws returned should have the column 'store' to True.
        """
        string = string if string is not None else self.modality.stim
        if string not in self.df.index:
            return None
        res = self.df[(~self.df.index.str.contains('~')) & ((self.df.index == string) | (self.df.index.str.contains(string + '_')))]
        if check_len:
            res = res[res.len_class == self.modality.N] if check_len else res
        if check_store:
            res = res[res.store == True]
        return res

    def get_word_entry(self, string=None):
        """
        Gets the entry of the lexicon dataframe that corresponds to the stimulus.

        :param string: If not None, the correspondance is made with the string.
        :return: A dataframe that contains relevant entries in the dataframe
        """
        string = string if string else self.modality.stim
        df = self.df[self.df.len_class == self.modality.N]
        df = df[(df.index == string) | (df.index.str.contains(string + '_'))] if string in df.index else None
        if isinstance(df, pd.DataFrame):
            df = df.iloc[0]
        return df

    def get_name(self, index):
        """
        Returns the name of a word in a lexicon dataframe based on its index.

        :param index: int. The index of the word in a lexicon dataframe
        :return: string. The name of the word corresponding to the given index in the lexicon dataframe.
        """
        res = self.get_names([index])
        return self.get_names([index])[0] if len(res) > 0 else None

    def get_names(self, indexes):
        """
        Takes a list of indexes and returns the corresponding words

        :param indexes: the indexes of the words to be retrieved
        :return: The words that are being returned are the words that are in the lexicon and have the same length as the ortho.N.
        """
        try:
            # sort according to the order indicated by indexes
            res = self.df[(self.df.idx.isin(indexes)) & (self.df.len_class == self.modality.N)]
            res_words = list(res.index.values)
            res_idx = list(res.idx.values)
            return [res_words[res_idx.index(i)] for i in indexes if i in res_idx]
        except IndexError:
            logging.exception("Word index not found")
            pdb.set_trace()

    @utl.abstractmethod
    def get_empty_percept(self, value=None):
        """
        Creates an empty percept with the same dimensions as the percept distribution

        :param value: The value to fill the empty percept with. If no value is provided, it will be filled with equal probabilities.
        :return: returns a numpy array with dimensions `(self.N,self.n)`
        """
        u = np.empty((self.modality.N, self.modality.n))
        u.fill(value if value is not None else 1.0 / self.modality.n)
        return u


class _LexicalOrtho(_Lexical):

    def __init__(self, modality, **modality_args):
        self.mod = "ortho"
        super().__init__(modality=modality, **modality_args)

    ###################################
    ##### INIT LEXICON DATAFRAME ######
    ###################################

    def extract_lexicon(self):
        self.open_lexicon()
        self.df["word"] = self.df.word.str.lower()
        self.df["len_class"] = self.df.len
        super().extract_lexicon()
        self.df["idx"] = self.df.groupby("len").cumcount()

    def set_char_dict(self):
        """
        Chooses the alphabet to choose for the simulations
        """
        if len(self.chars_filename) == 0:
            self.chars_filename = "alphabet_ge.csv" if self.modality.model.langue == "ge" else "alphabet_en.csv" if self.modality.model.langue == "en" else "alphabet_lat.csv"
        if self.modality.model.langue == "fr":
            self.chars_filename = "alphabet_fr_simplified.csv"
        super().set_char_dict()

    def verify_chars(self):
        if self.modality.enabled:
            lexicon_chars = list(set("".join(self.df.reset_index().word)))
            for i in lexicon_chars:
                if i not in list(self.chars) + ['~', '#', '_']:
                    raise ValueError(f"Unknown letter in lexicon : {i}")

    def simplify_alphabet(self):
        """
        Simplifies the lettershandle_lan in the lexicon dataframe by merging some characters (like à and a).
        """
        def f(val):
            a = {k: 'a' for k in ['à', 'â', 'ä', 'ã', 'á']}
            o = {k: 'o' for k in ['ö', 'ô', 'ó']}
            u = {k: 'u' for k in ['ù', 'û', 'ü', 'ú']}
            i = {k: 'i' for k in ['î', 'í']}
            return dict(**{' ': '', ':': '', '?': ''}, **a, **o, **u, **i)[val[0]]
        # when word is or isn't in index
        index_name = self.df.index.name
        if index_name is not None:
            self.df = self.df.reset_index()
        for col in ['orthosyll', 'segm', 'gpmatch', 'word']:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.replace('ã|à|â|ä|á|ö|ô|ó|ù|û|ü|ú|î|í| |:|\?', f, regex=True)

    def add_shift(self):
        for N in range(max(self.lenMin, 3), min(self.lenMax, max(self.all_shift_begin.keys())) - 1):
            # longer word: cut off at beginning and end
            # we also remove the beginning/end because you don't want to compare near the cut.
            # keep version 1, which gives vaguely better results
            # i.e. we only blur words that are too long, not those where we've already added blur
            # puts a '~' at the end, because if you don't put a hash at the end, it'll come out in the phoneme distribution without you wanting it to
            # with version 0, there are fewer unfinished words
            self.lex_shift(N, 1, [lambda s: s[:-2] + '#_' + s, lambda s: '#' + s[2:] + '_' + s])
            self.lex_shift(N, -1, [lambda s: s + '#_' + s, lambda s: '#' + s + '_' + s])

    #####################################
    ##### INIT LEXICAL REPRESENTATIONS ##
    #####################################

    def calculate_max_len(self):
        pass

    def get_repr_indices_length(self, n, lex, forbid_idx=None):
        """
        Gets the string for words of some length that will be used to create the lexical representations
        """
        wds = [wd.split('_')[0] if i not in forbid_idx else '' for i, wd in enumerate(list(lex["word"]))]
        return super().get_repr_indices(wds, n) if len(wds) > 0 else []

    def extract_all_repr(self):
        self.all_repr = pkl.load(open(os.path.join(_ROOT, 'all_repr.pkl'), 'rb')["ortho"])

    #######################
    ##### INFO ############
    #######################

    def get_empty_percept(self, value=None):
        """
        Creates an empty percept with the same dimensions as the percept distribution

        :param value: The value to fill the empty percept with. If no value is provided, it will be filled with equal probabilities.
        :return: returns a numpy array with dimensions `(self.N,self.n)`
        """
        u = np.empty((self.modality.N, self.modality.n))
        u.fill(value if value is not None else 1.0 / self.modality.n)
        return u

######### Learning ###########

    def get_nb_mu_pre(self, len_ortho):
        return len_ortho

    def get_nb_mu_post(self, stim, len_ortho, nb_mu_pre):
        return len_ortho - nb_mu_pre - len(stim)

    def handle_no_learning(self):
        ph = self.modality.model.phono
        if ph.learning and ph.enabled and ph.PM:
            # no learning in this modality but learning in the other modality -> adds a 'zero' distribution here
            return self.get_empty_percept(0)[np.newaxis]
        return None


class _LexicalPhono(_Lexical):
    def __init__(self, modality, placement_auto=True, **modality_args):
        self.mod = "phono"
        self.placement_auto = placement_auto
        super().__init__(modality=modality, **modality_args)

    ###################################
    ##### INIT LEXICON DATAFRAME ######
    ###################################

    def handle_languages(self):
        """
        The function handles language-specific operations during the lexicon extraction
        """
        if self.modality.model.langue == 'en':
            # '~' shift already used for word fragments and shifted representations
            self.df.index = self.df.index.str.replace('~', '(')
        super().handle_languages()

    def extract_lexicon(self):
        self.open_lexicon()
        self.df["len_class"] = self.df.word.str.len()
        self.df['word'] = self.df.pron
        super().extract_lexicon()
        self.df["idx"] = self.df.groupby("len_class").cumcount()

    def set_char_dict(self):
        """
        Automatically chooses the dictionary according to the language
        """
        if len(self.chars_filename) == 0:
            self.chars_filename = "xsampa_ELP.csv" if self.modality.model.langue in "en" else \
                "xsampa_fr_simplified.csv" if self.modality.model.langue in "fr" else "xsampa_sp.csv" if self.modality.model.langue == "sp" else "xsampa_celex_german.csv"
        super().set_char_dict()

    def verify_chars(self):
        if self.modality.enabled:
            lexicon_chars = list(set("".join(self.df.index)))
            for i in lexicon_chars:
                if i != '~' and i != '_' and i not in self.chars:
                    print("problematic words for letter ", i, " : ", list(self.df[self.df.index.str.contains(i)].index)[:10])
                    raise ValueError(f"Unknown letter in lexicon : {i}")

    def simplify_alphabet(self):
        """
        Simplifies the phonemes in the lexicon dataframe by merging some characters (like 2 and 9).
        """

        def f_fr(val):
            return {'O': 'o', 'E': 'e', 'I': 'i', '9': '2', '1': '5', '8': 'y', ' ': '', 'A': 'a', '*': '°', '§': '&', 'U': 'u', 'r': 'R'}[val[0]]

        def f_en(val):
            return {'O': 'o', 'I': 'i', ' ': '', 'U': 'u', '$': 'o', 'Q': 'o', 'r': 'R'}[val[0]]
        self.df.reset_index(inplace=True)
        for col in ['pron', 'syll', 'pseg', 'phono', 'gpmatch', 'pron_x', 'pron_y', 'word']:
            if col in self.df.columns and not self.df[col].dtype == 'bool':
                if col in self.df.columns:
                    if self.modality.model.langue == "fr":
                        self.df[col] = self.df[col].str.replace('O|E|I|9|1| |\*|8|§|r', f_fr, regex=True)
                    elif self.modality.model.langue == "en":
                        self.df[col] = self.df[col].str.replace('O|I| |U|\$|Q|r', f_en, regex=True)

    def add_shift(self):
        for N in range(max(self.lenMin, 3), min(self.lenMax, max(self.all_shift_begin.keys())) - 1):
            self.lex_shift(N, 1, [lambda s: (s[:-2] + '~')[:self.modality.model.max_len[N] + 1] + '_' + s, lambda s: ('~' + s[2:])[:self.modality.model.max_len[N] + 1] + '_' + s])
            self.lex_shift(N, -1, [lambda s: s + '~_' + s, lambda s: '~' + s + '_' + s])

    #####################################
    ##### INIT LEXICAL REPRESENTATIONS ##
    #####################################

    def calculate_max_len(self):
        self.modality.model.max_len = self.df.groupby('len_class').max()['len'].to_dict()

    def set_repr(self):
        super().set_repr()
        if len(self.repr) > 0:
            self.modality.M = np.shape(self.repr)[1]

    def get_repr_indices_length(self, n, lex, forbid_idx=None):
        """
        Gets the string for words of some length that will be used to create the lexical representations.
        """
        nph = self.modality.model.max_len[n]
        wds = [wd.split('_')[0] if i not in forbid_idx else '' for i, wd in enumerate(list(lex["word"]))]
        wds = [wd + '#' * (nph - len(wd)) if i not in forbid_idx else '' for i, wd in enumerate(wds)]
        return super().get_repr_indices(wds, nph) if len(wds) > 0 else []

    def extract_all_repr(self):
        self.all_repr = pkl.load(open(os.path.join(_ROOT, 'all_repr.pkl'), 'rb')["phono"])

    #######################
    ##### INFO ############
    #######################

    def get_empty_percept(self, value=None):
        """
        Creates an empty percept with the same dimensions as the percept distribution

        :param value: The value to fill the empty percept with. If no value is provided, it will be filled with equal probabilities.
        :return: returns a numpy array with dimensions `(self.M,self.n)`
        """
        u = np.empty((self.modality.M, self.modality.n))
        u.fill(value if value is not None else 1.0 / self.modality.n)
        return u

    def get_phono_name(self, string=None):
        """
        Gets the phonological name corresponding to the orthographic name.
        :param string: orthographic name
        :return: the phonological name
        """
        data = self.modality.model.ortho.lexical.get_word_entry(string)
        if data is not None:
            return self.get_name(data.idx)
        return ""

    #######################
    ####### Learning ######
    #######################

    def get_nb_mu_pre(self, len_ortho):
        return self.modality.attention.len2phlen(len_ortho)

    def get_nb_mu_post(self, stim_ortho, len_ortho, nb_mu_pre):
        return self.modality.model.max_len[len_ortho] - nb_mu_pre - self.modality.model.max_len[len(stim_ortho)]

    def handle_no_learning(self):
        ortho = self.modality.model.ortho
        if ortho.learning and ortho.enabled and ortho.PM:
            # no learning in this modality but learning in the other modality -> adds a 'zero' distribution here
            return self.get_empty_percept(0)[np.newaxis]
        return None
