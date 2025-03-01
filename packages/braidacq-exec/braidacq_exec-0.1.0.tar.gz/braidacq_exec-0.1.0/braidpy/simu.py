# -*- coding: utf-8 -*-
# General purpose libraries
import copy
import heapq
# Scientific/Numerical computing
import math
import os
import pdb
import logging
import pickle as pkl
from time import time

import numpy as np
from scipy.stats import entropy

# BRAID utlities
import braidpy.braid as braid
import braidpy.utilities as utl

# on désactive le mode debug de numba et numpy
from braidpy import detect_errors
from braidpy import _ROOT


# décorateurs des simulations individuelles

def generic_simu(func):
    def wrapper(self, *args, **kwargs):
        deb_simu = time()
        self.begin_simu()
        _ = func(self, *args, **kwargs)
        self.end_simu()  # formater les distributions dans un format facilement utilisable
        logging.simu(f"Simulation time: {time() - deb_simu}")
    return wrapper


def learning(func):
    def wrapper(self, *arg, **kw):
        res = func(self, *arg, **kw)
        if self.model.ortho.lexical.learning or self.model.phono.lexical.learning:
            self.model.ortho.lexical.learn()
            self.model.phono.lexical.learn()
            if self.mu and self.model.PM:  # seulement dans le cas où on ajoute une nouvelle trace ortho
                self.model.phono.lexical.learn_shift()
                self.model.ortho.lexical.learn_shift()
        return res
    return wrapper


