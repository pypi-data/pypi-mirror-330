# General purpose libraries
import logging
import pdb

# Scientific/Numerical computing
import numpy as np
import pandas as pd

# BRAID
import braidpy.utilities as utl
import braidpy.sensor as sens
import braidpy.lexical as lxc
import braidpy.percept as per
import braidpy.attention as att
import braidpy.word as wrd


class _Modality:
    """
    The _Modality class is an inner class of the model class and represents either an orthographic or phonological modality.
    """

    def __init__(self, model, mod, other_mod, enabled=True, stim=None, limited_TD=True, **modality_args):
        """
        :param model : braid model instance
        :param enabled : boolean. if True, the modality is 'activated'
        :param mod : string. the class modality (orthographic or phonological)
        :param other_mod : string. the other modality than the class (orthographic or phonological)
        :param stim : string corresponding to the stimulus
        :param limited_TD : boolean. if True, only the first 50 representations are used to calculate top-down, to limit calculation cost.
    """
        self.param = {}
        self.param["sensor"] = ['gaze', 'conf_mat_name']
        self.param["percept"] = ['leak', 'top_down', 'q', 'gamma_deb']
        self.param["word"] = ['leakW', 'L2_L_divison', 'ld_thr', 'word_reading', 'new_ld']
        self.param["lexical"] = ['gamma_ratio', 'eps', 'learning', 'remove_stim', 'force_app', 'force_update', 'force_word', 'fMin', 'fMax',
                                 'store', 'log_freq', 'cat', 'maxItem', 'maxItemLen', 'lenMin', 'lenMax', 'remove_neighbors', 'remove_lemma', 'mixture_knowledge', 'shift']
        self.param["attention"] = ['Q', 'QL', 'sd', 'sdM', 'mean', 'att_phono_auto', "grapheme_overlap"]
        # extraction of the parameters for each inner class
        self.inner_class_param = {inner: {key: value for key, value in modality_args.items() if key in self.param[inner]} for inner in
                                  ["sensor", "percept", "word", "lexical", "attention"]}
        self.desactivated_inferences = {"build": [], "update": []}

        self.model = model
        self.mod = mod
        self.other_mod = other_mod
        self.enabled = enabled
        self._stim = stim
        self.n = None
        self.N = self.M = None
        self.removed_words = None
        self.limited_TD = limited_TD

    @utl.abstractmethod
    def __contains__(self, item):
        return False

    @property
    def stim(self):
        return self._stim

    @stim.setter
    @utl.abstractmethod
    def stim(self, value):
        pass

    @utl.abstractmethod
    def get_pos(self):
        pass

    def __setattr__(self, name, value):
        """
        This function allows for setting attributes in the inner classes of class modality by checking if the attribute is in the corresponding class

        :param name: The name of the attribute being set
        :param value: The value that is being set for the attribute named 'name'.
        """
        if 'param' in self.__dict__:
            for inner_class, params in self.param.items():
                if name in params and inner_class in self.__dict__:
                    getattr(self, inner_class).__setattr__(name, value)
                    return
        super().__setattr__(name, value)

    ############################
    ##### INIT #################
    ############################

    def reset_modality(self, reset):
        """
        Resets all model's modal attributes

        :param reset: dictionary that contains two keys: "lexicon" and "dist". The value associated with each key determines whether to reset the lexicon or the distributions
        """
        if reset["lexicon"]:
            self.lexical.build_all_repr()
        self.lexical.set_repr()  # needed for reset_dist et build_context
        if reset["dist"]:
            self.percept.dist["percept"] = self.lexical.get_empty_percept()
            self.word.dist["ld"] = np.array([0.5, 0.5])
            self.word.dist["gamma"] = 0
            self.percept.dist["gamma"] = 0
            self.percept.dist["gamma_sem"] = 0
            self.percept.dist["gamma_sim"] = 0
            self.word.dist["word"] = utl.norm1D(self.lexical.freq[:self.lexical.shift_begin])
            self.word.dist["word_sim"] = utl.wsim(self.lexical.repr[:self.lexical.shift_begin], self.percept.dist["percept"])
            self.word.dist["word_sim_att"] = utl.norm1D(self.lexical.freq)
            self.percept.used_idx, self.percept.used_idx_tmp, self.percept.used_mask = {key: [] for key in range(30)}, [], []
        self.model.semantic.gamma_sem_init = np.dot(self.word.dist["word"], self.model.semantic.dist['sem'])
        self.build_bottom_up()  # needs position to be set before
        self.reset_inferences()

    @utl.abstractmethod
    def reset_inferences(self):
        pass

    ######################################
    ######## INFERENCES ##################
    ######################################

    ########## Bottom-up Inferences #####

    def build_bottom_up(self):
        """
        Builds the bottom-up matrix according to the interference matrix and the attention distribution
        """
        self.sensor.build_interference_matrix()
        self.attention.build_attention_distribution()
        if self.attention.mean >= 0 and self.sensor.dist["interference"] is not None and self.attention.dist is not None:
            self.percept.bottom_up_matrix = [i * a + (1 - a) / self.n for (i, a) in zip(self.sensor.dist["interference"], self.attention.dist)]

    def build_modality(self):
        """
        Calculates bottom-up inferences
        """
        if self.enabled:
            if 'sensor' not in self.desactivated_inferences['build']:
                self.sensor.build_sensor()
            if 'percept' not in self.desactivated_inferences['build']:
                self.percept.build_percept()
            if 'decoding' not in self.desactivated_inferences['build']:
                self.percept.build_decoding()
            if 'similarity' not in self.desactivated_inferences['build']:
                self.word.build_similarity()
            if 'word' not in self.desactivated_inferences['build']:
                self.word.build_word()
            if 'ld' not in self.desactivated_inferences['build']:
                self.word.build_ld()

    ########## Top-Down Inferences #####

    def update_modality(self):
        """
        Calculates top-down inferences
        """
        if self.enabled:
            self.word.gamma()
            self.percept.gamma()
            if 'word' not in self.desactivated_inferences['update']:
                self.word.update_word()
            if 'percept' not in self.desactivated_inferences['update']:
                self.percept.update_percept()
            if 'percept_sem' not in self.desactivated_inferences['update']:
                self.percept.update_percept_sem()
            if 'word_sem' not in self.desactivated_inferences['build']:
                self.word.build_word_sem()
            if 'word_color' not in self.desactivated_inferences['build']:
                self.word.build_word_color()

    ######################################
    ######### RESULT #####################
    ######################################

    def print_all_dists(self):
        """
        Prints out information about all distributions (ld,percept,word).
        """
        if self.enabled:
            logging.simu(f"\n {self.mod.upper()} : mot {'non' if self.word.PM else ''} reconnu")
            logging.simu(self.percept.print_dist())
            logging.simu(self.word.print_dist('ld'))
            logging.simu(self.word.print_dist("word"))
            logging.simu(self.word.print_dist("word_stim"))
            logging.simu(self.percept.print_dist("gamma"))

    @utl.abstractmethod
    def detect_context_error(self):
        """
        Detects a context error (word identified in the context, but not the stimulus).

        :return: a boolean value.
        """
        dec = self.word.decision("word")
        return (not self.word.PM or self.model.mismatch) and dec != self.stim and dec in self.semantic.context_sem_words and self.stim not in self.semantic.context_sem_words

    def get_dirac(self, string=None):
        """
        Returns the maximum value of the distribution on each letter/phoneme for a given stimulus.

        :param string: The input word. If it is None, the function calculates the distribution for the current model stimulus.
        :return: a list of maximum values of the distribution `P(Li|W=string)` if the word is known, `P(Pi)` if it's novel, for each letter position `i`.
        """
        if not self.enabled or self.word.PM or (string not in self):
            p = self.percept.dist["percept"]
            return [round(max(i), 3) for i in p] if p is not None else None
        else:
            idx = self.lexical.get_word_entry().idx if string is not None else self.decision("word_index")
            wd = self.lexical.repr[idx]
            return [round(max(i) / sum(i), 3) for i in wd]


