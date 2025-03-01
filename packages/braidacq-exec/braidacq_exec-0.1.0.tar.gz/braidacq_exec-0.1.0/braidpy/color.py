#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""color.py: [a file of the BRAID software] Color submodule for STROOP extension."""
__copyright__ = "2022, CNRS, UGA"
__authors__ = "Diard, Valdois, Phénix, Ginestet, Saghiran, Steinhilber, Charrier"
__contact__ = "Julien Diard, julien.diard@univ-grenoble-alpes.fr"
__date__ = "Nov 03 2022"

# General purpose libraries
import os
# debugging
import numpy as np
from numpy import linalg as LA
# Scientific/Numerical computing
import pandas as pd
import braidpy.utilities as utl
from braidpy import _ROOT


class color:
    """Color modality for an orthographic input

    stim_color: 1D array, RGB value of the stimulus
    enabled: boolean, activation status of the color submodel
    dist: dict, equivalent of modality's dist variable, contains the different probabilities
            distributions used by the color class
            - "input_dist" : probability of the color stimulus (given each color word)
            - "color_words" : probability of each color word of the lexicon
    lexicon_color_name: string, name of the color lexicon, which contains color names
            and RGB values, must be situated in 'ressources/color/' repository
    rgb_sigma: float, sigma for color 3D distributions (here, we consider the same sigma for
            R, G and B distributions)
    rgb_cov: float, covariance value for 3D distributions (here, we consider the same covariance
            value for every couple of color in RGB space)
    model: braid, reference to the model using this color submodel
    alpha_color: float, parameter of accumulation speed during color word identification (between C and Wc)
    alpha_wc: float, parameter of influence strength from color over ortho and phono modalities
    dynamic_color: boolean, activation status of the dynamic accumulation during color word identification
    """

    def __init__(self, stim_color=[255, 0, 0], enabled=False, dist=None, lexicon_color_name="color.csv", rgb_sigma=20,
                 rgb_cov=0, model=None, alpha_color=0.01, alpha_wcolor=0.05, dynamic_color=False):

        self.color_dict = None
        self.stim_color = stim_color
        self.enabled = enabled
        self.dist = dist
        self.color_index = None
        self.model = model
        self.lexicon_color_name = lexicon_color_name
        self.sigma_color = [[rgb_sigma ** 2, rgb_cov, rgb_cov], [rgb_cov, rgb_sigma ** 2, rgb_cov],
                            [rgb_cov, rgb_cov, rgb_sigma ** 2]]
        self.alpha_color = alpha_color
        self.alpha_wcolor = alpha_wcolor
        self.dynamic_color = dynamic_color

    def init_color(self):
        self.init_color_dist()
        self.color_input_dist()

    def set_color_dict(self):
        """Import and initialize the color lexicon of the model (i.e. all color words with RGB values)"""

        df_rgb = pd.read_csv(os.path.join(_ROOT, 'resources/color/', self.lexicon_color_name), keep_default_na=False)

        rgb_list = []

        for row_color in df_rgb.itertuples():
            rgb_list.append([row_color.R, row_color.G, row_color.B])

        df_rgb["RGB"] = rgb_list

        dict_rgb = dict(zip(df_rgb["color"], df_rgb["RGB"]))

        self.color_dict = dict_rgb

    def init_color_dist(self):
        """Initialise the probability distribution over the color lexicon at uniform"""

        self.dist["color_words"] = utl.uniform(len(self.color_dict))

    def color_input_dist(self):
        """Calculate the probability of the color for each word of the color lexicon"""

        if len(self.stim_color) == np.shape(self.sigma_color)[0]:

            det = LA.det(self.sigma_color)

            if det == 0:
                raise NameError("The covariance matrix can't be singular")

            self.dist["input_dist"] = []
            inv = LA.inv(self.sigma_color)

            for color_name, color_rgb in self.color_dict.items():
                x_mu = np.subtract(np.array(self.stim_color), np.array(color_rgb))
                norm_const = 1.0 / (np.power((2 * np.pi), len(self.stim_color) / 2) * np.power(det, 1.0 / 2))
                value = norm_const * (np.exp(-0.5 * (x_mu.dot(inv).dot(x_mu.T))))
                self.dist["input_dist"].append(value)
            self.dist["input_dist"] = utl.norm1D(self.dist["input_dist"])

        else:
            raise NameError("The dimensions of the input don't match")

    def color_bottom_up(self):
        """Bottom-up color information integration over the color words distribution"""

        if self.dynamic_color:
            self.dist["color_words"] = utl.norm1D(self.dist["color_words"] * (self.alpha_color * self.dist["input_dist"]
                                                  + (1 - self.alpha_color) / len(self.dist["color_words"])))
            # self.dist["color_words"] = utl.norm1D(self.alpha_color * self.dist["color_words"] * self.dist["input_dist"] \
            #                                      + (1 - self.alpha_color) / len(self.dist["color_words"]))
        else:
            self.dist["color_words"] = self.dist["input_dist"]

    def color_words_index(self):
        """Get indexes of words in the color lexicon from the ortho/phono lexicon
         to create correspondances between both lexicons"""

        self.color_index = {key: self.model.lexicon.loc[key].idx for key in self.color_dict.keys()}

        return self.color_index
