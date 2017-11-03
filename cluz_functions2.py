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

from PyQt4.QtCore import *
import qgis
from qgis.core import *
from qgis.gui import *

import os
import csv
import time
import math
import shutil
import stats

import cluz_equations
import cluz_mpfunctions
import cluz_mpsetup
import cluz_mpoutputs
import cluz_setup
import cluz_messages


def createSpecDatFile(setupObject):
    inputPathName = setupObject.inputPath
    specDatName = inputPathName + os.sep + "spec.dat"
    specDatWriter = csv.writer(open(specDatName, "wb"))
    specDatWriter.writerow(["id", "name", "target", "spf", "type"])

    featNameWarning = False
    targetDict = setupObject.targetDict
    featList = targetDict.keys()
    featList.sort()
    for aFeat in featList:
        featList = targetDict[aFeat]
        featName = featList[0]
        featTarget = featList[3]
        featSpf = featList[2]
        featType = featList[1]
        specDatWriter.writerow([aFeat, featName, featTarget, featSpf, featType])


def createPuDatFile(setupObject):
    decPrec = setupObject.decimalPlaces
    inputPathName = setupObject.inputPath
    puDatName = inputPathName + os.sep + "pu.dat"
    puDatWriter = csv.writer(open(puDatName, "wb"))
    puDatWriter.writerow(["id", "cost", "status", "xloc", "yloc"])
    puStatusDict = {"Available": 0, "Earmarked": 2, "Conserved": 2, "Excluded": 3}

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puFeatures = puLayer.getFeatures()
    puIDField = puLayer.fieldNameIndex('Unit_ID')
    puCostField = puLayer.fieldNameIndex('Cost')
    puStatusField = puLayer.fieldNameIndex('Status')

    for puFeature in puFeatures:
        puDatRowList = makePUDatRowList(puFeature, puStatusDict, puIDField, puCostField, puStatusField, decPrec)
        puDatWriter.writerow(puDatRowList)

def makePUDatRowList(puFeature, puStatusDict, puIDField, puCostField, puStatusField, decPrec):
    puAttributes = puFeature.attributes()
    puID = puAttributes[puIDField]
    puCost = puAttributes[puCostField]
    puStatus = puAttributes[puStatusField]
    puStatusCode = puStatusDict[puStatus]

    puCentroid = puFeature.geometry().centroid()
    rawXCoord = puCentroid.asPoint().x()
    xCoord = round(float(rawXCoord), decPrec)
    xCoord = format(xCoord, "." + str(decPrec) + "f")

    rawYCoord = puCentroid.asPoint().y()
    yCoord = round(float(rawYCoord), decPrec)
    yCoord = format(yCoord, "." + str(decPrec) + "f")

    puDatRowList = [puID, puCost, puStatusCode, xCoord, yCoord]

    return puDatRowList


def createBoundDatFile(setupObject, extEdgeBool):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    unitIDFieldIndex = puLayer.dataProvider().fieldNameIndex("Unit_ID")
    boundResultsDict = {}
    puPolygonDict = {}
    puIDGeomDict = {}
    spatialIndex = QgsSpatialIndex()
    for aPolygon in puLayer.getFeatures():
        puPolygonDict[aPolygon.id()] = aPolygon
        puIDGeomDict[aPolygon.attributes()[unitIDFieldIndex]] = aPolygon.geometry()
        spatialIndex.insertFeature(aPolygon)

    progressCount = 1
    numPUs = len(puPolygonDict.keys())

    emptyPolgyonPUIDSet = set()
    for puID in puIDGeomDict:
        progressMessage = "Bound.dat file: processed " + str(progressCount) + " of " + str(numPUs) + " planning units"
        qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)
        progressCount += 1

        puGeom = puIDGeomDict[puID]
        puVertexSet = makeNewPUVertexSet(puGeom)
        if len(puVertexSet) == 0:
            emptyPolgyonPUIDSet.add(puID)

        neighbPUIDSet = makeNeighbPUIDSet(puPolygonDict, spatialIndex, puGeom, puID, unitIDFieldIndex)
        neighbVertexDict = makeNeighbVertexDict(puIDGeomDict, neighbPUIDSet)
        vertexKeyNeighbPUIDDict = makeVertexKeyNeighbPUIDDict(neighbVertexDict)

        for aVertex in puVertexSet:
            neighbPUID = returnNeighbPUID(vertexKeyNeighbPUIDDict, aVertex, puID)
            if puID <= neighbPUID: #This stops double counting of shared edges
                puDictKey = (puID, neighbPUID)
                boundResultsDict[puDictKey] = returnRunningLengthValue(boundResultsDict, aVertex, puDictKey)

    if len(emptyPolgyonPUIDSet) > 0:
        emptyPolgyonPUIDSetErrorMessage(emptyPolgyonPUIDSet)

    writeBoundDatFile(setupObject, boundResultsDict, setupObject.decimalPlaces, extEdgeBool)


def returnRunningLengthValue(boundResultsDict, aVertex, puDictKey):
    vertexLength = calcVertexLength(aVertex)
    try:
        runningLengthValue = boundResultsDict[puDictKey]
        runningLengthValue += vertexLength
    except KeyError:
        runningLengthValue = vertexLength

    return runningLengthValue

def returnNeighbPUID(vertexKeyDict, aVertex, puID):
    try:
        neighbPUID = vertexKeyDict[aVertex]
    except KeyError:
        neighbPUID = puID

    return neighbPUID

def makeNewPUVertexSet(puGeom):
    aPolyPointList = puGeom.asPolygon()
    puVertexSet = convertPolygonPointList2VertexSet(aPolyPointList)

    return puVertexSet

def makeNeighbVertexDict(puIDGeomDict, neighbPUIDSet):
    neighbVertexDict = {}
    for neighbPUID in neighbPUIDSet:
        neighbPUGeom = puIDGeomDict[neighbPUID]
        neighPUVertexSet = makeNewPUVertexSet(neighbPUGeom)
        neighbVertexDict[neighbPUID] = neighPUVertexSet

    return neighbVertexDict

def makeVertexKeyNeighbPUIDDict(neighbVertexDict):
    vertexKeyNeighbPUIDDict = {}
    for aNeighbPUID in neighbVertexDict:
        aVertexSet = neighbVertexDict[aNeighbPUID]
        for aVertex in aVertexSet:
            vertexKeyNeighbPUIDDict[aVertex] = aNeighbPUID

    return vertexKeyNeighbPUIDDict

def makeNeighbPUIDSet(puPolygonDict, spatialIndex, puGeom, puID, unitIDFieldIndex):
    neighbPUIDSet = set()
    intersectPUList = spatialIndex.intersects(puGeom.boundingBox())
    for aPolygon in intersectPUList:
        intersectPolygon = puPolygonDict[aPolygon]

        if (aPolygon != intersectPolygon and not intersectPolygon.geometry().disjoint(puGeom)):
            intersectingAttributes = intersectPolygon.attributes()
            neighbPUID = intersectingAttributes[unitIDFieldIndex]
            if neighbPUID != puID:
                neighbPUIDSet.add(neighbPUID)

    return neighbPUIDSet

