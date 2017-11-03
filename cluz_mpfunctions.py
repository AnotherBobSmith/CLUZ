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

import qgis
from qgis.core import *
from qgis.gui import *

import cluz_setup

def puStatusDoesNotEqualExcluded(unitDictionary, puID):
    notExcludedBool = True
    if unitDictionary[puID][1] == 3:
        notExcludedBool = False

    return notExcludedBool

def puStatusIsEarmarkedOrConserved(unitDictionary, puID):
    isEarmarkedOrConserved = False
    if unitDictionary[puID][1] == 1 or unitDictionary[puID][1] == 2:
        isEarmarkedOrConserved = True

    return isEarmarkedOrConserved

def makePatchDict(unitDict, minpatchDataDictionary):
    areaDict = minpatchDataDictionary["areaDictionary"]
    boundaryMatrixDict = minpatchDataDictionary["boundaryMatrixDictionary"]
    patchDict = dict()
    patchID = 1
    runningPortfolioPUIDSet = makePortfolioPUIDSet(unitDict) #To contain data on all PUs in portfolio, then each PU will be removed & assiged to a patch

    while len(runningPortfolioPUIDSet) > 0:
        patchPUIDSet = makePatchPUIDSet(boundaryMatrixDict, runningPortfolioPUIDSet, patchID)
        runningPortfolioPUIDSet = runningPortfolioPUIDSet.difference(patchPUIDSet)
        patchPUIDList = list(patchPUIDSet)
        patchPUIDList.sort()
        patchArea = returnPatchArea(areaDict, patchPUIDList)
        patchDict[patchID] = [patchArea, len(patchPUIDList), patchPUIDList]
        patchID += 1

    return patchDict


def makePortfolioPUIDSet(unitDict):
    portfolioPUIDSet = set()
    for puID in unitDict:
        if puStatusIsEarmarkedOrConserved(unitDict, puID):
            portfolioPUIDSet.add(puID)

    return portfolioPUIDSet


def makePatchPUIDSet(boundaryMatrixDict, runningPortfolioPUIDSet, patchID):
    loopUnitSet = set()
    patchPUIDSet = set()
    initialPUID = list(runningPortfolioPUIDSet)[0]
    loopUnitSet.add(initialPUID)

    while len(loopUnitSet) > 0:
        puID = loopUnitSet.pop()
        patchPUIDSet.add(puID)
        neighbList = boundaryMatrixDict[puID]
        if len(neighbList) > 0:
            for neighbPUID in neighbList:
                if neighbPUID in runningPortfolioPUIDSet and neighbPUID not in patchPUIDSet:
                    loopUnitSet.add(neighbPUID)

    return patchPUIDSet


def returnPatchArea(areaDict, patchPUIDList):
    patchArea = 0
    for puID in patchPUIDList:
        patchArea += areaDict[puID]

    return patchArea


def remSmallPatchesFromUnitDict(minpatchDataDict, unitDict, patchDict):
    preMarxanUnitDict = minpatchDataDict["initialUnitDictionary"]
    zoneDict = minpatchDataDict["zoneDictionary"]

    for patchID in patchDict:
        patchSize = patchDict[patchID][0]
        patchSizeThreshold = calcPatchSizeThreshold(zoneDict, patchDict, patchID)

        if patchSize < patchSizeThreshold:
            patchIDList = patchDict[patchID][2]
            for unitIDValue in patchIDList:
                origStatus = preMarxanUnitDict[unitIDValue][1]
                unitList = unitDict[unitIDValue]
                unitStatus = unitList[1]
                if origStatus == 0 and unitStatus == 1:
                    unitList[1] = 0
                    unitDict[unitIDValue] = unitList

    return unitDict

def calcPatchSizeThreshold(zoneDict, patchDict, patchID):
    patchPUIDList = patchDict[patchID][2]
    if len(zoneDict) == 1:
        firstPUID = patchPUIDList[0] #Takes patch threshold size from first PU, as every PU has same threshold
        patchSizeThreshold = zoneDict[firstPUID][1]
    else:
        patchPUIDList = patchDict[patchID][2]
        patchSizeThreshold = "blank"
        for puID in patchPUIDList:
            puPatchThreshold = zoneDict[puID][1]
            if patchSizeThreshold == "blank":
                patchSizeThreshold = puPatchThreshold
            if patchSizeThreshold < puPatchThreshold:
                patchSizeThreshold = puPatchThreshold

    return patchSizeThreshold


