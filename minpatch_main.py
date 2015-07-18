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

import string
import os
import math
import copy

import qgis

import minpatch_functions
import minpatch_outputs

def runMinPatch(setupObject, minpatchObject):
    minpatchDataDict = makeMinpatchDataDict(setupObject, minpatchObject)
    minpatchDataDict = producePatchDetails(setupObject, minpatchDataDict)

    marxanNameString = minpatchObject.marxanFileName + "_r"
    finalNameString = "mp_" + marxanNameString
    marxanSolFileList = makeMarxanFileList(setupObject, marxanNameString)

    preMarxanUnitDict = minpatchDataDict["initialUnitDictionary"]
    summedSolDict = minpatch_outputs.produceSummedDict(preMarxanUnitDict)
    patchResultsDict = {}
    zoneStatsDict = {}
    zoneFeatureStatsDict = {}

    bestPortfolioCost = -1

    for aMarxanSolFilePath in marxanSolFileList:
        runningUnitDict = createRunningUnitDictionary(minpatchDataDict, aMarxanSolFilePath)
        patchDict = minpatch_functions.producePatchDict(runningUnitDict, minpatchDataDict)
        qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + aMarxanSolFilePath + ".")

        if minpatchDataDict["patch_stats"]:
            beforePatchStatsDict = minpatch_functions.producePatchStatsDict(patchDict, minpatchDataDict)

        if minpatchDataDict["rem_small_patch"]:
            runningUnitDict = minpatch_functions.remSmallPatchesFromUnitDict(minpatchDataDict,runningUnitDict,patchDict)
            qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + aMarxanSolFilePath + ". Removing patches that are smaller than the specified thresholds...")

        if minpatchDataDict["add_patches"]:
            runningUnitDict = minpatch_functions.addPatches(minpatchDataDict, runningUnitDict)
            qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + aMarxanSolFilePath + ". Adding new patches...")

        if minpatchDataDict["whittle_polish"]:
            runningUnitDict = minpatch_functions.runSimWhittle(runningUnitDict, minpatchDataDict)
            qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + aMarxanSolFilePath + ". Simulated whittling...")

        if minpatchDataDict["marxan_polish"]:
            runningUnitDict = runMarxanPolish(runningUnitDict, minpatchDataDict)
            qgis.utils.iface.mainWindow().statusBar().showMessage("Processing file " + aMarxanSolFilePath + ". Marxan polish...")

        runningUnitDict = addConservedPUs(runningUnitDict,minpatchDataDict)

        if minpatchDataDict["patch_stats"]:
            patchDict = minpatch_functions.producePatchDict(runningUnitDict, minpatchDataDict)
            afterPatchStatsDict = minpatch_functions.producePatchStatsDict(patchDict,minpatchDataDict)

        # outputFilePath = setupObject.outputPath + os.sep + finalNameString
        outputFilePath = aMarxanSolFilePath.replace(marxanNameString, finalNameString)
        minpatch_outputs.printRunResults(minpatchDataDict, runningUnitDict, outputFilePath)

        costDict = makeCostDict(setupObject, minpatchDataDict,runningUnitDict)
        totalCost = costDict['totalBoundaryCost'] + costDict['totalUnitCost']

        if minpatchDataDict["patch_stats"]:
            patchResultsDict = minpatch_outputs.producePatchResultsDict(patchResultsDict, aMarxanSolFilePath, beforePatchStatsDict, afterPatchStatsDict, costDict)

        if minpatchDataDict["zone_stats"]:
            zoneStatsDict, zoneFeatureStatsDict = minpatch_outputs.makeZoneStatsDict(aMarxanSolFilePath, minpatchDataDict, runningUnitDict, zoneStatsDict, zoneFeatureStatsDict)

        if bestPortfolioCost == -1:
            bestPortfolioCost = totalCost
            bestPortfolio = copy.deepcopy(runningUnitDict)

        if bestPortfolioCost <> -1 and totalCost < bestPortfolioCost:
            bestPortfolioCost = totalCost
            bestPortfolio = copy.deepcopy(runningUnitDict)

        summedDict = minpatch_outputs.updateSummedDict(summedSolDict,runningUnitDict)

    summedFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName + '_summed.txt'
    minpatch_outputs.printSummedResults(summedDict,summedFileName)
    bestFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName + '_best.txt'
    minpatch_outputs.printRunResults(minpatchDataDict, bestPortfolio, bestFileName)

    if minpatchDataDict["patch_stats"]:
        patchstatsFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName + '_patchstats.txt'
        minpatch_outputs.printPatchStats(patchResultsDict, patchstatsFileName)

    if minpatchDataDict["zone_stats"]:
        zoneStatsFileName = setupObject.outputPath + os.sep + 'mp_' + minpatchObject.marxanFileName
        zoneTypeDict = minpatchDataDict["zoneTypeDictionary"]
        minpatch_outputs.printZoneStats(zoneTypeDict,zoneStatsDict, zoneFeatureStatsDict,zoneStatsFileName)

