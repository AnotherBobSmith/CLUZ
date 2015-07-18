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

import stats

def producePatchDict(unitDictionary, minpatchDataDictionary):
    patchDict = {}
    patchID = 1
    runningPatchDict = {}
    areaDictionary = minpatchDataDictionary["areaDictionary"]
    boundaryMatrixDictionary = minpatchDataDictionary["boundaryMatrixDictionary"]
    for unitID in unitDictionary:
        unitList = unitDictionary[unitID]
        unitStatus = unitList[1]
        if unitStatus ==1 or unitStatus==2:
            unitArea = areaDictionary[unitID]
            runningPatchDict[unitID] = unitArea

    while len(runningPatchDict) > 0:
        firstUnitID = runningPatchDict.keys()[0]
        firstUnitArea = runningPatchDict[firstUnitID]
        loopUnitDict = {}
        loopUnitDict[firstUnitID] = firstUnitArea
        patchList = []
        patchSize = 0
        unitCount = 0

        while len(loopUnitDict) > 0:
            aUnitItem = loopUnitDict.popitem()
            aUnitID, aUnitArea = aUnitItem

            del runningPatchDict[aUnitID]
            patchList.append(aUnitID)
            patchSize += aUnitArea
            unitCount += 1
            neighbList = boundaryMatrixDictionary[aUnitID]
            if len(neighbList) > 0:
                for neighbUnit in neighbList:
                    if neighbUnit in runningPatchDict:
                        neighbArea = areaDictionary[neighbUnit]
                        loopUnitDict[neighbUnit] = neighbArea

        patchDict[patchID] = [patchSize,unitCount,patchList]
        patchID += 1
    return patchDict

def producePatchStatsDict(patchDictionary, minpatchDataDictionary):
    patchStatsDictionary = {}
    allAreaList = []
    validAreaList = []
    zoneDict = minpatchDataDictionary["zoneDictionary"]

    for aPatch in patchDictionary:
        patchArea = patchDictionary[aPatch][0]
        patchPUCount = patchDictionary[aPatch][1]
        patchPUIDList = patchDictionary[aPatch][2]
        minPatchSize = -1
        for aPU in patchPUIDList:
            puMinPatchSize = zoneDict[aPU][1]
            if minPatchSize == -1:
                minPatchSize = puMinPatchSize
            if puMinPatchSize > minPatchSize:
                minPatchSize = puMinPatchSize

        allAreaList.append(patchArea)
        if patchArea >= minPatchSize:
            validAreaList.append(patchArea)

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

def remSmallPatchesFromUnitDict(minpatchDataDictionary, unitDictionary, patchDictionary):
    preMarxanUnitDict = minpatchDataDictionary["initialUnitDictionary"]
    zoneDictionary = minpatchDataDictionary["zoneDictionary"]

    for aPatch in patchDictionary:
        patchSize = patchDictionary[aPatch][0]

        patchPUIDList = patchDictionary[aPatch][2]
        minPatchSize = - 1
        for aPUID in patchPUIDList:
            zonePUMinPatch = zoneDictionary[aPUID][1]
            if minPatchSize == -1:
                minPatchSize = zonePUMinPatch
            if minPatchSize < zonePUMinPatch:
                minPatchSize = zonePUMinPatch

        if patchSize < minPatchSize:
            patchIDList = patchDictionary[aPatch][2]
            for unitIDValue in patchIDList:
                origStatus = preMarxanUnitDict[unitIDValue][1]
                unitList = unitDictionary[unitIDValue]
                unitStatus = unitList[1]
                if origStatus == 0 and unitStatus == 1:
                    unitList[1] = 0
                    unitDictionary[unitIDValue] = unitList

    return unitDictionary