def addPatches(minpatchDataDict, runningUnitDict):
    continueBool = True
    featAmountConsDict = makeFeatAmountConsDict(minpatchDataDict, runningUnitDict)
    unmetTargetIDSet = makeUnmetTargetIDSet(featAmountConsDict, minpatchDataDict)
    puSelectionSet = makePUSelectionSet(minpatchDataDict, runningUnitDict)
    puPatchSetDict = makePUPatchSetDict(puSelectionSet, minpatchDataDict)
    allPUPatchAbundDict = makePUPatchAbundDict(minpatchDataDict, runningUnitDict, puSelectionSet, puPatchSetDict, unmetTargetIDSet)

    while len(unmetTargetIDSet) > 0:
        puPatchScoreDict = makePUPatchScoreDict(minpatchDataDict, featAmountConsDict, allPUPatchAbundDict, puSelectionSet)
        puID = returnBestPU(puPatchScoreDict)

        if puID == -1:
            featIDListString = makeFeatureIDListOfUnmeetableTargetsString(unmetTargetIDSet)
            qgis.utils.iface.messageBar().pushMessage("Target error: ", "Targets for the following features cannot be met: " + featIDListString +". This occurs when there is not enough of the relevant features found in patches with the specified minimum area. MinPatch has been terminated.", QgsMessageBar.WARNING)
            continueBool = False
            break

        runningUnitDict = addPatch(minpatchDataDict, runningUnitDict, puID)
        puSelectionSet.remove(puID)

        allPUPatchAbundDict = updatePUPatchAbundDict(allPUPatchAbundDict, minpatchDataDict, runningUnitDict, puSelectionSet, puPatchSetDict, unmetTargetIDSet, puID)
        featAmountConsDict = makeFeatAmountConsDict(minpatchDataDict, runningUnitDict)
        unmetTargetIDSet = makeUnmetTargetIDSet(featAmountConsDict, minpatchDataDict)

    return runningUnitDict, continueBool


def makeFeatureIDListOfUnmeetableTargetsString(unmetTargetIDSet):
    featIDListString = ""
    for featID in unmetTargetIDSet:
        featIDListString = featIDListString + str(featID) + ", "

    finalFeatIDListString = featIDListString[0:-2]

    return finalFeatIDListString


def makeFeatAmountConsDict(minpatchDataDict, unitDict):
    targetDict = minpatchDataDict["targetDictionary"]
    abundanceMatrixDict = minpatchDataDict["abundanceMatrixDictionary"]

    featAmountConsDict = dict(zip(targetDict.keys(), len(targetDict.keys()) * [0]))

    for puID in abundanceMatrixDict:
        puStatus = unitDict[puID][1]
        if puStatus == 1 or puStatus == 2:
            puAbundDict = abundanceMatrixDict[puID]
            for featID in puAbundDict:
                featAmount = puAbundDict[featID]
                conTotalAmount = featAmountConsDict[featID]
                conTotalAmount += featAmount
                featAmountConsDict[featID] = conTotalAmount

    return featAmountConsDict

def makeUnmetTargetIDSet(amountConDict, minpatchDataDict):
    unmetTargetSet = set()
    targetDict = minpatchDataDict["targetDictionary"]
    for featID in amountConDict:
        amountConserved = amountConDict[featID]
        targetValue = targetDict[featID][1]

        if targetValue > 0 and amountConserved < targetValue:
            unmetTargetSet.add(featID)

    return unmetTargetSet

def makePUSelectionSet(minpatchDataDictionary, runningUnitDict):
    puSelectionSet = set()
    addPatchPUIDDict = minpatchDataDictionary["addPatchPUIDDictionary"]
    for puID in runningUnitDict:
        if puStatusDoesNotEqualExcluded(runningUnitDict, puID):
            neighbPatchIDList = addPatchPUIDDict[puID]
            if len(neighbPatchIDList) > 0:
                puSelectionSet.add(puID)

    return puSelectionSet

def makePUPatchSetDict(puSelectionSet, minpatchDataDictionary):
    puPatchSetDict = {}
    addPatchPUIDDict = minpatchDataDictionary["addPatchPUIDDictionary"]
    for puID in puSelectionSet:
        puSet = set(addPatchPUIDDict[puID])
        puSet.add(puID)
        puPatchSetDict[puID] = puSet

    return puPatchSetDict

