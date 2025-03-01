import logging
import pdb

import numpy as np
from numpy import linalg as LA
import braidpy.utilities as utl
import matplotlib.pyplot as plt
from scipy.stats import entropy


class _Word:
    """
    The _Word class is an inner class of the modality class and represents the word perceptual submodel, either in the orthographic or phonological modality.

        :param modality : the modality object
        :param gamma_ratio : float. The maximum value of the sigmoïd used to calculate the top-down
        :param top_down: boolean. If False, top-down id deactivated.
        :param leakW : int. Calibrated parameter for decline in the word distribution
        :param L2_L_division : boolean, division by L2 norm of L distribution ?
        :param ld_thr : float. Threshold for lexical novelty detection.
        :param word_reading : boolean. if True, phono DL is considered equal to 1 for the lexical feedback
        :param new_ld : if True, uses the ld version with the Monthy Hall problem.
    """

    def __init__(self, modality, gamma_ratio, top_down, leakW=1250, L2_L_division=False, ld_thr=0.5, word_reading=False, new_ld=False):
        self.modality = modality
        self.gamma_ratio = gamma_ratio
        self.top_down = top_down
        self.leakW = leakW
        self.L2_L_division = L2_L_division
        self.weightLDYES = self.weightLDNO = 0.15
        self.ld_trans_mat = np.array([[1 - self.weightLDYES, self.weightLDYES], [self.weightLDNO, 1 - self.weightLDNO]])
        self.ld_thr = ld_thr  # more corrections than needed, but misses almost no case where correction is needed
        self.word_reading = word_reading
        self.new_ld = new_ld
        self.PM = True
        self.chosen_word = ""
        self.dist = {}

    #################################
    #### INFERENCES #################
    #################################

    ############## Bottom-up #######

    def build_word_inferences(self):
        """
        Builds bottom-up distributions by building the similarity, the word and the ld distributions
        """
        if self.modality.enabled:
            self.build_similarity()
            self.build_word()
            self.build_ld()

    @utl.abstractmethod
    def build_similarity(self):
        """
        Updates the the similarity between the percept and the lexicon
        """
        pass

    def build_word(self):
        """
        Builds the word distribution according to the similarity
        """
        self.dist["word"] = utl.norm1D(self.dist["word_sim"][:, 0])
        if self.modality.model.L2_L_division:
            # necessary to limit the jump at the beginning of the simulation: the division by the norm is only for the DL, not for W
            # since the representations are stored in a noramalized way, it's necessary to 'unnormalize' by multiplicating by the norm
            self.dist["word"] = utl.norm1D(self.modality.lexical.repr_norm[:self.modality.lexical.shift_begin] * self.dist["word"])

    def build_word_sem(self):
        """
        Updates the word distribution with the word-semantic distribution : not depending on a dl value
        """
        sem = self.modality.model.semantic
        if True or not sem.top_down or not sem.online_prod:
            self.dist["word"] = utl.norm1D(self.modality.model.semantic.dist["sem"] * self.dist["word"])

    def build_word_color(self):
        """
        Updates the word distribution with the word-color distribution : not depending on a dl value
        """
        if self.modality.exists and self.modality.model.color.enabled:
            col = self.modality.model.color
            alpha_wc = col.alpha_wcolor
            idx = {self.modality.model.ortho.lexical.df.loc[key].idx: p for key, p in zip(col.color_dict.keys(), col.dist["color_words"])}
            dist_wc = utl.norm1D([idx[index] if index in idx.keys() else np.exp(-5) for index in range(len(self.modality.word.dist["word"]))])
            mod_dist = [alpha_wc * dist_wc[i] + (1 - alpha_wc) / len(dist_wc) for i in range(len(dist_wc))]
            self.dist["word"] = utl.norm1D(mod_dist * self.dist["word"])

    def build_ld(self):
        """
        Builds the lexical decision distribution according to the similarity
        """
        if self.new_ld:
            pba_yes = self.dist["sim_n"]
            pba_no = self.dist["err_n"]
            self.ld_trans_mat = np.array([[1 - 0.15, 0.15], [0.15, 1 - 0.15]])
            proba_ld_new = utl.norm1D([pba_yes, pba_no])
            ld_proba_trans_new = np.matmul(self.ld_trans_mat, self.dist["ld"]) * proba_ld_new  # Markov transition
            self.dist["ld"] = utl.norm1D(ld_proba_trans_new)
        else:
            proba_error_i = self.dist["word_sim"].sum(0)
            # equivalent calculation, but the kept version is faster.
            # proba_ok=[1]+[LA.norm(i)/LA.norm(1-i) for i in self.percept.dis["percept"]t]
            proba_ok = [1] + [1 / np.sqrt(1 + (self.modality.n - 2) / LA.norm(i) ** 2) for i in self.modality.percept.dist["percept"]]
            proba_err = [i * j for i, j in zip(proba_ok, proba_error_i)]
            proba_ld = np.array([proba_err[0], np.mean(proba_err[1:])])
            ld_proba_trans = np.matmul(self.ld_trans_mat, self.dist["ld"]) * proba_ld  # Markov transition
            self.dist["ld"] = utl.norm1D(ld_proba_trans)

    ############## Top-Down #######

    def plot_sigm(self):
        """
        Plots a sigmoid curve to test different gamma functions
        """
        x = [i / 100 for i in range(120)]
        y = [self.sigm(i) / 10 for i in x]
        y = [0.2 / np.power((1. + np.exp(-90 * ratio + 85)), .3) for ratio in x]
        plt.plot(x, y)
        plt.show()

    @utl.abstractmethod
    def gamma(self):
        """
        Updates the gamma coefficient for top-down lexical retroaction
        """
        pass

    @utl.abstractmethod
    def sigm(self, val):
        """
        Calculates the top-down lexical retroaction strength

        :param val: input value to the sigmoid function (generally the value of the lexical decision distribution)
        :return: the top-down lexical retroaction strength
        """
        pass

    def update_word(self, other_dist):
        """
        Updates the word distribution according to the word distribution in the other modality, modulated by the ld distribution
        """
        if self.modality.enabled and self.modality.model.semantic.top_down:
            gamma = self.sigm(other_dist["ld"][0])
            TD_dist = other_dist["word"] * gamma + np.ones(len(other_dist["word"])) / len(other_dist["word"]) * (1 - gamma)
            self.dist["word"] = utl.norm1D(TD_dist * self.dist["word"])

    #################################
    #### INFO #######################
    #################################

    def get_entropy(self):
        """
        Calculates the entropy of the word distribution

        :return: The entropy of the word distribution.
        """
        return entropy(self.dist["word"])

    #################################
    #### DECISIONS ##################
    #################################

    def PM_decision(self):
        """
        Makes the lexical novelty detection for this modality
        """
        self.PM = False if self.modality.lexical.force_update else True
        if self.modality.enabled and not self.modality.lexical.force_app:
            # recognition via lexical decision
            if self.dist["ld"][0] > self.ld_thr:
                self.PM = False
            # recognition via context
            elif self.modality.model.semantic.context_identification and \
                    self.modality.model.semantic.p_sem > 1 and \
                    not self.modality.model.detect_mismatch():
                idx_res = self.modality.lexical.df.loc[self.decision("word")].idx
                idx_res = np.array(idx_res) if not isinstance(idx_res, np.int64) else np.array([idx_res])
                ident = len([i for i in idx_res if i in self.modality.model.semantic.idx_sem]) > 0
                if ident:
                    self.PM = False

    def decision(self, dist_name="word", dist=None, **kwargs):
        """
        The function takes in a distribution name or a distribution and returns the decision based on it.

        :param dist_name: the name of the distribution to be used for the decision, defaults to word (optional)
        :param dist: the probability distribution to use for the decision. If it's not set, the model state is used instead.
        :return: The decision is being returned.
        """
        dist = dist if dist is not None else self.dist[dist_name] if dist_name in ['word', 'ld', 'word_sim', 'word_sim_att'] else \
            self.dist["word"] if dist_name == "word_index" else None
        if self.modality.enabled:
            if dist_name == 'ld':
                return dist[0] > (self.ld_thr if "ld_thr" not in kwargs else kwargs["ld_thr"])
            elif dist_name in ['word', 'word_sim_att', 'word_sim']:
                dsort = np.argsort(dist)[::-1][:1]
                try:
                    return np.array(self.modality.lexical.get_names(dsort))[dsort.argsort()][0]
                except:
                    return ""
            elif dist_name == "word_index":
                return np.argmax(dist) if len(dist) > 0 else -1
            elif dist_name in ['word_stim']:
                raw = self.modality.lexical.get_word_entries(check_store=True)
                try:
                    raw = raw[(raw.store) & (raw.len_class == self.modality.N)]
                    idx = int(raw.idx) if len(raw) > 0 else None
                except:
                    try:
                        idx = raw.idx
                    except:
                        idx = None
                return self.dist["word"][idx] if idx is not None else -1

    def print_dist(self, dist_name="ld"):
        """
        Prints information about a given distribution (used at the end of a simulation)

        :param dist_name: The name of the distribution to be printed.
        :return: a string with information about the distribution.
        """
        if self.modality.enabled:
            if dist_name == 'word':
                dist = self.dist["word"]
                idx = self.decision("word_index")
                if idx > -1:
                    wd = self.modality.lexical.get_word_entry(self.modality.lexical.get_name(index=idx))
                    if wd is not None:
                        return f' {wd.name}, idx = {idx}, freq = {wd.freq}, wmax = {round(dist[idx], 6)}, {len(dist)} words '
                    return ''
            elif dist_name == 'ld':
                return self.dist["ld"][0]
            elif dist_name == 'word_stim':
                return f' : {self.decision(dist_name)}'
        return ''

    def evaluate_decision(self, dist=None):
        """
        Evaluates the decision taken by the model (function decision of this class), for the distribution "word" only.

        :param dist: the probability distribution to use for the decision. If it's not set, the model state is used instead.
        :return: a boolean value indicating whether the decision is correct.
        """
        # not every decision can be evaluated by the model. For example, for the dl, one must know if it's the first exposure to a word or not
        # -> evaluation not implemented here
        dist = dist if dist else self.dist["word"]
        idx = self.decision("word_index", dist)
        return self.modality.stim == self.modality.lexical.get_name(index=idx) if idx >= 0 else False


