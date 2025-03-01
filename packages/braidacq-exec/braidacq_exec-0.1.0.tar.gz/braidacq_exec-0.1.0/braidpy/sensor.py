import os
import pdb

import logging
import pandas as pd
import numpy as np
# BRAID utlities
import braidpy.utilities as utl
from braidpy import _ROOT


class sensor:
    """
    The sensor class is an inner class of the modality class and represents the sensory submodel, either in the orthographic or phonological modality.

    :param gaze: float. GazePosition at the beginning of the simulation.
    :param conf_mat_name : string. name of the confusion matrix file
    """

    def __init__(self, modality, gaze, conf_mat_name):
        self.modality = modality
        self._gaze = gaze
        self.dist = {}
        self.conf_mat_name = conf_mat_name
        self.build_confusion_matrix()

    @property
    def gaze(self):
        return self._gaze

    @gaze.setter
    def gaze(self, value):
        """
        Sets eye position, starts at 0. Position should be set at -1 at the end of a simulation

        :param value: int, the position to be set.
        """
        if value < -1 or ('lexical' in self.__dict__ and self.modality.N is not None and value >= self.modality.N):
            logging.warning(f"bad gaze position is trying to be set : {value}")
        self._gaze = value

    @utl.abstractmethod
    def build_confusion_matrix(self):
        """
        Sets the models confusion matrix
        """
        return

    @utl.abstractmethod
    def build_interference_matrix(self):
        """
        Computes the interference matrix.
        """
        return


class sensorOrtho(sensor):
    """
    The sensorOrtho class is an inner class of the modality class and represents the orthographic sensory submodel.

    :param crowding: float, crowding (lateral interferences) parameter.
    :param scaleI: float, parameter for low level visual extraction
    :param slopeG: float, parameter for the acuity gradient
    :param conf_factor: float, strength of the confusions between letters
    """

    def __init__(self, modality, gaze=-1, conf_mat_name="", crowding=0.675, scaleI=5.8, slopeG=1, conf_factor=1, **modality_args):
        self.crowding = crowding
        self.scaleI = scaleI
        self.slopeG = slopeG
        self._conf_factor = conf_factor
        super().__init__(modality, gaze, conf_mat_name, **modality_args)

    @property
    def conf_factor(self):
        return self._conf_factor

    @conf_factor.setter
    def conf_factor(self, value):
        self._conf_factor = value
        self.build_confusion_matrix()

    def build_confusion_matrix(self):
        """
        The function builds and selects relevant lines of a confusion matrix by reading data from an Excel file.
        """
        if len(self.conf_mat_name) == 0:
            self.conf_mat_name = "TownsendMod.csv" if self.modality.model.langue == "en" else "Simpson13Mod.csv"
        dict_path = os.path.join(_ROOT, 'resources/confusionMatrix/', self.conf_mat_name)
        self.dist["conf_mat"] = pd.read_csv(dict_path, header=None)
        self.modality.n = len(self.dist["conf_mat"].index)
        # needs to remove some letters to get the right size
        if self.modality.model.langue in ["ge", "fr"]:
            idx_forbid = [1, 2, 3, 4, 6, 9, 12, 13, 14, 20, 21, 28, 30, 31, 32, 33, 35, 40, 43, 44, 45] if self.modality.model.langue == "ge" else \
                [1, 2, 3, 4, 5, 6, 20, 21, 28, 30, 31, 32, 33, 34, 35, 40, 43, 44, 45, 46]
            idx = [i for i in range(len(self.dist["conf_mat"])) if i not in idx_forbid]
            self.dist["conf_mat"] = self.dist["conf_mat"].loc[idx, idx]
            self.dist["conf_mat"].reset_index(drop=True, inplace=True)
            self.dist["conf_mat"].columns = range(len(self.dist["conf_mat"].columns))
            self.modality.n = len(self.dist["conf_mat"].index)
            for i in range(self.modality.n):
                self.dist["conf_mat"][i] = self.dist["conf_mat"][i] / self.dist["conf_mat"][i].sum()
        for i in range(self.modality.n):
            self.dist["conf_mat"].loc[i, i] = float(self.dist["conf_mat"][i][i]) / self.conf_factor
            somme = sum(self.dist["conf_mat"].loc[i])
            self.dist["conf_mat"].loc[i] = self.dist["conf_mat"].loc[i] / somme

    def build_interference_matrix(self):
        """
        Computes the interference matrix, which is the product of the crowding matrix and the acuity matrix
        """
        # Sensory trace modified by the confusion matrix
        input_mat = self.build_sensor()
        # Acuity gradient
        acuity_mat = [(input_mat[..., x] + self.scaleI + abs(self.gaze - x) * self.slopeG) /
                      (1 + self.modality.n * (self.scaleI + abs(self.gaze - x) * self.slopeG)) for x in np.arange(input_mat.shape[1])]
        # lateral interferences
        crowding_mat = np.array([[self.crowding if i == j else (1 - self.crowding) / 2
                                  if abs(i - j) == 1 else 0 for j in range(self.modality.N)] for i in range(self.modality.N)])
        crowding_mat = crowding_mat / crowding_mat.sum(axis=1)[:, np.newaxis]
        self.dist["interference"] = np.dot(crowding_mat, acuity_mat)

    def build_sensor(self):
        """
        Extract from the confusion matrix lines corresponding to phonoemes/letters of the input
        If the sign is not a known letter, its distribution is considered as uniform

        :return: a numpy array which represents the sensory trace.
        """
        # this code block is part of the `_sensorortho` class and is responsible for building the sensory trace.
        if self.modality.N > self.modality.N_max:
            raise ValueError(f"String is longer than known words ({self.modality.N_max}), cannot handle this case")
        res = np.ones((self.modality.n, self.modality.N))
        for i in range(self.modality.N):
            res[:, i] = np.array(self.dist["conf_mat"][self.modality.lexical.chars.index(self.modality.stim[i])]) if self.modality.stim[i] != '~' else np.ones(self.modality.n) / self.modality.n
        return res


class sensorPhono(sensor):
    def __init__(self, modality, gaze=-1, conf_mat_name="", **modality_args):
        super().__init__(modality, gaze, conf_mat_name, **modality_args)

    def build_confusion_matrix(self):
        """
        Defines the phonological confusion matrix as an identity matrix, i.e. no confusion is implemented
        """
        self.dist["conf_mat"] = None

    def build_interference_matrix(self):
        """
        Defines the phonological confusion matrix as an identity matrix, i.e. no interference is implemented
        """
        self.dist["interference"] = None