def calcVertexLength(aVertex):
    (x1, y1, x2, y2) = aVertex
    xLength = x2 - x1
    yLength = y2 - y1
    vertexLength = math.sqrt(xLength**2 + yLength**2)

    return vertexLength


def emptyPolgyonPUIDSetErrorMessage(emptyPolgyonPUIDSet):
    emptyPolgyonPUIDList = list(emptyPolgyonPUIDSet)
    emptyPolgyonPUIDList.sort()
    puIDString = ''
    for puID in emptyPolgyonPUIDList:
        puIDString += str(puID) + ', '
    finalPUIDString = puIDString[0:-2]

    qgis.utils.iface.messageBar().pushMessage("Shapefile error", "Planning units with the following ID values have problems with their topology and could not be processed by QGIS: " + finalPUIDString, QgsMessageBar.WARNING)


def writeBoundDatFile(setupObject, boundResultsDict, decPrec, extEdgeBool):
    boundDatName = setupObject.inputPath + os.sep + "bound.dat"
    boundDatWriter = csv.writer(open(boundDatName, "wb"))
    boundDatWriter.writerow(["id1", "id2", "boundary"])

    keyList = boundResultsDict.keys()
    keyList.sort()
    for aKey in keyList:
        (id1, id2) = aKey
        rawAmount = boundResultsDict[aKey]
        aAmount = round(float(rawAmount), decPrec)
        aAmount = format(aAmount, "." + str(decPrec) + "f")
        if id1 <> id2:
            boundDatWriter.writerow([id1, id2, aAmount])
        if id1 == id2 and extEdgeBool == True:
            boundDatWriter.writerow([id1, id2, aAmount])


def convertPolygonPointList2VertexSet(polyPointList): #This deals with multi polygon planning units
    vertexSet = set()

    for aPolygonPointList in polyPointList:
        listLength = len(aPolygonPointList)
        for aNumber in range(0, listLength - 1):
            x1 = aPolygonPointList[aNumber][0]
            y1 = aPolygonPointList[aNumber][1]
            x2 = aPolygonPointList[aNumber + 1][0]
            y2 = aPolygonPointList[aNumber + 1][1]

            if x1 > x2:
                finalX1 = x2
                finalX2 = x1
            else:
                finalX1 = x1
                finalX2 = x2

            if y1 > y2:
                finalY1 = y2
                finalY2 = y1
            else:
                finalY1 = y1
                finalY2 = y2

            vecTuple = (finalX1, finalY1, finalX2, finalY2)

            vertexSet.add(vecTuple)

    return vertexSet

def returnOutputName(setupObject):
    oldOutputName = setupObject.outputName
    outputPath = setupObject.outputPath
    oldOutputBestName = outputPath + os.sep + oldOutputName + "_best.txt"

    oldOutputNameStem = ""
    numValueBool = True
    for aNum in xrange(len(oldOutputName), 0, -1):
        aChar = oldOutputName[aNum - 1]
        try:
            int(aChar)
        except ValueError:
            numValueBool = False
        if numValueBool is False:
            oldOutputNameStem = aChar + oldOutputNameStem

    if os.path.isfile(oldOutputBestName):
        nameSuffix = 1
        newName = outputPath + os.sep + oldOutputNameStem + str(nameSuffix) + "_best.txt"
        while os.path.isfile(newName):
            nameSuffix += 1
            newName = outputPath + os.sep + oldOutputNameStem + str(nameSuffix) + "_best.txt"

        outputName = oldOutputNameStem + str(nameSuffix)
    else:
        outputName = oldOutputName

    return outputName

def checkMarxanInputValuesBool(numIterString, numRunString, blmValueString, missingPropString, initialPropString, numParallelAnalyses):
    numIterBool = checkNumIter(numIterString)
    numRunBool = checkNumRuns(numRunString)
    blmValueBool = checkBlmValue(blmValueString)
    missingPropBool = checkMissingPropValue(missingPropString)
    initialPropValueBool = checkInitialPropValue(initialPropString)
    numParallelAnalysesBool = checkNumParallelAnalysesValue(numRunString, numParallelAnalyses)

    if [numIterBool, numRunBool, blmValueBool, missingPropBool, initialPropValueBool, numParallelAnalysesBool] == [True, True, True, True, True, True]:
        marxanInputValuesBool = True
    else:
        marxanInputValuesBool = False

    return marxanInputValuesBool

def checkNumIter(numIter):
    checkBool = True
    try:
        int(numIter)
        if int(numIter) < 10000:
            checkBool = False
            qgis.utils.iface.messageBar().pushMessage("Input error", "The number of iterations must be higher than 10000 because it must be be higher than the NUMTEMP value used in Marxan (see the Marxan manual for more details).", QgsMessageBar.WARNING)
    except ValueError:
        checkBool = False
        qgis.utils.iface.messageBar().pushMessage("Input error", "The number of iterations must be an integer", QgsMessageBar.WARNING)

    return checkBool

def checkNumRuns(numRun):
    checkBool = True
    try:
        int(numRun)
        if int(numRun) < 1:
            checkBool = False
            qgis.utils.iface.messageBar().pushMessage("Input error", "The number of runs must be 1 or a larger whole number", QgsMessageBar.WARNING)
    except ValueError:
        checkBool = False
        qgis.utils.iface.messageBar().pushMessage("Input error", "The number of runs must be an integer.", QgsMessageBar.WARNING)

    return checkBool

def checkBlmValue(blmValue):
    checkBool = True
    try:
        float(blmValue)
        if float(blmValue) < 0:
            checkBool = False
            qgis.utils.iface.messageBar().pushMessage("Input error", "The boundary length modifier must be a non-negative number.", QgsMessageBar.WARNING)
    except ValueError:
        checkBool = False
        qgis.utils.iface.messageBar().pushMessage("Input error", "The boundary length modifier must be a non-negative number.", QgsMessageBar.WARNING)

    return checkBool

def checkMissingPropValue(missingProp):
    checkBool = True
    try:
        float(missingProp)
        if float(missingProp) < 0 or float(missingProp) > 1:
            checkBool = False
            qgis.utils.iface.messageBar().pushMessage("Input error", "The species proportion value must be a number between 0 and 1.", QgsMessageBar.WARNING)
    except ValueError:
        checkBool = False
        qgis.utils.iface.messageBar().pushMessage("Input error", "The species proportion value must be a number between 0 and 1.", QgsMessageBar.WARNING)

    return checkBool


