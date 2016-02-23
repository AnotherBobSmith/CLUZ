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

import copy
import os
import csv
import stats

import cluz_mpfunctions


def makePatchStatsDict(patchDict, minpatchDataDict):
    zoneDict = minpatchDataDict["zoneDictionary"]
    patchStatsDictionary = {}
    allAreaList, validAreaList = makePatchAreaLists(patchDict, zoneDict)

    if len(allAreaList) > 0:
        medianAllPatch = stats.lmedianscore(allAreaList)
    else:
        medianAllPatch = 0

    if len(validAreaList) > 0:
        medianValidPatch = stats.lmedianscore(validAreaList)
    else:
        medianValidPatch = 0

    patchStatsDictionary["AllPatchCount"] = len(allAreaList)
    patchStatsDictionary["AllPatchArea"] = sum(allAreaList)
    patchStatsDictionary["medianAllPatch"] = medianAllPatch
    patchStatsDictionary["ValidPatchCount"] = len(validAreaList)
    patchStatsDictionary["ValidPatchArea"] = sum(validAreaList)
    patchStatsDictionary["medianValidPatch"] = medianValidPatch

    return patchStatsDictionary

def makePatchAreaLists(patchDict, zoneDict):
    allAreaList = []
    validAreaList = []
    for patchID in patchDict:
        patchArea = patchDict[patchID][0]
        patchSizeThreshold = cluz_mpfunctions.calcPatchSizeThreshold(zoneDict, patchDict, patchID)

        allAreaList.append(patchArea)
        if patchArea >= patchSizeThreshold:
            validAreaList.append(patchArea)

    return allAreaList, validAreaList


def printPatchListDict(patchNeighbListDict, zoneTypeDict, outputPath):
    outputFile = open(outputPath, "wb")
    writer = csv.writer(outputFile)
    writer.writerow(['*** MinPatch v3.0'])

    for zoneID in zoneTypeDict:
        zoneRadius = zoneTypeDict[zoneID][1]
        writer.writerow(['*** Patch search distance for Zone ' + str(zoneID) + ' = ' + str(zoneRadius)])

    for puID in patchNeighbListDict:
        lineValueList = copy.deepcopy(patchNeighbListDict[puID])
        if len(lineValueList) > 0:
            lineStringList = [str(x) for x in lineValueList]
            firstValue = lineStringList.pop(0)
            firstValueString = str(puID) + ':[' + firstValue
            endValue = lineStringList.pop(len(lineStringList) - 1)
            endValueString = endValue + ']'
            lineStringList.insert(0, firstValueString)
            lineStringList.append(endValueString)
        else:
            lineStringList = [str(puID) + ':[]']
        writer.writerow(lineStringList)

def produceSummedDict(unitDictionary):
    idList = unitDictionary.keys()
    countList = [0] * len(idList)
    initTuple = zip(idList,countList)
    summedDict = dict(initTuple)

    return summedDict


def producePatchResultsDict(patchResultsDict, aMarxanSolFilePath, beforePatchStatsDict, afterPatchStatsDict, costDict):
    befAllPatchCount = beforePatchStatsDict["AllPatchCount"]
    befAllPatchArea = beforePatchStatsDict["AllPatchArea"]
    befMedianAllPatch = beforePatchStatsDict["medianAllPatch"]
    befValidPatchCount = beforePatchStatsDict["ValidPatchCount"]
    befValidPatchArea = beforePatchStatsDict["ValidPatchArea"]
    befMedianValidPatch = beforePatchStatsDict["medianValidPatch"]

    aftAllPatchCount = afterPatchStatsDict["AllPatchCount"]
    aftAllPatchArea = afterPatchStatsDict["AllPatchArea"]
    aftMedianAllPatch = afterPatchStatsDict["medianAllPatch"]
    aftValidPatchCount = afterPatchStatsDict["ValidPatchCount"]
    aftValidPatchArea = afterPatchStatsDict["ValidPatchArea"]
    aftMedianValidPatch = afterPatchStatsDict["medianValidPatch"]

    portfolioPUCost = costDict["totalUnitCost"]
    portfolioBoundLength = costDict["totalBoundaryLength"]
    portfolioBoundCost = costDict["totalBoundaryCost"]
    portfolioTotalCost = portfolioPUCost + portfolioBoundCost

    name_string = os.path.basename(aMarxanSolFilePath)
    result_List1 = [befAllPatchCount, befAllPatchArea, befMedianAllPatch, befValidPatchCount, befValidPatchArea, befMedianValidPatch]
    result_List2 = [aftAllPatchCount, aftAllPatchArea, aftMedianAllPatch, aftValidPatchCount, aftValidPatchArea, aftMedianValidPatch]
    result_List3 = [portfolioPUCost, portfolioBoundLength, portfolioBoundCost, portfolioTotalCost]

    patchResultsDict[name_string] = result_List1 + result_List2 + result_List3

    return patchResultsDict

