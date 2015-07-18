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

from PyQt4.QtCore import *
import qgis
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *

import os
import csv
import time
import math
import shutil
import stats

import cluz_equations


def createSpecDatFile(setupObject):
    inputPathName = setupObject.inputPath
    specDatName = inputPathName + os.sep + "spec.dat"
    specDatWriter = csv.writer(open(specDatName, "wb"))
    specDatWriter.writerow(["id", "name", "target", "spf", "type"])

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

        puDatWriter.writerow([puID, puCost, puStatusCode, xCoord, yCoord])

def createBoundDatFile(setupObject, extEdgeBool):

# ################################################################################
# Initial part of script adapted from http://www.qgistutorials.com/en/_downloads/neighbors.py
# # Copyright 2014 Ujaval Gandhi
# #
# #This program is free software; you can redistribute it and/or
# #modify it under the terms of the GNU General Public License
# #as published by the Free Software Foundation; either version 2
# #of the License, or (at your option) any later version.

# ################################################################################

    decPrec = setupObject.decimalPlaces

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    unitIDFieldOrder = provider.fieldNameIndex("Unit_ID")
    boundResultsDict = {}

    runningPUVertexDict = {}

    # Create a dictionary of all features
    feature_dict = {f.id(): f for f in puLayer.getFeatures()}

    # Build a spatial index
    index = QgsSpatialIndex()
    for aPolygon in feature_dict.values():
        index.insertFeature(aPolygon)

    progressCount = 0
    numPUs = len(feature_dict.keys())
    puIDSet = set()
    # Loop through all features and find features that touch each feature
    for aPolygon in feature_dict.values():
        puGeom = aPolygon.geometry()
        puAttributes = aPolygon.attributes()
        puID = puAttributes[unitIDFieldOrder]
        puIDSet.add(puID)
        progressCount += 1
        progressMessage = "Bound.dat file: processed " + str(progressCount) + " of " + str(numPUs) + " planning units"
        qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)

        try:
            puVertexSet = runningPUVertexDict[puID]
        except KeyError:
            aPolyPointList = puGeom.asPolygon()
            puVertexSet = convertPolygonPointList2VertexSet(aPolyPointList)
            runningPUVertexDict[puID] = puVertexSet


        # Find all features that intersect the bounding box of the current feature.
        # We use spatial index to find the features intersecting the bounding box
        # of the current feature. This will narrow down the features that we need
        # to check neighboring features.
        intersecting_pu_list = index.intersects(puGeom.boundingBox())
        neighbVertexDict = {}

        for intersecting_pu in intersecting_pu_list:
            # Look up the feature from the dictionary
            intersecting_Polygon = feature_dict[intersecting_pu]
            intersectingAttributes = intersecting_Polygon.attributes()
            intersectPUID = intersectingAttributes[unitIDFieldOrder]

            # For our purpose we consider a feature as 'neighbor' if it touches or
            # intersects a feature. We use the 'disjoint' predicate to satisfy
            # these conditions. So if a feature is not disjoint, it is a neighbor.
            if (aPolygon != intersecting_Polygon and not intersecting_Polygon.geometry().disjoint(puGeom) and not intersectPUID in puIDSet):
                intersectingAttributes = intersecting_Polygon.attributes()
                neighbPUID = intersectingAttributes[unitIDFieldOrder]

                # Get set of vertices for each neighbour. Create them first, then put them in a dict for later

                try:
                    neighPUVertexSet = runningPUVertexDict[neighbPUID]
                except KeyError:
                    neighGeom = intersecting_Polygon.geometry()
                    aNeighbPolyPointList = neighGeom.asPolygon()
                    neighPUVertexSet = convertPolygonPointList2VertexSet(aNeighbPolyPointList)
                    runningPUVertexDict[neighbPUID] = neighPUVertexSet

                neighbVertexDict[neighbPUID] = neighPUVertexSet

        vertexKeyDict = {}
        for aNeighbPUID in neighbVertexDict:
            aVertexSet = neighbVertexDict[aNeighbPUID]
            for aVertex in aVertexSet:
                vertexKeyDict[aVertex] = aNeighbPUID

        for aVertex in puVertexSet:
            (x1, y1, x2, y2) = aVertex
            xLength = x2 - x1
            yLength = y2 - y1
            vertexLength = math.sqrt(xLength**2 + yLength**2)
            try:
                bNeighbPUID = vertexKeyDict[aVertex]
                neighPUVertexSet = runningPUVertexDict[bNeighbPUID]
                runningPUVertexDict[bNeighbPUID] = neighPUVertexSet

            except KeyError:
                bNeighbPUID = puID

            if puID > bNeighbPUID:
                puDictKey = (bNeighbPUID, puID)
            else:
                puDictKey = (puID, bNeighbPUID)

            try:
                runningLengthValue = boundResultsDict[puDictKey]
                runningLengthValue += vertexLength
                boundResultsDict[puDictKey] = runningLengthValue
            except KeyError:
                boundResultsDict[puDictKey] = vertexLength

        runningPUVertexDict.pop(puID, None)

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

