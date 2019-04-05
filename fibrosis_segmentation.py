#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains the additional color segmentation algorithms used after the
color filters have been run
"""


import sklearn.linear_model as lm
import sklearn.neighbors as nei
import numpy as np

import settings

#categorize white pixes in other/unknown given the pixes which are white and
#colored from the rest of the image
def whiteVsColor(whiteMask,colorMask,otherMask,HSV):
    labels = np.ones(shape=(HSV.shape[0],HSV.shape[1]))*-1
    labels[whiteMask] = 0
    labels[colorMask] = 1

    HSVflat = np.reshape(HSV, (HSV.shape[0]*HSV.shape[1],3))
    labelsFlat = labels.flatten()
    whereCat = np.where(labelsFlat != -1)[0]
    whereOther = np.where(otherMask.flatten())[0]
    labelsFlatCat = labelsFlat[whereCat]
    HSVflatOther = HSVflat[whereOther,:]
    HSVflatCat = HSVflat[whereCat,:]

    regress = lm.LinearRegression()
    #regress = lm.Lars()
    regress.fit(HSVflatCat,labelsFlatCat)
    pred = regress.predict(HSVflatOther)
    pred_round = np.round(pred)
    #print(pred.min(),pred.max())

    whereOther2D = np.where(otherMask)
    otherwhiteMask = otherMask.copy()
    otherwhiteMask[whereOther2D[0][pred_round!=0],whereOther2D[1][pred_round!=0]] = False
    return otherwhiteMask

#segement out the white from other/unknown
#this uses linear regression on the already categorized white in order to
#predict which uncategorized pixels may be white
def findWhite(whiteMask,redMask,blueMask,otherMask,HSV):
    whiteVRedMask = whiteVsColor(whiteMask,redMask,otherMask,HSV)
    whiteVBlueMask = whiteVsColor(whiteMask,blueMask,otherMask,HSV)
    otherwhiteMask = whiteVRedMask & whiteVBlueMask
    return otherwhiteMask

#segement out blue and red from other/unkown
#this uses KNN to predict the color label for unkown pixels
def findBlueAndRed(whiteMask,redMask,blueMask,otherMask,HSV,RGB):
    def getWeights(dists):
        weights = np.zeros_like(dists)
        for i in range(dists.shape[0]):
            avg = np.mean(dists[i,:])
            std = np.std(dists[i,:])
            for j in range(dists.shape[1]):
                if dists[i,j] > avg+std*settings.stdevMultiplier:
                    weights[i,j] = 1
        return weights

    labels = np.ones(shape=(HSV.shape[0],HSV.shape[1]))*-1
    labels[redMask] = 0
    labels[blueMask] = 1

    whereWhite = np.where(whiteMask)
    numColor = np.sum(redMask)+np.sum(blueMask)
    numWhite = int(numColor*settings.frac_white/(1-settings.frac_white))
    whiteIdx = np.random.randint(0, len(whereWhite[0]), numWhite)
    labels[whereWhite[0][whiteIdx],whereWhite[1][whiteIdx]] = 2

    HSVflat = np.reshape(RGB, (RGB.shape[0]*RGB.shape[1],3))
    labelsFlat = labels.flatten()

    whereCat = np.where(labelsFlat != -1)[0]
    whereOther = np.where(otherMask.flatten())[0]
    labelsFlatCat = labelsFlat[whereCat]
    HSVflatOther = HSVflat[whereOther,:]
    HSVflatCat = HSVflat[whereCat,:]

    if settings.useWeights and 'weights' not in settings.KNN:
        settings.KNN['weights'] = getWeights

    regress = nei.KNeighborsClassifier(**settings.KNN)
    regress.fit(HSVflatCat,labelsFlatCat)
    pred_prob = regress.predict_proba(HSVflatOther)
    pred_round = np.argmax(pred_prob,axis=1)
    max_prob = np.max(pred_prob,axis=1)
    pred_round[max_prob < settings.min_consensus] = -1
    pred_round[pred_round == 2] = -1

    whereOther2D = np.where(otherMask)
    otherredMask = otherMask.copy()
    otherredMask[whereOther2D[0][pred_round!=0],whereOther2D[1][pred_round!=0]] = False
    otherblueMask = otherMask.copy()
    otherblueMask[whereOther2D[0][pred_round!=1],whereOther2D[1][pred_round!=1]] = False
    otherotherMask = otherMask.copy()
    otherotherMask[whereOther2D[0][pred_round!=-1],whereOther2D[1][pred_round!=-1]] = False

    return otherredMask, otherblueMask, otherotherMask