def checkInitialPropValue(initialProp):
    checkBool = True
    try:
        float(initialProp)
        if float(initialProp) < 0 or float(initialProp) > 1:
            checkBool = False
            qgis.utils.iface.messageBar().pushMessage("Input error", "The proportion of planning units randomly included at the beginning of each run must be a number between 0 and 1.", QgsMessageBar.WARNING)
    except ValueError:
        checkBool = False
        qgis.utils.iface.messageBar().pushMessage("Input error", "The proportion of planning units randomly included at the beginning of each run must be a number between 0 and 1.", QgsMessageBar.WARNING)

    return checkBool


def checkNumParallelAnalysesValue(numRunString, numParallelAnalyses):
    checkBool = True
    try:
        if int(numRunString) < numParallelAnalyses:
            checkBool = False
            qgis.utils.iface.messageBar().pushMessage("Input error", "The number of parallel analyses must be less than the specified number of runs.", QgsMessageBar.WARNING)
    except ValueError:
        pass

    return checkBool


def marxanInputDict(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool):
    marxanInputDict = dict()
    marxanInputDict["numIter"] = numIter
    marxanInputDict["numRun"] = numRun
    marxanInputDict["blmValue"] = blmValue
    marxanInputDict["missingProp"] = missingProp
    marxanInputDict["initialProp"] = initialProp
    marxanInputDict["outputName"] = outputName
    marxanInputDict["extraOutputsBool"] = extraOutputsBool

    marxanPath = setupObject.marxanPath
    marxanFolderName = os.path.dirname(marxanPath)
    marxanSetupPath = marxanFolderName + os.sep + "input.dat"
    marxanInputDict["marxanPath"] = marxanPath
    marxanInputDict["marxanSetupPath"] = marxanSetupPath

    return marxanInputDict


def makeMarxanInputFile(setupObject, marxanInputDict):
    if marxanInputDict["extraOutputsBool"]:
        extraOutputValue = "2"
    else:
        extraOutputValue = "0"

    marxanPath = marxanInputDict["marxanPath"]
    marxanSetupPath = marxanInputDict["marxanSetupPath"]
    if os.path.isfile(marxanPath):
        writeMarxanInputFile(setupObject, marxanInputDict, marxanSetupPath, extraOutputValue)


def writeMarxanInputFile(setupObject, marxanInputDict, marxanSetupPath, extraOutputValue):
    marxanWriter = csv.writer(open(marxanSetupPath, "wb"))

    header1 = "Input file for Marxan program, written by Ian Ball, Hugh Possingham and Matt Watts."
    header2 = "This file was generated using CLUZ, written by Bob Smith"
    marxanWriter.writerow([header1])
    marxanWriter.writerow([header2])
    marxanWriter.writerow([])

    marxanWriter.writerow(["General Parameters"])
    marxanWriter.writerow(["VERSION 0.1"])
    marxanWriter.writerow(["BLM " + str(marxanInputDict["blmValue"])])
    marxanWriter.writerow(["PROP  " + str(marxanInputDict["initialProp"])])
    marxanWriter.writerow(["RANDSEED -1"])
    marxanWriter.writerow(["BESTSCORE  10"])
    marxanWriter.writerow(["NUMREPS " + str(marxanInputDict["numRun"])])
    marxanWriter.writerow([])

    marxanWriter.writerow(["Annealing Parameters"])
    marxanWriter.writerow(["NUMITNS " + str(marxanInputDict["numIter"])])
    marxanWriter.writerow(["STARTTEMP -1.00000000000000E+0000"])
    marxanWriter.writerow(["COOLFAC  6.00000000000000E+0000"])
    marxanWriter.writerow(["NUMTEMP 10000"])
    marxanWriter.writerow([])

    marxanWriter.writerow(["Cost Threshold"])
    marxanWriter.writerow(["COSTTHRESH  0.00000000000000E+0000"])
    marxanWriter.writerow(["THRESHPEN1  1.40000000000000E+0001"])
    marxanWriter.writerow(["THRESHPEN2  1.00000000000000E+0000"])
    marxanWriter.writerow([])

    marxanWriter.writerow(["Input Files"])
    marxanWriter.writerow(["INPUTDIR " + setupObject.inputPath])
    marxanWriter.writerow(["SPECNAME spec.dat"])
    marxanWriter.writerow(["PUNAME pu.dat"])
    marxanWriter.writerow(["PUVSPRNAME puvspr2.dat"])
    marxanWriter.writerow(["MATRIXSPORDERNAME sporder.dat"])
    marxanWriter.writerow(["BOUNDNAME bound.dat"])
    marxanWriter.writerow([])

    marxanWriter.writerow(["Save Files"])
    marxanWriter.writerow(["SCENNAME " + marxanInputDict["outputName"]])
    marxanWriter.writerow(["SAVERUN " + extraOutputValue])
    marxanWriter.writerow(["SAVEBEST 2"])
    marxanWriter.writerow(["SAVESUMMARY 2"])
    marxanWriter.writerow(["SAVESCEN " + extraOutputValue])
    marxanWriter.writerow(["SAVETARGMET 2"])
    marxanWriter.writerow(["SAVESUMSOLN 2"])
    marxanWriter.writerow(["SAVELOG " + extraOutputValue])
    marxanWriter.writerow(["OUTPUTDIR " + setupObject.outputPath])
    marxanWriter.writerow([])

    marxanWriter.writerow(["Program control."])
    marxanWriter.writerow(["RUNMODE 1"])
    marxanWriter.writerow(["MISSLEVEL  " + str(marxanInputDict["missingProp"])])
    marxanWriter.writerow(["ITIMPTYPE 0"])
    marxanWriter.writerow(["HEURTYPE -1"])
    marxanWriter.writerow(["CLUMPTYPE 0"])
    marxanWriter.writerow(["VERBOSITY 3"])
    marxanWriter.writerow([])


def makeParallelAnalysesDetailsList(numParallelAnalyses, outputName, numRuns):
    parallelAnalysesDetailsList = []
    runBlock = int(numRuns) // numParallelAnalyses
    shortfallRuns = int(numRuns) - (runBlock * numParallelAnalyses)
    blockList = [runBlock] * (numParallelAnalyses - 1)
    blockList.append(runBlock + shortfallRuns)
    outputNameSuffixValue = 1
    for aBlockValue in blockList:
        outputNameBlock = outputName + "_" + str(outputNameSuffixValue)
        blockTuple = (aBlockValue, outputNameBlock)
        parallelAnalysesDetailsList.append(blockTuple)
        outputNameSuffixValue += 1

    return parallelAnalysesDetailsList


def marxanUpdateSetupObject(setupObject, outputName, numIter, numRun, blmValue, extraOutputsBool, missingProp, initialProp):
    setupObject.outputName = outputName
    setupObject.numIter = numIter
    setupObject.numRuns = numRun
    setupObject.blmValue = blmValue
    if blmValue > 0:
        blmBool = True
    else:
        blmBool = False
    setupObject.boundFlag = blmBool
    setupObject.extraOutputsFlag = extraOutputsBool
    setupObject.startProp = initialProp
    setupObject.targetProp = missingProp

    return setupObject


