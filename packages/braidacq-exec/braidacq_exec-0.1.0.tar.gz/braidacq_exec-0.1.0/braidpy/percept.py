# BRAID utlities
import copy
import math
import pdb
from time import time

import numpy as np
import braidpy.utilities as utl
from scipy.stats import entropy
import logging


class percept:
    """
    The percept class is an inner class of the modality class and represents the perceptual submodel, either in the orthographic or phonological modality.

    :param leak: float. Parameter for the decline of the percept distribution
    """

    def __init__(self, modality, leak, gamma_ratio, top_down, word_reading=False):
        self.modality = modality
        self.leak = leak
        self.gamma_ratio = gamma_ratio
        self.top_down = top_down
        self.word_reading = word_reading
        self.limited_TD = True  # only the first 50 representation to limit calculation cost
        self.dist = {}
        self.H = None
        self.max_HDer = 1000
        self.stimulation = True  # presence of the input stimulus

    #################################
    #### INFERENCES #################
    #################################

    #### Calcul Gamma ##############

    def sigm(self, val):
        """
        Calculates the top-down lexical retroaction strength

        :param val: input value to the sigmoid function (generally the value of the lexical decision distribution)
        :return: the top-down lexical retroaction strength
        """
        return 2e-6 + 1 * (self.gamma_ratio / np.power((1. + np.exp(-(97 * val) + 95)), .7))

    def gamma(self):
        """
        Updates the gamma coefficient for top-down lexical retroaction
        """
        self.dist["gamma"] = self.sigm((1 if self.word_reading else self.modality.word.dist["ld"][0]))

    def gamma_sem(self):
        """
        Not used anymore. Calculates values for gamma_sem and gamma_sim based on the similarity between the semantic distribution and the word distribution.
        """
        if self.modality.model.semantic.gamma_sem_init == 0:
            self.modality.model.semantic.gamma_sem_init = np.dot(self.modality.word.dist["word"], self.modality.model.semantic.dist["sem"])
        sim = np.dot(self.modality.word.dist["word"], self.modality.model.semantic.dist['sem']) / self.modality.model.semantic.gamma_sem_init
        gamma = 2 * self.gamma_ratio / np.power((1. + np.exp(-3 * sim + 11)), .7)
        self.dist["gamma_sem"] = gamma
        self.dist["gamma_sim"] = sim

    ##### Calcul probability distributions ########

    @utl.abstractmethod
    def build_percept(self):
        """
        Builds the percept distribution with bottom-up information
        """
        return

    def update_percept(self):
        """
        Updates the percept distribution with the top down retroaction
        """
        for mod in ['ortho', 'phono']:
            data = getattr(self.modality.model, mod)
            if data.exists and data.percept.top_down:
                if self.limited_TD:
                    idx = data.word.dist['word'].argsort()[::-1][:50]
                    dist = utl.TD_dist(data.word.dist["word"][idx], self.modality.lexical.repr[:data.lexical.shift_begin][idx])
                else:
                    dist = utl.TD_dist(data.word.dist["word"], self.modality.lexical.repr[:data.lexical.shift_begin])
                self.dist["percept"] *= (
                    data.percept.dist["gamma"] * dist + (1 / self.modality.n) * (1 - data.percept.dist["gamma"]) * np.ones(self.dist["percept"].shape))
                self.dist["percept"] = utl.norm_percept(self.dist["percept"])

    #################################
    #### INFO #######################
    #################################

    def get_entropy(self, dist=None):
        """
        Calculates the entropy of the percept distribution

        :param dist: a distribution in the same shape as self.dist["percept"]. If None, returns the percept entropy.
        :return: The entropy of the distribution, one value per position.
        """
        dist = dist if dist is not None else self.dist["percept"]
        return [entropy(i) for i in dist]

    #################################
    #### DECISIONS ##################
    #################################

    @utl.abstractmethod
    def decision(self, dist=None):
        pass

    def evaluate_decision(self, dist=None, dist_name="percept"):
        """
        Evaluates the percept decision taken by the model (function decision of this class).

        :param dist: a distribution in the same shape as self. If None, the model state is used instead.
        :param type: "percept" or "pron_first_pass" if you want to evaluate the pronunciation at the end of the first pass on the word
        :return: a boolean value indicating whether the decision is correct.
        """
        if dist_name == "pron_first_pass":
            string = self.decision() if len(self.pron_first_pass) == 0 else self.pron_first_pass
            return self.modality.stim == utl.str_transfo(string)
        else:
            dist = dist if dist else self.dist["percept"]
            return self.modality.stim == utl.str_transfo(self.decision(dist))

    def print_dist(self, dist_name="percept"):
        """
        Prints information about the percept distribution (used at the end of a simulation)

        :param dist_name: The name of the distribution to be printed.
        :return: a string with information about the distribution.
        """
        if self.modality.enabled:
            if dist_name == "percept":
                return f' {self.decision()}, {[round(np.max(i), 4) for i in self.dist["percept"]]}'
            else:
                return f' final : {self.dist["gamma"]}'
        return ''