def addPatches(minpatchDataDict, runningUnitDict):
    targetAttainmentDict = makeTargetAttainDict(minpatchDataDict,runningUnitDict)
    unmetTargetIDList = makeUnmetTargetIDList(targetAttainmentDict, minpatchDataDict)

    puSelectionList = makepuSelectionList(minpatchDataDict,runningUnitDict)
    puPatchSetDict = makepuPatchSetDict(puSelectionList,minpatchDataDict)
    allPUPatchAbundDict = calcPUPatchAbundDict(minpatchDataDict ,runningUnitDict, targetAttainmentDict, puSelectionList, puPatchSetDict, unmetTargetIDList)

    while len(unmetTargetIDList) > 0:
        puPatchScoreDict = calcPUPatchScoreDict(minpatchDataDict,runningUnitDict,targetAttainmentDict,allPUPatchAbundDict,puSelectionList)
        puIDValue = returnBestPU(puPatchScoreDict)

        if puIDValue == -1:
            print "Targets couldn't be met!"
            break

        runningUnitDict = addPatch(minpatchDataDict,runningUnitDict,puIDValue)
        puSelectionList.remove(puIDValue)

        allPUPatchAbundDict = updatePUPatchAbundDict(allPUPatchAbundDict,minpatchDataDict,runningUnitDict,targetAttainmentDict,puSelectionList,puPatchSetDict,unmetTargetIDList,puIDValue)
        targetAttainmentDict = makeTargetAttainDict(minpatchDataDict,runningUnitDict)
        unmetTargetIDList = makeUnmetTargetIDList(targetAttainmentDict,minpatchDataDict)

    return runningUnitDict

def makeTargetAttainDict(minpatchDataDictionary, unitDictionary):
    targetAttainDict = {}
    targetDict = minpatchDataDictionary["targetDictionary"]
    abundanceDictionary = minpatchDataDictionary["abundanceDictionary"]

    targetList = targetDict.keys()
    for bNum in targetList:
        targetAttainDict[bNum] = 0

    for aRow in abundanceDictionary:
        abundList = abundanceDictionary[aRow]
        featureID, puIDvalue, abundValue = abundList

        unitList = unitDictionary[puIDvalue]
        unitStatus = unitList[1]
        if unitStatus == 1 or unitStatus == 2:
            conTotalValue = targetAttainDict[featureID]
            conTotalValue += abundValue
            targetAttainDict[featureID] = conTotalValue
    return targetAttainDict

def makeUnmetTargetIDList(amountConDict, minpatchDataDictionary):
    unmetTargetList = []
    targetDict = minpatchDataDictionary["targetDictionary"]
    for featureID in amountConDict:
        amountConserved = amountConDict[featureID]
        targetValue = targetDict[featureID][1]

        if targetValue > 0 and amountConserved < targetValue:
            unmetTargetList.append(featureID)

    return unmetTargetList

def makepuSelectionList(minpatchDataDictionary, runningUnitDict):
    puSelectionList = []
    neighbPatchIDDict = minpatchDataDictionary["addNeighbPUIDDictionary"]
    for aPU in runningUnitDict:
        puStatus = runningUnitDict[aPU][1]
        if puStatus <> 3:
            neighbPatchIDList = neighbPatchIDDict[aPU]
            if len(neighbPatchIDList) > 0:
                puSelectionList.append(aPU)

    return puSelectionList

def makepuPatchSetDict(puSelectionList, minpatchDataDictionary):
    puPatchSetDict = {}
    neighbPatchIDDict = minpatchDataDictionary["addNeighbPUIDDictionary"]
    for aPU in puSelectionList:
        puSet = set(neighbPatchIDDict[aPU])
        puSet.add(aPU)
        puPatchSetDict[aPU] = puSet

    return puPatchSetDict