def makeMinpatchDataDict(setupObject, minpatchObject):
    minpatchDataDict = {}

    qgis.utils.iface.mainWindow().statusBar().showMessage("Producing initial MinPatch files...")

    unitLocString = setupObject.inputPath + os.sep + 'pu.dat'
    unitNameList = ["id", "cost", "status"]
    unitNameTypeList = ["int", "float", "int"]
    unitDict = makeDataDict(unitLocString, unitNameList, unitNameTypeList)
    minpatchDataDict["initialUnitDictionary"] = unitDict

    targetLocString = setupObject.inputPath + os.sep + 'spec.dat'
    targetNameList = ["id", "name", "target", "spf"]
    targetNameTypeList = ["int", "str", "float", "float", "int"]
    targetDict = makeDataDict(targetLocString, targetNameList, targetNameTypeList)
    minpatchDataDict["targetDictionary"] = targetDict

    abundLocString = setupObject.inputPath + os.sep + 'puvspr2.dat'
    abundDict = makeAbundDict(abundLocString, targetDict, unitDict)
    abundanceMatrixDictionary = makeAbundMatrixDict(abundLocString, abundDict, unitDict)
    minpatchDataDict["abundanceDictionary"] = abundDict
    minpatchDataDict["abundanceMatrixDictionary"] = abundanceMatrixDictionary

    boundLocString = setupObject.inputPath + os.sep + 'bound.dat'
    boundDict = makeBoundDict(boundLocString,unitDict)
    boundMatrixDict = makeBoundMatrixDict(boundLocString, boundDict, unitDict)
    minpatchDataDict["boundaryDictionary"] = boundDict
    minpatchDataDict["boundaryMatrixDictionary"] = boundMatrixDict

    unitLocString = setupObject.inputPath + os.sep + 'pu.dat'
    unitNameList = ["id", "status","xloc", "yloc"]
    unitNameTypeList = ["int","int","float","float"]
    cluzanXYDictionary = makeDataDict(unitLocString, unitNameList, unitNameTypeList)
    minpatchDataDict["cluzanXYDictionary"] = cluzanXYDictionary

    minpLocString = minpatchObject.detailsDatPath
    minpNameList = ["id","zone","patch_area","radius"]
    minpNameTypeList = ["int","float","float","float"]
    minpDict = makeDataDict(minpLocString, minpNameList, minpNameTypeList)
    minpatchDataDict["minpatchDictionary"] = minpDict

    unitLocString = minpatchObject.detailsDatPath
    unitNameList = ["id", "area"]
    unitNameTypeList = ["int","float"]
    rawAreaDictionary = makeDataDict(unitLocString, unitNameList, unitNameTypeList)
    areaDictionary = {}
    for puUnitValue in rawAreaDictionary:
        areaDictionary[puUnitValue] = rawAreaDictionary[puUnitValue][0]
    minpatchDataDict["areaDictionary"] = areaDictionary

    zonalLocString = minpatchObject.detailsDatPath
    zonalNameList = ["id", "zone", "patch_area", "radius"]
    zonalNameTypeList  = ["int", "int", "float", "float"]
    zoneDict = makeDataDict(zonalLocString, zonalNameList, zonalNameTypeList)
    minpatchDataDict["zoneDictionary"] = zoneDict

    zoneTypeDict = {}
    for aRow in zoneDict:
        zoneList = zoneDict[aRow]
        zoneID = zoneList[0]
        if zoneID in zoneTypeDict:
            continue
        else:
            patchValue = zoneList[1]
            radiusValue = zoneList[2]
            zoneTypeDict[zoneID] = [float(patchValue), float(radiusValue)]
    minpatchDataDict["zoneTypeDictionary"] = zoneTypeDict

    if len(zoneTypeDict.keys()) > 1:
        minpatchObject.zonestatsBool = True
    else:
        minpatchObject.zonestatsBool = False

    minpatchDataDict["bound_cost"] = minpatchObject.blm #float(setupDict["bound_cost"])
    minpatchDataDict["rem_small_patch"] = minpatchObject.removeBool #setupDict["rem_small_patch"]
    minpatchDataDict["add_patches"] = minpatchObject.addBool #setupDict["add_patches"]
    minpatchDataDict["whittle_polish"] = minpatchObject.whittleBool #setupDict["whittle_polish"]
    minpatchDataDict["marxan_polish"] = minpatchObject.marxanBool #setupDict["marxan_polish"]
    minpatchDataDict["patch_stats"] = True #setupDict["patch_stats"]
    minpatchDataDict["zone_stats"] = minpatchObject.zonestatsBool #setupDict["zone_stats"]

    return minpatchDataDict