class perceptOrtho(percept):
    def __init__(self, modality, top_down=True, gamma_ratio=1e-3, leak=1.5e-5, word_reading=False, **modality_args):
        super().__init__(modality=modality, top_down=top_down, gamma_ratio=gamma_ratio, leak=leak, word_reading=word_reading, **modality_args)

    #################################
    #### INFERENCES #################
    #################################

    def build_percept(self):
        """
        Builds the orthographic percept distribution
        """
        mem = (self.dist["percept"] + self.leak) / (1 + self.modality.n * self.leak)
        if self.stimulation:
            self.dist["percept"] = utl.norm_percept(mem * self.bottom_up_matrix)
        else:
            self.dist["percept"] = utl.norm_percept(mem)

    def update_percept_sem(self):
        pass

    #################################
    #### DECISIONS ##################
    #################################

    def decision(self, dist=None):
        """
        Takes a decision on the most probable letter in each position (maximum of the probability distribution)
        """
        dist = dist if dist is not None else self.dist["percept"]
        return "".join([self.modality.lexical.chars[i] if i > -1 else '~' for i in [np.argmax(dist[i, :]) for i in range(np.shape(dist)[0])]])

    def print_dist(self, dist_name="percept"):
        if dist_name == "percept":
            return "percept ortho : " + super().print_dist(dist_name)
        else:
            return "gamma ortho : " + super().print_dist(dist_name)


