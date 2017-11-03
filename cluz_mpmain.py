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
from qgis.gui import *

import os
import copy

import cluz_mpfunctions
import cluz_mpoutputs
import cluz_mpsetup
import cluz_functions2
import cluz_display
import cluz_setup

def runMinPatch(setupObject, minpatchObject, minpatchDataDict):
    marxanNameString = minpatchObject.marxanFileName + "_r"
    finalNameString = "mp_" + marxanNameString
    marxanSolFileList = cluz_mpsetup.makeMarxanFileList(setupObject, marxanNameString)

    preMarxanUnitDict = minpatchDataDict["initialUnitDictionary"]
    summedSolDict = cluz_mpoutputs.produceSummedDict(preMarxanUnitDict)
    patchResultsDict = {}
    zoneStatsDict = {}
    zoneFeaturePropStatsDict = {}

    bestPortfolioCost = -1
    continueBool = True

    for marxanSolFilePath in marxanSolFileList:
        runningUnitDict = createRunningUnitDictionary(minpatchDataDict, marxanSolFilePath)
        patchDict = cluz_mpfunctions.makePatchDict(runningUnitDict, minpatchDataDict)
        qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + marxanSolFilePath + ".")

        if minpatchDataDict["patch_stats"] and continueBool:
            beforePatchStatsDict = cluz_mpoutputs.makePatchStatsDict(patchDict, minpatchDataDict)

        if minpatchDataDict["rem_small_patch"] and continueBool:
            runningUnitDict = cluz_mpfunctions.remSmallPatchesFromUnitDict(minpatchDataDict,runningUnitDict, patchDict)
            qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + marxanSolFilePath + ". Removing patches that are smaller than the specified thresholds...")

        if minpatchDataDict["add_patches"] and continueBool:
            runningUnitDict, continueBool = cluz_mpfunctions.addPatches(minpatchDataDict, runningUnitDict)
            qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + marxanSolFilePath + ". Adding new patches...")

        if minpatchDataDict["whittle_polish"] and continueBool:
            runningUnitDict = cluz_mpfunctions.runSimWhittle(runningUnitDict, minpatchDataDict)
            qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + marxanSolFilePath + ". Simulated whittling...")

        runningUnitDict = addConservedPUs(runningUnitDict,minpatchDataDict)

        if minpatchDataDict["patch_stats"] and continueBool:
            patchDict = cluz_mpfunctions.makePatchDict(runningUnitDict, minpatchDataDict)
            afterPatchStatsDict = cluz_mpoutputs.makePatchStatsDict(patchDict, minpatchDataDict)

        if continueBool:
            outputFilePath = marxanSolFilePath.replace(marxanNameString, finalNameString)
            cluz_mpoutputs.printRunResults(minpatchDataDict, runningUnitDict, outputFilePath)

            costDict = makeCostDict(minpatchDataDict, runningUnitDict)
            totalCost = costDict['totalBoundaryCost'] + costDict['totalUnitCost']

            if minpatchDataDict["patch_stats"]:
                patchResultsDict = cluz_mpoutputs.producePatchResultsDict(patchResultsDict, marxanSolFilePath, beforePatchStatsDict, afterPatchStatsDict, costDict)

            if minpatchDataDict["zone_stats"]:
                zoneNameString = os.path.basename(marxanSolFilePath)
                zoneStatsDict[zoneNameString] = cluz_mpoutputs.makeRunZoneStatsDict(minpatchDataDict, runningUnitDict, zoneStatsDict)
                zoneFeaturePropStatsDict[zoneNameString] = cluz_mpoutputs.makeRunZoneFeaturePropStatsDict(minpatchDataDict, runningUnitDict)

            if bestPortfolioCost == -1:
                bestPortfolioCost = totalCost
                bestPortfolio = copy.deepcopy(runningUnitDict)

            if bestPortfolioCost <> -1 and totalCost < bestPortfolioCost:
                bestPortfolioCost = totalCost
                bestPortfolio = copy.deepcopy(runningUnitDict)

            summedDict = cluz_mpoutputs.updateSummedDict(summedSolDict,runningUnitDict)

    if continueBool:
        bestFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName + '_best.txt'
        cluz_mpoutputs.printRunResults(minpatchDataDict, bestPortfolio, bestFileName)

        summedFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName + '_summed.txt'
        cluz_mpoutputs.printSummedResults(summedDict, summedFileName)

        if minpatchDataDict["patch_stats"]:
            patchstatsFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName + '_patchstats.csv'
            cluz_mpoutputs.printPatchStats(patchResultsDict, patchstatsFileName)

        if minpatchDataDict["zone_stats"]:
            zoneStatsBaseFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName
            cluz_mpoutputs.printZoneStats(minpatchDataDict, zoneStatsDict, zoneStatsBaseFileName)
            cluz_mpoutputs.printZoneFeaturePropStats(minpatchDataDict, zoneFeaturePropStatsDict, zoneStatsBaseFileName)

        cluz_functions2.addBestMarxanOutputToPUShapefile(setupObject, bestFileName, "MP_Best")
        cluz_functions2.addSummedMarxanOutputToPUShapefile(setupObject, summedFileName, "MP_SF_Scr")

        cluz_display.reloadPULayer(setupObject)
        cluz_display.removePreviousMinPatchLayers()
        bestLayerName = "MP Best (" + minpatchObject.marxanFileName + ")"
        summedLayerName = "MP SF_Score (" + minpatchObject.marxanFileName + ")"
        cluz_display.displayBestOutput(setupObject, "MP_Best", bestLayerName)
        cluz_display.displayGraduatedLayer(setupObject, "MP_SF_Scr", summedLayerName, 1) #1 is SF legend code

        qgis.utils.iface.mainWindow().statusBar().showMessage("")
        qgis.utils.iface.messageBar().pushMessage("MinPatch results", "MinPatch has completed the analysis and the results files are in the specified output folder.", QgsMessageBar.INFO, 3)