class _WordOrtho(_Word):
    def __init__(self, modality, top_down=True, gamma_ratio=5e-2, **modality_args):
        super().__init__(modality=modality, top_down=top_down, gamma_ratio=gamma_ratio, **modality_args)

    #################################
    #### INFERENCES #################
    #################################

    def build_similarity(self):
        wtrans = utl.build_word_transition_vector(self.dist["word"][:self.modality.lexical.shift_begin], self.modality.lexical.freq[:self.modality.lexical.shift_begin], self.leakW)
        att = self.modality.attention.dist
        att[att > 1] = 1
        # no markov chain on word_sim_att, otherwise the prior will reinforce himself
        logging.debug(f"attention profile ortho : {utl.l_round(att)}")
        self.dist["word_sim_att"] = utl.norm1D(utl.word_sim_att(self.modality.lexical.repr, self.modality.percept.dist["percept"], att))
        wsim = utl.wsim(self.modality.lexical.repr[:self.modality.lexical.shift_begin], self.modality.percept.dist["percept"])
        self.dist["word_sim"] = np.array(wtrans)[:, np.newaxis] * wsim
        if self.new_ld:
            anti_diag = np.array([[0 if i == j else 1 for j in range(self.modality.n)] for i in range(self.modality.n)])
            anti_diag = np.repeat(anti_diag[np.newaxis, :], self.modality.N, axis=0)
            # normalisation here doesn't change anything
            mh_matrix = [utl.norm2D(i, n=1) for i in anti_diag * self.modality.percept.dist["percept"][:, np.newaxis]]
            # err_n = np.sum(mh_matrix * self.dist["percept"][:, np.newaxis],axis=2)
            err_n = utl.norm2D(np.sum(mh_matrix * self.modality.percept.dist["percept"][:, np.newaxis], axis=2), n=1)
            err = [[err_n[j] if i == j else self.modality.percept.dist["percept"][i] for j in range(self.modality.N)] for i in range(self.modality.N)]
            err_n = np.sum(np.repeat(wtrans[:, np.newaxis], self.modality.N, axis=1) * np.prod(np.einsum('kij,ilj->kil', self.modality.lexical.repr[:self.modality.lexical.shift_begin], err), axis=1), axis=0)
            self.dist["err_n"] = np.max(err_n)
            prod = np.prod(np.einsum('kij,ij->ki', self.modality.lexical.repr[:self.modality.lexical.shift_begin], self.modality.percept.dist["percept"]), axis=1)
            self.dist["sim_n"] = (wtrans * prod).sum()
            # no markov chain on wsim_mask, otherwise the prior will reinforce himself
            logging.debug(self.modality.percept.print_dist())

    def sigm(self, val):
        """
        Calculates the top-down lexical retroaction strength

        :param val: input value to the sigmoid function (generally the value of the lexical decision distribution)
        :return: the top-down lexical retroaction strength
        """
        pass
        return 2e-6 + 1 * (self.gamma_ratio / np.power((1. + np.exp(-(97 * val) + 95)), .3))

    def gamma(self):
        self.dist["gamma"] = self.sigm(self.dist["ld"][0])

    def update_word(self):
        other_mod = self.modality.model.phono
        if other_mod.enabled:
            super().update_word(other_mod.word.dist)

    #################################
    #### INFO #######################
    #################################

    def print_dist(self, dist_name):
        return dist_name + " ortho : " + str(super().print_dist(dist_name))