def producePatchDetails(setupObject, minpatchDataDict):
    makeTextFileBool = checkNeighbPUIDFile(setupObject, minpatchDataDict)
    if makeTextFileBool == 1:
        radiusNeighbDict = makeRadiusPUDict(setupObject, minpatchDataDict)
        makeNeighbPUID(radiusNeighbDict,setupObject, minpatchDataDict)

    qgis.utils.iface.mainWindow().statusBar().showMessage("Producing MinPatch patch files...")
    addNeighbPUIDDict = makeNeighbPUIDDict(setupObject, minpatchDataDict, "add")
    minpatchDataDict["addNeighbPUIDDictionary"] = addNeighbPUIDDict

    whittleNeighbPUIDDict = makeNeighbPUIDDict(setupObject, minpatchDataDict, "whittle")
    minpatchDataDict["whittleNeighbPUIDDict"] = whittleNeighbPUIDDict

    patchAreaDict = makePatchAreaDict(setupObject, minpatchDataDict)
    minpatchDataDict["patchAreaDictionary"] = patchAreaDict

    return minpatchDataDict

def returnValue(theString, theType):
    theFinalValue = 0
    if theType == "str":
        theFinalValue = theString
    if theType == "int":
        theFinalValue = int(theString)
    if theType == "float":
        theFinalValue = float(theString)

    return theFinalValue

def makeDataDict(filePath, headerNamesList, headerTypeList):
    dataDict = {}
    dataFile =  open(filePath,'r')
    dataText = dataFile.read()
    dataText.strip
    dataRows = dataText.split('\n')
    rawDataHeaderList = dataRows[0].split(',')
    dataHeaderList = []
    for rawHeaderString in rawDataHeaderList:
        aHeaderString = string.replace(rawHeaderString,'"','')
        dataHeaderList.append(aHeaderString)

    idName = headerNamesList[0]
    idType = headerTypeList.pop(0)
    headingOrderList = []

    for aName in headerNamesList:
        nameOrder = dataHeaderList.index(aName)
        headingOrderList.append(nameOrder)
    del headingOrderList[0]

    del dataRows[0]

    for aRow in dataRows:
        tempRowList = aRow.split(",")
        if len(tempRowList) == len(dataHeaderList):
            idKey = returnValue(tempRowList[0],idType)
            newRowList = []
            headingOrderListLength = len(headingOrderList)
            rangeList = range(headingOrderListLength)
            for aNum in rangeList:
                theOrder = headingOrderList[aNum]
                theVariable = tempRowList[theOrder]
                theVariableType = headerTypeList[aNum]
                finalVariable = returnValue(theVariable,theVariableType)
                newRowList.append(finalVariable)
            dataDict[idKey] = newRowList
    return dataDict

