# -*- coding: utf-8 -*-
# General purpose libraries
import copy
# Scientific/Numerical computing

import itertools
# BRAID utlities
from braidpy.simu import simu
import logging
import os
import pdb
import pickle as pkl
import gc
from scipy import stats

import numpy as np
import pandas as pd


# on désactive le mode debug de numba et numpy
numba_logger = logging.getLogger('numba')
numba_logger.setLevel(logging.WARNING)
numpy_logger = logging.getLogger('numpy')
numpy_logger.setLevel(logging.WARNING)


class expe:
    """
    Experiment involving simulations from several stimuli, exposures, parameters
    """

    def __init__(self, simu_param=None, model_param=None, ortho_param=None, phono_param=None, semantic_param=None, color_param=None,
                 res_fct_name='t_tot', basename="simu", test={}, test_modality={},
                 n_expo=1, reinit=True, lenMin=4, lenMax=8, n_stim_len=100, liste_type="random", liste=None,
                 word_action=None, word_action_value=None, simulation_action=None, simulation_action_value=None,
                 last_expo_isolation=False, shuffle=False, print_res=True, store_txt=True, store_simu=False):
        """
        :param simu_param: parameters to instance the 'simu' class
        :param model_param: parameters to instance the 'braid' class
        :param ortho_param: parameters to instance the 'ortho' class
        :param phono_param: parameters to instance the 'phono' class
        :param semantic_param: parameters to instance the 'semantic' class
        :param color_param: parameters to instance the 'color' class
        :param res_fct_name: A string or a list of strings representing the name(s) of the function(s) that will be used to compute the results of the simulation.
            All the possibilities are listed in the function simu.one_res of class simu
        :param basename: The basename for the simulation files that will be saved, it will be completed according to simulation parameters (orthographically/phonologically novel ?)
        :param test: A dictionary containing the parameters that will be tested (keys), and the values that will be tested for each parameters (values). The cross-product of each combination of parameters will be tested.
            ex test={"Q": [1,2], "max_iter" :[500,1000]}
        :param test_modality: A dictionary containing the parameters that will be tested in the test dictionary and are present in both modalities (ortho and phono) as keys, and the corresponding modality to be tested as value.
                if the modality is not indicated in this disctionary, it will be the orthographic modality by default.
        :param n_expo: The number of exposures for each word, defaults to 1 (optional)
                           /!\ in the stored dataframe, t can be either a number of iterations or a number of exposures
                           but in the simulation it's possible to vary both the number of exposures and store one result per iteration simulated
                           the correspoding columns in the dataframe (t,num) will be affected according to the value of self.n_expo and length of the result
                           If self.n_expo>1, t in exposures, if you want a result in iterations it will be stored as num
                           If self.n_expo == 1 and len(res) > 20, we have a long result -> it is a number of iterations, every element of res will be stored with varying t values
                           If self.n_expo == 1 and we have len(res) < 21, it's a list of non - temporal data, every element of res will be stored with varying num values
        :param reinit: A boolean parameter that determines whether to reinitialize the lexicon at each simulation or not.
        :param lenMin: The minimum length of a word in the list of stimuli, defaults to 4 (optional)
        :param lenMax: The maximum length of a word in the list of stimuli, defaults to 8 (optional)
        :param n_stim_len: The number of stimuli of each length to generate for the simulation, defaults to 10 (optional)
        :param liste_type : The type of words selected, can be "random", "cons", or "incons".
        :param liste: A list of strings representing the stimuli to be used in the simulation. If not provided, a random list of stimuli will be generated based on the values of lenMin, lenMax, and n_stim_len
        :param word_action: A string representing the name of the function to be applied on a word before the simulation (ex change its frequency)
        :param word_action_value: word_action_value is an eventual function parameter (ex the frequency to be assigned). It is a dico used as kwargs.
        :param simulation_action: The simulation_action parameter is used to specify an action to be performed before the simulation, for each word and each exposure.
            prototype is f(t,**value)
            ex explicit learning : force learning for t=0 and force update for t>0
        :param simulation_action_value: The dico containing values to be passed as an argument to the simulation_action function when it is called (kwargs)
        :param last_expo_isolation: A boolean indicating if the last exposition should be done without context, no matter how it was during all the previous ones.
        :param shuffle: A boolean parameter that determines whether the list of stimuli should be shuffled before running the simulation.
        :param print_res: A boolean parameter that determines whether or not to print the results of the simulation.
        :param store_txt: A boolean parameter that determines whether or not to store results in a readable form in a txt file.
        :param store_simu: A boolean parameter that determines whether to store the simulation object or not.
        """
        # instanciation of all classes before instanciating the experiment
        if simu_param is None:
            simu_param = {}
        if 'level' not in simu_param.keys():
            simu_param['level'] = 'expe'
        self.simu = simu(model_param={**(model_param or {})},
                         ortho_param={**{"sd": 1}, **(ortho_param or {})},
                         phono_param=phono_param, semantic_param=semantic_param, color_param=color_param,
                         **(simu_param or {}))
        self.res_fct_name = res_fct_name if isinstance(res_fct_name, list) else [res_fct_name]
        self.simu.update_store_dist(self.res_fct_name)
        self.basename = basename
        self.test = test
        self.test_modality = test_modality
        self.n_expo = n_expo
        self.reinit = reinit
        self.lenMin, self.lenMax, self.n_stim_len = lenMin, lenMax, n_stim_len
        self.list_type = liste_type
        self.liste = liste if liste is not None else self.generate_stimulus_list()
        print(self.liste)
        if len(self.liste) < 300:
            print(self.liste)
        else:
            print(self.liste[:150], "\n ... \n", self.liste[:150:])
        # self.print_stimulus_caracteristics()
        self.word_action = word_action
        self.word_action_value = word_action_value
        self.simulation_action = simulation_action
        self.simulation_action_value = simulation_action_value
        self.shuffle = shuffle
        self.print_res = print_res
        self.store_txt = store_txt
        self.store_simu = store_simu
        self.csv_name = self.txt_name = None
        self.copy_model = None
        self.dico = self.already_tested_words = None
        self.succ = True
        self.last_expo_isolation = last_expo_isolation

    def update(self, **kwargs):
        """ used to set several attributes at once"""
        for k, v in kwargs.items():
            setattr(self, k, v)

    ########################
    ### Beginning of expe ##
    ########################

    def get_regularity_indicators(self):
        df = pd.read_csv(os.path.join(self.path, "resources/lexicon/Lexique_infra_cons.csv"))
        df['len'] = df.word.str.len()
        df = df[(df.len >= self.lenMin) & (df.len <= self.lenMax) & (df.freq > 0)].astype({'cons_min': float}).groupby(
            'word').first().reset_index().copy()
        df['comp'] = df.word.str.len() - df.pron.str.len()
        return df

    def get_list_consistency(self, liste=None, return_df=False):
        """
        Retrieves the consistency of words of the expe list.
        :return: a list of consistency values
        """
        liste = liste if liste is not None else self.liste
        df = self.get_regularity_indicators()
        df = df[df.word.isin(liste)].set_index('word')
        if return_df:
            return df[['len', 'freq', 'cons_min']]
        return [df.loc[i].cons_min for i in liste if i in df.index.values]

    def get_list_frequency(self, liste=None, return_df=False):
        """
        Retrieves the consistency of words of the expe list.
        :return: a list of consistency values
        """
        liste = liste if liste is not None else self.liste
        df = self.simu.model.ortho.lexical.df
        df = df[df.word.isin(liste)].set_index('word')
        if return_df:
            return df[['len', 'freq', 'cons_min']]
        return [df.loc[i].freq for i in liste if i in df.index.values]

    def generate_stimulus_list(self):
        """
        Get list of stimuli from the lexicon
        They can be either "random", "random_GS" (with known graphemic segmentation), "cons" or "incons"
        """
        # words with '~' are words fragments, not real words, and cannot be used as stimuli
        lx = self.simu.model.get_joint_lexicon().set_index('word')
        if "_GS" in self.list_type or "cons" in self.list_type:
            df = self.get_regularity_indicators()
            df = df[(df.word.isin(lx.index.values))].copy()
            lx = lx[(lx.index.isin(df.word.values))].copy()
        if "random" in self.list_type:
            lx = lx[~lx.index.str.contains('_#|#_|_~|~_')].reset_index().groupby('word').first()
            if 'pron' in lx.columns:
                # no selection of homophones
                hp = lx.groupby('pron').count()['idx'].reset_index()
                hp = list(hp[hp.idx > 1].pron.values)
                lx = lx[~lx.pron.isin(hp)].copy()
            print(1, self.lenMin, self.lenMax, self.n_stim_len)
            return list(lx[(lx.freq > 0) & (lx.len >= self.lenMin) & (lx.len <= self.lenMax) & (~lx.index.str.contains('#|~'))].groupby('len').sample(n=self.n_stim_len, random_state=24).index)
        if "cons" in self.list_type:
            thr = 0.05
            if "incons" in self.list_type:
                incons_df = df[(df['cons_min'] < thr)]
                return list(incons_df.groupby('len').sample(n=self.n_stim_len, random_state=23).word)
            elif "cons" in self.list_type:
                cons_df = df[(df['cons_min'] > 1 - thr)]
                return list(cons_df.groupby('len').sample(n=self.n_stim_len, random_state=23).word)
        return []

    def print_stimulus_caracteristics(self):
        df_lex = self.simu.model.ortho.lexical.df
        df_lex = df_lex[(df_lex.len > 3) & (df_lex.len < 9)]
        df_stim = df_lex[df_lex.index.isin(self.liste)]
        freq_lex = df_lex.groupby('len').freq
        freq_stim = df_stim.groupby('len').freq
        print('frequences lexicon ', 'freq moyenne :', df_lex.freq.mean(), ' +/- ', df_lex.freq.std())
        print('frequences stim ', 'freq moyenne :', df_stim.freq.mean(), ' +/- ', df_stim.freq.std())
        print('ecart en terme de sigma', abs(df_lex.freq.mean() - df_stim.freq.mean()) / df_stim.freq.std())
        t_stat, p_value = stats.ttest_1samp(df_stim.freq.values, df_lex.freq.mean())
        print("t-test", p_value, t_stat)

        cons_stim = self.get_list_consistency(return_df=True)
        cons_lex = self.get_list_consistency(return_df=True, liste=list(df_lex.index.values))
        # for n in range(4,9):
        #    t_stat, p_value = stats.ttest_1samp(df_stim[df_stim.len==n].freq.values, df_lex[df_lex.len==n].freq.mean())
        print('cons lexicon ', 'cons moyenne :', cons_lex.cons_min.mean(), ' +/- ', cons_lex.cons_min.std())
        print('cons stim ', 'cons moyenne :', cons_stim.cons_min.mean(), ' +/- ', cons_stim.cons_min.std())
        print('ecart en terme de sigma', abs(cons_lex.mean().cons_min - cons_stim.cons_min.mean()) / cons_lex.cons_min.std())
        t_stat, p_value = stats.ttest_1samp(cons_stim.cons_min.values, cons_lex.cons_min.mean())
        print("t-test", p_value, t_stat)

        print("Par LONGUEURS")
        print('frequences lexicon ', pd.DataFrame({'mean_freq': freq_lex.mean(), 'std_freq': freq_lex.std()}))
        print('frequences stim ', pd.DataFrame({'mean_freq': freq_stim.mean(), 'std_freq': freq_stim.std()}))
        print('ecart en terme de sigma', abs(freq_lex.mean() - freq_stim.mean()) / freq_lex.std())
        cons_stim = cons_stim.groupby('len').cons_min
        cons_lex = cons_lex.groupby('len').cons_min
        print('cons lexicon ', pd.DataFrame({'mean_freq': cons_lex.mean(), 'std_freq': cons_lex.std()}))
        print('cons stim ', pd.DataFrame({'mean_freq': cons_stim.mean(), 'std_freq': cons_stim.std()}))
        print('ecart en terme de sigma', abs(cons_lex.mean() - cons_stim.mean()) / cons_lex.std())

    def set_filename(self):
        """
        Sets the filenames for saving simulation data in csv format.
        """
        if not os.path.exists('csv'):
            os.mkdir('csv')
        o = self.simu.model.ortho.lexical.remove_stim
        p = self.simu.model.phono.lexical.remove_stim
        name = self.basename + '_PM_' + ('X' if not (o or p) else 'O' * o + 'P' * p)
        self.csv_name = 'csv/' + name + '.csv'
        self.txt_name = 'txt/' + name + '.txt'
        if len(self.liste) < 300:
            logging.expe(f"{self.liste} \n {self.csv_name}")
        else:
            logging.expe(f"{self.liste[:150]} \n ... \n {self.liste[-150:]} \n {self.csv_name}")

    def load_existing_data(self):
        """
        Loads preliminary results if part of the simulation was already conducted.
        """
        self.initialize_data()
        try:
            # simulation already started
            df = pd.read_csv(self.csv_name)
            self.already_tested_words = list(set(df.word.values))
        except:
            self.already_tested_words = []
            if self.store_txt:
                file1 = open(self.txt_name, "w")
                file1.writelines("Beginning of simulation \n ")
                file1.close()
            pd.DataFrame.from_dict(self.dico).to_csv(self.csv_name, mode='w', index=False)

    def initialize_data(self):
        """
        This function initializes the dictionary that will contain the results.
        """
        self.dico = dict(**{'num': [], 't': [], 'word': [], 'value': [], 'success': [], 'error_type': []}, **{key: [] for key in self.test})

    def begin_expe(self):
        """
        Sets up various parameters and variables before the simulation begins.
        """
        self.set_filename()
        self.load_existing_data()
        self.param_product = [dict(zip(self.test, x)) for x in itertools.product(*self.test.values())]
        self.simu.model.ortho.lexical.build_all_repr()
        self.simu.model.phono.lexical.build_all_repr()
        try:
            self.copy_model = copy.deepcopy(self.simu.model) if self.reinit else None
        except:
            pdb.set_trace()

    ##############################################################
    # Result function (used by compare_param end RealSimulation)
    ##############################################################

    def res_fct(self):
        """
        This function concatenates the results of different function names and returns them.
        :return: a list of results obtained by calling the `one_res` method of the `simu` object for each name in the
        `res_fct_name` list. If there is only one result and it is a list with more than one element, it returns the list. If there is more than one
        result and they are not strings, it concatenates them.
        """
        if len(self.res_fct_name) == 1:
            res = self.simu.one_res(self.res_fct_name[0])
            return res if isinstance(res, list) or isinstance(res, np.ndarray)else [res]
        elif len(self.res_fct_name) > 1:
            res = [self.simu.one_res(i) for i in self.res_fct_name]
            return [res_ii for res_i in res for res_ii in (res_i if isinstance(res_i, list) else [res_i])]
        return []

    def success(self):
        if len(self.res_fct_name) == 1:
            succ = self.simu.success(self.res_fct_name[0])
            return succ if isinstance(succ, list) else [succ]
        elif len(self.res_fct_name) > 1:
            succ = [self.simu.success(i) for i in self.res_fct_name]
            return [succ_ii for succ_i in succ for succ_ii in (succ_i if isinstance(succ_i, list) else [succ_i])]
        return []

    ####################
    ### Data storing ###
    ####################

    def store_res(self):
        """
        Stores the results in a pkl file
        """
        try:
            df = pd.DataFrame.from_dict(self.dico)
        except:
            logging.error("Erreur dans la création du dataframe")
            print(self.dico)
            pdb.set_trace()
        if self.store_simu:
            cp = copy.deepcopy(self.simu)
            # removes heavy part of the object before storing it
            cp.ortho.all_repr = {}
            cp.ortho.repr = []
            if self.simu.model.phono.enabled:
                cp.phono.all_repr = {}
            cp.phono.repr = []
            pkl.dump(cp, open(os.path.join(self.path, self.csv_name), 'wb'))
        df.to_csv(self.csv_name, mode='a', header=False, index=False)

    ####################
    ### Big simulations ###
    ####################

    def compare_param(self):
        """ Generic simulation to compare different values of parameters :
            for example max_iter, Q, leak ...
            it sets automatically the value of the parameter, given the name of the parameter (ex "Q","max_iter")
            and its possible values (ex [1,2],[250,500]) and test all combinations of parameters ex [1,2]x[250,500] -> 4
            /!\ In these simulations, all words are tested independantly

            If you wqnt to run this kind of simulation with a new parameter, you have to :
                1/ choose/define a new name in the simu.one_res function to define how to get the result you're interested in.
                2/ define how you set the parameter in the set_attr function from class simu (if it's not automatic)
        """
        self.begin_expe()
        for iw, word in enumerate(self.liste):
            print(word)
            if word not in self.already_tested_words:
                try:
                    logging.expe(f"{word} {iw}/{len(self.liste)}")
                    self.initialize_data()
                    if self.store_txt:
                        file1 = open(self.txt_name, "a")
                        file1.write("\n")
                        file1.close()
                    for ip, indices in enumerate(self.param_product):
                        if self.reinit:
                            self.simu.model = copy.deepcopy(self.copy_model)
                        self.simu.model.ortho.stim = word
                        self.simu.reset_n()
                        for p, val in indices.items():
                            if p not in self.test_modality:
                                setattr(self.simu, p, val)
                            elif self.test_modality[p] == 'ortho':
                                setattr(self.simu.model.ortho, p, val)
                            else:
                                setattr(self.simu.model.phono, p, val)
                        if self.word_action:
                            self.word_action(word, **self.word_action_value)
                        for t in range(self.n_expo):
                            if self.last_expo_isolation and t == self.n_expo - 1:
                                ctxt = self.simu.model.semantic.context_sem
                                self.simu.model.semantic.context_sem = False
                            if self.simulation_action:
                                self.simulation_action(t, **self.simulation_action_value)
                            self.simu.run_simu_general()
                            res = self.res_fct()
                            succ = [self.simu.success(r) for r in self.res_fct_name]
                            if isinstance(succ[0], list) and len(succ[0]) > 1:
                                succ = np.concatenate((succ[0], succ[1:])) if len(succ) > 1 else succ[0]
                            if self.print_res:
                                print(word, indices, [round(i, 4) if isinstance(i, float) else i for i in res])
                            if self.store_txt:
                                summary = " ".join(["\n", word, str(indices), str([round(i, 4) if isinstance(i, float) else i for i in res])])
                                file1 = open(self.txt_name, "a")
                                file1.write(summary)
                                file1.close()
                            self.simu.increase_n()
                            for ir, r in enumerate(res):  # 2D array with time as second dimension
                                if isinstance(r, np.ndarray):
                                    for iit, it in enumerate(r):
                                        app = dict(**{'word': word, 't': iit, 'num': ir, 'value': it, 'success': succ[ir], 'error_type': self.simu.error_type}, **indices)
                                        for k, v in app.items():
                                            try:
                                                self.dico[k].append(v)
                                            except:
                                                pdb.set_trace()
                                else:
                                    # /!\ t can be either a number of iterations or a number of exposures
                                    # but in the simulation it's possible to vary both the number of exposures and store one result per iteration simulated
                                    # If self.n_expo>1, time in exposures, if you want a result in iterations it will be stored as num
                                    # If self.n_expo == 1 and len(res) > 20, we have a long result -> it is a number of iterations(time=ir, num=0)
                                    # If self.n_expo == 1 and we have len(res) < 21, it's a list of non - temporal data(num=ir, time=t)
                                    time = ir if (self.n_expo == 1 and len(res) > 20) else t
                                    num = 0 if (self.n_expo == 1 and len(res) > 20) else ir
                                    try:
                                        app = dict(**{'word': word, 't': time, 'num': num, 'value': r, 'success': succ[ir] if len(succ) > ir else None, 'error_type': self.simu.error_type}, **indices)
                                    except:
                                        pdb.set_trace()
                                    for k, v in app.items():
                                        self.dico[k].append(v)
                                    if self.last_expo_isolation and t == self.n_expo - 1:
                                        self.simu.model.semantic.context_sem = ctxt
                except:
                    pdb.set_trace()
                    pass
            self.store_res()
            gc.collect()

    def learnLiliPaco_old(self, test_phase=True):
        def initialize_data():
            self.dico = dict(**{'t': [], 'num': [], 'word': [], 'value': [], 'success': []}, **{key: [] for key in self.test})

        def run_word(rank, word):
            self.simu.model.ortho.stim = word
            if self.simulation_action:
                self.simulation_action(self.simulation_action_value)
            self.simu.run_simu_general()
            res = self.res_fct()
            if self.print_res:
                print(word, indices, [round(i, 4) if isinstance(i, float) else i for i in res])
            succ = self.success()
            for ir, r in enumerate(res):
                app = dict(**{'t': rank, 'num': ir, 'word': word, 'value': r, 'success': succ[ir]}, **indices)
                for k, v in app.items():
                    self.dico[k].append(v)
            pd.DataFrame.from_dict(self.dico).to_csv(self.csv_name, mode='a', header=False, index=False)
        self.liste = [l for l in self.liste for _ in range(self.n_expo)]
        # random.shuffle(self.liste)
        rank_list = list(pd.DataFrame({'word': self.liste}).groupby('word').cumcount().values)
        test_list = list(set(self.liste))
        initialize_data()
        pd.DataFrame.from_dict(self.dico).to_csv(self.csv_name, mode='w', header=True, index=False)
        self.param_product = [dict(zip(self.test, x)) for x in itertools.product(*self.test.values())]
        self.copy_model = copy.deepcopy(self.simu.model)
        for ip, indices in enumerate(self.param_product):
            self.simu.model = copy.deepcopy(self.copy_model)
            for p, val in indices.items():
                setattr(self.simu, p, val)
            logging.expe("learning..")
            for i, word in enumerate(self.liste):  # learning phase
                initialize_data()
                run_word(rank_list[i], word)
            logging.expe("testing")
            if test_phase:
                self.simu.model.learning = False
                self.simu.model.semantic.context_sem = False
                for i, word in enumerate(test_list):  # testing phase
                    run_word(rank_list[i], word)

    def learnLiliPaco(self, test_phase=False, gonfle=False, correction_automatique=False):
        # elodie : ajout d'une comparaison de la prononciation self.model.phono.percept.decision() avec la pron du lexique associée au mot
        # nécessite variables n_simu = nombre de simus (dans cette fonction), reussite = nombre de réussites (en tant que variable globale de la classe EXPE)
        # et self.mots_inconnus = mots présentés mais pas connus par le lexique de référence (variable temporaire pour m'assurer que le lexique contient toutes les formes sans apostrophe (c'est -> cest, etc))
        reference = pd.read_csv(os.path.join(self.path, 'resources/lexicon/LiliPaco.csv'))

        def initialize_data():
            self.dico = dict(**{'t': [], 'num': [], 'word': [], 'value': [], 'success': []}, **{key: [] for key in self.test})

        def run_word(rank, word):
            self.simu.model.ortho.stim = word
            if self.simulation_action:
                self.simulation_action(self.simulation_action_value)
            # self.simu.model.phono.lexical.remove_stim=True   federico
            self.simu.run_simu_H()

            # ajout dans le lexique des mots à toutes les positions après la simu
            # if gonfle:
            #    words_at_different_pos = self.simu.model.phono.lexical.grossir_mot(5, word)
            #    pdb.set_trace()
            #    mots_ajoutes = 0
            #    # print("index : ", self.simu.model.ortho.lexical.df.index)
            #    for w in words_at_different_pos:
            #        if w not in self.simu.model.ortho.lexical.df.index:
            #            print("word : ", w)
            #            self.simu.model.phono.lexical.add_df_entry(w, len(w))
            #            self.simu.model.ortho.lexical.add_df_entry(w, len(w))
            #            mots_ajoutes += 1

            # Alexandra :
            # creation des traces associées pour les mots de la forme liµµ, µliµ, µµli etc.

            #    print("Nombre de mots ajoutés : ", mots_ajoutes)

            # self.simu.model.ortho.update_modality()
            # self.simu.model.phono.update_modality()

            # elodie : comparaison decision prononciation et prononciation dans le lexique de référence
            # TODO : utiliser la fonction self.success de la classe simu, si elle ne marche pas parce que ton cas est particulier, envoie-moi un mail
            print("Mot           : ", word)
            prononciation = self.simu.model.phono.percept.decision().replace("#", "")
            print("Prononciation : ", prononciation)
            if word in reference['word'].values:
                # TODO normalement la prononciation exacte devrait être self.modality.stim dans la classe phono
                # TODO si ce n'est pas le cas c'est que le setter de l'attribut stim ne fonctionne pas correctement, il faut regarder pourquoi.
                prononciation_exacte = reference['pron'][reference['word'] == word].values[0]
                print("prononciation_exacte : ", prononciation_exacte)
                print(prononciation_exacte == prononciation)
                if prononciation_exacte == prononciation:
                    self.reussite = self.reussite + 1

                else:  # mot non lu correctement
                    # elodie : mot simu(simu) braid(model) modality(mod) lexical(lexical)
                    # etape 1: voir si la pron correcte existe déjà -> l'incrementer, sinon ajouter nouveau mot avec freq = 1
                    # if name in self.df.index:
                    print("correction needed ")
                    # wd = self.simu.model.mod.lexical.get_word_entry(name)
                    # self.repr[int(wd.idx)] = newTrace
                    # ajout d'une correction automatique
                    # self.simu.model.ortho.lexical.add_df_entry(word, len(word))
                    # self.simu.model.phono.lexical.add_df_entry(word, len(word))

                    # Alexandra :
                    # verification que le mot n'a pas déjà été lu correctement: s'il a déjà été lu correctement donner plus d'importance à cette trace
                    #                                                           sinon créer une nouvelle entrée dans le lexique

            else:
                print("mot inconnu par le lexique de référence")
                self.mots_inconnus = self.mots_inconnus + 1

            res = self.res_fct()
            if self.print_res:
                print(word, indices, [round(i, 4) if isinstance(i, float) else i for i in res])
            succ = self.success()
            for ir, r in enumerate(res):
                app = dict(**{'t': rank, 'num': ir, 'word': word, 'value': r, 'success': succ[ir]}, **indices)
                for k, v in app.items():
                    self.dico[k].append(v)
            pd.DataFrame.from_dict(self.dico).to_csv(self.csv_name, mode='a', header=False, index=False)

        self.liste = [l for l in self.liste for _ in range(self.n_expo)]
        # random.shuffle(self.liste)
        print("n_expo : ", self.n_expo, " liste len : ", len(self.liste))
        n_simu = len(self.liste) * self.n_expo
        print("N : ", n_simu)
        print(self.liste)
        rank_list = list(pd.DataFrame({'word': self.liste}).groupby('word').cumcount().values)
        test_list = list(set(self.liste))
        initialize_data()
        pd.DataFrame.from_dict(self.dico).to_csv(self.csv_name, mode='w', header=True, index=False)
        self.param_product = [dict(zip(self.test, x)) for x in itertools.product(*self.test.values())]
        self.copy_model = copy.deepcopy(self.simu.model)
        for ip, indices in enumerate(self.param_product):
            self.simu.model = copy.deepcopy(self.copy_model)
            for p, val in indices.items():
                setattr(self.simu, p, val)
            logging.expe("learning..")
            for i, word in enumerate(self.liste):  # learning phase
                initialize_data()
                run_word(rank_list[i], word)
            if test_phase:
                logging.expe("testing")
                self.simu.model.learning = False
                self.simu.model.semantic.context_sem = False
                for i, word in enumerate(test_list):  # testing phase
                    run_word(rank_list[i], word)
        self.simu.dual_print(
            f"\n____________________________________________________________________________________\nEXPE SUMMARY\n____________________________________________________________________________________")
        self.simu.dual_print(
            f"Nombre de mots lus : {len(self.liste)} \nNombre de mots correctement lus : {self.reussite}\nPourcentage de réussite : {self.reussite / len(self.liste) * 100}\nPourcentage de mots nouveaux : {self.mots_inconnus / len(self.liste) * 100}")