def makeMarxanBatFile(setupObject):
    marxanFullName = setupObject.marxanPath
    marxanBatFileName = marxanFullName.replace(".exe", ".bat")
    batWriter = csv.writer(open(marxanBatFileName, "wb"))
    batWriter.writerow(["cd " + os.path.dirname(marxanFullName)])
    batWriter.writerow([marxanFullName])

    return marxanBatFileName


def waitingForMarxan(setupObject, outputName):
    marxanPathName = setupObject.outputPath + os.sep + outputName + "_best.txt"
    try:
        while os.path.isfile(marxanPathName) is False:
            time.sleep(2)
    except KeyboardInterrupt:
        pass


def waitingForParallelMarxan(setupObject, parallelAnalysesDetailsList):
    marxanPathNameList = []
    for (numRun, outputName) in parallelAnalysesDetailsList:
        marxanPathNameList.append(setupObject.outputPath + os.sep + outputName + "_best.txt")
    waitingCount = 999
    try:
        while waitingCount > 0:
            waitingCount = 0
            for aMarxanPathName in marxanPathNameList:
                if os.path.isfile(aMarxanPathName) is False:
                    waitingCount += 1
            time.sleep(2)
    except KeyboardInterrupt:
        pass


def makeBestParralelFile(setupObject, mainOutputName, parallelAnalysesDetailsList):
    bestScoreValue = "blank"
    bestScoreOutputName = "blank"
    for (numRun, outputName) in parallelAnalysesDetailsList:
        summaryMarxanFile = setupObject.outputPath + os.sep + outputName + "_sum.txt"

        with open(summaryMarxanFile, 'rb') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                scoreValue = float(row[1])
                if scoreValue < bestScoreValue or bestScoreValue == "blank":
                    bestScoreValue = scoreValue
                    bestScoreOutputName = outputName

    bestParralelFilePath = setupObject.outputPath + os.sep + bestScoreOutputName + "_best.txt"
    bestFilePath = setupObject.outputPath + os.sep + mainOutputName + "_best.txt"
    shutil.copyfile(bestParralelFilePath, bestFilePath)

    mvbestParralelFilePath = setupObject.outputPath + os.sep + bestScoreOutputName + "_mvbest.txt"
    mvbestFilePath = setupObject.outputPath + os.sep + mainOutputName + "_mvbest.txt"
    shutil.copyfile(mvbestParralelFilePath, mvbestFilePath)


def makeSummedParralelFile(setupObject, mainOutputName, parallelAnalysesDetailsList):
    summedDict = {}
    for (numRun, outputName) in parallelAnalysesDetailsList:
        summaryMarxanFile = setupObject.outputPath + os.sep + outputName + "_ssoln.txt"

        with open(summaryMarxanFile, 'rb') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                idValue = int(row[0])
                summedValue = int(row[1])
                try:
                    runningCount = summedDict[idValue]
                except KeyError:
                    runningCount = 0
                runningCount += summedValue
                summedDict[idValue] = runningCount

    summedFilePath = setupObject.outputPath + os.sep + mainOutputName + "_ssoln.txt"
    writer = csv.writer(open(summedFilePath, "wb"))
    headerRow = ["planning_unit", "number"]
    writer.writerow(headerRow)

    summedPUIDList = summedDict.keys()
    summedPUIDList.sort()

    for aPUID in summedPUIDList:
        writer.writerow([str(aPUID), str(summedDict[aPUID])])

####################################################################http://www.opengis.ch/2015/04/29/performance-for-mass-updating-features-on-layers/
def addBestMarxanOutputToPUShapefile(setupObject, bestOutputFilePath, bestFieldName):
    bestDict = makeBestScoresDict(bestOutputFilePath)
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")
    statusFieldOrder = provider.fieldNameIndex("Status")

    bestFieldOrder = provider.fieldNameIndex(bestFieldName)
    if bestFieldOrder == -1:
        bestField = provider.addAttributes([QgsField(bestFieldName, QVariant.String)])
        puLayer.updateFields()
    bestFieldOrder = provider.fieldNameIndex(bestFieldName)

    puFeatures = puLayer.getFeatures()
    puLayer.startEditing()
    for puFeature in puFeatures:
        puRow = puFeature.id()
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldOrder]
        puStatus = puAttributes[statusFieldOrder]
        bestBool = bestDict[puID]
        if puStatus == "Conserved":
            bestStatus = "Conserved"
        elif puStatus <> "Conserved" and bestBool == 1:
            bestStatus = "Selected"
        else:
            bestStatus = "-"
        puLayer.changeAttributeValue(puRow, bestFieldOrder, bestStatus, True)
    puLayer.commitChanges()


def makeBestScoresDict(bestOutputFilePath):
    bestScoresDict = {}
    with open(bestOutputFilePath, 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        for row in reader:
            puID = int(float(row[0]))
            bestBool = int(float(row[1]))
            bestScoresDict[puID] = bestBool

    return bestScoresDict

####################################################################http://www.opengis.ch/2015/04/29/performance-for-mass-updating-features-on-layers/
def addSummedMarxanOutputToPUShapefile(setupObject, summedOutputFilePath, summedFieldName):
    summedScoreDict = makeSummedScoresDict(summedOutputFilePath)

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")
    statusFieldOrder = provider.fieldNameIndex("Status")

    summedFieldOrder = provider.fieldNameIndex(summedFieldName)
    if summedFieldOrder == -1:
        summedField = provider.addAttributes([QgsField(summedFieldName, QVariant.Int)])
        puLayer.updateFields()
        summedFieldOrder = provider.fieldNameIndex(summedFieldName)

    puFeatures = puLayer.getFeatures()
    puLayer.startEditing()
    for puFeature in puFeatures:
        puRow = puFeature.id()
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldOrder]
        puStatus = puAttributes[statusFieldOrder]
        if puStatus == "Conserved":
            summedScore = -99
        else:
            summedScore = summedScoreDict[puID]
        puLayer.changeAttributeValue(puRow, summedFieldOrder, summedScore, True)
    puLayer.commitChanges()
    puLayer.reload() #DOES THIS WORK????????????????????????????????????????????????????????????????