def makeBoundDict(boundaryLocationString, unitDictionary):
    headerNamesList = ["id1", "id2", "boundary"]
    boundDict = {}
    boundFile =  open(boundaryLocationString,'r')
    boundText = boundFile.read()
    boundText.strip
    boundRows = boundText.split('\n')

    del boundRows[0]

    puIDList = unitDictionary.keys()
    idKey = 1
    for aRow in boundRows:
        tempRowList = aRow.split(",")
        if len(tempRowList) == len(headerNamesList):
            theID1Value = int(tempRowList[0])
            theID2Value = int(tempRowList[1])
            boundValue = float(tempRowList[2])
            if theID1Value in puIDList and theID2Value in puIDList:
                newRowList = [theID1Value,theID2Value,boundValue]
                boundDict[idKey] = newRowList
                idKey = idKey + 1
    return boundDict

def makeBoundMatrixDict(filePath, boundDictionary, unitDictionary):
    printErrorMessage = 0
    boundMatrixDict = {}
    puList = unitDictionary.keys()
    for aNum in puList:
        boundMatrixDict[aNum]={}

    for aRow in boundDictionary:
        boundList = boundDictionary[aRow]
        id1Value = int(boundList[0])
        id2Value = int(boundList[1])
        boundValue = float(boundList[2])
        try:
            boundDict1 = boundMatrixDict[id1Value]
            boundDict1[id2Value] = boundValue
            boundDict2 = boundMatrixDict[id2Value]
            boundDict2[id1Value] = boundValue
        except:
            printErrorMessage = 2
            continue

    return boundMatrixDict


def makeAbundDict(abundanceLocationString, targetDictionary, unitDictionary):
    printErrorMessage = 0
    headerNamesList = ["species","pu","amount"]
    abundDict = {}
    abundFile =  open(abundanceLocationString,'r')
    abundText = abundFile.read()
    abundText.strip
    abundRows = abundText.split('\n')
    abundHeaderList = abundRows[0].split(',')

    headingOrderList = []
    for aName in headerNamesList:
        headingOrderList.append(abundHeaderList.index(aName))

    dictName = {-1:headerNamesList}
    del abundRows[0]

    idKey = 1
    puList = unitDictionary.keys()
    featList = targetDictionary.keys()
    for aRow in abundRows:
        try:
            tempRowList = aRow.split(",")
            theFeatID = int(tempRowList[0])
            thePUID = int(tempRowList[1])
            theAmount = float(tempRowList[2])
            newRowList = [theFeatID,thePUID,theAmount]
            if theFeatID in featList and thePUID in puList:
                abundDict[idKey] = newRowList
                idKey = idKey + 1
        except:
            continue

    return abundDict

def makeAbundMatrixDict(filePath, abundDictionary, unitDictionary):
    printErrorMessage = 0
    abundMatrixDict = {}
    puList = unitDictionary.keys()
    for aNum in puList:
        abundMatrixDict[aNum]={}

    for aRow in abundDictionary:
        abundList = abundDictionary[aRow]
        sppValue = int(abundList[0])
        puValue = int(abundList[1])
        amountValue = float(abundList[2])

        try:
            abundDict = abundMatrixDict[puValue]
            abundDict[sppValue] = amountValue
        except:
            printErrorMessage = 1

    if printErrorMessage == 1:
        # minpat_messages.printErrorMessage(1)
        pass

    return abundMatrixDict

