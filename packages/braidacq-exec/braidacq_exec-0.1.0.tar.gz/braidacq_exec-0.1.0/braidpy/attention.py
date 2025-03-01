import logging
import math
import pdb

import braidpy.utilities as utl
import braidpy.lexicon as lex
import numpy as np


class attention:
    """
    The attention class is an inner class of the modality class and represents the attentional submodel, either in the orthographic or phonological modality.

    """

    def __init__(self, modality, Q, mean, sd, sdM=5, segment_reading=False, reading_unit="None"):
        """
        Attention class constructor.

         :param Q : quantity of attention
         :param mean : float, position of the attentional focus
         :param sd : float, attentional dispersion
         :param sdM : float, max value of the attentional dispersion
         :param segment_reading: boolean. If set to True, the attention distribution is not Gaussian but uniform on 1 or several letters corresponding to one phoneme.
         :param reading_unit: boolean. Can be "None", "letter" or "grapheme"
        """
        self.modality = modality
        self.Q = Q
        self.mean = mean
        self.sd = sd
        self.sdM = sdM
        self.dist = None
        self.segment_reading = segment_reading
        self.reading_unit = reading_unit

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, value):
        """
        Sets attention position, starts at 0. Position should be set at -1 at the end of a simulation

        :param value: int, the position to be set.
        """
        if value < -1 or ('lexical' in self.__dict__ and self.modality.N is not None and value >= self.modality.N):
            logging.warning(f"bad mean position is trying to be set : {value}")
        self._mean = value

    @property
    def sd(self):
        return self._sd

    @sd.setter
    def sd(self, value):
        if value < 0:
            logging.warning("You're trying to set a negative value of sdA")
        sdM = self.__getattribute__("sdM") if hasattr(self, 'sdM') and self.sdM is not None else 10000
        self._sd = min(value, sdM)

    @property
    def sdM(self):
        return self._sdM

    @sdM.setter
    def sdM(self, value):
        if value < 0:
            logging.warning("You're trying to set a negative value of sdM")
        self._sdM = value
        self.__setattr__('sd', self.sd)

    @utl.abstractmethod
    def init_pos(self):
        """
        Sets the position of the attentional focus in each modality.
        """

    @utl.abstractmethod
    def build_attention_distribution(self):
        """
        Builds the attention distribution according to the attentional position mean, the standard deviation sd,
        the attentional Quantity Q and the length of the stimulus N.
        """
        pass