def makeSummedScoresDict(summedOutputFile):
    summedScoreDict = {}
    with open(summedOutputFile, 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        for row in reader:
            puID = int(float(row[0]))
            summedScore = int(float(row[1]))
            summedScoreDict[puID] = summedScore

    return summedScoreDict

def produceCountField(setupObject, countFieldName, selectedTypeList):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")

    provider.addAttributes([QgsField(countFieldName, QVariant.Int)])
    puLayer.updateFields()
    countFieldOrder = provider.fieldNameIndex(countFieldName)

    countDict = {}
    typeSet = set(selectedTypeList)
    for puID in setupObject.abundPUKeyDict:
        featCount = 0
        puFeatDict = setupObject.abundPUKeyDict[puID]
        for featID in puFeatDict:
            featAmount = puFeatDict[featID]
            featType = setupObject.targetDict[featID][1]
            if featAmount > 0 and featType in typeSet:
                featCount += 1
        countDict[puID] = featCount

    puFeatures = puLayer.getFeatures()
    puLayer.startEditing()
    for puFeature in puFeatures:
        puRow = puFeature.id()
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldOrder]
        try:
            countValue = countDict[puID]
        except KeyError:
            countValue = 0
        puLayer.changeAttributeValue(puRow, countFieldOrder, countValue, True)

    puLayer.commitChanges()

def produceRestrictedRangeField(setupObject, rangeFieldName, selectedTypeList):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")

    puIDSet = set()
    puFeatures = puLayer.getFeatures()
    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldOrder]
        puIDSet.add(puID)

    scoreDict, highScorePUID = cluz_equations.makeRestrictedRangeDict(setupObject, selectedTypeList, puIDSet)

    puLayer.startEditing()
    provider.addAttributes([QgsField(rangeFieldName, QVariant.Double)])
    puLayer.updateFields()
    rangeFieldOrder = provider.fieldNameIndex(rangeFieldName)

    puFeatures = puLayer.getFeatures()
    puLayer.startEditing()
    for puFeature in puFeatures:
        puRow = puFeature.id()
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldOrder]
        try:
            rangeValue = scoreDict[puID]
        except KeyError:
            rangeValue = 0
        puLayer.changeAttributeValue(puRow, rangeFieldOrder, rangeValue, True)

    puLayer.commitChanges()

def calcIrrepCombinationSize(setupObject, selectedTypeList):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")

    puIDSet = set()
    puFeatures = puLayer.getFeatures()
    puLayer.startEditing()
    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldOrder]
        puIDSet.add(puID)
    puSize = len(puIDSet)

    targetShortfallDict = cluz_equations.makeTargetShortfallDict(setupObject, selectedTypeList)

    selectedPUSet = set()
    loopBool = True

    while loopBool == True:
        scoreDict, highScorePUID = cluz_equations.makeRestrictedRangeDict(setupObject, selectedTypeList, puIDSet)
        selectedPUSet.add(highScorePUID)
        puIDSet.remove(highScorePUID)
        targetShortfallDict = cluz_equations.updateTargetShortfallDict(setupObject, targetShortfallDict, highScorePUID)
        loopBool = cluz_equations.checkTargetShortfallDict(targetShortfallDict)

    combSize = len(selectedPUSet)
    return combSize, puSize

def produceIrrepField(setupObject, irrepFieldName, selectedTypeList, combSize, puSize):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")

    provider.addAttributes([QgsField(irrepFieldName, QVariant.Double)])
    puLayer.updateFields()
    irrepFieldOrder = provider.fieldNameIndex(irrepFieldName)

    irrepInitVarDict = cluz_equations.makeIrrepInitVarDict(combSize, puSize)
    totFeatDict, totSqrFeatDict = cluz_equations.makeIrrepTot_Tot2FeatDict(setupObject, selectedTypeList)

    scoreDict = {}
    for puID in setupObject.abundPUKeyDict:
        irrepScore = cluz_equations.calcUnitIrreplScore(setupObject, puID, irrepInitVarDict, totFeatDict, totSqrFeatDict)
        scoreDict[puID] = irrepScore

    puFeatures = puLayer.getFeatures()
    puLayer.startEditing()
    for puFeature in puFeatures:
        puRow = puFeature.id()
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldOrder]
        try:
            irrepValue = scoreDict[puID]
        except KeyError:
            irrepValue = 0
        puLayer.changeAttributeValue(puRow, irrepFieldOrder, irrepValue, True)

    puLayer.commitChanges()

def makeParameterValueList(numAnalysesText, minAnalysesText, maxAnalysesText, exponentialBool):
    parameterValueList = []
    numAnalyses = float(numAnalysesText)
    origMinAnalyses = float(minAnalysesText)
    origMaxAnalyses = float(maxAnalysesText)

    if exponentialBool == True:
        if origMinAnalyses == 0:
            minAnalyses = 0.00000000000000000000000000000001
        else:
            minAnalyses = math.log(origMinAnalyses)
        maxAnalyses = math.log(origMaxAnalyses)
    else:
        minAnalyses = origMinAnalyses
        maxAnalyses = origMaxAnalyses

    valIncrease = (maxAnalyses - minAnalyses) / (numAnalyses - 1)

    for aValue in range(0, int(numAnalyses)):
        parameterValue = float(minAnalyses) + (valIncrease * aValue)
        if exponentialBool == True:
            if origMinAnalyses == 0 and aValue == 0:
                parameterValue = 0
            else:
                parameterValue = math.exp(parameterValue)
        parameterValueList.append(parameterValue)

    return parameterValueList

def makeAnalysisResultsDict(setupObject, marxanInputDict):
    scoreList = []
    costList = []
    puCountList = []
    connectivityCostList = []
    penaltyList = []
    mpmList = []

    summaryTextPath = setupObject.outputPath + os.sep + marxanInputDict["outputName"] + "_sum.txt"
    if os.path.isfile(summaryTextPath):
        with open(summaryTextPath, 'rb') as f:
            summaryReader = csv.reader(f)
            headerList = summaryReader.next()
            for aRow in summaryReader:
                scoreValue = float(aRow[headerList.index('Score')])
                costValue = float(aRow[headerList.index('Cost')])
                puCountValue = int(aRow[headerList.index('Planning_Units')])
                connectivityCostValue = float(aRow[headerList.index('Connectivity')])
                penaltyValue = float(aRow[headerList.index('Penalty')])
                mpmValue = float(aRow[headerList.index('MPM')])

                scoreList.append(scoreValue)
                costList.append(costValue)
                puCountList.append(puCountValue)
                connectivityCostList.append(connectivityCostValue)
                penaltyList.append(penaltyValue)
                mpmList.append(mpmValue)

        medianScore = stats.lmedianscore(scoreList)
        medianCost = stats.lmedianscore(costList)
        medianpuCount = stats.lmedianscore(puCountList)
        medianConnectivity = stats.lmedianscore(connectivityCostList)
        medianPenalty = stats.lmedianscore(penaltyList)
        medianMPM = stats.lmedianscore(mpmList)

        analysisDict = {}

        analysisDict["numIter"] = marxanInputDict["numIter"]
        analysisDict["numRun"] = marxanInputDict["numRun"]
        analysisDict["blmValue"] = marxanInputDict["blmValue"]
        analysisDict["outputName"] = str(marxanInputDict["outputName"])

        analysisDict["medianScore"] = medianScore
        analysisDict["medianCost"] = medianCost
        analysisDict["medianpuCount"] = medianpuCount
        analysisDict["medianConnectivity"] = medianConnectivity
        analysisDict["medianPenalty"] = medianPenalty
        analysisDict["medianMPM"] = medianMPM

    else:
        qgis.utils.iface.messageBar().pushMessage("No files found", "The Marxan summary file was not found and so this process will terminate.", QgsMessageBar.WARNING)

    return analysisDict