def checkNeighbPUIDFile(setupObject, dataDict):
    zoneTypeDict = dataDict["zoneTypeDictionary"]
    trueString = ""
    for aRow in zoneTypeDict:
        zoneTypeList = zoneTypeDict[aRow]
        zoneRadius = zoneTypeList[1]
        trueString += str(zoneRadius) + ", "

    addNeighbPUIDLocString = setupObject.inputPath + os.sep + 'addpatch_neighbPUID.dat'
    whittleNeighbPUIDLocString = setupObject.inputPath + os.sep + 'whittle_neighbPUID.dat'
    nameList = [addNeighbPUIDLocString, whittleNeighbPUIDLocString]
    makeTextFileBool = 0

    for locString in nameList:
        try:
            checkNeighbPUIDFile = open(locString,'r')
            testText = checkNeighbPUIDFile.read()
            testText.strip
            try:
                dataRows = testText.split('\n')
                ZoneOrNotRow = dataRows[1]
                checkRow = dataRows[2]
                if zoneString <> "true" and ZoneOrNotRow == "*** The patches are based on different parameters (zone details are below)":
                    makeTextFileBool = 1
                    print "Old PU proximity file used different zones to specify the parameters"
                    print "The current parameters specify that only one distance value should be used for all PUs"
                    print "Proximity distance specified in setup file =",minPatchDist
                    print "Making new PU proximity file"

                if zoneString <> "true" and ZoneOrNotRow == "*** The patches are based on the same parameters":
                    checkString = checkRow.split(" = ")[1]
                    if float(minPatchDist) <> float(checkString):
                        makeTextFileBool = 1
                        print "Old PU proximity file was based on proximity distance =",checkString
                        print "Proximity distance specified in setup file =",minPatchDist
                        print "Making new PU proximity file"

                if zoneString == "true" and ZoneOrNotRow == "*** The patches are based on different parameters (zone details are below)":
                    checkString = checkRow.split(" = ")[1]
                    if checkString <> trueString:
                        makeTextFileBool = 1
                        print "Old PU proximity file used values, i.e.",checkString
                        print "Proximity distance specified in zonal.dat file =",trueString
                        print "Making new PU proximity file"

                if zoneString == "true" and ZoneOrNotRow == "*** The patches are based on the same parameters":
                    makeTextFileBool = 1
                    print "Old PU proximity file only used one parameter value"
                    print "The current parameters specify to use several zonal values"
                    print "Proximity distances specified in setup file =",trueString
                    print "Making new PU proximity file"


            except:
                makeTextFileBool = 1
                print "Making new PU proximity file"

        except IOError:
            makeTextFileBool = 1
            print "Making new PU proximity file"

    return makeTextFileBool

def makeRadiusPUDict(setupObject, minpatchDataDict):
    neighbPUIDLocString = setupObject.inputPath + os.sep + 'neighbPUID.dat'
    cluzanXYDictionary = minpatchDataDict["cluzanXYDictionary"]
    unitDict = minpatchDataDict["initialUnitDictionary"]
    zoneDict = minpatchDataDict["zoneDictionary"]

    radiusNeighbDict = {}
    for aPUValue in cluzanXYDictionary:
        aXValue = cluzanXYDictionary[aPUValue][1]
        aYValue = cluzanXYDictionary[aPUValue][2]
        aStatus = cluzanXYDictionary[aPUValue][0]
        aNeighbList = []

        #This identifies which PUs are within the specified radius
        for bPUValue in cluzanXYDictionary:
            bStatus = cluzanXYDictionary[bPUValue][0]

            if aPUValue == bPUValue:
                continue
            elif aStatus == 3 or bStatus == 3:
                continue
            else:
                bXValue = cluzanXYDictionary[bPUValue][1]
                bYValue = cluzanXYDictionary[bPUValue][2]
                xDiff = aXValue - bXValue
                yDiff = aYValue - bYValue
                xDiffSquare = pow(xDiff,2)
                yDiffSquare = pow(yDiff,2)
                centrDist = math.sqrt(xDiffSquare + yDiffSquare)
                minPatchDist = float(zoneDict[aPUValue][2])
                if centrDist <= minPatchDist:
                    aNeighbList.append(bPUValue)

            radiusNeighbDict[aPUValue] = aNeighbList

    return radiusNeighbDict