def calcPUPatchAbundDict(minpatchDataDictionary, unitDictionary, targetAttainmentDictionary, puSelectionList, puPatchSetDict, unmetTargetIDList):
    allPUPatchAbundDict = {}
    neighbPatchIDDict = minpatchDataDictionary["addNeighbPUIDDictionary"]
    patchAreaDict = minpatchDataDictionary["patchAreaDictionary"]
    targetDict = minpatchDataDictionary["targetDictionary"]
    abundMatrixDict = minpatchDataDictionary["abundanceMatrixDictionary"]

    for puIDValue in puSelectionList:
        patchPUIDSet = puPatchSetDict[puIDValue]
        patchCost = 0
        puPatchAbundDict = {}

        for aPUID in patchPUIDSet:
            puStatus = unitDictionary[aPUID][1]
            puCost = unitDictionary[aPUID][0]
            if puStatus == 0:
                patchCost += puCost

        for featID in unmetTargetIDList:
            patchAmount = 0
            for bPUID in patchPUIDSet:
                bPUStatus = unitDictionary[bPUID][1]
                if bPUStatus == 0:
                    abundDict = abundMatrixDict[bPUID]
                    try:
                        abundAmount = abundDict[featID]
                        patchAmount += abundAmount
                    except:
                        whatever = 5
            if patchAmount > 0:
                puPatchAbundDict[featID] = patchAmount

        allPUPatchAbundDict[puIDValue] = [puPatchAbundDict, patchCost]

    return allPUPatchAbundDict

def calcPUPatchScoreDict(minpatchDataDictionary, unitDictionary, targetAttainmentDictionary, allPUPatchAbundDictionary, puSelectionList):
    puPatchScoreDict = {}
    targetDict = minpatchDataDictionary["targetDictionary"]

    for puIDValue in puSelectionList:
        puScore = 0
        puPatchAbundDict = allPUPatchAbundDictionary[puIDValue][0]
        puPatchCost = allPUPatchAbundDictionary[puIDValue][1]
        if puPatchCost > 0:
            for aFeature in puPatchAbundDict:
                patchAmount = puPatchAbundDict[aFeature]
                targetAmount = targetDict[aFeature][1]
                conAmount = targetAttainmentDictionary[aFeature]
                targetGap = targetAmount - conAmount
                if targetGap > 0:
                    featScore = patchAmount / targetGap

                    ####Reduce featScore if over 1, as we only need to meet the target
                    if featScore > 1:
                        featScore = 1

                    puScore += featScore
        try:
            finalpuScore = puScore / puPatchCost
        except:
            finalpuScore = 0
        puPatchScoreDict[puIDValue] = finalpuScore

    return puPatchScoreDict

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
    patchIDDict = minpatchDataDictionary["addNeighbPUIDDictionary"]
    initPUList = patchIDDict[puIDValue]
    puList = initPUList + [puIDValue]
    for aPUIDValue in puList:
        puList = unitDictionary[aPUIDValue]
        puStatus = puList[1]
        if puStatus == 0:
            puList[1] = 1
            unitDictionary[aPUIDValue] = puList
    return unitDictionary

def updatePUPatchAbundDict(allPUPatchAbundDict, minpatchDataDictionary, unitDictionary, targetAttainmentDict, puSelectionList, puPatchSetDict, unmetTargetIDList, bestPUID):
    neighbPatchIDDict = minpatchDataDictionary["addNeighbPUIDDictionary"]
    targetDict = minpatchDataDictionary["targetDictionary"]
    abundMatrixDict = minpatchDataDictionary["abundanceMatrixDictionary"]
    runningPUSelectionList = []
    bestPatchSet = puPatchSetDict[bestPUID]

    for aPatchCentrePU in puSelectionList:
        aPatchPUIDSet = puPatchSetDict[aPatchCentrePU]
        setOverLap = bestPatchSet.intersection(aPatchPUIDSet)
        if len(setOverLap) > 0:
            aPatchCost = 0
            for bPUID in aPatchPUIDSet:
                bPUStatus = unitDictionary[bPUID][1]
                bPUCost = unitDictionary[bPUID][0]
                if bPUStatus == 0:
                    aPatchCost += bPUCost

            puPatchAbundDict = {}
            for featID in unmetTargetIDList:
                featPatchAmount = 0
                for cPUID in aPatchPUIDSet:
                    abundDict = abundMatrixDict[cPUID]
                    if unitDictionary[cPUID][1] == 0 and featID in abundDict:
                        abundAmount = abundDict[featID]
                        featPatchAmount += abundAmount
                if featPatchAmount > 0:
                    puPatchAbundDict[featID] = featPatchAmount

            allPUPatchAbundDict[aPatchCentrePU] = [puPatchAbundDict, aPatchCost]

    return allPUPatchAbundDict

