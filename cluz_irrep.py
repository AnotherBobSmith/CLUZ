# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
 CLUZ for QGIS
                              -------------------
        begin                : 18-07-2015
        copyright            : (C) 2015 by Bob Smith, DICE
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

def makeIrrepInitVarDict(combsize, sites):
    irrepInitVarDict = {}

    mult = sites /(sites - 1)
    wt_include = float(combsize) / float(sites)
    wt_exclude = 1 - wt_include

    initVarDict["combsize"] = combsize
    initVarDict["mult"] = mult
    initVarDict["wt_include"] = wt_include
    initVarDict["wt_exclude"] = wt_exclude

    return irrepInitVarDict

def makeIrrepTot_Tot2FeatDict(setupObject, selectedTypeList):
    totFeatDict = {}
    totSqrFeatDict = {}

    typeSet = set(selectedTypeList)
    for puID in setupObject.abundPUKeyDict:
        puFeatDict = setupObject.abundPUKeyDict[puID]
        puFeatList = puFeatDict.keys()
        for featID in puFeatList:
            featType = setupObject.targetDict[featID][1]
            if featType in typeSet:
                featAmount = puFeatDict[featID]
                featSqrAmount = featAmount ** 2
                try:
                    runningTotAmount = totFeatDict[featID]
                except KeyError:
                    runningTotAmount = 0
                runningTotAmount += featAmount
                totFeatDict[featID] = runningTotAmount
                try:
                    runningTotSqrAmount = totSqrFeatDict[featID]
                except KeyError:
                    runningTotSqrAmount = 0
                runningTotSqrAmount += featSqrAmount
                totSqrFeatDict[featID] = runningTotSqrAmount

    return totFeatDict, totSqrFeatDict


def calcMeanAmountSD(featAmount, totFeatAmount, featAmountSqr, totFeatAmountSqr, mult):
    outsideAmount = (totFeatAmount - featAmount) * mult      #:=(sum[feature]-area_site)*mult;
    outsideSquaredAmount = (totFeatAmountSqr - featAmountSqr) * mult   #:=(sum2[feature]-area2_site)*mult;
    meanAmount = outsideAmount / sites             #:=sumarea/sites;

    sitesMinusOne = sites - 1
    combSizeMinusOne = combsize - 1
    if combSizeMinusOne > sitesMinusOne / 2.0:  #if (combsize-1) > (sites-1)/2.0 then
        combadj = math.sqrt(sitesMinusOne - combSizeMinusOne / combSizeMinusOne)            #combadj:=sqrt((sites-1)-(combsize-1))/(combsize-1)
    else:
        combadj = math.sqrt(combSizeMinusOne / combSizeMinusOne)        #combadj:=sqrt(combsize-1)/(combsize-1);

    sd = (math.sqrt((outsideSquaredAmount - (outsideAmount **2)/sites)/sites)) * combadj   #sd:=(sqrt((sumarea2-sqr(sumarea)/sites)/(sites)))*combadj;

    return meanAmount, sd