def makePUPatchAbundDict(minpatchDataDict, unitDict, puSelectionSet, puPatchSetDict, unmetTargetIDSet):
    allPUPatchAbundDict = {}
    for puID in puSelectionSet:
        patchCost = returnSinglePUPatchCost(unitDict, puPatchSetDict, puID)
        puPatchAbundDict = makeSinglePUPatchAbundDict(minpatchDataDict, unitDict, puPatchSetDict, unmetTargetIDSet, puID)
        allPUPatchAbundDict[puID] = [puPatchAbundDict, patchCost]

    return allPUPatchAbundDict

def returnSinglePUPatchCost(unitDict, puPatchSetDict, puID):
    patchPUIDSet = puPatchSetDict[puID]
    patchCost = 0

    for puPatchID in patchPUIDSet:
        puStatus = unitDict[puPatchID][1]
        puCost = unitDict[puPatchID][0]
        if puStatus == 0:
            patchCost += puCost

    return patchCost

def makeSinglePUPatchAbundDict(minpatchDataDict, unitDict, puPatchSetDict, unmetTargetIDSet, puID):
    abundMatrixDict = minpatchDataDict["abundanceMatrixDictionary"]
    patchPUIDSet = puPatchSetDict[puID]
    puPatchAbundDict = {}

    for featID in unmetTargetIDSet:
        patchAmount = 0
        for puPatchID in patchPUIDSet:
            puPatchStatus = unitDict[puPatchID][1]
            if puPatchStatus == 0:
                abundDict = abundMatrixDict[puPatchID]
                try:
                    abundAmount = abundDict[featID]
                except KeyError:
                    abundAmount = 0
                patchAmount += abundAmount
        if patchAmount > 0:
            puPatchAbundDict[featID] = patchAmount

    return puPatchAbundDict

def makePUPatchScoreDict(minpatchDataDictionary, featAmountConsDict, allPUPatchAbundDict, puSelectionSet):
    puPatchScoreDict = {}
    for puID in puSelectionSet:
        puPatchScoreDict[puID] = calcPUPatchScore(minpatchDataDictionary, featAmountConsDict, allPUPatchAbundDict, puID)

    return puPatchScoreDict

def calcPUPatchScore(minpatchDataDictionary, featAmountConsDict, allPUPatchAbundDict, puID):
    targetDict = minpatchDataDictionary["targetDictionary"]
    puScore = 0
    puPatchAbundDict = allPUPatchAbundDict[puID][0]
    puPatchCost = allPUPatchAbundDict[puID][1]
    for featID in puPatchAbundDict:
        featScore = calcPUPatchFeatureScore(targetDict, featAmountConsDict, puPatchAbundDict, featID)
        if featScore <> "blank":
            puScore += featScore

    try:
        finalpuScore = puScore / puPatchCost
    except ArithmeticError:
        finalpuScore = 0

    return finalpuScore

def calcPUPatchFeatureScore(targetDict, featAmountConsDict, puPatchAbundDict, featID):
    featScore = "blank"
    patchAmount = puPatchAbundDict[featID]
    targetAmount = targetDict[featID][1]
    conAmount = featAmountConsDict[featID]
    targetGap = targetAmount - conAmount
    if targetGap > 0:
        featScore = patchAmount / targetGap

        if featScore > 1: ####Reduce featScore if over 1, as we only need to meet the target
            featScore = 1

    return featScore

def returnBestPU(puPatchScoreDictionary):
    puIDValue = -1
    runningScore = 0
    for puValue in puPatchScoreDictionary:
        scoreValue = puPatchScoreDictionary[puValue]
        #If joint equal then always selects first PU in list
        if scoreValue > runningScore:
            runningScore = scoreValue
            puIDValue = puValue

    return puIDValue

def addPatch(minpatchDataDictionary, unitDictionary, puIDValue):
    addPatchPUIDDict = minpatchDataDictionary["addPatchPUIDDictionary"]
    initPUList = addPatchPUIDDict[puIDValue]
    puList = initPUList + [puIDValue]
    for aPUIDValue in puList:
        puList = unitDictionary[aPUIDValue]
        puStatus = puList[1]
        if puStatus == 0:
            puList[1] = 1
            unitDictionary[aPUIDValue] = puList
    return unitDictionary