def makeRunZoneStatsDict(minpatchDataDictionary ,runningUnitDict, zoneStatsDict):
    areaDictionary = minpatchDataDictionary["areaDictionary"]
    zoneDict = minpatchDataDictionary["zoneDictionary"]
    zoneTypeDict = minpatchDataDictionary["zoneTypeDictionary"]

    runZoneStatsDict = {}
    for aZone in zoneTypeDict:
        runZoneStatsDict[aZone] = [0, 0]

    for aUnit in runningUnitDict:
        puStatus = runningUnitDict[aUnit][1]
        if puStatus == 1 or puStatus == 2:
            puCost = runningUnitDict[aUnit][0]
            puArea = areaDictionary[aUnit]
            puZone = zoneDict[aUnit][0]

            runningAreaValue = runZoneStatsDict[puZone][0]
            runningCostValue = runZoneStatsDict[puZone][1]
            runningAreaValue += puArea
            runningCostValue += puCost

            runZoneStatsDict[puZone] = [runningAreaValue, runningCostValue]

    return runZoneStatsDict

def makeRunZoneFeaturePropStatsDict(minpatchDataDict, runningUnitDict):
    targetDict = minpatchDataDict["targetDictionary"]
    abundanceMatrixDict = minpatchDataDict["abundanceMatrixDictionary"]
    zoneDict = minpatchDataDict["zoneDictionary"]
    zoneTypeDict = minpatchDataDict["zoneTypeDictionary"]

    runZoneFeatureStatsDict = makeRunZoneFeatureStatsDict(targetDict, abundanceMatrixDict, runningUnitDict, zoneDict, zoneTypeDict)

    zonePropTargetDict = {}
    for zoneID in runZoneFeatureStatsDict:
        propTargetDict = {}
        featureStatsDict = runZoneFeatureStatsDict[zoneID]
        for featID in featureStatsDict:
            targetValue = targetDict[featID][1]
            finalAmount = featureStatsDict[featID]
            try:
                propAmount = finalAmount / targetValue
            except ArithmeticError:
                propAmount = 0

            propTargetDict[featID] = propAmount

            zonePropTargetDict[zoneID] = propTargetDict

    return zonePropTargetDict

def makeRunZoneFeatureStatsDict(targetDict, abundanceMatrixDict, unitDict, zoneDict, zoneTypeDict):
    featureList = targetDict.keys()
    featureList.sort()
    blankList = [0] * len(featureList)
    blankFeatDict = dict(zip(featureList, blankList))

    runZoneFeatureStatsDict = {}
    for zoneID in zoneTypeDict:
        runZoneFeatureStatsDict[zoneID] = copy.deepcopy(blankFeatDict)

    for puID in unitDict:
        puStatus = unitDict[puID][1]
        if puStatus == 1 or puStatus == 2:
            puZoneID = zoneDict[puID][0]
            puAbundanceDict = abundanceMatrixDict[puID]

            for featID in puAbundanceDict:
                featAmount = puAbundanceDict[featID]
                runningFeatAmount = runZoneFeatureStatsDict[puZoneID][featID]
                runningFeatAmount += featAmount
                runZoneFeatureStatsDict[puZoneID][featID] = runningFeatAmount

    return runZoneFeatureStatsDict

def updateSummedDict(summedDictionary, unitDictionary):
    for puID in unitDictionary:
        unitList = unitDictionary[puID]
        unitStatus = unitList[1]
        if unitStatus == 1 or unitStatus == 2:
            initialCount = summedDictionary[puID]
            finalCount = initialCount + 1
            summedDictionary[puID] = finalCount

    return summedDictionary

def printSummedResults(summedDictionary, summedFilePath):
    summedResultsWriter = csv.writer(open(summedFilePath, "wb"))
    headerRow = ["planning_unit", "solution"]
    summedResultsWriter.writerow(headerRow)

    puList = summedDictionary.keys()
    puList.sort()
    for puID in puList:
        summedResultsWriter.writerow([puID, summedDictionary[puID]])