def makeCalibrateOutputFile(resultPathText, calibrateResultsDict):
    calibrateWriter = csv.writer(open(resultPathText, "wb"))

    header1 = ["Analysis", "Name", "Iterations", "Runs", "BLM"]
    header2 = ["Med Portfolio Cost", "Med Planning Unit cost", "Med Boundary length", "Med Feature Penalty cost", "Med MPM", "Med PU Count"]
    finalHeaderRow = header1 + header2
    calibrateWriter.writerow(finalHeaderRow)

    analysisNumberList = calibrateResultsDict.keys()
    analysisNumberList.sort()
    for aNumber in analysisNumberList:
        analysisDict = calibrateResultsDict[aNumber]

        numIter = analysisDict["numIter"]
        numRun = analysisDict["numRun"]
        blmValue = analysisDict["blmValue"]
        outputName = analysisDict["outputName"]

        medianScore = analysisDict["medianScore"]
        medianCost = analysisDict["medianCost"]
        medianpuCount = analysisDict["medianpuCount"]
        medianConnectivity = analysisDict["medianConnectivity"]
        medianPenalty = analysisDict["medianPenalty"]
        medianMPM = analysisDict["medianMPM"]

        rowList1 = [str(aNumber + 1), outputName, str(numIter), str(numRun), str(blmValue)]
        rowList2 = [str(medianScore), str(medianCost), str(medianConnectivity), str(medianPenalty), str(medianMPM), str(medianpuCount)]
        finalRowList = rowList1 + rowList2

        calibrateWriter.writerow(finalRowList)


def makePortfolioPUDetailsDict():
    portfolioPUDetailsDict = dict()
    portfolioPUDetailsDict["statusDetailsBool"] = False
    portfolioPUDetailsDict["spatialDetailsBool"] = False
    portfolioPUDetailsDict["sfDetailsBool"] = False
    portfolioPUDetailsDict["patchFeatDetailsBool"] = False
    portfolioPUDetailsDict["peDetailsBool"] = False

    return portfolioPUDetailsDict


def addStatusDetailsToPortfolioDict(setupObject, portfolioPUDetailsDict):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puFeatures = puLayer.getFeatures()
    idFieldIndex = puLayer.fieldNameIndex('Unit_ID')
    statusFieldIndex = puLayer.fieldNameIndex('Status')
    puDict, areaDict = makePUDictFromCLUZPortfolio(setupObject)

    rawStatusDict = {'Available': [0, 0, 0], 'Conserved': [0, 0, 0], 'Earmarked': [0, 0, 0], 'Excluded': [0, 0, 0]}
    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldIndex]
        puStatusText = str(puAttributes[statusFieldIndex])
        rawStatusDict = updatePortfolioStatusDict(rawStatusDict, puDict, areaDict, puID, puStatusText)

    portfolioPUDetailsDict["statusDetailsBool"] = True
    portfolioPUDetailsDict["statusDataDict"] = makeStatusDataDict(rawStatusDict)

    return portfolioPUDetailsDict


def updatePortfolioStatusDict(portfolioStatusDict, puDict, areaDict, puID, puStatusText):
    puArea = areaDict[puID]
    puCost = puDict[puID][0]
    puList = portfolioStatusDict[puStatusText]
    [runningArea, runningCost, runningPUCount] = puList
    puList = [runningArea + puArea, runningCost + puCost, runningPUCount + 1]
    portfolioStatusDict[puStatusText] = puList

    return portfolioStatusDict


def makeStatusDataDict(rawStatusDict):
    statusDataDict = dict()
    [availableArea, availableCost, availablePUCount] = rawStatusDict['Available']
    [conservedArea, conservedCost, conservedPUCount] = rawStatusDict['Conserved']
    [earmarkedArea, earmarkedCost, earmarkedPUCount] = rawStatusDict['Earmarked']
    [excludedArea, excludedCost, excludedPUCount] = rawStatusDict['Excluded']

    regionArea = availableArea + conservedArea + earmarkedArea + excludedArea
    regionCost = availableCost + conservedCost + earmarkedCost + excludedCost
    regionPUCount = availablePUCount + conservedPUCount + earmarkedPUCount + excludedPUCount

    portfolioArea = conservedArea + earmarkedArea
    portfolioCost = conservedCost + earmarkedCost
    portfolioPUCount = conservedPUCount + earmarkedPUCount

    statusDataDict['Region'] = [regionArea, regionCost, regionPUCount]
    statusDataDict['Portfolio'] = [portfolioArea, portfolioCost, portfolioPUCount]
    statusDataDict['Available'] = rawStatusDict['Available']
    statusDataDict['Conserved'] = rawStatusDict['Conserved']
    statusDataDict['Earmarked'] = rawStatusDict['Earmarked']
    statusDataDict['Excluded'] = rawStatusDict['Excluded']

    return statusDataDict


def addSpatialDetailsToPortfolioDict(setupObject, portfolioPUDetailsDict):
    puDict, patchDict, dummyZoneDict = makePatchDictBasedOnDummyZoneFile(setupObject)
    spatialDataDict = makeSpatialDataDict(setupObject, puDict, patchDict, dummyZoneDict)
    portfolioPUDetailsDict["spatialDetailsBool"] = True
    portfolioPUDetailsDict["spatialDataDict"] = spatialDataDict

    return portfolioPUDetailsDict


def makePatchDictBasedOnDummyZoneFile(setupObject):
    puDict, areaDict = makePUDictFromCLUZPortfolio(setupObject)
    minpatchDataDict = {'areaDictionary': areaDict}
    boundMatrixDict = checkMakeBoundDatFile(setupObject, puDict)
    minpatchDataDict["boundaryMatrixDictionary"] = boundMatrixDict
    dummyZoneDict = makeDummyZoneDict(puDict)
    minpatchDataDict["zoneDictionary"] = dummyZoneDict
    patchDict = cluz_mpfunctions.makePatchDict(puDict, minpatchDataDict)

    return puDict, patchDict, dummyZoneDict