def updatePUPatchAbundDict(allPUPatchAbundDict, minpatchDataDict, unitDict, puSelectionList, puPatchSetDict, unmetTargetIDList, bestPUID):
    abundMatrixDict = minpatchDataDict["abundanceMatrixDictionary"]
    bestPatchSet = puPatchSetDict[bestPUID]

    for aPatchCentrePU in puSelectionList:
        aPatchPUIDSet = puPatchSetDict[aPatchCentrePU]
        setOverLap = bestPatchSet.intersection(aPatchPUIDSet)
        if len(setOverLap) > 0:
            aPatchCost = 0
            for bPUID in aPatchPUIDSet:
                bPUStatus = unitDict[bPUID][1]
                bPUCost = unitDict[bPUID][0]
                if bPUStatus == 0:
                    aPatchCost += bPUCost

            puPatchAbundDict = {}
            for featID in unmetTargetIDList:
                featPatchAmount = 0
                for cPUID in aPatchPUIDSet:
                    abundDict = abundMatrixDict[cPUID]
                    if unitDict[cPUID][1] == 0 and featID in abundDict:
                        abundAmount = abundDict[featID]
                        featPatchAmount += abundAmount
                if featPatchAmount > 0:
                    puPatchAbundDict[featID] = featPatchAmount

            allPUPatchAbundDict[aPatchCentrePU] = [puPatchAbundDict, aPatchCost]

    return allPUPatchAbundDict

def runSimWhittle(runningUnitDict, minpatchDataDict):
    patchDict = makePatchDict(runningUnitDict, minpatchDataDict)
    rawEdgePUIDSet = makeEdgePUIDSet(runningUnitDict, minpatchDataDict)
    puPatchIDDict = makePUPatchIDDict(runningUnitDict, patchDict)
    featAmountConsDict = makeFeatAmountConsDict(minpatchDataDict, runningUnitDict)
    keystonePUIDSet = set()     #Keystone list is of PUs that can't be removed without affecting patch size or targets
    costlyPUIDSet = set()       #List of PUs that increases portfolio so shouldn't be removed. PUs REMOVED WHEN NEIGHBOURING PLANNING UNITS ARE WHITTLED.

    candidateEdgePUIDSet, keystonePUIDSet = makeEdgePUIDSets(minpatchDataDict, runningUnitDict, patchDict, puPatchIDDict, rawEdgePUIDSet, keystonePUIDSet)

    whittlePUID = "initialising"
    while whittlePUID <> "blank":
        whittleScoreDict, keystonePUIDSet = makeWhittleScoreDict_KeystoneSet(minpatchDataDict, featAmountConsDict, candidateEdgePUIDSet, keystonePUIDSet)
        whittlePUID, keystonePUIDSet, costlyPUIDSet = returnWhittlePUID_KeystoneSet(minpatchDataDict, runningUnitDict, patchDict, puPatchIDDict, whittleScoreDict, keystonePUIDSet, costlyPUIDSet)
        if whittlePUID <> "blank":
            runningUnitDict = removeWhittlePU(runningUnitDict, whittlePUID)
            featAmountConsDict = makeFeatAmountConsDict(minpatchDataDict, runningUnitDict)
            patchDict = makePatchDict(runningUnitDict, minpatchDataDict)
            puPatchIDDict = makePUPatchIDDict(runningUnitDict, patchDict)

            candidateEdgePUIDSet.remove(whittlePUID)

            costlyPUIDSet = updateCostlyPUIDSetToRemoveNeighbOfWhittlePUID(minpatchDataDict, costlyPUIDSet, whittlePUID)
            excludedFromCandidateEdgePUIDSet = keystonePUIDSet.union(costlyPUIDSet)

            candidateEdgePUIDSet = candidateEdgePUIDSet.difference(excludedFromCandidateEdgePUIDSet)
            neighbEdgePUSet = makeNeighbEdgePUSet(minpatchDataDict, runningUnitDict, excludedFromCandidateEdgePUIDSet, whittlePUID)
            candidateEdgePUIDSet = candidateEdgePUIDSet.union(neighbEdgePUSet)

    return runningUnitDict

def updateCostlyPUIDSetToRemoveNeighbOfWhittlePUID(minpatchDataDict, costlyPUIDSet, puID):
    boundMatrixDict = minpatchDataDict["boundaryMatrixDictionary"]
    neighbList = boundMatrixDict[puID].keys()
    neighbSet = set(neighbList)

    updatedCostlyPUIDSet = costlyPUIDSet.difference(neighbSet)

    return updatedCostlyPUIDSet

