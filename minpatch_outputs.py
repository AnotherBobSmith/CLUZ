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

import os

def printDictionary(theDictionary,theFileName, extraText):
    textList = []
    if len(extraText) > 0:
        textList += extraText
    for aKey in theDictionary:
        valueString = str(theDictionary[aKey])
        keyString = str(aKey) +": " + valueString + "\n"
        textList.append(keyString)

    theFile = open(str(theFileName), 'w')
    for textString in textList:
        theFile.writelines(textString)
    theFile.close()

def produceSummedDict(unitDictionary):
    idList = unitDictionary.keys()
    countList = [0] * len(idList)
    initTuple = zip(idList,countList)
    summedDict = dict(initTuple)

    return summedDict

def printRunResults(minpatchDataDictionary, limboBestResultDictionary, nameString):
    unitDict = minpatchDataDictionary["initialUnitDictionary"]
    textList = ["planning_unit,solution" + "\n"]
    for unitID in unitDict:
        unitList = unitDict[unitID]
        unitStatus = unitList[1]
        unitLimboList = limboBestResultDictionary[unitID]
        unitLimboStatus = unitLimboList[1]
        if unitStatus ==2 or unitLimboStatus == 1:
            theString = [str(unitID) + ",1" + "\n"]
        else:
            theString = [str(unitID) + ",0" + "\n"]
        textList.append(theString)

    file = open(nameString, 'w')
    for textString in textList:
        file.writelines(textString)

def producePatchResultsDict(patchResultsDict, aMarxanSolFilePath, beforePatchStatsDictionary, afterPatchStatsDictionary, costDictionary):
    os.path.basename(aMarxanSolFilePath)
    befAllPatchCount = beforePatchStatsDictionary["AllPatchCount"]
    befAllPatchArea = beforePatchStatsDictionary["AllPatchArea"]
    befMedianAllPatch = beforePatchStatsDictionary["medianAllPatch"]
    befValidPatchCount = beforePatchStatsDictionary["ValidPatchCount"]
    befValidPatchArea = beforePatchStatsDictionary["ValidPatchArea"]
    befMedianValidPatch = beforePatchStatsDictionary["medianValidPatch"]

    aftAllPatchCount = afterPatchStatsDictionary["AllPatchCount"]
    aftAllPatchArea = afterPatchStatsDictionary["AllPatchArea"]
    aftMedianAllPatch = afterPatchStatsDictionary["medianAllPatch"]
    aftValidPatchCount = afterPatchStatsDictionary["ValidPatchCount"]
    aftValidPatchArea = afterPatchStatsDictionary["ValidPatchArea"]
    aftMedianValidPatch = afterPatchStatsDictionary["medianValidPatch"]

    portfolioPUCost = costDictionary["totalUnitCost"]
    portfolioBoundLength = costDictionary["totalBoundaryLength"]
    portfolioBoundCost = costDictionary["totalBoundaryCost"]
    portfolioTotalCost = portfolioPUCost + portfolioBoundCost

    name_string = os.path.basename(aMarxanSolFilePath)
    result_string = str(befAllPatchCount)+","+str(befAllPatchArea)+","+str(befMedianAllPatch)+","+str(befValidPatchCount)+","+str(befValidPatchArea)+","+str(befMedianValidPatch)+","
    result_string += str(aftAllPatchCount)+","+str(aftAllPatchArea)+","+str(aftMedianAllPatch)+","+str(aftValidPatchCount)+","+str(aftValidPatchArea)+","+str(aftMedianValidPatch)+","
    result_string += str(portfolioPUCost)+","+str(portfolioBoundLength)+","+str(portfolioBoundCost)+","+str(portfolioTotalCost)
    result_string += '\n'

    patchResultsDict[name_string] = result_string

    return patchResultsDict

