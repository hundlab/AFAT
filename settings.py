#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

###############################################################################
# this function creates the color masks
# change it if the first pass is picking up the wrong colors
def createColorMasks(HSV, RGB):
    whiteMask = (HSV[...,1] <= 0.06) & (HSV[...,2] >= 0.8)
    redMask = (0.745 < HSV[...,0]) & (HSV[...,0] < 1) & np.logical_not(whiteMask)
    blueMask = (0.549 < HSV[...,0]) & (HSV[...,0] < 0.706) & (HSV[...,1] >= .1) & np.logical_not(whiteMask)
    otherMask = np.logical_not(whiteMask|blueMask|redMask)

    return whiteMask, redMask, blueMask, otherMask

###############################################################################
# k neighbors classifier settings
## this is the second pass which attempts to classify pixes missed in the first
## pass into blue, red, or unidentifiable. It does not classify white, that is
## is done separately

#raw settings for KNeighborsClassifier
#see https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier
KNN : dict = {'n_neighbors':5}

# dont classify points if the color is very different from red, blue or white
useWeights : bool = False
# number of standard deviations which makes a color very different
stdevMultiplier : float = 2

# minimum fraction of neighbors with the same label needed to classify a pixel
#default 1 or 100% of neighbors must be the same
min_consensus : float = 1

###############################################################################
# other settings

# show masks of the color filter results
show_firstPass = False

# save mask images to a directory
save_images = True

# show image plots
show_images = True
###############################################################################