def returnWhittlePUID_KeystoneSet(minpatchDataDict, unitDict, patchDict, puPatchIDDict, whittleScoreDict, keystonePUIDSet, costlyPUIDSet):
    boundMatrixDict = minpatchDataDict["boundaryMatrixDictionary"]
    whittlePUID = "blank"
    while whittleScoreDictNotEmpty(whittleScoreDict) and whittlePUID == "blank":
        candidatePUID = returnCandidateWhittlePUID(whittleScoreDict)
        if removingPUIncreasesMarxanCost(minpatchDataDict, unitDict, boundMatrixDict, candidatePUID):
            costlyPUIDSet.add(candidatePUID)
            whittleScoreDict.pop(candidatePUID)
        else:
            if removingPUMakesPatchTooSmall(minpatchDataDict, patchDict, puPatchIDDict, candidatePUID):
                keystonePUIDSet.add(candidatePUID)
                whittleScoreDict.pop(candidatePUID)
            else:
                if removingPUSplitsIntoNonviablePatches(minpatchDataDict, unitDict, patchDict, puPatchIDDict, candidatePUID):
                    keystonePUIDSet.add(candidatePUID)
                    whittleScoreDict.pop(candidatePUID)
                else:
                    whittlePUID = candidatePUID

    return whittlePUID, keystonePUIDSet, costlyPUIDSet

def removingPUSplitsIntoNonviablePatches(minpatchDataDict, unitDict, patchDict, puPatchIDDict, candidatePUID):
    zoneDict = minpatchDataDict["zoneDictionary"]
    removingPUSplitsIntoNonviablePatchesBool = False

    afterSplitPatchDict = makeAfterSplitPatchDict(minpatchDataDict, unitDict, patchDict, puPatchIDDict, candidatePUID)

    for patchID in afterSplitPatchDict:
        patchSizeThreshold = calcPatchSizeThreshold(zoneDict, afterSplitPatchDict, patchID)
        if afterSplitPatchDict[patchID][0] < patchSizeThreshold:
            removingPUSplitsIntoNonviablePatchesBool = True


    return removingPUSplitsIntoNonviablePatchesBool

def makeAfterSplitPatchDict(minpatchDataDict, unitDict, patchDict, puPatchIDDict, candidatePUID):
    toSplitPatchPUDict = {}
    patchID = puPatchIDDict[candidatePUID]
    patchPUIDList = patchDict[patchID][2]

    for puID in patchPUIDList:
        toSplitPatchPUDict[puID] = unitDict[puID]
    toSplitPatchPUDict.pop(candidatePUID)

    afterSplitPatchDict = makePatchDict(toSplitPatchPUDict, minpatchDataDict)

    return afterSplitPatchDict

def removingPUMakesPatchTooSmall(minpatchDataDict, patchDict, puPatchIDDict, puID):
    areaDict = minpatchDataDict["areaDictionary"]
    zoneDict = minpatchDataDict["zoneDictionary"]
    removingPUMakesPatchTooSmallBool = False

    puSize = areaDict[puID]
    patchID = puPatchIDDict[puID]
    patchSize = patchDict[patchID][0]
    patchSizeThreshold = calcPatchSizeThreshold(zoneDict, patchDict, patchID)
    if patchSize - puSize < patchSizeThreshold:
        removingPUMakesPatchTooSmallBool = True

    return removingPUMakesPatchTooSmallBool

def whittleScoreDictNotEmpty(whittleScoreDict):
    isWhittleScoreDictNotEmpty = True
    if len(whittleScoreDict) == 0:
        isWhittleScoreDictNotEmpty = False

    return isWhittleScoreDictNotEmpty

def returnCandidateWhittlePUID(whittleScoreDict):
    candidatePUID = "blank"
    candidateScore = "blank"
    for puID in whittleScoreDict:
        whittleScore = whittleScoreDict[puID]
        if candidatePUID == "blank" or whittleScore < candidateScore:
            candidateScore = whittleScore
            candidatePUID = puID
        if whittleScore < candidateScore:
            candidateScore = whittleScore
            candidatePUID = puID

    return candidatePUID