def makeZoneStatsDict(aMarxanSolFilePath, minpatchDataDictionary ,runningUnitDict, zoneStatsDict, zoneFeatureStatsDict):
    name_string = os.path.basename(aMarxanSolFilePath)

    targetDict = minpatchDataDictionary["targetDictionary"]
    areaDictionary = minpatchDataDictionary["areaDictionary"]
    abundanceMatrixDictionary = minpatchDataDictionary["abundanceMatrixDictionary"]
    zoneDict = minpatchDataDictionary["zoneDictionary"]
    zoneTypeDict = minpatchDataDictionary["zoneTypeDictionary"]

    featureList = targetDict.keys()
    blankList = [0]*len(featureList)
    blankFeatDict = dict(zip(featureList, blankList))

    runZoneStatsDict = {}
    runZoneFeatureStatsDict = {}
    for aZone in zoneTypeDict:
        runZoneStatsDict[aZone] = [0,0]
        runZoneFeatureStatsDict[aZone] = copy.deepcopy(blankFeatDict)

    for aUnit in runningUnitDict:
        puStatus = runningUnitDict[aUnit][1]
        if puStatus == 1 or puStatus == 2:
            puCost = runningUnitDict[aUnit][0]
            puArea = areaDictionary[aUnit]
            puZone = zoneDict[aUnit][0]
            puAbundanceDict = abundanceMatrixDictionary[aUnit]

            runningAreaValue = runZoneStatsDict[puZone][0]
            runningCostValue = runZoneStatsDict[puZone][1]
            runningAreaValue += puArea
            runningCostValue += puCost

            runZoneStatsDict[puZone] = [runningAreaValue, runningCostValue]

            for aFeat in puAbundanceDict:
                aFeatAmount = puAbundanceDict[aFeat]
                runningFeatAmount = runZoneFeatureStatsDict[puZone][aFeat]
                runningFeatAmount += aFeatAmount
                runZoneFeatureStatsDict[puZone][aFeat] = runningFeatAmount

    zonePropTargetDict = {}
    for aZone in runZoneFeatureStatsDict:
        propTargetDict = {}
        featureStatsDict = runZoneFeatureStatsDict[aZone]
        for aFeature in featureStatsDict:
            theTarget = targetDict[aFeature][1]
            theFinalAmount = featureStatsDict[aFeature]
            try:
                propAmount = theFinalAmount / theTarget
            except:
                propAmount = 0

            propTargetDict[aFeature] = propAmount

            zonePropTargetDict[aZone] = propTargetDict

    zoneStatsDict[name_string] = runZoneStatsDict
    zoneFeatureStatsDict[name_string] = zonePropTargetDict

    return [zoneStatsDict, zoneFeatureStatsDict]

def updateSummedDict(summedDictionary, unitDictionary):
    for unitID in unitDictionary:
        unitList = unitDictionary[unitID]
        unitStatus = unitList[1]
        ##Check why some earmarked PUs have status of 2
        if unitStatus ==1 or unitStatus ==2:
            initialCount = summedDictionary[unitID]
            finalCount = initialCount + 1
            summedDictionary[unitID] = finalCount

    return summedDictionary

def printSummedResults(summedDictionary, summedFileName):
    tempList = ["planning unit,solution" + "\n"]
    for aRow in summedDictionary.keys():
        theString = str(aRow) + "," + str(summedDictionary[aRow]) +"\n"
        tempList.append(theString)
        final_string = ''.join(tempList)

    file = open(summedFileName, 'w')
    file.writelines(final_string)

def printRunResults(dataDictionary, limboBestResultDictionary, nameString):
    unitDict = dataDictionary["initialUnitDictionary"]
    textList = ["planning_unit,solution" + "\n"]
    for unitID in unitDict:
        unitList = unitDict[unitID]
        unitStatus = unitList[1]
        unitLimboList = limboBestResultDictionary[unitID]
        unitLimboStatus = unitLimboList[1]
        if unitStatus ==2 or unitLimboStatus == 1:
            theString = [str(unitID) + ",1" + "\n"]
        else:
            theString = [str(unitID) + ",0" + "\n"]
        textList.append(theString)

    file = open(nameString, 'w')
    for textString in textList:
        file.writelines(textString)