def createRunningUnitDictionary(minpatchDataDict, marxanSolLocationString):
    preMarxanUnitDict = minpatchDataDict["initialUnitDictionary"]
    initUnitDict = copy.deepcopy(preMarxanUnitDict)
    marxanSolDictOKBool, aMarxanSolDict = cluz_mpsetup.makeMarxanSolDict(marxanSolLocationString) #marxanSolDictOKBool not used here
    runningUnitDict = makeStartUnitDict(initUnitDict, aMarxanSolDict)

    return runningUnitDict

def makeStartUnitDict(unitDictionary, marxanSolDictionary):
    for aRow in marxanSolDictionary:
        solPUStatus = marxanSolDictionary[aRow]
        if solPUStatus == 1:
            puList = unitDictionary[aRow]
            puList[1] = 1
            unitDictionary[aRow] = puList

    return unitDictionary

def addConservedPUs(runningUnitDict, minpatchDataDict):
    initUnitDict = minpatchDataDict["initialUnitDictionary"]
    for puUnitValue in runningUnitDict:
        if initUnitDict[puUnitValue][1] == 2:
            puList = runningUnitDict[puUnitValue]
            puList[1] = 2
            runningUnitDict[puUnitValue] = puList

    return runningUnitDict

def makeCostDict(minpatchDataDict, puDict):
    costDict = {}

    abundanceMatrixDict = minpatchDataDict["abundanceMatrixDictionary"]
    targetDict = minpatchDataDict["targetDictionary"]
    boundaryMatrixDict = minpatchDataDict["boundaryMatrixDictionary"]
    targetList = targetDict.keys()
    targetList.sort()

    abundValuesDict, numActivePUs = makeAbundValuesDict_numActivePUs(targetList, abundanceMatrixDict, puDict)
    costDict["abundanceValuesDictionary"] = abundValuesDict
    costDict["numberActivePUs"] = numActivePUs

    totalUnitCost, conUnitCount = calcUnitCosts(puDict)
    costDict["totalUnitCost"] = totalUnitCost
    costDict["conservedUnitCount"] = conUnitCount

    amountConservedDict = makeAmountConservedDictionary(targetList, abundanceMatrixDict, puDict)
    costDict["amountConservedDictionary"] = amountConservedDict
    costDict["totalTargetCost"] = makeTotalTargetCost(amountConservedDict, targetDict)

    totalBoundLength, totalBoundaryCost = makeBoundCosts(minpatchDataDict, boundaryMatrixDict, puDict)
    costDict["totalBoundaryLength"] = totalBoundLength
    costDict["totalBoundaryCost"] = totalBoundaryCost

    return costDict

def makeAbundValuesDict_numActivePUs(targetList, abundanceMatrixDict, puDict):
    numActivePUs = 0
    abundValuesDict = {}
    for aRow in targetList:
        abundValuesDict[aRow] = [0, 0, 0, 0]

    for aUnit in abundanceMatrixDict:
        puList = puDict[aUnit]
        puStatus = puList[1]
        #Count the number of units that could be selected in the iteration section
        if puStatus == 0 or puStatus ==1:
            numActivePUs += 1
        puAbundDict = abundanceMatrixDict[aUnit]
        for aFeature in puAbundDict:
            theAmount = puAbundDict[aFeature]
            featureList = abundValuesDict[aFeature]
            runningValue = featureList[puStatus]
            runningValue += theAmount
            featureList[puStatus] = runningValue
            abundValuesDict[aFeature] = featureList

    return abundValuesDict, numActivePUs

def calcUnitCosts(puDict):
    totalUnitCost = 0
    conUnitCount = 0
    for unitID in puDict:
        theList = puDict[unitID]
        unitValue, unitStatus = theList
        if unitStatus == 1 or unitStatus == 2:
            totalUnitCost += unitValue
            conUnitCount += 1

    return totalUnitCost, conUnitCount

def makeAmountConservedDictionary(targetList, abundanceMatrixDictionary, unitDictionary):
    amountConservedDict = {}

    for bNum in targetList:
        amountConservedDict[bNum] = 0

    for puID in abundanceMatrixDictionary:
        puStatus = unitDictionary[puID][1]
        if puStatus == 1 or puStatus == 2:
            puAbundDict = abundanceMatrixDictionary[puID]
            for featID in puAbundDict:
                featAmount = puAbundDict[featID]
                conTotalValue = amountConservedDict[featID]
                conTotalValue += featAmount
                amountConservedDict[featID] = conTotalValue

    return amountConservedDict

def makeTotalTargetCost(amountConservedDictionary, targetDictionary):
    totalTargetCost = 0
    for featureID in amountConservedDictionary.keys():
        amountConserved = amountConservedDictionary[featureID]
        targetValuesList = targetDictionary[featureID]
        theTarget = targetValuesList[1]
        thePenalty = targetValuesList[2]
        if amountConserved < theTarget:
            totalTargetCost = totalTargetCost + thePenalty

    return totalTargetCost

def makeBoundCosts(minpatchDataDict, boundaryMatrixDict, puDict):
    totalBoundLength = cluz_functions2.calcTotalBoundLength(boundaryMatrixDict, puDict)

    BLMvalue = minpatchDataDict["bound_cost"]
    totalBoundaryCost = totalBoundLength * BLMvalue

    return totalBoundLength, totalBoundaryCost