class attentionOrtho(attention):
    def __init__(self, modality, Q=1, mean=-1, sd=1.75, pos_init=-1, sdM=5, grapheme_overlap=0.1, **modality_args):
        """
        :param QL: Attention quantity during the comparison L/P
        """
        super().__init__(modality=modality, Q=Q, mean=mean, sd=sd, **modality_args)
        self.pos_init = pos_init
        self.sdM = sdM
        self.grapheme_overlap = grapheme_overlap

    def init_pos(self):
        """
        Sets the visual attention position (and also the gaze position) at the beginning of the simulation.
        If its value has already been set, the function do not change it. Otherwise, it is set automatically.
        """
        if self.pos_init != -1:
            self.modality.pos = self.pos_init
        elif self.reading_unit == "grapheme":
            self.mean = 0
            self.modality.pos, _ = self.next_grapheme()
        elif self.reading_unit == "bigram":
            self.modality.pos = 0
        elif self.reading_unit == "trigram":
            self.modality.pos = 1
        elif self.Q > 1.7 and self.sd > 1:
            self.modality.pos = [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4][self.modality.N - 1]
        else:
            self.modality.pos = 0

    def init_sd(self):
        """
        Initializes the attentional dispersion of the model : value changed only for the grapheme case
        """
        pass
        # if self.reading_unit=="grapheme":
        #    self.calculate_sigma_grapheme(self.modality.model.gs)

    def phlen2len(self, x, rnd=1):
        """
        Calculates the predicted phonological length as a function of the orthographic length according to the linear regression.

        :param x: the orthographic length
        :return: the predicted phonological length
        """
        return round(float((x - self.modality.model.phono.attention.coupling_b) / self.modality.model.phono.attention.coupling_a) / rnd) * rnd

    def position_mapping(self, pos_phono):
        """
        Chooses the next orthographic position according to the next phonological position.
        """
        pos_phono = pos_phono if pos_phono >= 0 else self.modality.pos
        phono = self.modality.model.phono
        if pos_phono == 0:
            self.modality.pos = 0
        elif pos_phono < 0:
            pass
        elif phono.attention.att_phono_auto and self.modality.stim in self.modality.model.df_graphemic_segmentation.index:
            gs = self.modality.model.gs
            str_phono = str(pos_phono)
            if str_phono in gs:
                self.modality.pos = gs.find(str_phono) + (gs.rfind(str_phono) - gs.find(str_phono)) // 2 if str_phono in gs else -1
                # self.modality.pos = self.modality.model.gs.index(str(phono.pos))
            else:
                self.modality.pos = len(self.modality.stim) - 1
        elif phono.attention.att_phono_auto:
            logging.simu("ATTENTION : segmentation graphémique absente!")
            pdb.set_trace()
        else:
            self.modality.pos = min(len(self.modality.stim) - 1, self.phlen2len(phono.pos))

    def build_attention_distribution(self):
        """
        Builds the distribution of attention according to the attention parameters.
        :return:
        """
        m = self.mean
        if m >= 0:
            # the attention distribution is concentrated on one phoneme only
            # phoneme decided by the graphemic segmentation
            if self.reading_unit == 'grapheme' and self.segment_reading and self.modality.model.phono.attention.att_phono_auto:
                gs = self.modality.model.gs
                len_grapheme = gs.count(gs[int(m)])
                # new_mean=gs.index(gs[int(m)])
                tmp = np.array([1 / len_grapheme if m <= i < m + len_grapheme else 0 for i in range(self.modality.M)])
            # ortho and phono segments correspond to one letter/phoneme
            elif self.reading_unit == "letter":
                tmp = np.array([1 if i == m else 0 for i in range(self.modality.N)])
            elif self.reading_unit == "bigram":
                tmp = np.array([1 / 2 if i == m or i == m + 1 else 0 for i in range(self.modality.N)])
            elif self.reading_unit == "trigram":
                tmp = np.array([1 / 3 if abs(m - i) <= 1 else 0 for i in range(self.modality.N)])
            else:
                tmp = utl.gaussian(self.mean, self.sd, self.modality.N)
                if self.segment_reading:
                    tmp = utl.gaussian_to_creneau(tmp)
            tmp = self.Q * tmp
            tmp[tmp > 1] = 1
            self.dist = tmp

    def next_grapheme(self):
        return self.calculate_milieu_grapheme(self.modality.model.gs)

    def calculate_milieu_grapheme(self, gs):
        """
        return the attentional position needed to have attention centered in the middle of the grapheme
        :param gs: string. The graphemic segmentation of the stimulus.
        """
        len_grapheme = gs.count(gs[int(self.mean)])
        grapheme_deb = gs.index(gs[int(self.mean)])
        if grapheme_deb + len_grapheme - 1 >= len(gs) or grapheme_deb < 0:
            print("Error : bad configuration of parameters")
        return int(grapheme_deb + (len_grapheme - 1) / 2), len_grapheme

    def calculate_sigma_grapheme(self, gs, threshold=0.001):
        """
        Calculates gaussian parameters to align visual attention with a single grapheme.

        :param gs: string. The graphemic segmentation of the stimulus.
        :param threshold: float. quntity of attention authorized outside the grapheme.
        :return: values for mu and sigma
        """
        mu, len_grapheme = self.calculate_milieu_grapheme(gs)
        sigma_min = 0.25
        sigma_max = 2.25
        fin = False
        calcule_min = True
        calcule_max = True
        while not fin:
            if calcule_min:
                mu_min_gaussian = utl.gaussian(mu, sigma_min, len(gs))
                mu_min_val = sum([val if abs(i - mu) > len_grapheme / 2 else 0 for i, val in enumerate(mu_min_gaussian)])
            if calcule_max:
                mu_max_gaussian = utl.gaussian(mu, sigma_max, len(gs))
                mu_max_val = sum([val if abs(i - mu) > len_grapheme / 2 else 0 for i, val in enumerate(mu_max_gaussian)])
            if abs(mu_min_val - self.grapheme_overlap) < threshold or abs(mu_max_val - self.grapheme_overlap) < threshold or mu_max_val < self.grapheme_overlap or mu_min_val > self.grapheme_overlap:
                fin = True
            if abs(mu_min_val - self.grapheme_overlap) < abs(mu_max_val - self.grapheme_overlap):
                calcule_min = False
                calcule_max = True
                sigma_max = (sigma_min + sigma_max) / 2
            else:
                calcule_max = False
                calcule_min = True
                sigma_min = (sigma_min + sigma_max) / 2
        self.modality.pos, self.sd = mu, round((sigma_max if calcule_min else sigma_min), 1)
        self.modality.model.phono.attention.position_mapping()