def printPatchStats(patchResultsDict, patchstatsFileName):

    header_string = "File_name,"

    header_string += "Bef_AllPatchCount,Bef_AllPatchArea,Bef_medianAllPatch,Bef_ValidPatchCount,Bef_ValidPatchArea,Bef_medianValidPatch,"
    header_string += "Aft_AllPatchCount,Aft_AllPatchArea,Aft_medianAllPatch,Aft_ValidPatchCount,Aft_ValidPatchArea,Aft_medianValidPatch,"
    header_string += "PU_cost,Bound_length,Bound_cost,Total_cost"
    header_string += "\n"

    body_string = ""

    for filenameString in patchResultsDict:
        body_string += filenameString + "," + patchResultsDict[filenameString]

    final_string = header_string + body_string

    patchResultFile = open(patchstatsFileName, 'w')
    patchResultFile.writelines(final_string)
    patchResultFile.close()

def printZoneStats(zoneTypeDict, zoneStatsDict, zoneFeatureStatsDict, zoneStatsFileName):
    zoneList = zoneTypeDict.keys()

    ##Produce ZoneStats output
    zoneStats_header_string = "File_name"
    for aZone in zoneList:
        zoneStats_header_string += ",Zone" + str(aZone) +"_Area" + ",Zone" + str(aZone) + "_Cost"
    zoneStats_header_string += "\n"

    zoneStats_body_string = ""

    filenameList = zoneStatsDict.keys()
    filenameList.sort()

    for filenameString in filenameList:
        aRunDict = zoneStatsDict[filenameString]
        zoneStatsDataString = ""
        for aZone in aRunDict:
            aArea = aRunDict[aZone][0]
            aCost = aRunDict[aZone][1]
            zoneStatsDataString += "," + str(aArea) + "," + str(aCost)

        zoneStats_body_string += filenameString + zoneStatsDataString + "\n"

    zoneStats_final_string = zoneStats_header_string + zoneStats_body_string
    zoneStatsResultsFileName = zoneStatsFileName + '_zonestats.txt'
    zoneStatsResultsFile = open(zoneStatsResultsFileName, 'w')
    zoneStatsResultsFile.writelines(zoneStats_final_string)
    zoneStatsResultsFile.close()

    ##Produce ZoneFeature Stats output
    zonefeatureOutputDict = {}
    runList = zoneFeatureStatsDict.keys()

    zonefeatureStats_header_string = "File_name"
    firstRun = zoneFeatureStatsDict.keys()[0]
    firstRunDict = zoneFeatureStatsDict[firstRun]
    firstRunDictKeys = firstRunDict.keys()
    firstRunDictFeatureList = firstRunDict[firstRunDictKeys[0]].keys()
    for bFeat in firstRunDictFeatureList:
        zonefeatureStats_header_string += ",Feat_" + str(bFeat)

    for bZone in zoneList:
        zoneDetailsDict = {}

        for bRun in runList:
            bContentString = bRun
            bFeatureResultDict = zoneFeatureStatsDict[bRun][bZone]
            for cFeat in bFeatureResultDict:
                cAmount = bFeatureResultDict[cFeat]
                bContentString += "," + str(cAmount)

            zoneDetailsDict[bRun] = [bContentString]

        zonefeatureOutputDict[bZone] = zoneDetailsDict

    for ZoneOutputDictRun in zonefeatureOutputDict:
        zonefeatureStats_final_string = zonefeatureStats_header_string

        zoneOutputDetailsDict = zonefeatureOutputDict[ZoneOutputDictRun]
        for dText in zoneOutputDetailsDict:
            zonefeatureStats_final_string += "\n"
            zonefeatureStats_final_string +=  zoneOutputDetailsDict[dText][0]

        zoneFeatStatsResultsFileName = zoneStatsFileName + '_zonefeaturestat' + str(ZoneOutputDictRun) + '.txt'
        zoneFeatStatsResultsFile = open(zoneFeatStatsResultsFileName, 'w')
        zoneFeatStatsResultsFile.writelines(zonefeatureStats_final_string)
        zoneFeatStatsResultsFile.close()