class _WordPhono(_Word):
    def __init__(self, modality, top_down=True, gamma_ratio=5e-2, ld_thr=0.8, **modality_args):
        super().__init__(modality=modality, top_down=top_down, gamma_ratio=gamma_ratio, ld_thr=ld_thr, **modality_args)

    #################################
    #### INFERENCES #################
    #################################

    def build_similarity(self):
        wtrans = utl.build_word_transition_vector(self.dist["word"], self.modality.lexical.freq[:self.modality.lexical.shift_begin], self.modality.lexical.leak)
        wsim = utl.wsim(self.modality.lexical.repr[:self.modality.lexical.shift_begin], self.modality.percept.dist["percept"])
        self.dist["word_sim"] = np.array(wtrans)[:, np.newaxis] * wsim
        if self.new_ld:
            anti_diag = np.array([[0 if i == j else 1 for j in range(self.modality.n)] for i in range(self.modality.n)])
            anti_diag = np.repeat(anti_diag[np.newaxis, :], self.modality.M, axis=0)
            # normalisation here doesn't change anything
            mh_matrix = [utl.norm2D(i, n=1) for i in anti_diag * self.modality.percept.dist["percept"][:, np.newaxis]]
            err_n = utl.norm2D(np.sum(mh_matrix * self.modality.percept.dist["percept"][:, np.newaxis], axis=2), n=1)
            err = [[err_n[j] if i == j else self.modality.percept.dist["percept"][i] for j in range(self.modality.M)] for i in range(self.modality.M)]
            err_n = np.sum(np.repeat(wtrans[:, np.newaxis], self.modality.M, axis=1) * np.prod(np.einsum('kij,ilj->kil', self.modality.lexical.repr[:self.modality.lexical.shift_begin], err), axis=1), axis=0)
            self.dist["err_n"] = np.max(err_n)
            prod = np.prod(np.einsum('kij,ij->ki', self.modality.lexical.repr[:self.modality.lexical.shift_begin], self.modality.percept.dist["percept"]), axis=1)
            self.dist["sim_n"] = (wtrans * prod).sum()

    def sigm(self, val):
        """
        Calculates the top-down lexical retroaction strength

        :param val: input value to the sigmoid function (generally the value of the lexical decision distribution)
        :return: the top-down lexical retroaction strength
        """
        return 2e-6 + 1 * (self.gamma_ratio / np.power((1. + np.exp(-(97 * val) + 95)), .3))

    def gamma(self):
        self.dist["gamma"] = self.sigm((1 if self.word_reading else self.dist["ld"][0]))

    def update_word(self):
        other_mod = self.modality.model.ortho
        if other_mod.enabled:
            super().update_word(other_mod.word.dist)

    #################################
    #### INFO #######################
    #################################

    def print_dist(self, dist_name):
        return dist_name + " phono : " + str(super().print_dist(dist_name))