class simu:
    """ Simulation context, includes model, simulation parameters and the outputs """

    def __init__(self, model_param=None, ortho_param=None, phono_param=None, semantic_param=None, color_param=None, simu_args=None,
                 level='simu', build_prototype=False, max_iter=3000, t_min=100, simu_type="H", thr_expo=0.30, segment_reading=False,
                 stop_criterion_type="phiMax", fixation_criterion_type="phono", pos_init=-1, reading_unit="None", mu=False, regression=True, transition_saccadic=False):
        """
        Object constructor, simulation context initiator

        Args:
            model_param, ortho_param, phono_param, semantic_param, color_param : dict, parameters for inner classes
            simu_args : dictionary of optional parameters for the simulation
            level : string, level for the logging package, among simu,expe,debug
            build_prototype : boolean, if True, build the prototype from the simulation file
            max_iter: int, number of iterations
            t_min : int, minimum number of iterations for a fixation
            simu_type : string, simulation type among normal, threshold, H, change_pos
            thr_expo : float, threshold for the end of the exposure (mean entropy on letters or phonemes)
            segment_reading : boolean. If True, word read by segment corresponding to either grapheme/letter (unit given by the reading_unit parameter)
            stop_criterion_type : for simulations with a termination criterion, like simu_H, criterion type to end the exposure
            fixation_criterion_type : str, "ortho" or "phono". Type of criterion to move on to the next fixation.
            pos_init : float, initial position of the attention. if set to -1, let the model decide
            reading_unit : string, among "letter", "grapheme", "bigram", "trigram" or "None". If "None", next position is chosen according to entropy. If "letter" or "phoneme", the next unit in the word is chosen.
            mu : boolean. If True, adding new lexical representations padded with 'mu'
            regression : boolean. If True, regressions (next position < current position) are authorized.
            transition_saccadic : boolean. If True, transition saccadic time is implemented, with no visual input during a certain amount of time.
        """

        if model_param is None:
            model_param = {}
        self.model = braid.braid(ortho_param, phono_param, semantic_param, color_param, **model_param)
        self.simu_args = simu_args if simu_args is not None else {}
        logging.basicConfig(format='%(levelname)s - %(message)s')
        self.level = level
        self.max_iter = max_iter
        self.t_min = t_min
        self.simu_type = simu_type
        self.thr_expo = thr_expo
        self.thr_expo_phono = 1.0 * thr_expo
        self.segment_reading = segment_reading
        self.stop_criterion_type = stop_criterion_type
        self.fixation_criterion_type = fixation_criterion_type
        self.pos_init = pos_init
        self.reading_unit = reading_unit
        self.init_simu_attributes()
        self.init_res()
        self.store_dist = {"ortho": [], "phono": []}
        self.mu = mu
        self.regression = regression
        self.transition_saccadic = transition_saccadic

    ############################
    ### Getters / Setters ######
    ############################

    def __setattr__(self, name, value):
        """
        This function allows for setting attributes in a model, ortho, or phono class.

        :param name: The name of the attribute being set
        :param value: The value that is being assigned to the attribute named "name". This is the value that will be stored in the attribute
        """
        if 'model' in self.__dict__ and ((name in self.model.__dict__ or '_' + name in self.model.__dict__) or
                                         ('ortho' in self.model.__dict__ and name in self.model.ortho_param_names) or
                                         ('phono' in self.model.__dict__ and name in self.model.phono_param_names)):
            self.model.__setattr__(name, value)
        # definition of simulation args here to facilitate the run of simulations with class expe
        elif name in ['thr_fix', 'alpha', 'n_choose_word']:
            self.simu_args[name] = value
        elif name in ['context_sem', 'context_identification', 'N_sem', 'p_sem', 'Q_sem']:
            self.model.semantic.__setattr__(name, value)
        elif name in ['stim_color', 'alpha_color', 'alpha_wcolor']:
            self.model.color.__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        """
        This function tries to get an attribute from the model class if not present in the simu class. Otherwise it raises an AttributeError.

        :param name: name of the attribute that is being accessed.
        :return: value of the attribute.
        """
        if 'model' in self.__dict__:
            return getattr(self.model, name)

    def __getstate__(self):
        """
        Redefinition of this function necessary to use the pkl package because getattr is overwritten (do not touch)
        """
        return self.__dict__

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        try:
            logging.getLogger().setLevel(getattr(logging, value.upper()))
        except:
            print("except")
            logging.basicConfig(level=getattr(logging, value.upper()), format='%(levelname)s - %(message)s')

    @property
    def segment_reading(self):
        return self._segment_reading

    @segment_reading.setter
    def segment_reading(self, value):
        self._segment_reading = value
        try:
            self.model.ortho.attention.segment_reading = value
            self.model.phono.attention.segment_reading = value
        except:
            print("Attentional modules undefined : cannot set property segment reading")

    @property
    def reading_unit(self):
        return self._reading_unit

    @reading_unit.setter
    def reading_unit(self, value):
        self._reading_unit = value
        try:
            self.model.ortho.attention.reading_unit = value
            self.model.phono.attention.reading_unit = value
        except:
            print("Attentional modules undefined : cannot set property serial reading")
    ############################
    ### Init of the simulation ##
    ############################

    def init_res(self):
        """
        Initializes the dictionary of results
        """
        self.res = {"ortho": {}, "phono": {}}
        for mod in ["phono", "ortho"]:
            modality = getattr(self.model, mod)
            perceptual_submodels = ['percept', 'word']
            for submodel_str in perceptual_submodels:
                submodel = getattr(modality, submodel_str)
                for key, value in submodel.dist.items():
                    self.res[mod][key] = []

    def init_attention(self):
        # ortho part
        self.model.ortho.attention.init_pos()
        self.model.ortho.attention.init_sd()
        self.model.ortho.attention.build_attention_distribution()
        # phono part
        self.model.phono.attention.position_mapping(self.model.ortho.pos)
        self.model.phono.attention.dispersion_mapping(self.model.ortho.attention.sd)
        self.model.phono.attention.build_attention_distribution()

    def init_removal(self):
        """
        Removes a stimulus from the orthographic and phonological representations when needed
        """
        self.model.ortho.lexical.remove_stim_repr()
        self.model.phono.lexical.remove_stim_repr()
        self.model.removed_stim = self.model.stim

    def init_simu_attributes(self):
        """
        Initializes various attributes for a simulation.
        """
        self.n_simu = 0
        self.error_type = "None"
        self.corrected = "None"
        self.pron_sans_corr = ""
        self.t_tot = 0
        self.model.mismatch = False
        self.model.chosen_modality = None
        self.model.phono.missing_letter = False
        self.reset = {"mean": True, "gazePos": True, "dist": True, "lexicon": False}
        if self.simu_type != "change_pos":
            self.fix = {mod: {key: [] for key in ["t", "att", "pos", "sd", "err"]} for mod in ["ortho", "phono"]}
        self.HPhonoDer = [1000 for _ in range(20)]
        self.t_local = 0
        self.model.phono.percept.pron_first_pass = ""

    def begin_simu(self):
        """
        Beginning of simulation common to all of simulation types
        """
        self.model.get_joint_lexicon()
        self.init_attention()
        self.init_removal()
        self.model.reset_model(self.reset)  # after removal ?
        self.init_res()
        self.init_simu_attributes()
        self.update_fix_info()
        self.complete_dist()

    ############################
    ### Results handling #######
    ############################

    def complete_dist(self):
        """
        Takes the current model distributions and adds them to the simulation results
        """
        for mod in ["phono", "ortho"]:
            modality = getattr(self.model, mod)
            perceptual_submodels = ['percept', 'word']
            for submodel_str in perceptual_submodels:
                if submodel_str in self.store_dist[mod]:
                    submodel = getattr(modality, submodel_str)
                    for key, value in submodel.dist.items():
                        if submodel_str != 'word' or key not in ['gamma', 'err_n', 'sim_n']:
                            self.res[mod][key] += [submodel.dist[key]]

    def update_fix_info(self):
        """
        Updates the fixation information (position, standard deviation, time, attention profile) for the orthographic and phonological modules
        """
        # remove the fixation if the orthographic position does not change
        if len(self.fix["ortho"]["pos"]) == 0 or (len(self.fix["ortho"]["pos"]) > 0 and self.fix["ortho"]["pos"][-1] != self.model.ortho.pos):
            self.fix['ortho']["pos"].append(self.model.ortho.pos)
            self.fix['ortho']["sd"].append(self.model.ortho.attention.sd)
            self.fix['ortho']["t"].append(self.t_tot)
            self.fix['ortho']["att"].append(self.model.ortho.attention.dist)
            if self.phono.enabled:
                self.fix["phono"]["pos"].append(self.model.phono.pos)
                self.fix["phono"]["att"].append(self.model.phono.attention.dist)
                self.fix['phono']["sd"].append(self.model.phono.attention.sd)
                if self.model.gs is not None:
                    self.fix["phono"]["err"].append(abs(int(self.model.gs[int(self.model.ortho.pos)]) - self.model.phono.pos))

    def delete_fixation(self, t):
        """
        Removes the last fixation from the stored result

        :param t: the number of fixations to delete
        """
        for mod in ["phono", "ortho"]:
            for name in self.model.dist_names:
                self.res[mod][name] = self.res[mod][name][:-max(t, 1)]
                # the state of the model must be the same as before the deleted fixations
                getattr(self.model, mod).dist[name] = self.res[mod][name][-1]
            for k, val in self.fix.items():
                self.fix[mod][k] = val[:-1]
        self.t_tot -= t
        logging.simu(f"fixation supprimée : {t} iterations")

    def increase_n(self):
        """
        Increases the number of simulations by one
        """
        self.n_simu += 1

    def reset_n(self):
        """
        Resets the number of simulations to zero
        """
        self.n_simu = 0

    ############################
    ### End of the simulation #######
    ############################

    def stopCriterion(self):
        """
         Detects if the creterion for the end of the exposure has been met
        """
        if self.stop_criterion_type == "pMax":
            return max(self.model.ortho.percept.get_entropy()) < self.thr_expo * math.log(self.model.ortho.n, 2)
        elif self.stop_criterion_type == "pMean":
            return np.mean(self.model.ortho.percept.get_entropy()) < self.thr_expo * math.log(self.model.ortho.n, 2)
        elif self.stop_criterion_type in ["phiMean", "pphiMean", "phiMax"]:
            if self.model.phono.enabled:
                dz_pos = self.model.phono.percept.get_dz_pos()
                # print(dz_pos)
                try:
                    Hunif = math.log(self.model.phono.n)
                    self.HPhonoDer = self.HPhonoDer[1:] + [self.model.phono.percept.max_HDer]
                    if "Mean" in self.stop_criterion_type:
                        c1 = dz_pos > 1 and np.mean(self.model.phono.percept.get_entropy()[:dz_pos]) < self.thr_expo * Hunif
                    elif "Max" in self.stop_criterion_type:
                        # print("Hunif",self.thr_expo*Hunif,"dz_pos",dz_pos,self.model.phono.percept.get_entropy()[:dz_pos])
                        c1 = dz_pos > 1 and np.max(self.model.phono.percept.get_entropy()[:dz_pos]) < self.thr_expo * Hunif
                except:
                    pdb.set_trace()
                if self.stop_criterion_type in ["phiMean", "phiMax"]:
                    return c1
            c0 = np.mean(self.model.ortho.percept.get_entropy()) < 0.25 * self.thr_expo * math.log(self.model.ortho.n, 2)
            return c0 or c1
        elif self.stop_criterion_type == "W":
            return self.model.ortho.word.get_entropy() > 0.04
        elif self.stop_criterion_type == "WPhi":
            return self.model.ortho.word.get_entropy() < 1 or self.derHPhonoW < 0.001
        elif self.stop_criterion_type == "ld":
            ld = self.model.ortho.word.dist["ld"][0]
            return ld < 0.1 or ld > self.model.ortho.ld_thr
        elif self.stop_criterion_type == "phono":
            return max(self.model.phono.dist["percept"][0]) > self.thr_expo
        elif self.stop_criterion_type == "phono_pos":
            return max(self.model.phono.dist["percept"][self.model.phono.pos]) > self.thr_expo

    def PM_decisions(self):
        """
        This function makes novelty decisions for the orthographic and phonological branches of the model and then makes a global decision based on both decisions.
        """
        # decision in each modality
        self.model.ortho.word.PM_decision()
        self.model.phono.word.PM_decision()
        # amodal decision
        self.model.PM_decision_global()

    def reshape_results(self):
        """
        This function reshapes the results for easier use.
        """
        for mod in ["ortho", "phono"]:
            for name in self.res[mod].keys():
                if len(self.res[mod][name]) > 0:
                    self.res[mod][name] = np.moveaxis(self.res[mod][name], 0, -1)

    def print_results(self):
        """
        Prints the results of the simulation. See the notebook one_word.ipynb for more information.
        """
        ex = self.model.phono.enabled and self.model.phono.stim
        logging.simu(f"stimulus {self.stim}, {self.model.phono.stim if ex else 'NO PHONO REPR'} {',f = ' + str(self.model.ortho.lexical.df.loc[self.stim].freq) if ex else ''}")
        if self.model.gs is not None:
            try:
                logging.simu(f"graphemic segmentation {self.model.df_graphemic_segmentation.loc[self.model.stim].gpmatch}")
            except:
                pass
        logging.simu(f"lexical status ortho: {'novel' if self.model.ortho.lexical.remove_stim else 'known'}")
        logging.simu(f"lexical status phono: {'novel' if self.model.phono.lexical.remove_stim else 'known'}")
        logging.simu(f"simulation duration : {self.t_tot}")
        if self.model.mixture_knowledge:
            if self.stim in self.model.ortho:
                tp = self.model.ortho.lexical.df.loc[self.stim].repr_type
                tp_str = 'expert' if tp == 0 else 'enfant' if tp == 1 else 'inconnu'
                logging.simu(f"type of ortho representation: {tp_str}")
        self.ortho.print_all_dists()
        self.phono.print_all_dists()
        logging.simu("\n IDENTIFICATION")
        logging.simu(f"chosen modality: {self.chosen_modality if self.chosen_modality is not None else 'None'}")
        if self.model.semantic.context_sem:
            if not self.PM:
                logging.simu(f"Context decision: known word {self.model.chosen_modality} {self.model.ortho.word.chosen_word}")
            else:
                logging.simu("Context decision: novel word")
        ident_type = self.model.chosen_modality if self.model.chosen_modality is not None else 'fusion' if self.model.fusion else 'phono'
        word_dec = self.model.phono.word.decision('word')
        if isinstance(word_dec, list):
            word_dec = word_dec[0]
        logging.simu(f"Identification {ident_type}: /{word_dec}/")
        logging.simu("\n SUCCESS ")
        if self.model.phono.enabled:
            if self.model.phono.percept.evaluate_decision():
                logging.simu("Psi Ok")
            else:
                logging.simu("Erreur Psi: " + self.error_type)
            if self.model.phono.percept.evaluate_decision(dist_name="pron_first_pass"):
                logging.simu("Psi first pass Ok")
        logging.simu("WFusion Ok" if self.success("wfusion") else "Erreur W Fusion")
        logging.simu("\n FIXATIONS")
        logging.simu(f"fixation times: {self.fix['ortho']['t']}")
        logging.simu(f"fixation positions : {self.fix['ortho']['pos']}")
        logging.simu(f"fixation dispersion : {self.fix['ortho']['sd']}")
        if self.model.phono.enabled:
            logging.simu(f"fixation phono positions : {self.fix['phono']['pos']}")
            logging.simu(f"errors phono positions : {self.fix['phono']['err']}")
            logging.simu("\n USED WORDS")
            for key, value in self.model.phono.percept.get_used_words().items():
                logging.simu(f"position {key}, {self.model.stim[key] if isinstance(key, int) else self.model.stim[int(key - 0.5):int(key + 1.5)]} \n words {value}")
            self.model.phono.percept.missing_bigram()
        logging.simu("\n")

    def end_simu(self):
        """
        This function ends a simulation : it changes the shape of the results for easier use, makes decisions based on orthographic and phonological results,
        detects error types, resets eye position, restores stimulus representation, prints results
        """
        self.PM_decisions()
        self.reshape_results()
        self.model.ortho.pos = -1
        self.detect_error_type()
        self.print_results()

   #############################
   #### Results generation #####
   #############################

    def getH(self):
        """
        Returns the entropy of the percept.
        """
        return [[entropy(i) for i in p] for p in np.moveaxis(self.model.ortho.percept.dist["percept"], -1, 0)]

    def one_res(self, typ):
        """
        Returns the result according to name

        :param typ: the type of result you want to get, among them:
        ld_ortho : ortho dl value at the end of the simulation
        ld_phono : phoo dl value at the end of the simulation
        ld_ortho_all : all ortho dl values during the simulation
        ld_phono_all : all phono dl values during the simulation
        PM : new word categorization
        PM_ortho : new word categorization in the ortho modality
        PM_phono : new word categorization in the phono modality
        dirac : get the maximum of the L dstribution (quasi dirac for adults)
        sd : return attention dispersion chosen (sd at the end of the simulation)
        meanH : return the mean entropy of the letters
        meanH_all : return the mean entropy of the letters during the exposure
        sumH : return the sum entropy of the letters
        t_tot : simulation duration
        nb_fix : number of fixations
        duree_fix : duration of successive fuxations
        fixations_visuelles : list of ortho positions
        fixations_phono : list of phono positions
        first_phoneme : maximum of the first phoneme distribution
        fixation_positions : position of all the fixations
        fixation_times : time of all the fixations
        phi : calculated pronunciation
        pron_first_pass : calculated pronunciation at the end of the first pass (before the regression)
        wphi : phono recognized word
        wl : ortho recognized word
        wl_all : ortho most likely recognized word over time
        wfusion : recognized word
        maxwphi : value of the mawimum of the distribution wphi
        psi_score : similarity between theretical and calculated pronunciation
        sum_err_pos_phono : sum of position estimation errors
        missing_bigram : looks for the missing bigrams in decoding
        """
        if typ == "ld_ortho":
            return self.model.ortho.word.dist["ld"][0]
        elif typ == "ld_phono":
            return self.model.phono.word.dist["ld"][0]
        elif typ == "ld_ortho_all":
            return self.res["ortho"]["ld"][0]
        elif typ == "ld_phono_all":
            return self.res["phono"]["ld"][0]
        elif typ == "PM":
            return self.model.PM
        elif typ == "PM_ortho":
            return self.model.ortho.PM
        elif typ == "PM_phono":
            return self.model.phono.PM
        elif typ == "dirac":
            return [self.model.get_dirac(self.stim)]
        elif typ == "sd":
            return [self.model.ortho.attention.sd]
        elif typ == "meanH":
            return [np.mean(i) for i in self.model.phono.percept.get_entropy()]
        elif typ == "meanH_all":
            return [np.mean(self.model.phono.percept.get_entropy(self.res["phono"]["percept"][:, :, i])) for i in range(self.t_tot)]
        elif typ == "sumH":
            return [sum(i) for i in self.model.phono.percept.get_entropy()]
        elif typ == "t_tot":
            return self.t_tot
        elif typ == "nb_fix":
            return len(self.fix['ortho']["t"])
        elif typ == "duree_fix":
            return np.diff(self.fix['ortho']["t"])
        elif typ == "fixations_visuelles":
            return self.fix['ortho']["pos"]
        elif typ == "fixations_phono":
            return self.fix["phono"]["pos"]
        elif typ == "first_phoneme":
            return np.max(self.get_res(mod="phono", dist="percept")[0], axis=0)
        elif typ == "fixation_positions":
            return "-".join([str(i) for i in self.fix['ortho']["pos"]])
        elif typ == "fixation_times":
            return "-".join([str(i) for i in self.fix['ortho']["t"]])
        elif typ == "phi":
            return self.model.phono.percept.decision()
        elif typ == "pron_first_pass":
            return self.model.phono.percept.pron_first_pass
        elif typ == "wphi":
            return self.model.phono.word.decision("word")
        elif typ == "wl":
            return self.model.ortho.word.decision("word")
        elif typ == "wl_all":
            return np.max(self.res["ortho"]["word"], axis=0)
        elif typ == "wfusion":
            return self.model.ortho.word.chosen_word
        elif typ == "maxwphi":
            return max(self.model.phono.word.dist["word"])
        elif typ == "psi_score":
            return self.model.phono.percept.psi_score()
        elif typ == "sum_err_pos_phono":
            return np.mean(self.fix['phono']["err"])
        elif typ == "missing_bigram":
            return str(self.miss_bigram_res)
        else:
            raise ValueError(f"wrong result type: {typ}")

    def update_store_dist(self, result_names):
        """
        calculates which distributions have to be stored in the res array to avoid memory consumption
        :param result_name: the results that will be stored
        :return: the list of results that have to be stored in the res array
        """
        res = {"ortho": [], "phono": []}
        for i in result_names:
            if i == 'ld_ortho_all':
                res["ortho"].append("ld")
            if i == 'ld_phono_all':
                res["ortho"].append("ld")
            if i == 'meanH_all':
                res["phono"].append("percept")
            if i == 'wl_all':
                res["phono"].append("word")
        self.store_dist = res

    #############################
    #### Error Analysis #####
    #############################

    def success(self, typ="phi"):
        """
        Returns a boolean value indicating whether the simulation was successful or not, depending on the measure considered
        Attention, the success is according to the "one res" result, so it should have the same size

        :param typ: the type of success we want to measure, defaults to phi (optional)
        :return: The success of the simulation according to the measure considered.
        """
        if typ == "phi":
            return self.model.phono.percept.evaluate_decision()
        if typ == "pron_first_pass":
            return self.model.phono.percept.evaluate_decision(dist_name="pron_first_pass")
        elif typ == "psi_score":
            return self.model.phono.percept.psi_score() > 0.9
        elif typ == "p":
            return self.model.ortho.percept.evaluate_decision()
        elif typ == "wl":
            return self.model.ortho.word.evaluate_decision("word")
        elif typ == "wphi":
            return self.model.phono.word.evaluate_decision("word")
        elif typ == "wfusion":
            return utl.str_transfo(self.model.ortho.word.chosen_word) == self.model.ortho.stim
        elif "ortho" in typ or "phono" in typ:  # ld_phono/ortho ou PM_ortho/phono
            data = getattr(self.model, "ortho" if "ortho" in typ else "phono")
            is_PM = self.n_simu == 0 and (data.lexical.remove_stim or self.model.stim not in self.model.ortho.lexical.df.index)
            return (data.word.dist["ld"][0] < data.word.ld_thr) == is_PM if "ld" in typ else data.word.PM == is_PM if "PM" in typ else False
        elif typ == "PM":
            return (self.n_simu == 0 and self.model.PM and ((self.model.ortho.lexical.remove_stim and self.model.phono.lexical.remove_stim) or (self.model.stim not in self.model.ortho.lexical.df.index)))\
                or (self.n_simu > 0 and not self.model.PM)
        elif typ == "correction":
            return self.model.phono.percept.evaluate_decision()
        elif typ == "duree_fix":
            return [True if self.model.PM else False] + [True] * len(np.diff(self.fix['ortho']["t"] + [self.t_tot]) - 1)

    def detect_lexicalisation_error(self):
        """
        Detects lexicalisation errors, which are defined as the case where the model's fusion word is not equal to the stimulus
        """
        pron_error = utl.str_transfo(self.model.ortho.word.chosen_word) != self.model.stim
        pron_equal_identif = utl.str_transfo(self.model.phono.percept.decision()) == utl.str_transfo(self.model.phono.word.decision())
        top_down = self.model.ortho.percept.dist['gamma'] > 3e-6 or self.model.phono.percept.dist['gamma'] > 3e-6
        return pron_error and pron_equal_identif and top_down

    def detect_context_error(self):
        """
        Detects context errors, which are defined as the case where the pronunciation of the word is in the list of context semantic words
        """
        return self.model.phono.percept.decision() in self.model.semantic.context_sem_words_phono or self.model.ortho.detect_context_error() or self.model.phono.detect_context_error()

    def detect_missing_letter_error(self):
        """
        Detects error when no word used for decoding had some letter in stimulus
        """
        used_words = [i.split('_')[0] for j in self.model.phono.percept.get_used_words().values() for i in j]
        stim = self.model.ortho.stim
        for l in range(len(stim)):
            if not any([stim[l] == wd[l] for wd in used_words]):
                return True
        return False

    def detect_missing_bigram_error(self):
        """
        Detects error when no word used for decoding had some bigram in stimulus
        """
        used_words = [i.split('_')[0] for j in self.model.phono.percept.get_used_words().values() for i in j]
        stim = self.model.ortho.stim
        for l in range(len(stim) - 1):
            if not any([stim[l:l + 2] == wd[l:l + 2] for wd in used_words]):
                return True
        return False

    def detect_error_type(self):
        """
        Detects the type of error made by the model while decoding
        """

        self.error_type = "None"
        if self.model.phono.enabled and self.model.phono.stim:
            str_lex = utl.str_transfo(self.model.phono.stim)
            str_perc = utl.str_transfo(self.model.phono.percept.decision())
            if str_lex != str_perc:
                self.error_type = "unknown"
                # substitution
                err = detect_errors.detect_substitution_error(self.model.ortho.stim, str_lex, str_perc)
                if err != "":
                    self.error_type = err
                # deletion
                err = detect_errors.detect_deletion_error(str_lex, str_perc)
                if err != "":
                    self.error_type = err
                # insertion
                err = detect_errors.detect_insertion_error(str_lex, str_perc)
                if err != "":
                    self.error_type = err
                if self.model.mismatch:
                    self.error_type = "mismatch detected"
                    if self.detect_context_error():
                        self.error_type = "context"
                if self.detect_missing_bigram_error():
                    self.error_type = "missing bigram"
                if self.detect_missing_letter_error():
                    self.error_type = "missing letter"
                if self.detect_lexicalisation_error():
                    self.error_type = "lexicalisation"
                    # if self.detect_context_error(): self.error_type = "context"

    #################################################################
    ###### Simulations corresponding to one exposure to one word ####
    ################################################################

    def run_simu_general(self):
        """
        Runs the simulation corresponding to it's name : normal, app, change_pos, grid_search, H
        """
        getattr(simu, "run_simu_" + self.simu_type)(self, **self.simu_args if self.simu_args is not None else {})

    def one_step_general(self):
        """
        Runs one step corresponding to the type : normal, phono (others to come)
        """
        self.model.one_iteration()
        self.complete_dist()
        self.t_tot += 1

    @generic_simu
    def run_simu_normal(self):
        """
        Runs the simulation for `max_iter` iterations, where each iteration is a call to the function `one_step_general`
        """
        for t in range(self.max_iter):
            self.one_step_general()

    @learning
    def run_simu_app(self):
        """
        Runs the simulation in normal mode with learning at the end
        """
        self.run_simu_normal()

    @generic_simu
    def run_simu_threshold(self):
        """
        Runs the simulation until the stop criterion is met
        """
        for t in range(self.max_iter):
            if not self.stopCriterion():
                self.one_step_general()

    @learning
    @generic_simu
    def run_simu_change_pos(self):
        """
        Runs a simulation where the times, ortho positions and attentional dispersions of all fixations are given in advance in the dictionary self.fix
        """
        if self.fix is None:
            self.fix = {"t": [], "pos": [], "pos_phono": [], "sd": []}
        if 0 not in self.fix['ortho']["t"]:  # si on renseigne pas 0, on le rajoute à la main dans les fix faites
            self.fix['ortho']["t"] = [0] + self.fix['ortho']["t"]
            self.fix['ortho']["pos"] = [self.model.ortho.pos] + self.fix['ortho']["pos"]
            if self.model.phono.enabled:
                self.fix["phono"]["pos"] = [self.model.phono.pos] + self.fix["phono"]["pos"]
            self.fix['ortho']["sd"] = [self.model.ortho.attention.sd] + self.fix['ortho']["sd"]
        self.fix['ortho']["att"] = []
        if self.phono.enabled:
            self.fix["phono"]["att"] = []
        self.fix['ortho']["sd"] = []
        for i in np.arange(0, self.max_iter):
            if i in self.fix['ortho']["t"]:
                idx = self.fix['ortho']["t"].index(i)
                self.model.pos = self.fix['ortho']["pos"][idx]
                self.fix['ortho']["att"] += [list(self.model.ortho.attention.dist)]
                if self.model.phono.enabled:
                    self.fix["phono"]["att"] += [list(self.model.phono.attention.dist)]
                self.fix['ortho']["sd"].append(self.model.ortho.attention.sd)
            self.one_step_general()

    ########################################
    ### subsidiary functions for simu_H ####
    ########################################

    def get_prototype(self, der=False):
        """
        Gets the simulation prototype
        """
        eng = "Eng" if self.model.langue == "en" else ""
        with open(os.path.join(_ROOT, 'resources/prototype/HProto' + eng + '.pkl'), 'rb') as f:
            [dfH, dfHDer] = pkl.load(f)
        if len(self.stim) in dfHDer.keys():
            return list(dfHDer[len(self.stim)]) if der else list(dfH[len(self.stim)])
        return None

    def run_correction(self, len_corr):
        """
        The function runs a correction by adjusting the gamma ratio to a high value and running a specified number of time steps in the model.

        :param len_corr: len_corr is an integer parameter that represents the number of correction steps to be performed by the model.
        """
        self.one_step_general()  # pour ne pas écraser le percept
        old_word_reading = self.model.phono.percept.word_reading
        self.model.phono.percept.word_reading = True
        self.model.phono.percept.gamma_ratio *= 10
        for _ in range(len_corr):
            self.one_step_general()
        self.model.phono.percept.gamma_ratio /= 10
        self.model.phono.percept.word_reading = old_word_reading

    def delete_correction(self, len_corr):
        """
        This function deletes the pronunciation correction if needed.

        :param len_corr: `len_corr` is an integer parameter that represents the duration of the pronunciation correction.
        """
        for mod in ["ortho", "phono"]:
            for name in self.model.dist_names:
                if name in self.res[mod] and len(self.res[mod][name]) > len_corr:
                    old_dist = self.res[mod][name][-(len_corr + 1)]
                    for i in range(1, len_corr + 1):
                        self.res[mod][name][-i] = old_dist
        self.model = self.copy_model

    def pronunciation_correction(self):
        """
        This function checks if a correction is needed for a pronunciation and performs the correction if necessary.
        """
        len_corr = 100
        if self.model.phono.enabled:
            self.pron_sans_corr = self.model.phono.percept.decision()
            self.id_sans_corr = self.model.phono.word.evaluate_decision() if len(self.model.ortho.lexical.repr) > 0 else False
            # necessity of correction
            # only if there is no online correction (semantic.top down at False)
            if self.phono.enabled and not self.model.semantic.top_down and (self.model.word_reading or (self.model.semantic.context_sem and self.model.semantic.p_sem > 1)) and not self.model.phono.word.decision("ld", ld_thr=0.85):
                logging.simu(f"succès de l'identification avant correction : {self.id_sans_corr}")
                logging.simu(f"CORRECTION A {self.t_tot}")
                logging.simu(f"percept avant correction : {self.pron_sans_corr}")
                self.copy_model = copy.deepcopy(self.model)
                self.run_correction(len_corr)
                logging.simu(f"percept après correction : {self.model.phono.percept.decision()}")
                self.success_correction = self.model.phono.percept.evaluate_decision()
                logging.simu(f"succès de la correction : {self.success_correction}")
                if (self.model.phono.word.decision(dist_name="word") in self.model.semantic.context_sem_words_phono and self.model.semantic.p_sem > 1) or self.model.word_reading:
                    self.corrected = "kept"
                    logging.simu("CORRECTION GARDÉE")
                else:
                    self.corrected = "deleted"
                    logging.simu("CORRECTION SUPPRIMÉE")
                    self.correction = False
                    self.delete_correction(len_corr)

    def update_sigma(self, Hinit, H):
        """
        This function updates the standard deviation of the attention distribution based on the speed of perceptual information accumulation compared to a prototype

        :param Hinit: Hinit is a list of initial entropies for each position. It is used to check the validity of the prototype.
        :param H: H is a list of current entropies for each position.
        """
        proto = self.get_prototype()  # prototype entropy
        sd_list = [3, 2.5, 2, 1.75, 1.5, 1.25, 1, 0.9, 0.8, 0.7, 0.6, 0.5]
        rapport_list = [20, 5, 2, 1, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, -10]
        rapport = (sum(Hinit) - sum(H)) / (sum(Hinit) - proto[self.t_tot - 1])
        if rapport > 0:
            sd = next(sd for sd, rapp in zip(sd_list, rapport_list) if rapport > rapp)
            self.model.ortho.attention.sd = sd

    def update_entropy(self, alpha, thr_fix):
        """
        This function updates all measures related to entropy : the letter entropy, a list of positional entropy values modulated by motor cost, and a criterion for stopping
        the fixation according to entropy values

        :param alpha : motor cost
        :param thr_fix : entropy threshold to stop a fixation
        :return: three values: H, Hesp, and criterion1.
        """
        HPhonoPrec = copy.copy(self.model.phono.percept.H)
        self.model.phono.percept.H = self.model.phono.percept.get_entropy()
        self.model.ortho.percept.H = self.model.ortho.percept.get_entropy()
        self.model.phono.percept.max_HDer = np.max(HPhonoPrec - np.array(self.model.phono.percept.H))
        if self.fixation_criterion_type == "phono":
            dz_pos = self.model.phono.percept.get_dz_pos()
            dz_pos_large = self.model.phono.percept.get_dz_pos(0.6)
            Hesp = [(1 - alpha) * (h - self.model.phono.percept.H[self.model.phono.pos]) / np.max(self.model.phono.percept.H[:dz_pos]) - alpha * abs(
                i - self.model.phono.pos) - thr_fix for i, h in enumerate(self.model.phono.percept.H[:dz_pos])]
            # print(dz_pos,Hesp,"\n",self.model.phono.percept.get_entropy()[self.model.phono.pos],self.model.phono.percept.get_entropy(),"\n",)
            if self.model.phono.pos >= dz_pos_large:
                criterion1 = True
            else:
                criterion1 = max(Hesp) > 0
            self.HDerPhono = HPhonoPrec - np.array(self.model.phono.percept.H)
        else:  # ortho
            Hesp = [((1 - alpha) * (h - self.model.ortho.percept.H[self.model.ortho.pos]) / np.max(self.model.ortho.percept.H) - alpha * abs(i - self.model.ortho.pos)) - thr_fix for i, h in enumerate(self.model.ortho.percept.H)]
            # the objective is not to wait until it stabilizes, because if you wait too much, it will be impossible to change your mind after
            # therefore, no criterion that waits until the derivative is sufficiently low
            criterion1 = max(Hesp) > 0
        return Hesp, criterion1

    def find_missing_bigram(self):
        """
        Verify if all the bigrams in the stimulus have a corresponding lexical entry in the lexical (word with same letters at the bigram's position).
        :return: boolean, True if all bigrams have a corresponding entry.
        """
        self.miss_bigram_res, cond = self.model.phono.percept.missing_bigram()
        if False in cond:
            logging.simu(f"missing bigram at {self.t_tot} : {self.miss_bigram_res}")
            pos_to_visit = [i for j in [[i, i + 1] for i, bool in enumerate(cond) if not bool] for i in j if i not in self.fix['ortho']['pos']]
            if len(pos_to_visit) > 0:
                self.model.ortho.pos = pos_to_visit[-1]
                if self.model.phono.enabled:
                    self.model.phono.attention.position_mapping(end_verif=True)
            else:
                return True
        else:
            logging.simu(f"all bigrams at {self.t_tot} : {self.miss_bigram_res}")
            return True

    def update_position(self, Hesp):
        """
        This function updates the orthographic and phonological position of the model based on letter identity information on each position

        :param Hesp: Hesp is a list of floats representing the level of orthographic uncertainty of each position modulated by motor cost
        """
        # only case where ortho position is inferred from phono position
        if self.reading_unit == "None" and self.fixation_criterion_type == "phono" or (self.reading_unit == "grapheme"):
            if self.reading_unit == "None":
                pos_tmp_phono = np.argmax(Hesp)
                # oblige to change position when gets "stucked" without gaining some info
                if pos_tmp_phono == self.model.phono.pos and abs(self.HPhonoDer[pos_tmp_phono]) < 1e-3:
                    pos_tmp_phono = Hesp.index(heapq.nlargest(2, Hesp)[-1])
                # we stop at the first # well perceived
                pos_tmp_phono = min(pos_tmp_phono, self.model.phono.percept.get_dz_pos() - 1)
            else:
                pos_tmp_phono = self.model.phono.pos + 1 if self.model.phono.pos < len(Hesp) else 0
            if pos_tmp_phono < self.model.phono.pos:
                if not self.regression:  # check if it is a regression, and if it is authorized
                    return True
                else:
                    self.model.phono.percept.pron_first_pass = self.model.phono.percept.decision()
            self.model.phono.pos = pos_tmp_phono
            self.model.ortho.attention.position_mapping(pos_tmp_phono)
        else:
            pos = self.model.ortho.pos
            if self.reading_unit == "None":
                pos_tmp = np.argmax(Hesp)
                # oblige change position
                if pos_tmp < pos and not self.regression:
                    return True
                elif pos_tmp == pos:
                    pos_tmp = self.model.phono.attention.len2phlen(Hesp.index(heapq.nlargest(2, Hesp)[-1]))
                self.model.ortho.pos = min(len(self.model.stim) - 1, pos_tmp)
            elif self.reading_unit == "letter":
                if pos == self.model.ortho.N - 1 and not self.regression:
                    return True
                self.model.ortho.pos = pos + 1 if pos < self.model.ortho.N - 1 else 0
            elif self.reading_unit == "bigram":
                if pos >= self.model.ortho.N - 2 and not self.regression:
                    return True
                self.model.ortho.pos = pos + 2 if pos < self.model.ortho.N - 2 else 0
            elif self.reading_unit == "trigram":
                if pos >= self.model.ortho.N - 3 and not self.regression:
                    return True
                self.model.ortho.pos = pos + 2 if pos < self.model.ortho.N - 2 else 1
            elif self.reading_unit == "grapheme":
                gs = self.model.gs
                next_grapheme = str(int(gs[int(pos)]) + 1)
                print(next_grapheme)
                if next_grapheme not in gs:
                    if not self.regression:
                        print('no reg', next_grapheme)
                        return True
                    else:
                        self.model.phono.percept.pron_first_pass = self.model.phono.percept.decision()
                self.model.ortho.pos = gs.index(next_grapheme) if next_grapheme in gs else 0
                self.model.ortho.pos = self.model.ortho.attention.next_grapheme()
                self.model.ortho.attention.build_attention_distribution()
            if self.model.phono.enabled:
                self.model.phono.attention.position_mapping(end_verif=(True and self.reading_unit == "None"))
        self.update_fix_info()
        return False

    @learning
    @generic_simu
    def run_simu_H(self, alpha=0.1, thr_fix=0.5):
        """
        This function runs a simulation with visuo-attentional exploration of the stimulus based on entropy optimization

        :param alpha: float, motor cost (careful, if too high, typically 0.2, simulation can stuck in one position)
        :param thr_fix: float, threshold for a new fixation (entropy difference)
        """
        self.model.ortho.percept.H = self.model.ortho.percept.get_entropy()
        self.model.phono.percept.H = self.model.phono.percept.get_entropy()
        Hinit = copy.copy(self.model.ortho.percept.H)
        waiting_time_saccade = 0
        time_saccade = 25 if self.transition_saccadic else 0
        while self.t_tot < self.max_iter:
            for self.t_local in range(400):
                if self.t_tot < self.max_iter + time_saccade:
                    if waiting_time_saccade > 0:
                        waiting_time_saccade -= 1
                    if waiting_time_saccade == 1:
                        self.model.ortho.percept.stimulation = True
                        self.model.phono.percept.stimulation = True
                    logging.debug('\n\n')
                    logging.debug(f"TIME {self.t_tot}     position {self.model.ortho.pos}")
                    self.one_step_general()
                    Hesp, criterion1 = self.update_entropy(alpha, thr_fix)
                    criterion2 = self.stopCriterion()
                    if (criterion1 and self.t_local >= self.t_min - 1 + time_saccade) or criterion2 or self.t_tot == self.max_iter:  # end of fixation
                        logging.braid(f"fin fixation,  time : {self.t_local}, crit Hfix : {criterion1}, critHExpo : {criterion2}")
                        logging.braid(f"{self.model.ortho.percept.get_entropy()}")
                        waiting_time_saccade = time_saccade
                        if self.transition_saccadic:
                            self.model.ortho.percept.stimulation = False
                            self.model.phono.percept.stimulation = False
                        break
            # end of exposure
            end_expo = criterion2 or self.t_tot == self.max_iter or len(self.fix['ortho']['t']) > 2 * len(self.model.stim)
            if not end_expo:
                end_expo = self.update_position(Hesp)  # all fixations : position update
            if end_expo:
                logging.braid(f"fin exposition,  time total : {self.t_tot}")
                logging.braid(f"dz_pos : {self.model.phono.percept.get_dz_pos()}, entropy {self.model.phono.percept.get_entropy()}")
                # self.find_missing_bigram()
                self.pronunciation_correction()
                if self.t_local >= 50:
                    self.fix["ortho"]["t"].append(self.t_tot)
                else:
                    self.t_tot = self.fix['ortho']['t'][-1]
                return
            # if False and len(self.fix['ortho']["t"]) == 1:  # first fixation : sigma update
            #    self.update_sigma(Hinit,H)
        return  # if t_tot > max_iter -> old criterion

    def run_simu_choose_word(self, n_choose_word=10, **kwargs):
        """
        Runs a simulation where only a certain number of words (n_choose_word) are used for decoding,
        the words being externally selected by similarity with the stimulus.
        """
        self.model.ortho.lexical.build_all_repr()
        self.model.phono.lexical.build_all_repr()
        self.model.ortho.lexical.set_repr()
        self.model.phono.lexical.set_repr()
        p = utl.create_repr(np.array([[self.model.ortho.chars.index(i) for i in self.stim]]), self.model.ortho.n, self.model.ortho.eps)[0]
        sim = np.prod(utl.wsim(self.model.ortho.repr[:self.lexical.shift_begin], p), axis=1)
        idx = sim.argsort()[::-1][:n_choose_word]
        logging.simu(f"used words for decoding {self.model.ortho.get_names(idx)}")
        self.model.ortho.lexical.df.loc[~self.model.ortho.lexical.df.idx.isin(idx), 'ortho'] = False
        self.model.ortho.lexical.df.loc[self.model.ortho.lexical.df.idx.isin(idx), 'ortho'] = True
        self.model.ortho.all_repr[len(self.stim) - 1] = self.model.ortho.build_repr(len(self.stim))
        self.model.ortho.repr = self.model.ortho.all_repr[len(self.stim)]
        self.run_simu_H(**kwargs)
