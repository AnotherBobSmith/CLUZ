from __future__ import division

# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
 CLUZ for QGIS
                             -------------------
        begin                : 2016-23-02
        copyright            : (C) 2016 by Bob Smith, DICE
        email                : r.j.smith@kent.ac.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import math


# {----------------------------------------------------------------------------}
def calcZprob(x):
    if x < 0:
        negative = True
        x = 0 - x
    else:
        negative = False
    if x > 50:
        x = 50
    z = 0.3989 * math.exp((0 - math.sqrt(x)) / 2)
    t = 1 / (1 + 0.23164 * x)
    m = t
    q = 0.31938 * m
    m = m * t
    q = q - 0.35656 * m
    m = m * t
    q = q + 1.78148 * m
    m = m * t
    q = q -1.82126 * m
    m = m * t
    q = q + 1.33027 * m
    if negative:
        zprob = 1 - q * z
    else:
        zprob = q * z

    return zprob



def calcFeatUnitIrreplValue(setupObject, initVarDict, puID, featID, sumFeatAmountDict, sumSqrFeatAmount2Dict, targetShortfallDict):
    totNumSites = initVarDict["totNumSites"]
    mult = initVarDict["mult"]

    featTarget = targetShortfallDict[featID][3]
    featAmount = setupObject.abundPUKeyDict[puID][featID]
    featAmountSqr = featAmount ** 2
    featSumAmount = (sumFeatAmountDict[featID] - featAmount) * mult
    featSumAmountSqr = (sumSqrFeatAmount2Dict[featID] - featAmountSqr) * mult
    meanFeatAmountPerPU = featSumAmount / totNumSites
    sd = calcStandardDev(featSumAmount, featSumAmountSqr, totNumSites)

    rxRemoved = calcRxRemoved(initVarDict, sd, featAmount, featTarget, meanFeatAmountPerPU, featSumAmount)
    rxIncluded = calcRxIncluded(initVarDict, sd, featAmount, featTarget, meanFeatAmountPerPU)
    rxExcluded = calcRxExcluded(initVarDict, sd, featAmount, featTarget, featSumAmount, meanFeatAmountPerPU)

    if (rxIncluded + rxExcluded) == 0:
        irrepValue = 0
    else:
        irrepValue = calcIrrFeature(initVarDict, rxRemoved, rxIncluded, rxExcluded, featAmount)

    return irrepValue


def calcStandardDev(featSumAmount, featSumAmountSqr, totNumSites):
    step1 = featSumAmountSqr - ((featSumAmount ** 2) / totNumSites) / totNumSites
    sd = math.sqrt(step1)

    return sd


def calcAdjustedPortfolioSize(totNumSites, portfolioSize):
    if portfolioSize > totNumSites / 2.0:
        adjustedPortfolioSize = math.sqrt(totNumSites - portfolioSize) / portfolioSize
    else:
        adjustedPortfolioSize = math.sqrt(portfolioSize) / portfolioSize

    return adjustedPortfolioSize


def calcRxRemoved(initVarDict, sd, featAmount, featTarget, meanFeatAmountPerPU, featSumAmount):
    totNumSites = initVarDict["totNumSites"]
    portfolioSize = initVarDict["portfolioSize"]
    meanTargetPerPortfolioSize = featTarget / (portfolioSize - 1)
    adjustedPortfolioSize = calcAdjustedPortfolioSize(totNumSites - 1, portfolioSize - 1)
    adjSD = sd * adjustedPortfolioSize
    z = "aaa"
    if (featSumAmount - featAmount) < featTarget:
        rxRemoved = 0
    else:
        if adjSD < 0.00000000001:
            if meanFeatAmountPerPU < meanTargetPerPortfolioSize:
                rxRemoved = 0
            else:
                 rxRemoved = 1
        else:
            z = (meanTargetPerPortfolioSize - meanFeatAmountPerPU) / adjSD
            rxRemoved = calcZprob(z)

    return rxRemoved


def calcRxIncluded(initVarDict, sd, featAmount, featTarget, meanFeatAmountPerPU):
    totNumSites = initVarDict["totNumSites"]
    portfolioSize = initVarDict["portfolioSize"]
    meanTargetPerPortfolioSize = (featTarget - featAmount) / (portfolioSize - 1)
    adjustedPortfolioSize = calcAdjustedPortfolioSize(totNumSites - 1, portfolioSize - 1)
    adjSD = sd * adjustedPortfolioSize
    z = "aaa"
    if featAmount >= featTarget:
        rxIncluded = 1
    else:
        if adjSD < 0.00000000001:
            if meanFeatAmountPerPU < meanTargetPerPortfolioSize:
                rxIncluded = 0
            else:
                rxIncluded = 1
        else:
             z = (meanTargetPerPortfolioSize - meanFeatAmountPerPU) / adjSD
             rxIncluded = calcZprob(z)

    return rxIncluded


def calcRxExcluded(initVarDict, sd, featAmount, featTarget, featSumAmount, meanFeatAmountPerPU):
    totNumSites = initVarDict["totNumSites"]
    portfolioSize = initVarDict["portfolioSize"]
    meanTargetPerPortfolioSize = featTarget / portfolioSize
    adjustedPortfolioSize = calcAdjustedPortfolioSize(totNumSites - 1, portfolioSize)
    adjSD = sd * adjustedPortfolioSize
    if (featSumAmount - featAmount) < featTarget:
        rxExcluded = 0
    else:
        if adjSD < 0.00000000001:
            if meanFeatAmountPerPU < meanTargetPerPortfolioSize:
                rxExcluded = 0
            else:
                rxExcluded = 1
        else:
            z = (meanTargetPerPortfolioSize - meanFeatAmountPerPU) / adjSD
            rxExcluded = calcZprob(z)

    return rxExcluded


def calcIrrFeature(initVarDict, rxRemoved, rxIncluded, rxExcluded, featAmount):
    wt_include = initVarDict["wt_include"]
    wt_exclude = initVarDict["wt_exclude"]

    if rxIncluded == 0 and featAmount > 0:
        rxIncluded = 1
    if rxIncluded + rxExcluded == 0:
        irr_feature = 0
    else:
        irr_feature = ((rxIncluded - rxRemoved) * wt_include) / (rxIncluded * wt_include + rxExcluded * wt_exclude)

    return irr_feature