class perceptPhono(percept):
    def __init__(self, modality, top_down=True, gamma_ratio=1e-3, gamma_deb=90, leak=0.000005, placement_auto=True, word_reading=False, recalage=True, **modality_args):
        """
        :param recalage : boolean. if True, "recalage" performed at the end of the simulation
        """
        super().__init__(modality=modality, top_down=top_down, gamma_ratio=gamma_ratio, leak=leak, word_reading=word_reading, **modality_args)
        self.use_word = False
        self._pos = -1
        self.used_idx, self.used_idx_tmp, self.used_mask = {key: [] for key in range(30)}, [], []
        # better results with placement auto at True, would like to be able to put it at False
        self.placement_auto = placement_auto
        self.gamma_deb = gamma_deb
        self.recalage = recalage
        self.pron_first_pass = ""

    #################################
    #### INFERENCES #################
    #################################

    def sigm(self, val):
        """
        Calculates the top-down lexical retroaction strength

        :param val: input value to the sigmoid function (generally the value of the lexical decision distribution)
        :return: the top-down lexical retroaction strength
        """
        return 2e-6 + 1 * (self.gamma_ratio / np.power((1. + np.exp(-(97 * val) + self.gamma_deb)), .7))

    def filter_att(self, dist=None, att=None):
        """
        Calculates the perceptual distribution filtered by attention.

        :param dist: the percept distribution. If None, takes the model current percept distribution.
        :param att: the attention profile, which is a list of floats between 0 and 1. If None, takes the model current attentional distribution.
        :return: The filtered percept distribution
        """
        att = att if att is not None else self.modality.attention.dist
        dist = dist if dist is not None else self.dist["percept"]
        return np.array([i * a + (1 - a) / self.modality.n for (i, a) in zip(dist, att)])

    def get_dz_pos(self, threshold=0.5):
        """
        Finds the position of the next # identified by the model.
        :param threshold: threshold to consider a # has been recognized. This parameter's default value is set at a high value because otherwise,
        when a # is incorrectly recognized, the attention cannot anymore be place at this position, and a change of mind (correction) is unlikely.
        """
        if 'percept' not in self.modality.percept.dist:
            return self.modality.M
        decision = self.modality.percept.decision()
        # automatically retrieved if attention phono is automatically set
        if False and self.modality.attention.att_phono_auto:
            dz_pos = int(self.modality.model.gs[-1]) + 1
        # elif self.modality.attention.reading_unit=="grapheme":
        #    dz_pos=len(self.modality.stim)
        elif '#' not in decision:
            dz_pos = len(decision)
        else:
            dz_pos = next((idx for idx, char in enumerate(decision) if char == '#' and max(self.modality.percept.dist['percept'][idx]) > threshold), None)
            dz_pos = dz_pos if dz_pos is not None else len(decision)
            # idx=decision.index('#')
            # if max(self.modality.percept.dist['percept'][idx]) > threshold:
            #    dz_pos=idx
            # if max([max(i) for i in self.modality.percept.dist['percept'][idx:]]):
            #    dz_pos= int(next(i for i, val in enumerate(decision) if
            #              (val == '#' and max(self.modality.percept.dist["percept"][i]) > threshold)))
            # else:
            #    dz_pos = len(decision)
            # dz_pos = int(next(i for i, val in enumerate(decision) if
            #              (val == '#' and max(self.modality.percept.dist["percept"][i]) > threshold) #or i == len(decision)-1))
            # print("thr dz pos", decision)
        return dz_pos

    def select_phono_repr(self):
        """
        Selects the phonological representations that will be used during decoding based on the similarity between letter percept and orthographic representations.

        :return: the number of words selected and the phonological representations selected.
        """
        mask = utl.norm1D(self.modality.model.ortho.word.dist["word_sim_att"])
        nb_words = min(len(mask), 5)
        # faster than argsort : selects 10 maximum values
        idx_sort = np.sort(np.argpartition(mask, len(mask) - nb_words)[-nb_words:])
        self.used_idx_tmp = [i for i in idx_sort if mask[i] > 0]  # for the case where there are less than 10 words in the lexicon
        if self.modality.attention.reading_unit == 'grapheme' and self.modality.model.ortho.pos not in self.used_idx.keys():
            self.used_idx[self.modality.model.ortho.pos] = []
        self.used_idx[self.modality.model.ortho.pos] = list(dict.fromkeys(self.used_idx[self.modality.model.ortho.pos] + self.used_idx_tmp))
        self.used_mask = utl.norm1D([mask[i] for i in self.used_idx_tmp])
        self.used_mask = [mask[i] for i in self.used_idx_tmp]
        # self.used_mask=utl.norm1D([i ** 4 for i in self.used_mask])
        if logging.DEBUG >= logging.root.level:
            logging.debug(f"used words {self.modality.model.ortho.lexical.get_names(self.used_idx_tmp)}")
            logging.debug(f"sim value adjusted {utl.l_round(self.used_mask, 6)}")
            logging.debug(f"sim value {[round(mask[i] * 1000, 5) for i in self.used_idx_tmp]}")
            logging.debug(f"psi : {self.decision()}")
        return len(self.used_idx_tmp), copy.copy(self.modality.lexical.repr[self.used_idx_tmp])

    def phono_alignment(self, nb_words, phono_repr):
        """
        Determines if the selected phonological representations need to be shifted left or right to improve the alignment, and performs the shift if necessary.
        To do that, the model calculates for each phonological representation the similarity between the phonological percept and the phonological representation,
        which can be either left untouched, shifted left or right. If similarity is higher for a shifted representation, it's done this way.

        :param nb_words: int. Number of phonological words selected.
        :param phono_repr: np.array. The selected phonological representations.
        :return: the updated phono_repr array after performing phonological alignment on it.
        """
        psi = self.dist["percept"]
        ref = self.modality.lexical.repr[self.modality.lexical.get_word_entry().idx] if self.placement_auto and self.modality.stim is not None and len(self.modality.stim) > 0 else psi
        if sum(sum(ref)) == 0:
            ref = utl.create_repr(np.array([[self.modality.lexical.chars.index(i) for i in self.modality.stim + '#' * (self.modality.M - len(self.modality.stim))]]), self.modality.n, self.modality.lexical.eps)[0]
        unif = np.ones(self.modality.n) / self.modality.n
        # shifted phono representations
        repr_decal = np.zeros((3, nb_words, self.modality.M, self.modality.n))
        repr_decal_db = np.zeros((2, nb_words, self.modality.M, self.modality.n))
        repr_decal[0] = np.concatenate((phono_repr[:, 1:], np.repeat(unif[np.newaxis, np.newaxis], nb_words, axis=0)), axis=1)
        repr_decal[1] = phono_repr
        repr_decal[2] = np.concatenate((np.repeat(unif[np.newaxis, np.newaxis], nb_words, axis=0), phono_repr[:, :-1]), axis=1)
        # double shift
        repr_decal_db[0] = np.concatenate((phono_repr[:, 2:], np.repeat(np.repeat(unif[np.newaxis, np.newaxis], nb_words, axis=0), 2, axis=1)), axis=1)
        repr_decal_db[1] = np.concatenate((np.repeat(np.repeat(unif[np.newaxis, np.newaxis], nb_words, axis=0), 2, axis=1), phono_repr[:, :-2]), axis=1)

        # alignment precisely on the precessed segment, not at other positions -> comparison filtered by attention
        logging.debug(f"attention profile phono : {utl.l_round(self.modality.attention.dist / self.modality.attention.Q)}")
        sim1 = np.einsum('jk,xijk->xij', ref, repr_decal)
        sim = np.array([[np.prod(self.filter_att(i, att=utl.norm1D(self.modality.attention.dist))) for i in w] for w in sim1])
        sim1_db = np.einsum('jk,xijk->xij', ref, repr_decal_db)
        sim_db = np.array([[np.prod(self.filter_att(i, att=utl.norm1D(self.modality.attention.dist))) for i in w] for w in sim1_db])
        for i in range(nb_words):
            if i in range(len(self.used_idx_tmp)):
                S = sim[:, i]
                S_db = sim_db[:, i]
                amax = np.argmax(S)
                amax_db = np.argmax(S_db)
                if amax != 1 and max(S) > 1.1 * S[1] and max(S_db) < 10 * max(S):
                    if logging.DEBUG >= logging.root.level:
                        logging.debug(f"dec {'gauche' if amax == 0 else 'droit'}, {self.decision(phono_repr[i])}, {S}")
                    phono_repr[i] = repr_decal[amax, i]
                    S[1] = S[amax]
                elif max(S_db) > 25 * S[1]:
                    if logging.DEBUG >= logging.root.level:
                        logging.debug(f"dec double {'gauche' if amax_db == 0 else 'droit'}, {self.decision(phono_repr[i])}, {[S_db[0], S[1], S_db[1]]}")
                    phono_repr[i] = repr_decal_db[amax_db, i]
                else:
                    if logging.DEBUG >= logging.root.level:
                        logging.debug(f"pas de décalage, {self.decision(phono_repr[i])},  {S}, {S_db}")
        return phono_repr

    def calculate_psi(self, phono_repr):
        """
        Updates the psi distribution according to the phonological representations previously selected and possibly shifted.

        :param phono_repr: the phonological representations selected.
        """
        # TODO
        # quand sigma=1, comparaison bien plus précise parce que att à 1
        # les mots qui correspondent ressortent beaucoup plus
        # 5 mots -> poids non constant en fonction de sigma
        # plusieurs mots : abandon beige
        # sigma=0.25 0.0117 0.0208 0.0107 att=[0.99 autres]
        # sigma=0.5 0.00203 0.00339 0.003 006 att=[80 10 10]
        # sigma=0.75 0.00104 0.00176 0.0017 003 att=[55 22 22 02 02]
        # sigma=1 0.001105 0.00157 0.0016 301 att=[40 24 05]
        # sigma=1.25 0.001039 0.00125 14 285 att=[33 24 09]
        # sigma =1.5 0.000881 0.00134 13 att=[29 23 12]
        # sigma=1.75 0.00829 0.00116 att=[26 22 13]
        att = self.modality.model.ortho.attention
        ph_tmp = np.einsum('i,ijk->jk', utl.norm1D(self.used_mask), phono_repr)
        logging.debug(f"decision : {self.decision(dist=ph_tmp)}")

        # Filtering of lexical information by phonological attention
        filt_ph = np.array([i * a + (1 - a) / self.modality.n for (i, a) in zip(ph_tmp, self.modality.attention.dist)])
        logging.debug([entropy(i) for i in filt_ph])

        # Phonological STM and output distribution
        mem_ph = (self.dist["percept"] + self.leak) / (1 + self.modality.n * self.leak)
        if self.stimulation:
            self.dist["percept"] = utl.norm_percept(mem_ph * filt_ph)
        else:
            self.dist["percept"] = utl.norm_percept(mem_ph)

    def build_decoding(self):
        """
        Decoding step : the model has previously selected the most similar words to the letter percept where the attention stands, it's stored in the distribution "word_sim_att".
        It now uses the phonological representations of those words, filtered by phonological attention, to update the psi distribution.
        These representations may possibly be shifted left or right, to ensure a better alignment between the actual phonological percept and
        the filtered phonological representations.
        """
        if self.modality.enabled:
            nb_words, phono_repr = self.select_phono_repr()
            logging.debug(f"percept ortho : {self.modality.model.ortho.percept.print_dist()}")
            logging.debug(f"percept phono : {self.print_dist()}")
            if self.modality.attention.mean > 0:
                phono_repr = self.phono_alignment(nb_words, phono_repr)
            self.calculate_psi(phono_repr)

    def recalage_stim(self):
        """
        This function attempts to increase the similarity between the phoneme percept and the phonological lexicon by deleting or adding a new phoneme.
        To do this it compares the similarity between the percept and the lexicon to the same similarity with a modified percept with insertion or deletion.
        The insertion/deletion is kept only if its similarity with the lexicon is greater than the original similarity.
        """
        if not self.modality.word.decision("ld") and len(self.modality.lexical.repr) > 0 and self.modality.lexical.shift_begin > 0:  # insertions/deletions needed ?
            for _ in range(2):  # 2 successive attempts to allow for 2 insertions/deletions
                # we delete/insert a character and see if it improves the comparison
                psi = self.dist["percept"]  # probability distribution
                pron_str = self.decision()  # string
                n = next(i for i in reversed(range(len(pron_str))) if pron_str[i] != '#') + 1  # nb of phonemes in the string
                n_maxi, res, maxi = -1, None, 1000
                n_ph = self.phono.n
                unif = np.ones(n_ph) / n_ph  # uniform distribution
                # comparison between 2 similarities : percept/lexicon and modified percept/lexicon
                # because modified percept is built by making a deletion (for example) and put an uniform at the end, we have to compensate
                # the loss of 'informativeness' of this new percept without insertion/deletion by changing it and putting an uniform too
                # so the reference for the comparison will not be the percept itself, but a modified percept too.
                # first 4 arrays (indices from 0 to 3) are the insertion/deletion representations, the 4 last are the references
                for exch in range(n):  # calculation of the insertions/deletions and their references at each position
                    cmp = np.zeros((8, self.modality.M, self.modality.n))
                    # deletion
                    cmp[0] = np.concatenate((np.delete(psi, exch, axis=0), unif[np.newaxis]))
                    cmp[4] = copy.copy(psi)
                    cmp[4, exch] = unif
                    # insertion
                    cmp[2] = np.concatenate((psi[:exch], unif[np.newaxis, :], psi[exch:-1]))
                    cmp[6] = np.concatenate((psi[:-1], unif[np.newaxis]))
                    if exch < n - 1:  # double insertions or double deletion
                        cmp[1] = np.concatenate((np.delete(np.delete(psi, exch, axis=0), exch, axis=0), unif[np.newaxis], unif[np.newaxis]))
                        cmp[5] = copy.copy(psi)
                        cmp[5, exch] = unif
                        cmp[5, exch + 1] = unif
                        cmp[3] = np.concatenate((psi[:exch], unif[np.newaxis, :], unif[np.newaxis, :], psi[exch:-2]))
                        cmp[7] = np.concatenate((psi[:-2], unif[np.newaxis], unif[np.newaxis]))
                    # similarity calculation
                    sim_word = np.prod(np.einsum('lij,kij->lki', cmp, self.modality.lexical.repr[:self.modality.lexical.shift_begin]), axis=2)
                    sim = np.max(sim_word, axis=1)
                    for i in range(4):
                        if sim[i + 4] > 0 and sim[i] / sim[i + 4] > maxi:
                            i_res, maxi, res, typ = np.argmax(sim_word[i]), sim[i] / sim[i + 4], cmp[i], "add" if i > 1 else "del"
                if res is not None:  # intertion/deletion selected
                    self.phono.dist["percept"] = res
                    logging.simu("recalage : " + pron_str + " -> " + self.decision() + " coeff = " + str(maxi))
                    logging.simu("for word " + self.ortho.get_name(i_res))

    #################################
    #### INFO #######################
    #################################

    def psi_score(self):
        """
        Computes the cosine similarity between the representation of the stimulus and the representation of the phonological percept distribution.

        :return: The mean of the cosine similarity between the representation of the stimulus and the representation of the percept.
        """
        if self.modality.stim:
            n = len(utl.str_transfo(self.modality.stim))
            p = self.dist["percept"][:n]
            # we don't compare with the stored representation but with an adult representation
            # this way, the reference is always the same
            wds_idx = self.modality.lexical.get_repr_indices([self.modality.stim], self.modality.model.max_len[self.modality.N])
            repr = utl.create_repr(wds_idx, self.modality.n, self.modality.lexical.eps)[0]
            scal = np.einsum('ij,ij->i', p, repr)
            norm = np.sqrt(np.einsum('ij,ij->i', repr, repr)) * np.sqrt(np.einsum('ij,ij->i', p, p))
            return np.mean(scal / norm) if sum(norm) > 0 else 0
        return -1

    def get_used_words(self):
        """
        A dictionary of the words used for decoding when attention landed on a specific position.

        :return: A dictionary of the used words in the format { position : [used_words] }
        """
        return {key: self.modality.model.ortho.lexical.get_names(list(dict.fromkeys(self.used_idx[key]))) for key, value in self.used_idx.items() if len(value) > 0}

    def missing_bigram(self):
        """
        Detects if some bigram didn't receive a corresponding word during decoding and finds a match if this is the case. Purely informative function.
        :return: possible words to use and boolean indicating if there is a missing bigram
        """
        used_words = {key: [i.split('_')[0] for i in val] for key, val in self.get_used_words().items()}
        stim = self.modality.model.stim
        conditions_remplies = [any(mot[i:][:2] == stim[i:i + 2]
                                   for position in [i, i + 1] for mot in used_words.get(position, []))
                               for i in range(len(stim) - 1)]
        logging.simu("bigram found ?")
        logging.simu(f"{[stim[i:i + 2] + ':' + str(conditions_remplies[i]) for i in range(len(stim) - 1)]}")
        possible_words = {}
        if not all(conditions_remplies):
            df = self.modality.model.ortho.lexical.df
            lexicon_words = list([i for i in df[df.len_class == len(stim)].index.values if i != stim])
            for i, bool in enumerate(conditions_remplies):
                if not bool:
                    bigram = stim[i:][:2]
                    words = [lexicon_word[i:][:2] for lexicon_word in lexicon_words]
                    if any(bigram == wd for wd in words):
                        res = lexicon_words[next(i for i, wd in enumerate(words) if bigram == wd)]
                        res = res if '_' not in res else res.split('_')[1]
                        possible_words[i] = res
                        if len(res) > 0:
                            logging.simu("Missing bigram : " + bigram + ", matching word in the lexicon : " + res)
                    else:
                        possible_words[i] = ""
        logging.simu(str(possible_words))
        return possible_words, conditions_remplies

    #################################
    #### DECISIONS ##################
    #################################

    def decision(self, dist=None):
        """
        Returns a string representing the pronunciation based on the maximum values of the phonological percept distribution.

        :param dist: 2D numpy array. The distribution of probabilities for each phoneme in a given word.
        :return: a string that represents the pronunciation of the word.
        """
        if isinstance(dist, str):
            raise TypeError("distribution should be an array of float values")
        dist = dist if dist is not None else self.dist["percept"]
        maxi = [max(d) for d in dist][::-1]
        last_idx = len(dist) - 1 - (next(i for i, val in enumerate(maxi) if val > 0.1) if max(maxi) > 0.1 else 0)
        pron_idx = [np.argmax(dist[i, :]) if max(dist[i, :]) > 0.1 and list(dist[i, :]).count(dist[i, 0]) != len(dist[i, :]) and (
            i <= last_idx or not (self.modality.enabled and self.modality.lexical.repr_unif)) else -1 for i in range(np.shape(dist)[0])]
        return "".join([self.modality.lexical.chars[i] if i > -1 else '~' for i in pron_idx])

    def print_dist(self, dist_name="percept"):
        if dist_name == "percept":
            return "percept phono : " + super().print_dist(dist_name)
        else:
            return "gamma phono : " + super().print_dist(dist_name)

    def update_percept_sem(self):
        """
        Updates the percept distribution with the top down retroaction according to the semantic context
        """
        sem = self.modality.model.semantic
        if self.modality.enabled and sem.context_sem and sem.top_down:
            w = self.modality.word.dist["word"]
            ws = sem.dist['sem']
            res = w * ws
            # a gamma is needed, otherwise even with a uniform context, there is strong top-down favoring # (end) phoneme
            ratio = 1 - entropy(res) / math.log(len(w))
            gamma = 1 / np.power((1. + np.exp(-(97 * ratio) + 90)), .7)
            dist = utl.TD_dist(w * ws, self.modality.lexical.repr[:self.modality.lexical.shift_begin])
            dist = (sem.Q_sem * gamma * dist + (1 / self.modality.n) * (1 - sem.Q_sem * gamma) * np.ones(self.dist["percept"].shape))
            self.dist["percept"] = utl.norm_percept(dist * self.dist["percept"])
            self.dist["gamma_sem"] = gamma
        # TODO
        # sim = np.dot(self.modality.word.dist["word"], self.modality.model.semantic.dist['sem']) / self.modality.model.semantic.gamma_sem_init
        # gamma = 2 * self.gamma_ratio / np.power((1. + np.exp(-3 * sim + 11)), .7)