def printRunResults(minpatchDataDict, limboBestResultDict, filePathString):
    runResultsWriter = csv.writer(open(filePathString, "wb"))
    headerRow = ["planning_unit", "solution"]
    runResultsWriter.writerow(headerRow)

    unitDict = minpatchDataDict["initialUnitDictionary"]
    for unitID in unitDict:
        unitStatus = unitDict[unitID][1]
        unitLimboStatus = limboBestResultDict[unitID][1]
        if unitStatus == 2 or unitLimboStatus == 1:
            finalUnitStatus = 1
        else:
            finalUnitStatus = 0

        runResultsWriter.writerow([unitID, finalUnitStatus])

def printPatchStats(patchResultsDict, filePathString):
    patchStatsWriter = csv.writer(open(filePathString, "wb"))
    headerRow1 = ["File_name", "Bef_AllPatchCount", "Bef_AllPatchArea", "Bef_medianAllPatch", "Bef_ValidPatchCount", "Bef_ValidPatchArea", "Bef_medianValidPatch"]
    headerRow2 = ["Aft_AllPatchCount", "Aft_AllPatchArea", "Aft_medianAllPatch", "Aft_ValidPatchCount", "Aft_ValidPatchArea", "Aft_medianValidPatch"]
    headerRow3 = ["PortfolioPUCost", "PortfolioBoundLength", "PortfolioBoundCost", "PortfolioTotalCost"]
    headerRow = headerRow1 + headerRow2 + headerRow3
    patchStatsWriter.writerow(headerRow)

    for filenameString in patchResultsDict:
        patchStatsWriter.writerow([filenameString] + patchResultsDict[filenameString])

def printZoneStats(minpatchDataDict, zoneStatsDict, zoneStatsBaseFileName):
    zoneList = minpatchDataDict["zoneTypeDictionary"].keys()
    zoneList.sort()

    zoneStatsHeaderList = makeZoneStatsHeaderList(zoneList)
    zoneStatsWriter = csv.writer(open(zoneStatsBaseFileName + '_zonestats.csv', "wb"))
    zoneStatsWriter.writerow(zoneStatsHeaderList)

    filenameList = zoneStatsDict.keys()
    filenameList.sort()

    for filenameString in filenameList:
        aRunDict = zoneStatsDict[filenameString]
        resultsList = [filenameString]
        for zoneID in aRunDict:
            aArea = aRunDict[zoneID][0]
            aCost = aRunDict[zoneID][1]
            resultsList += [aArea, aCost]
        zoneStatsWriter.writerow(resultsList)

def makeZoneStatsHeaderList(zoneList):
    zoneStatsHeaderList = ["File_name"]
    for zoneID in zoneList:
        zoneStatsHeaderList += ["Zone" + str(zoneID) + "_Area", "Zone" + str(zoneID) + "_Cost"]

    return zoneStatsHeaderList

def printZoneFeaturePropStats(minpatchDataDict, zoneFeaturePropStatsDict, zoneStatsBaseFileName):
    featList = minpatchDataDict["targetDictionary"].keys()
    featList.sort()

    zoneFeatStatsHeaderList = ["File_name"]
    for theFeat in featList:
        zoneFeatStatsHeaderList += ["Feat_" + str(theFeat)]

    zonefeatureOutputDict = makeZonefeatureOutputDict(minpatchDataDict, featList, zoneFeaturePropStatsDict)

    for zoneID in zonefeatureOutputDict:
        zoneFeatStatsWriter = csv.writer(open(zoneStatsBaseFileName + '_zonefeaturestat' + str(zoneID) + '.csv', "wb"))
        zoneFeatStatsWriter.writerow(zoneFeatStatsHeaderList)

        zoneDetailsDict = zonefeatureOutputDict[zoneID]
        for runName in zoneDetailsDict:
            contentList = zoneDetailsDict[runName]
            zoneFeatStatsWriter.writerow(contentList)

def makeZonefeatureOutputDict(minpatchDataDict, featList, zoneFeaturePropStatsDict):
    runList = zoneFeaturePropStatsDict.keys()
    runList.sort()
    zoneList = minpatchDataDict["zoneTypeDictionary"].keys()
    zonefeatureOutputDict = {}

    for zoneID in zoneList:
        zoneDetailsDict = {}
        for runName in runList:
            contentList = [runName]
            aFeaturePropResultDict = zoneFeaturePropStatsDict[runName][zoneID]
            for aFeat in featList:
                try:
                    propAmount = aFeaturePropResultDict[aFeat]
                except KeyError:
                    propAmount = 0
                propString = str(round(propAmount, 4))
                contentList += [propString]
            zoneDetailsDict[runName] = contentList
        zonefeatureOutputDict[zoneID] = zoneDetailsDict

    return zonefeatureOutputDict