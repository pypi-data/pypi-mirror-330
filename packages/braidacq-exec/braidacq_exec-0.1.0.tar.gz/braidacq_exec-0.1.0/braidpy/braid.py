# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:41:03 2020

@author: Alexandra, Ali
"""

# General purpose libraries
import os
import logging
from time import time
import pdb

# Scientific/Numerical computing
import pandas as pd
import numpy as np

# BRAID-Acq
import braidpy.modality as mod
import braidpy.semantic as sem
import braidpy.color as col
import braidpy.lexicon as lex

from braidpy import _ROOT


class braid:
    """ instantaneous BRAID model : Inner class of the Simu class"""

    def __init__(self, ortho_param, phono_param, semantic_param, color_param, langue="fr", lexicon_name="",
                 iteration_type="reading", set_graphemic_segmentation=False):
        """
        :param ortho_param: dict, parameters for the inner class
        :param phono_param: dict, parameters for the inner class
        :param semantic_param: dict, parameters for the inner class
        :param color_param: dict, parameters for the stroop extension
        :param langue : string, among "en" ,"fr" or "ge"
        :param lexicon_name: string, lexicon filename (abcdef.csv)
        :param iteration_type : string, among "reading", "spelling".
        """
        if ortho_param is None:
            ortho_param = {}
        if phono_param is None:
            phono_param = {}
        if semantic_param is None:
            semantic_param = {}
        if color_param is None:
            color_param = {}
        self.ortho_param_names = ['Q', 'QL', 'stim', 'eps', 'top_down', 'leak', 'crowding', 'scaleI', 'slopeG', 'segm',
                                  'gamma_ratio', 'att_factor', 'markov_sim', 'mean', 'gaze',
                                  'force_app', 'force_update', 'force_word', 'ld_thr', 'new_ld', 'sd', 'grapheme_overlap']
        self.phono_param_names = ['Q', 'leak', 'use_word', 'placement_auto', 'ld_thr', 'att_phono_auto', 'gamma_deb', 'sd']
        self.color_param_names = ['stim_color', 'alpha_color', 'alpha_wcolor']
        self.langue, self.lexicon_name = langue, lexicon_name
        self.init_model_args()

        # current length, corresponding phonoeme length (max), theoritical max length of stimulus
        self.df_lemma = pd.read_csv(os.path.join(_ROOT, 'resources/lexicon/Lexique_lemma.csv'))[['word', 'lemme']].set_index(
            'word') if self.remove_lemma else None
        if set_graphemic_segmentation:
            self.set_graphemic_segmentation(calc_complexity=True)
        self.df_graphemic_segmentation = pd.read_csv(os.path.join(_ROOT, 'resources/lexicon/graphemic_segmentation_corrected_lexique_fr.csv')).groupby('word').first()
        self.stim_graphemic_segmentation = {}
        self.max_len = {}
        self.dist_names = ["percept", "word", "ld", "gamma", "TD_dist", "TD_dist_sem", "word_sim_att"]
        self.color = col.color(dist={"color_words": None}, model=self, **color_param)
        self.phono = mod._Phono(mod="phono", other_mod="ortho", model=self, dist={key: None for key in self.dist_names}, **phono_param)
        self.ortho = mod._Ortho(mod="ortho", other_mod="phono", model=self, dist={key: None for key in self.dist_names}, **ortho_param)
        self.set_df_other_modality()
        self.verify_chars()
        if set_graphemic_segmentation:
            self.set_graphemic_segmentation_partial()
        self.semantic = sem.semantic(model=self, **semantic_param)
        if self.color.enabled:
            self.color.set_color_dict()
        if self.phono.enabled and self.ortho.enabled:
            self.phono.attention.set_regression()
        self.ortho.stim = ortho_param['stim'] if 'stim' in ortho_param else self.ortho.stim  # on le définit que maintenant pour pouvoir avoir accès au stim phono correspondant
        self.iteration_type = iteration_type
        self.mismatch = False
        self.PM = None
        self.chosen_modality = None

    def init_model_args(self):
        """
        This function initializes various attributes to their default values for the model.
        """
        self.old_freq = None
        self.PM = False
        self.chosen_modality = None
        self.mismatch = False
        self.store_all_repr = False  # not working

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, value):
        new = 'shift' in self.__dict__ and self._shift != value
        self._shift = value
        if new and 'ortho' in self.__dict__:
            self.start()

    def enable_phono(self, value):
        """
        This function enables or disables phonological processing and updates the lexical knowledge accordingly.

        :param value: boolean value that determines whether the "phono" feature is enabled or disabled.
        """
        self.phono.enabled = value
        if value and self.df is not None:
            self.phono.lexical.build_all_repr()
            if self.ortho.N is not None:
                self.phono.lexical.set_repr()
        else:
            self.phono.all_repr = None
            self.phono.repr = None

    def __getattr__(self, name):
        """
        Getter that also checks if the attribute is in the ortho/phono class and returns it if it is.

        :param name: variable that contains the name of the attribute that is being accessed.
        :return: If the attribute name is found in the model class, it's returned. If it's in `ortho_param_names` or `phono_param_names`, the corresponding attribute value from the `ortho` or
        `phono` object is returned using the `__getattribute__` method. Otherwise, an `AttributeError` will be raised.
        """
        if 'ortho_param_names' in self.__dict__ and name in self.ortho_param_names:
            return self.ortho.__getattribute__(name)
        elif 'phono_param_names' in self.__dict__ and name in self.phono_param_names:
            return self.phono.__getattribute__(name)

    def __getstate__(self):
        # necessary to use pkl because getattr is overwritten
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __setattr__(self, name, value):
        """
        This function allows for setting attributes in the model/ortho/phono classes by checking if the attribute is in the ortho or phono class.

        :param name: The name of the attribute being set
        :param value: The value that is being set for the attribute named 'name'.
        on the attribute being set
        """
        if 'ortho_param_names' in self.__dict__ and name in self.ortho_param_names:
            self.ortho.__setattr__(name, value)
        elif 'phono_param_names' in self.__dict__ and name in self.phono_param_names:
            self.phono.__setattr__(name, value)
        elif 'color_param_names' in self.__dict__ and name in self.color_param_names:
            self.color.__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    ################## INIT METHODS #################################

    def set_lexicon_name(self, phono_enabled):
        """
        Automatically sets the lexicon name according to the language.

        :param phono_enabled: boolean
        """
        if len(self.langue) == 0:
            self.langue = "en"
        if len(self.lexicon_name) == 0:
            if self.langue == "en" and self.color.enabled and phono_enabled:
                self.lexicon_name = "celex_wcolor_freq.csv"
            elif self.langue == "en":
                self.lexicon_name = "lexicon_CDP.csv" if phono_enabled else "ELP.csv"
            elif self.langue == "ge":
                self.lexicon_name = "celex_german.csv"
            elif self.langue == "sp":
                self.lexicon_name = "lexique_espagnol.csv"
            else:
                self.lexicon_name = "lexique_fr.csv" if phono_enabled else "FLP.csv"
        logging.simu(f"""\t Lexicon loaded! \t name: {self.lexicon_name} """)

    def get_joint_lexicon(self):
        """
        Gets the lexicon dataframe containing both the ortho and phono modalities, from the separate lexicon dataframes in each modality.
        :return: the joint dataframe
        """
        df_o = self.ortho.lexical.df.reset_index().rename(columns={'store': 'store_ortho'})
        df_p = self.phono.lexical.df.reset_index().rename(columns={'word': 'pron', 'freq': 'freq_phon', 'len': 'ph_len', 'store': 'store_phono'})
        return df_o.merge(df_p, on=['len_class', 'idx'])

    def verify_chars(self):
        """
        Verifies in each modality that the lexicon does not contain unauthorized characters.
        """
        self.ortho.lexical.verify_chars()
        self.phono.lexical.verify_chars()

    def set_df_other_modality(self):
        """
        Defines the field "other modality" in the ortho and phono dataframes, as "ortho" for the phono dataframe and vice versa.
        """
        df_ortho = self.ortho.lexical.df.reset_index()[['idx', 'len_class', 'word']].rename(columns={'word': 'other_modality'})
        df_phono = self.phono.lexical.df.reset_index()[['idx', 'len_class', 'word']].rename(columns={'word': 'other_modality'})
        self.ortho.lexical.df = pd.merge(self.ortho.lexical.df.reset_index(), df_phono, on=['idx', 'len_class'], how='left').set_index('word')
        self.phono.lexical.df = pd.merge(self.phono.lexical.df.reset_index(), df_ortho, on=['idx', 'len_class'], how='left').set_index('word')

    def set_graphemic_segmentation(self, calc_complexity=False):
        """
        loads and transforms the graphemic segmentation data
        """
        complete_name = os.path.join(_ROOT, 'resources/lexicon/Lexique_infra.csv')
        # May keep multiple phonemes for the same orthography and will select the most frequent one using freq
        gs = pd.read_csv(complete_name, keep_default_na=False)[['word', 'pron', 'gpmatch']].groupby(
            ['word', 'pron']).first().reset_index()
        lx = pd.read_csv(os.path.join(_ROOT, 'resources/lexicon/Lexique_lemma.csv'))
        # only one per word-phon, we take the one with the highest frequency, no sum because we need to associate a unique lemma
        lx = lx[lx.groupby(['word'])['freq'].transform(max) == lx['freq']]
        gs = gs.merge(lx, on=['word', 'pron'], how='inner').set_index('word')
        gs = gs[(~gs.index.str.contains('\.')) & (gs.index.str.len() > 1)]
        # we keep only the rows where the pronunciation matches
        gs['segm'] = gs['gpmatch'].apply(lambda s: ".".join([str(i.split('-')[0]) for i in s.split('.') if len(i) > 2]))
        gs['pseg'] = gs['gpmatch'].apply(lambda s: ".".join([str(i.split('-')[1]) for i in s.split('.') if len(i) > 2]))
        self.graphemic_segmentation = lex.correct_graphemic_segmentation(gs, new_phoneme=False, calc_complexity=calc_complexity)
        self.graphemic_segmentation = self.graphemic_segmentation[self.graphemic_segmentation.pb_longueur == False]
        # calculate the graphemic consistency scores
        if calc_complexity:
            self.graphemic_segmentation.to_csv(
                os.path.join(_ROOT, 'resources/lexicon/graphemic_segmentation_corrected_calc_complexity.csv'))
        else:
            self.graphemic_segmentation.to_csv(os.path.join(_ROOT, 'resources/lexicon/graphemic_segmentation_corrected.csv'))

    def set_graphemic_segmentation_partial(self):
        """
        Excludes all items from the graphemic segmentation database if they are not part of the model's lexicon.
        """
        self.graphemic_segmentation[self.graphemic_segmentation.index.isin(self.ortho.lexical.df.index)].to_csv(os.path.join(_ROOT, 'resources/lexicon/graphemic_segmentation_corrected_lexique_fr.csv'))

    ################# INIT MODEL CONFIGURATION FOR SIMU #########################

    def reset_model(self, reset):
        """
        init top down and bottom up information in each modality.
        """
        self.semantic.build_context()  # fait avant pour que l'init de sem se passe bien
        self.ortho.reset_modality(reset)
        self.phono.reset_modality(reset)
        if self.color.enabled:
            self.color.init_color()

    def change_freq(self, newF=1, string=""):
        """
        Artificially changes the frequency of a word (for the freq effect simulation)
        """
        string = string if len(string) > 0 else self.stim
        self.ortho.lexical.change_freq(newF, string)
        phono_string = self.phono.lexical.get_phono_name(string)
        self.phono.lexical.change_freq(newF, phono_string)

    ########### MAIN #########################

    def one_iteration(self):
        """ One iteration of the simulation """
        self.ortho.build_modality()
        self.phono.build_modality()
        if self.color.enabled:
            self.color.color_bottom_up()
        self.ortho.update_modality()
        self.phono.update_modality()

    ###################### UPDATE AFTER SIMU #######################

    def detect_mismatch(self):
        """
        Detects a mismatch between the orthographic percept and the orthographic representation corresponding to the phonological word identified
        """
        idx = self.phono.word.decision("word_index")
        dec_repr = self.ortho.lexical.repr[idx]
        p = self.ortho.percept.dist["percept"]
        if sum(sum(dec_repr)) > 0:
            sim = np.prod(np.einsum('ij,ij->i', dec_repr, p))
            sim_repr = np.prod(np.einsum('ij,ij->i', dec_repr, dec_repr))
            sim_p = np.prod(np.einsum('ij,ij->i', p, p))
            return sim / (sim_repr * sim_p) < 0.5

    def PM_decision_global(self):
        """
        Decisions at the end of the simulation :
        lexical membership evaluation according to the evaluation in the 2 modalities + modality choice + most probable word (in the chosen modality)
        """
        if self.phono.enabled:
            self.PM = True if self.ortho.word.PM and self.phono.word.PM else False
            # known in both modalities
            if not self.ortho.word.PM and not self.phono.word.PM:
                # chosen according to the most reliable modality
                self.chosen_modality = "phono" if max(self.phono.word.dist["word"]) > max(self.ortho.word.dist["word"]) else "ortho"
            # known in at least one modality
            elif not self.ortho.word.PM or not self.phono.word.PM:
                # if identification in one modality, checks if there is an existing lexical trace in the other modality (even if word not recognized)
                self.chosen_modality = "phono" if self.ortho.word.PM else "ortho"
                data = getattr(self, self.chosen_modality)
                other_data = getattr(self, data.other_mod)
                idx = data.word.decision("word_index")
                if sum(sum(other_data.lexical.repr[idx])) > 0:
                    other_data.word.PM = False
            # known in no modality
            else:
                self.chosen_modality = "phono"
            # only phon. known
            if self.ortho.word.PM and not self.phono.word.PM:
                # if the word is phonologically known, verification that the letter percept is not incoherent with an eventual existing ortho representation
                mismatch = self.detect_mismatch()
                if mismatch:
                    logging.simu('/!\ Lexicalisation probable')
                    self.mismatch = self.ortho.word.PM = self.phono.word.PM = self.PM = True
                    self.chosen_modality = None
                else:
                    self.mismatch = False
        else:
            self.PM = self.ortho.word.PM
            self.chosen_modality = "ortho"
        idx = getattr(self, self.chosen_modality).word.decision("word_index") if self.chosen_modality is not None else -1
        self.ortho.word.chosen_word = self.ortho.lexical.get_name(idx) if idx >= 0 else ""  # identification in the chosen modality
        self.phono.word.chosen_word = self.phono.lexical.get_name(idx) if idx >= 0 else ""  # identification in the chosen modality
        self.chosen_word = self.ortho.word.chosen_word if self.chosen_modality == "ortho" else self.phono.word.chosen_word