def makeNeighbEdgePUSet(minpatchDataDict, unitDict, keystonePUIDSet, puID):
    boundMatrixDict = minpatchDataDict["boundaryMatrixDictionary"]
    neighbList = boundMatrixDict[puID].keys()
    neighbEdgeSet = set()
    for neighbPUID in neighbList:
        neighbPUIsOnEdge = False
        if neighbPUID not in keystonePUIDSet and unitDict[neighbPUID][1] == 1:
            neighbNeighbList = boundMatrixDict[neighbPUID].keys()
            for neighbNeighbPUID in neighbNeighbList:
                neighbNeighbStatus = unitDict[neighbNeighbPUID][1]
                if neighbNeighbStatus == 0 or neighbNeighbStatus == 3:
                    neighbPUIsOnEdge = True
            if neighbPUIsOnEdge:
                neighbEdgeSet.add(neighbPUID)

    return neighbEdgeSet

def makeEdgePUIDSets(minpatchDataDict, unitDict, patchDict, puPatchIDDict, edgePUIDSet, keystonePUIDSet):
    preMarxanUnitDict = minpatchDataDict["initialUnitDictionary"]
    areaDict = minpatchDataDict["areaDictionary"]
    zoneDict = minpatchDataDict["zoneDictionary"]

    viableEdgePUIDSet = set()
    for edgePU in edgePUIDSet:
        edgePUStatus = unitDict[edgePU][1]
        edgePUInitStatus = preMarxanUnitDict[edgePU][1]

        if edgePUStatus == 1 and edgePUInitStatus <> 2:
            edgePUArea = areaDict[edgePU]
            edgePUPatchID = puPatchIDDict[edgePU]
            patchArea = patchDict[edgePUPatchID][0]
            patchAreaWithPURemoved = patchArea - edgePUArea

            minPatchSize = lookupMinSizeValueOfPatch(zoneDict, patchDict, edgePUPatchID)

            if edgePUStatus == 1 and patchAreaWithPURemoved >= minPatchSize:
                viableEdgePUIDSet.add(edgePU)
            elif edgePUStatus == 1 and patchAreaWithPURemoved < minPatchSize:
                keystonePUIDSet.add(edgePU)

    return viableEdgePUIDSet, keystonePUIDSet

def makePUPatchIDDict(unitDict, patchDict):
    puPatchIDDict = dict(zip(unitDict.keys(), len(unitDict.keys()) * [0]))
    for patchID in patchDict:
        patchList = patchDict[patchID][2]
        for patchPUID in patchList:
            puPatchIDDict[patchPUID] = patchID

    return puPatchIDDict

def makeWhittleScoreDict_KeystoneSet(minpatchDataDict, featAmountConsDict, edgePUIDSet, keystonePUIDSet):
    abundMatrixDict = minpatchDataDict["abundanceMatrixDictionary"]
    targetDict = minpatchDataDict["targetDictionary"]
    whittleScoreDict = {}

    for edgePUID in edgePUIDSet:
        whittleScore = calcPUWhittleScore(abundMatrixDict, targetDict, featAmountConsDict, edgePUID)
        if whittleScore == "PU cannot be whittled, as needed to meet targets":
            keystonePUIDSet.add(edgePUID)
        else:
            whittleScoreDict[edgePUID] = whittleScore

    return whittleScoreDict, keystonePUIDSet

def calcPUWhittleScore(abundMatrixDict, targetDict, featAmountConsDict, puID):
    puAbundDict = abundMatrixDict[puID]
    featScoreList = []
    for aFeat in puAbundDict:
        featAmount = puAbundDict[aFeat]
        featTarget = targetDict[aFeat][1]
        featConAmount = featAmountConsDict[aFeat]

        if puNeededToMeetTarget(featTarget, featConAmount, featAmount):
            featScoreList.append("Cannot be removed")
        else:
            try:
                whittleCalc = featAmount / (featConAmount - featTarget)
            except ZeroDivisionError:
                whittleCalc = 0
            featScoreList.append(whittleCalc)

    if "Cannot be removed" in featScoreList:
        whittleScore = "PU cannot be whittled, as needed to meet targets"
    else:
        try:
            whittleScore = max(featScoreList)
        except ValueError:
            whittleScore = 0

    return whittleScore

def puNeededToMeetTarget(featTarget, featConAmount, featAmount):
    puNeededToMeetTargetBool = False
    featConAmountMinusPU = featConAmount - featAmount

    if featConAmountMinusPU < featTarget and featTarget > 0:
        puNeededToMeetTargetBool = True

    return puNeededToMeetTargetBool