class _Ortho(_Modality):
    def __init__(self, stim="choisir", **modality_args):
        """
        :param stim: visual stimulus
        :param modality_args: additional parameters
        """
        super().__init__(stim=stim, **modality_args)

        # submodels in the orthographic branch
        self.sensor = sens.sensorOrtho(self, **self.inner_class_param['sensor'])
        self.percept = per.perceptOrtho(self, **self.inner_class_param['percept'])
        self.attention = att.attentionOrtho(self, **self.inner_class_param['attention'])
        self.lexical = lxc._LexicalOrtho(self, **self.inner_class_param['lexical'])
        self.word = wrd._WordOrtho(self, **self.inner_class_param['word'])
        self.desactivated_inferences = {"build": ["decoding"], "update": []}

    def __contains__(self, item):
        """
        Return True if the item is in the lexicon and its orthography is known
        """
        if item not in self.lexical.df.index:
            return False
        ortho = self.lexical.df.loc[item].ortho
        return any(ortho) if isinstance(ortho, pd.Series) else ortho

    @_Modality.stim.setter
    def stim(self, value):
        """
        Setter for the variable 'stim' with all associated actions :
        - sets the stimulus name in both modalities
        - calculates forbid entries for the current stimulus
        - build bottom-up information
        - affects the new value for the phonological length (N)
        - extracts the graphemic segmentation when it is known
        """
        if value is not None:
            self._stim = value if isinstance(value, str) else ""
            if len([i for i in self._stim if i not in self.lexical.chars]):
                raise ValueError("Invalid stimulus name")
            # On affecte N et M dans les 2 modalités pour plus de simplicité
            self.N = len(self._stim)
            if self.lexical.shift:
                self.lexical.shift_begin = self.lexical.all_shift_begin[self.N]
            if self.model.remove_neighbors or self.model.remove_lemma:
                self.forbid = self.model.ortho.get_forbid_entries()
            try:
                self.build_bottom_up()
            except:
                pass
            if 'phono' in self.model.__dict__ and self.model.phono.enabled and self.model.phono.lexical.df is not None:
                try:
                    self.model.phono.N = self.N
                    if self.model.phono.lexical.shift:
                        self.model.phono.lexical.shift_begin = self.lexical.all_shift_begin[self.N]
                    self.model.phono.M = 0 if len(self.model.max_len) == 0 else self.model.max_len[len(self.model.ortho.stim)]
                    self.M = self.model.phono.M
                    self.model.phono.stim = self.model.phono.lexical.get_phono_name()
                    if len(self.model.phono.stim) == 0:
                        print("Phono stim could not be set!")
                    if self.model.phono.stim is not None:
                        try:
                            raw = self.model.df_graphemic_segmentation.loc[value]
                            # theoritical phonological position for each ortho position
                            self.model.gs = "".join([len(val) * str(i) for i, val in enumerate(raw['segm'].split('.'))])
                        except:
                            pass
                    self.model.phono.attention.position_mapping(self.model.ortho.pos)
                    self.model.phono.attention.dispersion_mapping(self.model.ortho.attention.sd)
                    self.model.phono.attention.build_attention_distribution()
                except:
                    print("Phono stim could not be set!")
                    self.model.phono.stim = ""
                    self.model.phono.M = 0
                    self.model.phono.N = self.N

    @property
    def pos(self):
        return self.attention.mean

    @pos.setter
    def pos(self, value):
        """
        Sets attention and eye position, starts at 0. Position should be set at -1 at the end of a simulation

        :param: value: int, the position to be set.
        """
        if value < -1 or (self.N is not None and value >= self.N):
            logging.warning(f"bad ortho position is trying to be set : {value} {self.N}")
        self.attention.mean = value
        self.sensor.gaze = value
        self.build_bottom_up()

    ############################
    ##### INIT #################
    ############################

    def reset_inferences(self):
        """
        Sets inferences that are not used during calculation.
        """
        if self.model.iteration_type == "reading":
            self.desactivated_inferences = {"build": ["decoding"], "update": []}

    def detect_context_error(self):
        """
        Detects a context error (word identified in the context, but not the stimulus).

        :return: a boolean value.
        """
        dec = self.word.decision("word")
        return (not self.word.PM or self.model.mismatch) and dec != self.stim and dec in self.model.semantic.context_sem_words_phono and self.stim not in self.model.semantic.context_sem_words