def makeNeighbPUID(radiusNeighbDict, setupObject, minpatchDataDict):
    #First identify the patch within that radius that contains the focal PU
    unitDict = minpatchDataDict["initialUnitDictionary"]
    areaDict = minpatchDataDict["areaDictionary"]
    zoneDict = minpatchDataDict["zoneDictionary"]

    rawNeighbListDict = {}
    for cPUValue in radiusNeighbDict:
        radNeighbDict = {}
        cNeighbList = radiusNeighbDict[cPUValue]
        puCost = unitDict[cPUValue][0]
        puStatus = unitDict[cPUValue][1]
        if puStatus <> 3:
            radNeighbDict[cPUValue] = [puCost,1]
            for neighbPUValue in cNeighbList:
                neighbCost = unitDict[neighbPUValue][0]
                neighbStatus = unitDict[neighbPUValue][1]
                if neighbStatus <> 3:
                    radNeighbDict[neighbPUValue] = [neighbCost,1]

        focalPatchDict = minpatch_functions.producePatchDict(radNeighbDict, minpatchDataDict)
        patchNeighbList = [] #Stays blank if len(focalPatchDict) == 0
        if len(focalPatchDict) == 1:
            patchNeighbList = focalPatchDict[1][2]
        if len(focalPatchDict) > 1:
            patchNeighbList = focalPatchDict[1][2]
            for aRow in focalPatchDict:
                focalPatchDictPUList = focalPatchDict[aRow][2]
                if cPUValue in focalPatchDictPUList:
                    patchNeighbList = focalPatchDictPUList

        try:
            patchNeighbList.remove(cPUValue)
        except ValueError:
            continue

        rawNeighbListDict[cPUValue] = patchNeighbList

        #Added section to ensure only valid (large) patches are included
        finalNeighbListDict = {}
        for dPU in rawNeighbListDict:
            patchArea = 0
            dpuList = rawNeighbListDict[dPU]
            for ePU in dpuList:
                ePUArea = areaDict[ePU]
                patchArea += ePUArea
            minPatchSize = zoneDict[dPU][1]
            if patchArea > minPatchSize:
                finalNeighbListDict[dPU] = dpuList
            else:
                finalNeighbListDict[dPU] = []

    introText = "*** MinPatch v2.0 (http://www.mosaic-conservation.org)"+ "\n"
    introText += "*** The patches are based on different parameters (zone details are below)"+ "\n"
    zoneTypeDict = minpatchDataDict["zoneTypeDictionary"]
    trueString = ""
    for aRow in zoneTypeDict:
        zoneTypeList = zoneTypeDict[aRow]
        zoneRadius = zoneTypeList[1]
        trueString += str(zoneRadius) + ", "

    introText += "*** Patch search distances for the zones are = "+ trueString + "\n"
    minpatch_outputs.printDictionary(finalNeighbListDict, setupObject.inputPath + os.sep + 'addpatch_neighbPUID.dat', introText)
    minpatch_outputs.printDictionary(rawNeighbListDict, setupObject.inputPath + os.sep + 'whittle_neighbPUID.dat', introText)