def runSimWhittle(runningUnitDict, minpatchDataDict):
    patchDict = producePatchDict(runningUnitDict,minpatchDataDict)
    edgePUList = makeEdgePUList(runningUnitDict,minpatchDataDict)
    puPatchDict = makePUPatchDict(runningUnitDict,patchDict)
    targetAttainmentDict = makeTargetAttainDict(minpatchDataDict,runningUnitDict)
    #Keystone list is of PUs that can't be removed without affecting patch size or targets
    keystonePUList = []
    while len(edgePUList) > 0:
        whittleScoreDict = makeWhittleScoreDict(minpatchDataDict, runningUnitDict, targetAttainmentDict, patchDict, puPatchDict, edgePUList, keystonePUList)
        whittlePUDetailsList = makePUDetailsList(minpatchDataDict,runningUnitDict,patchDict,puPatchDict,whittleScoreDict,keystonePUList)
        whittlePU, edgePUList, keystonePUList = whittlePUDetailsList

        if len(edgePUList) > 0:
            runningUnitDict = remWhittlePU(runningUnitDict, whittlePU)
            targetAttainmentDict = makeTargetAttainDict(minpatchDataDict,runningUnitDict)
            patchDict = producePatchDict(runningUnitDict,minpatchDataDict)
            puPatchDict = makePUPatchDict(minpatchDataDict,runningUnitDict,patchDict)

    return runningUnitDict

def makeEdgePUList(unitDictionary, minpatchDataDictionary):
    edgePUList = []
    boundaryMatrixDictionary = minpatchDataDictionary["boundaryMatrixDictionary"]
    for puIDValue in unitDictionary:
        edgeBool = 0
        puStatus = unitDictionary[puIDValue][1]
        if puStatus == 1:
            neighbList = boundaryMatrixDictionary[puIDValue].keys()
            for neighbID in neighbList:
                neighbStatus = unitDictionary[neighbID][1]
                ##Check if neighbour is available, excluded or if PU has edge with itself (ie on edge of planning region)
                if neighbStatus == 0 or neighbStatus == 3 or puIDValue == neighbID:
                    edgeBool = 1

        if edgeBool == 1:
            edgePUList.append(puIDValue)

    return edgePUList

def makePUPatchDict(unitDictionary, patchDictionary):
    puIDList = unitDictionary.keys()
    PUPatchDict = {}
    for puIDValue in puIDList:
        PUPatchDict[puIDValue] = 0
    for patchIDValue in patchDictionary:
        patchList = patchDictionary[patchIDValue][2]
        for patchPUIDValue in patchList:
            PUPatchDict[patchPUIDValue] = -patchIDValue

    return PUPatchDict

def makeWhittleScoreDict(minpatchDataDict, unitDictionary, targetAttainmentDictionary, patchDictionary, puPatchDictionary, rawEdgePUList, keystonePUList):
    edgePUList = []
    areaDict = minpatchDataDict["areaDictionary"]
    abundMatrixDict = minpatchDataDict["abundanceMatrixDictionary"]
    targetDict = minpatchDataDict["targetDictionary"]
    preMarxanUnitDict = minpatchDataDict["initialUnitDictionary"]
    zoneDict = minpatchDataDict["zoneDictionary"]

    for edgePU in rawEdgePUList:
        edgePUStatus = unitDictionary[edgePU][1]
        edgePUInitStatus = preMarxanUnitDict[edgePU][1]

        if edgePUStatus == 1 and edgePUInitStatus <> 2:
            edgePUArea = areaDict[edgePU]
            edgePUPatchID = puPatchDictionary[edgePU] * -1
            patchArea = patchDictionary[edgePUPatchID][0]
            patchDiff = patchArea - edgePUArea

            patchPUIDList = patchDictionary[edgePUPatchID][2]
            minPatchSize = -1
            for thePU in patchPUIDList:
                zoneMinPatchSize = zoneDict[thePU][1]
                if minPatchSize == -1:
                    minPatchSize = zoneMinPatchSize
                if minPatchSize < zoneMinPatchSize:
                    minPatchSize = zoneMinPatchSize

            if edgePUStatus == 1 and patchDiff >= minPatchSize:
                edgePUList.append(edgePU)

    whittleScoreDict = {}
    for aEdgePU in edgePUList:
        whittleScore = 0
        abundDict = abundMatrixDict[aEdgePU]
        for aFeat in abundDict:
            featAmount = abundDict[aFeat]
            featTarget = targetDict[aFeat][1]
            featConAmount = targetAttainmentDictionary[aFeat]
            featDiff = featConAmount - featAmount

            if featDiff < featTarget and featTarget > 0:
                whittleScore = -1
                continue
            if whittleScore == -1:
                continue
            if featTarget == 0:
                whittleCalc = 0
            if featDiff >= featTarget and featTarget > 0:
                whittleCalc = featAmount / (featConAmount - featTarget)

            if whittleCalc > whittleScore:
                whittleScore = whittleCalc

        if whittleScore <> - 1:
            whittleScoreDict[aEdgePU] = whittleScore

    return whittleScoreDict