class attentionPhono(attention):
    def __init__(self, modality, Q=0.003, mean=-1, sd=2, att_phono_auto=False, **modality_args):
        """
        :param att_phono_auto: boolean. if True, automatically sets the phonological attention according to the graphemic segmentation
        """
        self.att_phono_auto = att_phono_auto
        self.coupling_a = self.coupling_b = None
        super().__init__(modality=modality, Q=Q, mean=mean, sd=sd, **modality_args)
        # def __init__(self, modality, Q=0.002, mean=-1, sd=2, att_phono_auto=False, **modality_args):

    def set_regression(self):
        """
        Performs linear regression to find the relationship between orthographic and phonological length.
        Use for attention coupling (matching orthographic positions to phonological positions)
        """
        from sklearn import linear_model
        x = self.modality.model.ortho.lexical.df.len.values.reshape(-1, 1)
        y = self.modality.lexical.df.len.values.reshape(-1, 1)
        reg = linear_model.LinearRegression()
        res = reg.fit(x, y)
        self.coupling_a, self.coupling_b = res.coef_[0][0], res.intercept_[0]

    def len2phlen(self, x, rnd=1):
        """
        Calculates the predicted phonological length as a function of the orthographic length according to the linear regression.

        :param x: the orthographic length
        :return: the predicted phonological length
        """
        return round(float(self.coupling_b + (self.coupling_a * x)) / rnd) * rnd

    def position_mapping(self, end_verif=False, ortho_pos=None):
        """
        Chooses the next phonological position and dispersion according to the orthographic position.
        """
        ortho_pos = ortho_pos if ortho_pos is not None else self.modality.model.ortho.pos
        if ortho_pos < 0:
            return
        elif ortho_pos == 0:
            self.modality.pos = 0
        elif self.reading_unit == "grapheme" or self.att_phono_auto and self.modality.model.ortho.stim in self.modality.model.df_graphemic_segmentation.index:
            self.modality.pos = int(self.modality.model.gs[int(self.modality.model.ortho.pos)])
        elif self.att_phono_auto:
            logging.simu("ATTENTION : segmentation graphémique absente!")
            pdb.set_trace()
        else:
            pos_tmp = round(self.len2phlen(self.modality.model.ortho.pos)) if self.coupling_a is not None else 0
            if end_verif:
                # we stop at the first # well perceived
                dz_pos = self.modality.percept.get_dz_pos(threshold=0.25)
                pos_tmp = min(pos_tmp, dz_pos)
            self.modality.pos = pos_tmp

    def dispersion_mapping(self, ortho_sd):
        self.sd = self.len2phlen(ortho_sd, rnd=0.05)

    def build_attention_distribution(self):
        """
        Builds the attention distribution according to the attention parameters.
        """
        if self.mean >= 0:
            mean_ortho = self.modality.model.ortho.attention.mean
            if self.reading_unit == "letter" or (self.reading_unit == "grapheme" and self.segment_reading):
                tmp = np.array([1 if i == self.mean else 0 for i in range(self.modality.M)])
            elif self.reading_unit == "bigram":
                mean_ortho = self.modality.model.ortho.attention.mean
                bigram_phono = self.modality.model.gs[mean_ortho:][:2]
                tmp = np.array([1 / len(bigram_phono) if str(i) in bigram_phono else 0 for i in range(self.modality.M)])
            elif self.reading_unit == "trigram":
                trigram_phono = list(set(self.modality.model.gs[mean_ortho - 1:][:3]))
                tmp = np.array([1 / len(trigram_phono) if str(i) in trigram_phono else 0 for i in range(self.modality.M)])
            else:
                tmp = np.array(utl.gaussian(self.mean, self.sd, self.modality.M))
                if self.segment_reading:
                    tmp = utl.gaussian_to_creneau(tmp)
            tmp = self.modality.model.ortho.attention.Q * self.Q * tmp
            # tmp =  self.Q * tmp
            tmp[tmp > 1] = 1
            self.dist = tmp