def makeNeighbPUIDDict(setupObject, minpatchDataDict, string):
    if string == "add":
        neighbPUIDLocString = setupObject.inputPath + os.sep + 'addpatch_neighbPUID.dat'
    if string == "whittle":
        neighbPUIDLocString = setupObject.inputPath + os.sep + 'whittle_neighbPUID.dat'
    unitDict = minpatchDataDict["initialUnitDictionary"]

    neighbPUIDFile = open(neighbPUIDLocString,'r')
    neighbPUIDText = neighbPUIDFile.read()
    neighbPUIDText.strip
    dataRows = neighbPUIDText.split('\n')
    neighbPUIDDict = {}
    for dataLine in dataRows:
        if "***" in dataLine:
            continue
        splitDataLine = dataLine.split(': [')
        try:
            keyValue = int(splitDataLine[0])
        except ValueError:
            continue

        rawDataValues = splitDataLine[1]
        rawDataValuesList = rawDataValues.replace(']','')
        rawDataValuesList2 = rawDataValuesList.split(', ')
        finalPUIDList = []

        for rawDataValueString in rawDataValuesList2:
            try:
                neighbID = int(rawDataValueString)
                finalPUIDList.append(neighbID)

            except ValueError:
                continue

        neighbPUIDDict[keyValue] = finalPUIDList

    return neighbPUIDDict

def makePatchAreaDict(setupObject, minpatchDataDict):
    patchAreaDict = {}
    neighbPUIDDict = minpatchDataDict["addNeighbPUIDDictionary"]
    unitDict = minpatchDataDict["initialUnitDictionary"]
    areaDictionary = minpatchDataDict["areaDictionary"]

    for puIDValue in neighbPUIDDict:
        neighbIDList = neighbPUIDDict[puIDValue]
        areaValue = 0
        if len(neighbIDList) > 0:
            for neighbIDValue in neighbIDList:
                neighbStatus = unitDict[puIDValue][1]
                #Don't include excluded units in patch size
                if neighbStatus <> 3:
                    neighbArea = areaDictionary[neighbIDValue]
                    areaValue += neighbArea

        patchAreaDict[puIDValue] = areaValue

    return patchAreaDict

def makeMarxanFileList(setupObject, marxanNameString):
    marxanFileList = []
    rawList = os.listdir(setupObject.outputPath)
    for aString in rawList:
        if aString.startswith(marxanNameString):
            bString = setupObject.outputPath + os.sep + aString
            cString = os.path.normpath(bString)
            marxanFileList.append(cString)

    return marxanFileList

def createRunningUnitDictionary(minpatchDataDict, aMarxanSolFilePath):
    preMarxanUnitDict = minpatchDataDict["initialUnitDictionary"]
    initUnitDict = copy.deepcopy(preMarxanUnitDict)
    solHeaderNamesList = ["planning_unit", "solution"]
    solHeaderTypeList = ["int", "int"]
    aMarxanSolDict = makeDataDict(aMarxanSolFilePath, solHeaderNamesList, solHeaderTypeList)
    runningUnitDict = MakeStartUnitDict(initUnitDict, aMarxanSolDict)

    return runningUnitDict

def MakeStartUnitDict(unitDictionary, marxanSolDictionary):
    for aRow in marxanSolDictionary:
        solPUStatus = marxanSolDictionary[aRow][0]
        if solPUStatus == 1:
            puList = unitDictionary[aRow]
            puList[1] = 1
            unitDictionary[aRow] = puList

    return unitDictionary

def runMarxanPolish(runningUnitDict, minpatchDataDict):
    polishEdgePUList = minpatch_functions.makeEdgePUList(runningUnitDict, minpatchDataDict)
    runningUnitDict = minpatch_functions.marxanPolishPUDict(minpatchDataDict, runningUnitDict,polishEdgePUList)
    if minpatchDataDict["patch_stats"]:
        patchDict = minpatch_functions.producePatchDict(runningUnitDict, minpatchDataDict)

    return runningUnitDict

def addConservedPUs(runningUnitDict, minpatchDataDict):
    initUnitDict = minpatchDataDict["initialUnitDictionary"]
    for puUnitValue in runningUnitDict:
        if initUnitDict[puUnitValue][1] == 2:
            puList = runningUnitDict[puUnitValue]
            puList[1] = 2
            runningUnitDict[puUnitValue] = puList

    return runningUnitDict