def makePUDetailsList(minpatchDataDictionary, unitDictionary, patchDictionary, puPatchDictionary, whittleScoreDictionary, keystonePUList):
    boundMatrixDict = minpatchDataDictionary["boundaryMatrixDictionary"]
    neighbPUIDDict = minpatchDataDictionary["whittleNeighbPUIDDict"]
    lowestPUIDValue = "blank"
    loopBool = 1
    remMarxanCostPUList = []

    if len(whittleScoreDictionary) == 0:
        loopBool = 0

    #Identify the best PU
    while loopBool == 1:
        lowestPUIDValue = "blank"
        lowestScore = "blank"
        checkPatchBool = 1
        for puIDValue in whittleScoreDictionary:
            whittleScore = whittleScoreDictionary[puIDValue]
            if lowestPUIDValue == "blank":
                lowestScore = whittleScore
                lowestPUIDValue = puIDValue
            if whittleScore < lowestScore:
                lowestScore = whittleScore
                lowestPUIDValue = puIDValue

        #Check that the PU can be removed without increasing the Marxan cost
        if lowestPUIDValue <> "blank":
            marxanBLM = minpatchDataDictionary["bound_cost"]
            puCost = unitDictionary[lowestPUIDValue][0]
            neighbDetailDict = boundMatrixDict[lowestPUIDValue]
            marxNeighbList = neighbDetailDict.keys()
            edgeScore = 0
            for neighbID in marxNeighbList:
                neighbStatus = unitDictionary[neighbID][1]
                if neighbStatus == 1 or neighbStatus == 2:
                    edgeScore += neighbDetailDict[neighbID]
                if neighbStatus == 0 or neighbStatus == 3:
                    edgeScore -= neighbDetailDict[neighbID]

            edgeScore *= marxanBLM
            finalEdgeScore = edgeScore #Removed mention of blmFudgeWeight
            if puCost < finalEdgeScore:
                whittleScoreDictionary.pop(lowestPUIDValue)
                remMarxanCostPUList.append(lowestPUIDValue)
                checkPatchBool = 0
                if len(whittleScoreDictionary) == 0:
                    loopBool = 0

        #Check that the PU can be removed without splitting the patches into two small fragments
        if lowestPUIDValue <> "blank" and checkPatchBool == 1:
            rawNeighbMiniPatchList = neighbPUIDDict[lowestPUIDValue]
            beforeMiniUnitDict = {}
            afterMiniUnitDict = {}
            if lowestPUIDValue in rawNeighbMiniPatchList:
                rawNeighbMiniPatchList.remove(lowestPUIDValue)

            for rawMiniPatchPUID in rawNeighbMiniPatchList:
                rawMiniPatchPUDetails = unitDictionary[rawMiniPatchPUID]
                rawMiniPatchPUIDStatus = rawMiniPatchPUDetails[1]
                if rawMiniPatchPUIDStatus == 1 or rawMiniPatchPUIDStatus == 2:
                    beforeMiniUnitDict[rawMiniPatchPUID] = rawMiniPatchPUDetails
                    afterMiniUnitDict[rawMiniPatchPUID] = rawMiniPatchPUDetails

                beforeMiniUnitDict[lowestPUIDValue] = unitDictionary[lowestPUIDValue]

            beforeMiniPatchDict = producePatchDict(beforeMiniUnitDict ,minpatchDataDictionary)
            afterMiniPatchDict = producePatchDict(afterMiniUnitDict ,minpatchDataDictionary)

            if len(beforeMiniPatchDict) == len(afterMiniPatchDict):
                loopBool = 0

            else:
                patchID = puPatchDictionary[lowestPUIDValue] * -1
                patchIDList = patchDictionary[patchID][2]
                afterPatchUnitDict = {}
                beforePatchUnitDict = {}
                for patchIDValue in patchIDList:
                    afterPatchUnitDict[patchIDValue] = unitDictionary[patchIDValue]

                beforePatchUnitDict[lowestPUIDValue] = unitDictionary[lowestPUIDValue]

                beforePatchDict = producePatchDict(beforeMiniUnitDict, minpatchDataDictionary)
                afterPatchDict = producePatchDict(afterMiniUnitDict ,minpatchDataDictionary)

                if len(beforePatchDict) <> len(afterPatchDict):
                    keystonePUList.append(lowestPUIDValue)
                    whittleScoreDictionary.pop(lowestPUIDValue)
                    if len(whittleScoreDictionary) == 0:
                        loopBool = 0
                else:
                    loopBool = 0

    #Make new edgeList
    edgeList = whittleScoreDictionary.keys()
    if len(edgeList) > 0:
        edgeList.remove(lowestPUIDValue)
        neighbList = boundMatrixDict[lowestPUIDValue].keys()
        neighbEdgeCount = 0
        newEdgeList = []
        for neighbID in neighbList:
            if neighbID in keystonePUList:
                continue
            if unitDictionary[neighbID][1] <> 1:
                continue

            neighbNeighbList = boundMatrixDict[neighbID].keys()
            for neighbNeighbID in neighbNeighbList:
                neighbNeighbStatus = unitDictionary[neighbNeighbID][1]
                if neighbNeighbStatus == 0 or neighbNeighbStatus == 3:
                    neighbEdgeCount += 1
            if neighbEdgeCount == 0:
                newEdgeList.append(neighbID)

        edgeList = edgeList + newEdgeList + remMarxanCostPUList

    remMarxanCostPUList.sort()
    return [lowestPUIDValue,edgeList,keystonePUList]