def calcUnitIrreplScore(setupObject, puID, irrepInitVarDict, totFeatDict, totSqrFeatDict):
    puAbundDict = setupObject.abundPUKeyDict[puID]
    combsize = float(irrepInitVarDict["combsize"])
    mult = irrepInitVarDict["mult"]
    wt_include = irrepInitVarDict["wt_include"]
    wt_exclude = irrepInitVarDict["wt_exclude"]

    print "wt_include =", wt_include
    print "wt_exclude =", wt_exclude
    print ""

    selectedFeatureList = totFeatDict.keys()
    selectedFeatureSet = set(selectedFeatureList)
    unitIrreplScore = 0

    for featID in puAbundDict:
        if featID in selectedFeatureSet:
            featAmount = float(puAbundDict[featID])
            featAmountSqr = featAmount ** 2
            totFeatAmount = float(totFeatDict[featID])
            totFeatAmountSqr = float(totSqrFeatDict[featID])
            featTarget = float(setupObject.targetDict[featID][3])

            meanAmount, sd = calcMeanAmountSD(featAmount, totFeatAmount, featAmountSqr, totFeatAmountSqr, mult)

            ### Calc repr_removed = Representative combinations when the site is removed
            if totFeatAmount - featAmount < featTarget: #if (sum[feature]-area_site) < target[feature] then
                repr_removed = 0.0             #repr_incexc[feature]:=0;
            else:
                mean_target = featTarget / (combsize - 1)   #mean_target:=target[feature]/(combsize-1);
                print "arse", featTarget, combsize, mean_target
                if sd < 0.00000000001:
                    if meanAmount < mean_target:
                        repr_removed = 0  #repr_incexc[feature]:=0
                    else:
                        repr_removed = 1   #repr_incexc[feature]:=1;
                else:
                    z = mean_target - meanAmount / sd   #z:=(mean_target-mean_site)/sd;
                    print "yyy", mean_target, meanAmount, sd, z
                    repr_removed = calcZprob(z)      #repr_incexc[feature]:=zprob(z);
            print "repr_removed =", repr_removed

            ### Calc repr_include  = Representative combinations when the site is included
            if featAmount >= featTarget:        #if area_site >= target[feature] then
                repr_include = 1       #repr_include[feature]:=1;
            else:
                mean_target = (featTarget - featAmount)/(combsize - 1);    #mean_target:=(target[feature]-area_site)/(combsize-1);
                if sd < 0.00000000001:
                    if meanAmount < mean_target:       #if mean_site < mean_target then
                        repr_include = 0       #repr_include[feature]:=0
                    else:
                       repr_include = 1   #repr_include[feature]:=1;
                else:
                    z = (mean_target - meanAmount)/sd    #z:=(mean_target-mean_site)/sd;
                    repr_include = calcZprob(z)   #repr_include[feature]:=zprob(z);

            print "repr_include =", repr_include

            ### Calc repr_exclude = Representative combinations when the site is excluded
            if totFeatAmount - featAmount < featTarget:          #if (sum[feature]-area_site) < target[feature] then
                repr_exclude = 0       #repr_exclude[feature]:=0;
            else:
                mean_target = featTarget / combsize       #mean_target:=target[feature]/(combsize);
                if sd < 0.00000000001:
                    if meanAmount < mean_target:
                        repr_exclude = 0       #repr_exclude[feature]:=0
                    else:
                       repr_exclude = 1         #repr_exclude[feature]:=1;
                else:
                    z = (mean_target - meanAmount) / sd   #z:=(mean_target-mean_site)/sd;
                    repr_exclude = calcZprob(z)    #repr_exclude[feature]:=zprob(z);
            print "repr_exclude =", repr_exclude

            ### Calc irr_feature
            if repr_include == 0 and featAmount > 0:    #if (repr_include[feature] = 0) and (area[site,feature] > 0) then
                finalRepr_include = 1                       #repr_include[feature]:=1;
            else:
                finalRepr_include = repr_include
            if repr_include == 0 and repr_exclude == 0:      #(repr_include[feature] + repr_exclude[feature]) = 0 then
                irr_feature = 0                 #irr_feature[feature]:=0
            else:
                irr_equationComp1 = (finalRepr_include - repr_removed) * wt_include
                irr_equationComp12 = (finalRepr_include * wt_include) + (repr_exclude * wt_exclude)
                irr_feature = irr_equationComp1 / irr_equationComp12    #irr_feature[feature]:=((repr_include[feature]-repr_incexc[feature])*wt_include) /(repr_include[feature]*wt_include+repr_exclude[feature]*wt_exclude);

            print "irr_feature = ", irr_feature
            unitIrreplScore += irr_feature

    return unitIrreplScore

def calcZprob(x):
    if x < 0:
        negative = True
        x = 0 - x
    else:
        negative = False
    if x > 50:
        x = 50
    sqrX = x * x
    z = 0.3989 * math.exp((0 - sqrX) / 2)
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
        finalValue = 1 - q * z
    else:
        finalValue = q * z

    return finalValue

dataDict = importIrrepData("C:\Users\Bob\Dropbox\Various\Q-CLUZ\Irreplaceability code\irr_data.txt")
combsize = 3
sites = len(dataDict.keys())
initVarDict = makeInitVarDict(combsize, sites)
totFeatDict = makeTotFeatDict(dataDict)
totSqrFeatDict = makeTotSqrFeatDict(dataDict)
target_proportion = 0.1
targetDict = makeTargetDict(totFeatDict, target_proportion)

unitID = 1
unitIrreplScore = calcUnitIrreplScore(unitID, initVarDict, dataDict, targetDict, totFeatDict, totSqrFeatDict)

print ""
print "Irrep = ", unitIrreplScore