def makeCostDict(setupObject, minpatchDataDictionary, unitDictionary):
    costDict = {}

    abundanceMatrixDictionary = minpatchDataDictionary["abundanceMatrixDictionary"]
    abundanceDictionary = minpatchDataDictionary["abundanceDictionary"]
    targetDictionary = minpatchDataDictionary["targetDictionary"]
    boundaryDictionary = minpatchDataDictionary["boundaryDictionary"]

    numActivePUs = 0
    targetList = targetDictionary.keys()
    targetList.sort()
    abundValuesDict = {}
    for aRow in targetList:
        abundValuesDict[aRow] = [0,0,0,0]

    for aUnit in abundanceMatrixDictionary:

        puList = unitDictionary[aUnit]
        puStatus = puList[1]
        #Count the number of units that could be selected in the iteration section
        if puStatus == 0 or puStatus ==1:
            numActivePUs += 1
        puAbundDict = abundanceMatrixDictionary[aUnit]
        for aFeature in puAbundDict:
            theAmount = puAbundDict[aFeature]
            featureList = abundValuesDict[aFeature]
            runningValue = featureList[puStatus]
            runningValue += theAmount
            featureList[puStatus] = runningValue
            abundValuesDict[aFeature] = featureList

    costDict["abundanceValuesDictionary"] = abundValuesDict
    costDict["numberActivePUs"] = numActivePUs

    ## Calculate the unit cost details
    totalUnitCost = 0
    conUnitCount = 0
    for unitID in unitDictionary:
        theList = unitDictionary[unitID]
        unitValue, unitStatus = theList
        if unitStatus == 1 or unitStatus == 2:
            totalUnitCost += unitValue
            conUnitCount += 1
    costDict["totalUnitCost"] = totalUnitCost
    costDict["conservedUnitCount"] = conUnitCount

    ##Produce the amountConservedDictionary
    amountConservedDictionary = {}

    for bNum in targetList:
        amountConservedDictionary[bNum] = 0

    for aRow in abundanceDictionary:
        abundList = abundanceDictionary[aRow]
        featureID, puIDvalue, abundValue = abundList

        unitList = unitDictionary[puIDvalue]
        unitStatus = unitList[1]
        if unitStatus == 1 or unitStatus == 2:
            conTotalValue = amountConservedDictionary[featureID]
            conTotalValue += abundValue
            amountConservedDictionary[featureID] = conTotalValue

    costDict["amountConservedDictionary"] = amountConservedDictionary

    ##Produce the target cost data
    totalTargetCost = 0
    for featureID in amountConservedDictionary.keys():
        amountConserved = amountConservedDictionary[featureID]
        targetValuesList = targetDictionary[featureID]
        theTarget = targetValuesList[1]
        thePenalty = targetValuesList[2]
        if amountConserved < theTarget:
            totalTargetCost = totalTargetCost + thePenalty

    costDict["totalTargetCost"] = totalTargetCost

    ##Produce boundary cost data
    totalBoundLength = 0
    for aValue in boundaryDictionary:
            boundList = boundaryDictionary[aValue]
            id1Value, id2Value, boundValue = boundList
            conCount = 0
            id1StatusList = unitDictionary[id1Value]
            id2StatusList = unitDictionary[id2Value]
            id1StatusValue = id1StatusList[1]
            id2StatusValue = id2StatusList[1]

            if id1StatusValue == 1 or id1StatusValue == 2:
                conCount += 1
            if id2StatusValue == 1 or id2StatusValue == 2:
                conCount += 1
            if conCount == 1:
                totalBoundLength += boundValue
            #Allow for external edges
            if conCount == 2 and id1Value == id2Value:
                totalBoundLength += boundValue

    ######################################################################################## BLMvalue = float(setupDictionary['bound_cost'])
    BLMvalue = 1
    totalBoundaryCost = totalBoundLength * BLMvalue

    costDict["totalBoundaryLength"] = totalBoundLength
    costDict["totalBoundaryCost"] = totalBoundaryCost

    return costDict