def makeSpatialDataDict(setupObject, puDict, patchDict, dummyZoneDict):
    spatialDataDict = dict()
    allAreaList, validAreaList = cluz_mpoutputs.makePatchAreaLists(patchDict, dummyZoneDict) #validAreaList is irrelevant
    allAreaList.sort()
    if len(allAreaList) > 0:
        spatialDataDict['patchCount'] = len(allAreaList)
        spatialDataDict['patchMedian'] = stats.lmedianscore(allAreaList)
        spatialDataDict['patchSmallest'] = allAreaList[0]
        spatialDataDict['patchLargest'] = allAreaList[-1]
    else:
        spatialDataDict['patchCount'] = 0
        spatialDataDict['patchMedian'] = 0
        spatialDataDict['patchSmallest'] = 0
        spatialDataDict['patchLargest'] = 0

    boundMatrixDict = checkMakeBoundDatFile(setupObject, puDict)
    spatialDataDict['totalBoundLength'] = calcTotalBoundLength(boundMatrixDict, puDict)

    return spatialDataDict


def makePUDictFromCLUZPortfolio(setupObject):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puFeatures = puLayer.getFeatures()
    idFieldIndex = puLayer.fieldNameIndex('Unit_ID')
    areaFieldIndex = puLayer.fieldNameIndex('Area')
    costFieldIndex = puLayer.fieldNameIndex('Cost')
    statusFieldIndex = puLayer.fieldNameIndex('Status')

    puDict = {}
    puStatusDict = {'Available': 0, 'Conserved': 2, 'Earmarked': 2, 'Excluded': 3}

    areaDict = {}

    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        puID = puAttributes[idFieldIndex]
        puArea = puAttributes[areaFieldIndex]
        puCost = puAttributes[costFieldIndex]
        puStatusText = str(puAttributes[statusFieldIndex])
        puStatus = puStatusDict[puStatusText]

        puDict[puID] = [puCost, puStatus]
        areaDict[puID] = puArea

    return puDict, areaDict


def checkMakeBoundDatFile(setupObject, puDict):
    boundDatFilePath = setupObject.inputPath + os.sep + 'bound.dat'
    if os.path.exists(boundDatFilePath):
        boundMatrixDict = cluz_mpsetup.makeBoundMatrixDict(boundDatFilePath, puDict)
    else:
        qgis.utils.iface.messageBar().pushMessage("Creating Bound.dat file", "CLUZ uses the Marxan bound.dat file to calculate the patch statistics. This did not exist and so has been created.", QgsMessageBar.INFO)
        extEdgeBool = False
        createBoundDatFile(setupObject, extEdgeBool)
        boundMatrixDict = cluz_mpsetup.makeBoundMatrixDict(boundDatFilePath, puDict)

    return boundMatrixDict


def makeDummyZoneDict(puDict):
    dummyZoneDict = {}
    for puID in puDict:
        dummyZoneDict[puID] = [1, 0, 0]

    return dummyZoneDict


def calcTotalBoundLength(boundaryMatrixDict, puDict):
    totalBoundLength = 0

    for id1Value in boundaryMatrixDict:
        puBoundDict = boundaryMatrixDict[id1Value]
        for id2Value in puBoundDict:
            if id2Value >= id1Value:
                boundValue = puBoundDict[id2Value]
                conCount = 0
                id1StatusValue = puDict[id1Value][1]
                id2StatusValue = puDict[id2Value][1]

                if id1StatusValue == 1 or id1StatusValue == 2:
                    conCount += 1
                if id2StatusValue == 1 or id2StatusValue == 2:
                    conCount += 1
                if conCount == 1:
                    totalBoundLength += boundValue
                #Allow for external edges
                if conCount == 2 and id1Value == id2Value:
                    totalBoundLength += boundValue

    return totalBoundLength


def returnStatusTabStringValues(setupObject, statusDataDict, statusType):
    decPrec = setupObject.decimalPlaces
    costValue = statusDataDict[statusType][0]
    limboCostValue = round(float(costValue), decPrec)
    costString = format(limboCostValue, "." + str(decPrec) + "f")

    areaValue = statusDataDict[statusType][1]
    limboAreaValue = round(float(areaValue), decPrec)
    areaString = format(limboAreaValue, "." + str(decPrec) + "f")

    countString = str(statusDataDict[statusType][2])

    return costString, areaString, countString


def makeSpatialTableItemDict(setupObject, spatialDataDict):
    decPrec = setupObject.decimalPlaces
    spatialTableItemDict = dict()
    spatialTableItemDict[0] = ['Number of patches', str(spatialDataDict['patchCount'])]

    smallPatchSize = spatialDataDict['patchSmallest']
    limboSmallPatchSize = round(float(smallPatchSize), decPrec)
    smallPatchSizeString = format(limboSmallPatchSize, "." + str(decPrec) + "f")
    spatialTableItemDict[1] = ['Area of smallest patch', smallPatchSizeString]

    medianPatchSize = spatialDataDict['patchMedian']
    limboMedianPatchSize = round(float(medianPatchSize), decPrec)
    medianPatchSizeString = format(limboMedianPatchSize, "." + str(decPrec) + "f")
    spatialTableItemDict[2] = ['Median area of patches', medianPatchSizeString]

    largePatchSize = spatialDataDict['patchLargest']
    limboLargePatchSize = round(float(largePatchSize), decPrec)
    largePatchSizeString = format(limboLargePatchSize, "." + str(decPrec) + "f")
    spatialTableItemDict[3] = ['Area of largest patch', largePatchSizeString]

    boundaryLength = spatialDataDict['totalBoundLength']
    limboBoundaryLength = round(float(boundaryLength), decPrec)
    boundaryString = format(limboBoundaryLength, "." + str(decPrec) + "f")
    spatialTableItemDict[4] = ['Portfolio boundary length', boundaryString]

    return spatialTableItemDict


def addSFDetailsToPortfolioDict(portfolioPUDetailsDict, sfValueList, sfRunsValue):
    sfDataDict = dict()
    sfValueList.sort()

    zeroSFCount, greaterThanZeroCount = countSFValuesZeroesGreaterThanZero(sfValueList)

    sfDataDict[0] = ['Equals 0', str(zeroSFCount)]
    sfDataDict[1] = ['Greater than 0', str(greaterThanZeroCount)]
    sfDataDict[2] = ['---', '---']

    sfDataDictKey = 3
    sfQuartileTupleList = makeSFQuartileTupleList(sfRunsValue)
    for (rangeName, minRangeValue, maxRangeValue) in sfQuartileTupleList:
        sfRangeValueList = makeSFRangeValueList(sfValueList, minRangeValue, maxRangeValue)
        finalRangeName = rangeName + ': ' + str(minRangeValue) + " - " + str(maxRangeValue)
        sfDataDict[sfDataDictKey] = [finalRangeName, str(len(sfRangeValueList))]
        sfDataDictKey += 1
    sfDataDict[7] = ['---', '---']

    top5pcValue = int(sfRunsValue * 0.95)
    top5pcValueName = "Top 5% of SF values" + ': ' + str(top5pcValue) + " - " + str(sfRunsValue)
    sfDataDict[8] = [top5pcValueName, str(len(makeSFRangeValueList(sfValueList, top5pcValue, sfRunsValue)))]
    sfDataDict[9] = ['Max SF: ' + str(sfRunsValue), str(sfValueList.count(sfRunsValue))]

    portfolioPUDetailsDict["sfDetailsBool"] = True
    portfolioPUDetailsDict["sfDataDict"] = sfDataDict

    return portfolioPUDetailsDict