def remWhittlePU(unitDictionary, whittlePU):
    puList = unitDictionary[whittlePU]
    puList[1] = 0
    unitDictionary[whittlePU] = puList

    return unitDictionary

def marxanPolishPUDict(minpatchDataDictionaryDictionary, unitDictionary, edgeList):
    boundMatrixDict = minpatchDataDictionaryDictionary["boundaryMatrixDictionary"]
    marxanBLM = minpatchDataDictionaryDictionary["bound_cost"]
    while len(edgeList) > 0:
        edgePU = edgeList[0]
        neighbList = boundMatrixDict[edgePU].keys()
        edgeList.remove(edgePU)
        for neighbPU in neighbList:
            neighbStatus = unitDictionary[neighbPU][1]
            if neighbStatus == 0:
                neighbCost = unitDictionary[neighbPU][0]
                neighNeighbDict = boundMatrixDict[neighbPU]
                neighbBoundCost = 0
                for neighNeighbPU in neighNeighbDict:
                    neighNeighbPUStatus = unitDictionary[neighNeighbPU][1]
                    neighNeighbBoundLength = neighNeighbDict[neighNeighbPU]
                    if neighNeighbPUStatus == 1 or neighNeighbPUStatus == 2:
                        neighbBoundCost -= neighNeighbBoundLength
                    if neighNeighbPUStatus == 0 or neighNeighbPUStatus == 3:
                        neighbBoundCost += neighNeighbBoundLength

                finalCost = neighbCost + (neighbBoundCost * marxanBLM)

                if finalCost < 0:
                    edgeList.append(neighbPU)
                    neighbPUList = unitDictionary[neighbPU]
                    neighbPUList[1] = 1
                    unitDictionary[neighbPU] = neighbPUList


    return unitDictionary