def checkMarxanInputValuesBool(marxanGUI, numIter, numRun, blmValue, missingProp, initialProp):
    checkBool = True

    try:
        int(numIter)
        if int(numIter) < 10000:
            checkBool = False
            QMessageBox.warning(marxanGUI,"Input error", "The number of iterations must be higher than 10000 (remind me to tell you why).")
    except ValueError:
        checkBool = False
        QMessageBox.warning(marxanGUI,"Input error", "The number of iterations must be an integer.")

    try:
        int(numRun)
        if int(numRun) < 1:
            checkBool = False
            QMessageBox.warning(marxanGUI,"Input error", "The number of runs must be 1 or more.")
    except ValueError:
        checkBool = False
        QMessageBox.warning(marxanGUI,"Input error", "The number of runs must be an integer.")

    try:
        float(blmValue)
        if float(blmValue) < 0:
            checkBool = False
            QMessageBox.warning(marxanGUI,"Input error", "The boundary length modifier must be a non-negative number.")
    except ValueError:
        checkBool = False
        QMessageBox.warning(marxanGUI,"Input error", "The boundary length modifier must be a non-negative number.")

    try:
        float(missingProp)
        if float(missingProp) < 0 or float(missingProp) > 1:
            checkBool = False
            QMessageBox.warning(marxanGUI,"Input error", "The species proportion value must be a number between 0 and 1.")
    except ValueError:
        checkBool = False
        QMessageBox.warning(marxanGUI,"Input error", "The species proportion value must be a number between 0 and 1")

    try:
        float(initialProp)
        if float(initialProp) < 0 or float(initialProp) > 1:
            checkBool = False
            QMessageBox.warning(marxanGUI,"Input error", "The proportion of planning units randomly included at the beginning of each run must be a number between 0 and 1.")
    except ValueError:
        checkBool = False
        QMessageBox.warning(marxanGUI,"Input error", "The proportion of planning units randomly included at the beginning of each run must be a number between 0 and 1.")

    return checkBool

def marxanInputDict(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool):
    marxanInputDict = {}
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
    numIter = marxanInputDict["numIter"]
    numRun = marxanInputDict["numRun"]
    blmValue = marxanInputDict["blmValue"]
    missingProp = marxanInputDict["missingProp"]
    initialProp = marxanInputDict["initialProp"]
    outputName = marxanInputDict["outputName"]
    extraOutputsBool = marxanInputDict["extraOutputsBool"]

    if marxanInputDict["extraOutputsBool"] == True:
        extraOutputValue = "2"
    else:
        extraOutputValue = "0"

    marxanPath = marxanInputDict["marxanPath"]
    marxanSetupPath = marxanInputDict["marxanSetupPath"]

    if os.path.isfile(marxanPath):
        marxanWriter = csv.writer(open(marxanSetupPath, "wb"))

        header1 = "Input file for Marxan program, written by Ian Ball, Hugh Possingham and Matt Watts."
        header2 = "This file was generated using CLUZ, written by Bob Smith"
        marxanWriter.writerow([header1])
        marxanWriter.writerow([header2])
        marxanWriter.writerow([])

        marxanWriter.writerow(["General Parameters"])
        marxanWriter.writerow(["VERSION 0.1"])
        marxanWriter.writerow(["BLM " + str(blmValue)])
        marxanWriter.writerow(["PROP  " + str(initialProp)])
        marxanWriter.writerow(["RANDSEED -1"])
        marxanWriter.writerow(["BESTSCORE  10"])
        marxanWriter.writerow(["NUMREPS " + str(numRun)])
        marxanWriter.writerow([])

        marxanWriter.writerow(["Annealing Parameters"])
        marxanWriter.writerow(["NUMITNS " + str(numIter)])
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
        marxanWriter.writerow(["SCENNAME " + outputName])
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
        marxanWriter.writerow(["MISSLEVEL  " + str(missingProp)])
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
    marxanName = os.path.basename(marxanFullName)
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
def addBestMarxanOutputToPUShapefile(setupObject, bestOutputFile, bestFieldName):
    bestDict = {}
    with open(bestOutputFile, 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        for row in reader:
            puID = int(float(row[0]))
            bestBool = int(float(row[1]))
            bestDict[puID] = bestBool

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
    puLayer.reload() #DOES THIS WORK????????????????????????????????????????????????????????????????

####################################################################http://www.opengis.ch/2015/04/29/performance-for-mass-updating-features-on-layers/
def addSummedMarxanOutputToPUShapefile(setupObject, summedOutputFile, summedFieldName):
    summedDict = {}
    with open(summedOutputFile, 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the headers
        for row in reader:
            puID = int(float(row[0]))
            summedScore = int(float(row[1]))
            summedDict[puID] = summedScore

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
            summedScore = summedDict[puID]
        puLayer.changeAttributeValue(puRow, summedFieldOrder, summedScore, True)
    puLayer.commitChanges()
    puLayer.reload() #DOES THIS WORK????????????????????????????????????????????????????????????????

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
        puFeatList = setupObject.abundPUKeyDict[puID].keys()
        for featID in puFeatList:
            featType = setupObject.targetDict[featID][1]
            if featType in typeSet:
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