def makeFullSFValueList(setupObject, sfFieldName):
    sfValueList = list()
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puFeatures = puLayer.getFeatures()
    sfFieldIndex = puLayer.fieldNameIndex(sfFieldName)
    statusFieldIndex = puLayer.fieldNameIndex('Status')

    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        puSFValue = puAttributes[sfFieldIndex]
        if puSFValue >= 0:
            puStatusText = puAttributes[statusFieldIndex]
            if puStatusText == 'Available' or puStatusText == 'Earmarked':
                sfValueList.append(puSFValue)

    return sfValueList

def countSFValuesZeroesGreaterThanZero(fullSFValueList):
    zeroSFCount, greaterThanZeroCount = 0, 0
    for aValue in fullSFValueList:
        if aValue == 0:
            zeroSFCount += 1
        elif aValue > 0:
            greaterThanZeroCount += 1

    return zeroSFCount, greaterThanZeroCount

def makeSFRangeValueList(fullSFValueList, minRange, maxRange):
    sfValueList = list()
    for aValue in fullSFValueList:
        if aValue >= minRange and aValue <= maxRange:
            sfValueList.append(aValue)

    return sfValueList


def makeSFQuartileTupleList(sfRunsValue):
    sfQuartileTupleList = list()
    sfQuartileTupleList.append(("1st Quartile", 1, int(sfRunsValue * 0.25)))
    sfQuartileTupleList.append(("2nd Quartile", int(sfRunsValue * 0.25) + 1, int(sfRunsValue * 0.5)))
    sfQuartileTupleList.append(("3rd Quartile", int(sfRunsValue * 0.5) + 1, int(sfRunsValue * 0.75)))
    sfQuartileTupleList.append(("4th Quartile", int(sfRunsValue * 0.75) + 1, sfRunsValue))

    return sfQuartileTupleList


def makeSFFieldList(setupObject):
    sfFieldList = []
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")

    for aField in puLayer.pendingFields():
        if str(aField.typeName()) == 'Integer' and str(aField.name()) != 'Unit_ID':
            sfFieldList.append(aField.name())

    if len(sfFieldList) == 0:
        sfFieldList.append("No suitable fields")

    return sfFieldList


def addPatchFeatDetailsToPortfolioDict(setupObject, portfolioPUDetailsDict):
    puDict, patchDict, dummyZoneDict = makePatchDictBasedOnDummyZoneFile(setupObject) #Only need patchDict
    patchFeatDataDict = makePatchFeatDataDict(setupObject, patchDict)

    portfolioPUDetailsDict["patchFeatDetailsBool"] = True
    portfolioPUDetailsDict["patchFeatDataDict"] = patchFeatDataDict

    return portfolioPUDetailsDict


def makePatchFeatDataDict(setupObject, patchDict):
    if setupObject.setupStatus == "files_checked":
        if setupObject.abundPUKeyDict == "blank":
            setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

    patchFeatDataDict = dict()
    for patchID in patchDict:
        patchFeatPresenceSet = set()
        patchPUIDList = patchDict[patchID][2]
        for puID in patchPUIDList:
            try:
                puIDFeatSet = set(setupObject.abundPUKeyDict[puID].keys())
                patchFeatPresenceSet = patchFeatPresenceSet.union(puIDFeatSet)
            except KeyError:
                pass
        for featID in patchFeatPresenceSet:
            try:
                featCount = patchFeatDataDict[featID]
            except KeyError:
                featCount = 0
            featCount += 1
            patchFeatDataDict[featID] = featCount

    return patchFeatDataDict

def returnSelectedPUIDDict(setupObject):
    selectedPUIDDict = dict()

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    qgis.utils.iface.setActiveLayer(puLayer)
    puLayer = qgis.utils.iface.activeLayer()
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")
    statusFieldOrder = provider.fieldNameIndex("Status")

    selectedPUs = puLayer.selectedFeatures()
    for aPU in selectedPUs:
        puID = aPU.attributes()[idFieldOrder]
        puStatus = str(aPU.attributes()[statusFieldOrder])
        selectedPUIDDict[puID] = puStatus

    return selectedPUIDDict

def returnSelectedPUDetailsDict(setupObject, selectedPUIDDict):
    selectedPUDetailsDict = dict()
    for puID in selectedPUIDDict:
        puStatus = selectedPUIDDict[puID]
        puAbundDict = setupObject.abundPUKeyDict[puID]
        try:
            statusDetailsDict = selectedPUDetailsDict[puStatus]
        except KeyError:
            statusDetailsDict = dict()

        for featID in puAbundDict:
            try:
                featAmount = puAbundDict[featID]
            except KeyError:
                featAmount = 0
            try:
                featRunningAmount = statusDetailsDict[featID] + featAmount
            except KeyError:
                featRunningAmount = 0
            featRunningAmount += featAmount
            statusDetailsDict[featID] = featRunningAmount

        selectedPUDetailsDict[puStatus] = statusDetailsDict

    return selectedPUDetailsDict

def returnStringAmountPerStatus(setupObject, selectedPUDetailsDict, statusValue, featID):
    decPrec = setupObject.decimalPlaces
    try:
        featAmount = selectedPUDetailsDict[statusValue][featID]
        featAmountRound = round(float(featAmount), decPrec)
        featAmountString = format(featAmountRound, "." + str(decPrec) + "f")

    except KeyError:
        featAmountString = '0'

    return featAmountString


def returnStringShortfall(setupObject, featID):
    decPrec = setupObject.decimalPlaces
    targetAmount = setupObject.targetDict[featID][3]
    conAmount = setupObject.targetDict[featID][4]
    if conAmount >= targetAmount:
        stringShortfall = 'Target met'
    else:
        shortValue = targetAmount - conAmount
        shortValueRound = round(float(shortValue), decPrec)
        stringShortfall = format(shortValueRound, "." + str(decPrec) + "f")


    return stringShortfall


def makePatchPortfolioDict(portfolioPathNameText):
    try:
        portfolioOKBool, portfolioDict = cluz_mpsetup.makeMarxanSolDict(portfolioPathNameText)
    except IOError:
        qgis.utils.iface.messageBar().pushMessage("File error", "The specified file path is not valid. Please select another one.", QgsMessageBar.WARNING)
        portfolioOKBool = False
        portfolioDict = dict()

    return portfolioOKBool, portfolioDict

def portfolioNotOKErrorMessage():
    qgis.utils.iface.messageBar().pushMessage("File error", "The specified file is not valid. It should consist of two fields: the first lists the planning unit ID values and the second shows a 0 or 1.", QgsMessageBar.WARNING)


def makePatchPortfolioShapefile(setupObject, portfolioDict):
    pass