class _Phono(_Modality):
    def __init__(self, **modality_args):

        super().__init__(**modality_args)
        self.model.set_lexicon_name(self.enabled)  # needs to know if phono is enabled to choose the lexicon name
        self.sensor = sens.sensorPhono(self, **self.inner_class_param['sensor'])
        self.percept = per.perceptPhono(self, **self.inner_class_param['percept'])
        self.attention = att.attentionPhono(self, **self.inner_class_param['attention'])
        self.lexical = lxc._LexicalPhono(self, **self.inner_class_param['lexical'])
        self.word = wrd._WordPhono(self, **self.inner_class_param['word'])
        self.desactivated_inferences = {"build": ["sensor", "percept"], "update": []}

    def __contains__(self, item):
        """
        If the item is in the lexicon, and the item has a phonological representation, then return True

        :param item: the word to be checked
        :return: The word entry for the word in the lexicon.
        """
        lx = self.lexical.df
        return item in lx.index.values and self.lexical.get_word_entry(item).store == True

    @_Modality.stim.setter
    def stim(self, value):
        """
        Stim setter, only used by the ortho setter to set the corresponding stim
        """
        self._stim = value

    @property
    def pos(self):
        return self.attention.mean

    @pos.setter
    def pos(self, value):
        """
        Sets attention position, starts at 0. Position should be set at -1 at the end of a simulation

        :param value: int, the position to be set.
        """
        if value < -1 or (self.M is not None and value >= self.M):
            logging.warning(f"bad phono position is trying to be set : {value} {self.M}")
        self.attention.mean = value
        self.sensor.gaze = value
        self.build_bottom_up()

    ############################
    ##### INIT #################
    ############################

    def reset_inferences(self):
        """
        Sets inferences that are not used during calculation.
        """
        if self.model.iteration_type == "reading":
            self.desactivated_inferences = {"build": ["sensor", "percept"], "update": []}

    ######################################
    ######### RESULT #####################
    ######################################

    def print_all_dists(self):
        """
        Prints all probability distributions.
        """
        super().print_all_dists()
        if self.enabled:
            logging.simu(f"Psi score : {self.percept.psi_score()}")
            logging.simu(f"Pron first pass : {self.percept.pron_first_pass}")

    def detect_context_error(self):
        """
        Detects a context error (word identified in the context, but not the stimulus).

        :return: a boolean value.
        """
        dec = self.word.decision("word")
        return (not self.word.PM or self.model.mismatch) and dec != self.stim and dec in self.model.semantic.context_sem_words_phono and self.stim not in self.model.semantic.context_sem_words_phono