def makeEdgePUIDSet(unitDict, minpatchDataDict):
    edgePUIDSet = set()
    boundaryMatrixDict = minpatchDataDict["boundaryMatrixDictionary"]
    for puID in unitDict:
        if puIsOnEdge(boundaryMatrixDict, unitDict, puID):
            edgePUIDSet.add(puID)

    return edgePUIDSet

def puIsOnEdge(boundaryMatrixDict, unitDict, puID):
    edgeBool = False
    puStatus = unitDict[puID][1]
    if puStatus == 1:
        neighbList = boundaryMatrixDict[puID].keys()
        for neighbID in neighbList:
            neighbStatus = unitDict[neighbID][1]
            ##Check if neighbour is available, excluded or if PU has edge with itself (ie on edge of planning region)
            if neighbStatus == 0 or neighbStatus == 3 or puID == neighbID:
                edgeBool = True

    return edgeBool

def lookupMinSizeValueOfPatch(zoneDict, patchDict, edgePUPatchID):
    patchPUIDList = patchDict[edgePUPatchID][2]
    minPatchSize = -1

    for thePU in patchPUIDList:
        zoneMinPatchSize = zoneDict[thePU][1]
        if minPatchSize == -1:
            minPatchSize = zoneMinPatchSize
        if minPatchSize < zoneMinPatchSize:
            minPatchSize = zoneMinPatchSize

    return minPatchSize

def removingPUIncreasesMarxanCost(minpatchDataDict, unitDict, boundMatrixDict, candidatePUID):
    marxanBLM = minpatchDataDict["bound_cost"]
    removingPUIncreasesMarxanCost = False

    puCost = unitDict[candidatePUID][0]
    neighbDetailDict = boundMatrixDict[candidatePUID]
    marxNeighbList = neighbDetailDict.keys()
    edgeScore = 0
    for neighbID in marxNeighbList:
        neighbStatus = unitDict[neighbID][1]
        if neighbStatus == 1 or neighbStatus == 2:
            edgeScore += neighbDetailDict[neighbID]
        if neighbStatus == 0 or neighbStatus == 3:
            edgeScore -= neighbDetailDict[neighbID]

    edgeScore *= marxanBLM
    finalEdgeScore = edgeScore #Removed mention of blmFudgeWeight
    if puCost < finalEdgeScore:
        removingPUIncreasesMarxanCost = True

    return removingPUIncreasesMarxanCost


def removeWhittlePU(unitDict, whittlePUID):
    puList = unitDict[whittlePUID]
    puList[1] = 0
    unitDict[whittlePUID] = puList

    return unitDict

def marxanPolishPUDict(minpatchDataDictionaryDict, unitDict, polishEdgePUSet):
    boundMatrixDict = minpatchDataDictionaryDict["boundaryMatrixDictionary"]
    marxanBLM = minpatchDataDictionaryDict["bound_cost"]
    while len(polishEdgePUSet) > 0:
        edgePU = polishEdgePUSet.pop()
        neighbList = boundMatrixDict[edgePU].keys()
        for neighbPU in neighbList:
            polishCost = makePolishCost(unitDict, boundMatrixDict, marxanBLM, neighbPU)

            if polishCost < 0:
                polishEdgePUSet.add(neighbPU)
                neighbPUList = unitDict[neighbPU]
                neighbPUList[1] = 1
                unitDict[neighbPU] = neighbPUList

    return unitDict

def makePolishCost(unitDict, boundMatrixDict, marxanBLM, neighbPU):
    neighbStatus = unitDict[neighbPU][1]
    if neighbStatus == 0:
        neighbCost = unitDict[neighbPU][0]
        neighNeighbDict = boundMatrixDict[neighbPU]
        neighbBoundCost = 0
        for neighNeighbPU in neighNeighbDict:
            neighNeighbPUStatus = unitDict[neighNeighbPU][1]
            neighNeighbBoundLength = neighNeighbDict[neighNeighbPU]
            if neighNeighbPUStatus == 1 or neighNeighbPUStatus == 2:
                neighbBoundCost -= neighNeighbBoundLength
            if neighNeighbPUStatus == 0 or neighNeighbPUStatus == 3:
                neighbBoundCost += neighNeighbBoundLength

        polishCost = neighbCost + (neighbBoundCost * marxanBLM)

    else:
        polishCost = "blank"

    return polishCost
