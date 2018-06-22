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
from qgis.analysis import *

import os
import csv

import cluz_setup


def returnConTotDict(setupObject):
    newConTotDict = {}
    for featID in setupObject.targetDict.keys():
        newConTotDict[featID] = [0, 0]

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puFeatures = puLayer.getFeatures()
    unitIDField = puLayer.fieldNameIndex('Unit_ID')
    unitStatusField = puLayer.fieldNameIndex('Status')

    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        unitID = puAttributes[unitIDField]
        unitStatus = puAttributes[unitStatusField]
        try:
            puAbundDict = setupObject.abundPUKeyDict[unitID]
            for featID in puAbundDict:
                featAmount = puAbundDict[featID]
                oldConAmount = newConTotDict[featID][0]
                oldTotalAmount = newConTotDict[featID][1]
                newTotalAmount = oldTotalAmount + featAmount
                if unitStatus == "Earmarked" or unitStatus == "Conserved":
                    newConAmount = oldConAmount + featAmount
                else:
                    newConAmount = oldConAmount

                newConTotDict[featID] = [newConAmount, newTotalAmount]
        except KeyError:
            pass

    return newConTotDict


def updateConTotFieldsTargetDict(setupObject, newConTotDict):
    targetDict = setupObject.targetDict
    decPrec = setupObject.decimalPlaces
    for featID in newConTotDict:
        targetList = targetDict[featID]
        featTarget = targetList[3]
        targetList[4] = newConTotDict[featID][0]
        targetList[5] = newConTotDict[featID][1]

        if featTarget > 0:
            pcTarget = targetDict[featID][4] / featTarget
            pcTarget *= 100
            pcTarget = round(float(pcTarget), decPrec)
            pcTarget = format(pcTarget, "." + str(decPrec) + "f")
        else:
            pcTarget = -1
        targetList[6] = pcTarget

        targetDict[featID] = targetList
    return targetDict

def makeVecAddAbundDict(setupObject, layerList, idFieldName, convFactor):
    addAbundDict = {}
    addFeatIDSet = set()
    decPrec = setupObject.decimalPlaces

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")

    layerNumber = 1
    for aLayer in layerList:
        layerGeomType = aLayer.geometryType()
        qgis.utils.iface.mainWindow().statusBar().showMessage("Intersecting layer " + str(layerNumber) + "...")

        dirPath = os.path.dirname(setupObject.puPath)
        intersectShapeFileNameNumber = cluz_setup.returnLowestUnusedFileNameNumber(dirPath, "temp_int", ".shp")
        tempIntersectLayer = dirPath + os.sep + "temp_int" + str(intersectShapeFileNameNumber) + ".shp"
        overlayAnalyzer = QgsOverlayAnalyzer()
        overlayAnalyzer.intersection(puLayer, aLayer, tempIntersectLayer)
        outputLayer = QgsVectorLayer(tempIntersectLayer, "Temp", "ogr")
        outputFeatures = outputLayer.getFeatures()

        outputIDField = outputLayer.fieldNameIndex('Unit_ID')
        outputFeatIDField = outputLayer.fieldNameIndex(idFieldName)

        if layerGeomType == 1:
            lineBool = True
            polyBool = False
        elif layerGeomType == 2:
            lineBool = False
            polyBool = True

        qgis.utils.iface.mainWindow().statusBar().showMessage("Calculating data from layer " + str(layerNumber) + "...")
        attributeFeatureError = False
        for outputFeature in outputFeatures:
            outputAttributes = outputFeature.attributes()
            unitID = outputAttributes[outputIDField]
            featID = outputAttributes[outputFeatIDField]
            addFeatIDSet.add(featID)

            #Produce intersect of lines
            if lineBool:
                try:
                    finalShapeAmount = calcFeatLineLengthInPU(outputFeature, convFactor, decPrec)
                except AttributeError:
                    finalShapeAmount = -1

            #Produce intersect of polygons
            if polyBool:
                try:
                    finalShapeAmount = calcFeatPolygonAreaInPU(outputFeature, convFactor, decPrec)
                except AttributeError:
                    finalShapeAmount = -1

            if finalShapeAmount > 0:
                try:
                    puAddAbundDict = addAbundDict[unitID]
                except KeyError:
                    puAddAbundDict = {}
                try:
                    addAmount = puAddAbundDict[featID]
                except KeyError:
                    addAmount = 0
                addAmount += finalShapeAmount
                puAddAbundDict[featID] = addAmount
                addAbundDict[unitID] = puAddAbundDict
            else:
                attributeFeatureError = True

        if attributeFeatureError:
             qgis.utils.iface.messageBar().pushMessage("Layer warning: ", "Layer " + str(aLayer.name()) + " contains at least one feature that produces fragments with no spatial characteristics when intersected with the planning units.", QgsMessageBar.WARNING)
        layerNumber += 1

    qgis.utils.iface.mainWindow().statusBar().showMessage("")
    addFeatIDList = list(addFeatIDSet)
    addFeatIDList.sort()
    return addAbundDict, addFeatIDList

def calcFeatLineLengthInPU(outputFeature, convFactor, decPrec):
    outputGeom = outputFeature.geometry()
    intersectShapeAmount = outputGeom.length()
    shapeAmount = intersectShapeAmount / convFactor
    finalShapeAmount = round(shapeAmount, decPrec)

    return finalShapeAmount

def calcFeatPolygonAreaInPU(outputFeature, convFactor, decPrec):
    outputGeom = outputFeature.geometry()
    intersectShapeAmount = outputGeom.area()
    shapeAmount = intersectShapeAmount / convFactor
    finalShapeAmount = round(shapeAmount, decPrec)

    return finalShapeAmount

def makeCsvAddAbundDict(setupObject, csvFilePath, rawUnitIDFieldName, convFactor):
    addAbundDict = {}
    featIDList = []
    warningStatus = "None"
    unitIDFieldName = str(rawUnitIDFieldName)# Removes u from beginning of string

    csvFile = open(csvFilePath, 'rb')
    headerReader = csv.reader(csvFile)
    fileHeaderList = headerReader.next()
    fileHeaderList.remove(unitIDFieldName)
    featHeaderDict = {}
    for aFeatHeader in fileHeaderList:
        featID = cluz_setup.removePrefixMakeIDValue(aFeatHeader)
        featHeaderDict[aFeatHeader] = featID
        featIDList.append(featID)

    if len(set(featIDList).intersection(set(setupObject.targetDict.keys()))) != 0:
        warningStatus = "ExistingFeatures"
    if featIDList.count("") != 0:
        warningStatus = "HeaderWithNoID"

    if warningStatus == "None":
        addAbundDict = makeAddAbundDict(csvFilePath, featHeaderDict, fileHeaderList, unitIDFieldName, convFactor)

    return addAbundDict, featIDList, warningStatus

def makeAddAbundDict(csvFilePath, featHeaderDict, fileHeaderList, unitIDFieldName, convFactor):
    addAbundDict = {}
    with open(csvFilePath, 'rb') as f:
        dataDict = csv.DictReader(f)
        for aDict in dataDict:
            unitID = int(aDict[unitIDFieldName])
            for aHeader in fileHeaderList:
                origAbundValue = float(aDict[aHeader])
                abundValue = origAbundValue / convFactor
                featID = featHeaderDict[aHeader]
                if abundValue > 0:
                    try:
                        puAddAbundDict = addAbundDict[unitID]
                    except KeyError:
                        puAddAbundDict = {}
                    try:
                        addAmount = puAddAbundDict[featID]
                    except KeyError:
                        addAmount = 0
                    addAmount += abundValue
                    puAddAbundDict[featID] = addAmount
                    addAbundDict[unitID] = puAddAbundDict

    return addAbundDict

def addAbundDictToAbundPUKeyDict(setupObject, addAbundDict):
    abundPUKeyDict = setupObject.abundPUKeyDict
    for puID in addAbundDict:
        puAddAbundDict = addAbundDict[puID]
        try:
            puAbundDict = setupObject.abundPUKeyDict[puID]
        except KeyError:
            puAbundDict = {}
        for aFeat in puAddAbundDict:
            aAmount = puAddAbundDict[aFeat]
            puAbundDict[aFeat] = aAmount

        abundPUKeyDict[puID] = puAbundDict

    return abundPUKeyDict

def addFeaturesToPuvspr2File(setupObject, addAbundDict):
    for puID in addAbundDict:
        puAddAbundDict = addAbundDict[puID]
        try:
            puAbundDict = setupObject.abundPUKeyDict[puID]
        except KeyError:
            puAbundDict = {}
        for featID in puAddAbundDict:
            puAbundDict[featID] = puAddAbundDict[featID]
        setupObject.abundPUKeyDict[puID] = puAbundDict

    cluz_setup.makePuvspr2DatFile(setupObject)


def addFeaturesToTargetCsvFile(setupObject, addAbundDict, featIDList):
    tempTargetPath = cluz_setup.returnTempPathName(setupObject.targetPath, "csv")
    tempTargetFile = open(tempTargetPath, "wb")
    writer = csv.writer(tempTargetFile)

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    addTargetDict = makeAddTargetDict(puLayer, addAbundDict, featIDList)

    with open(setupObject.targetPath, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            writer.writerow(row)

        addTargetList = addTargetDict.keys()
        addTargetList.sort()
        for featID in addTargetList:
            (featCon, featTotal) = addTargetDict[featID]
            row = [str(featID), "blank", "0", "0", "0", str(featCon), str(featTotal), "-1"]
            writer.writerow(row)

    tempTargetFile.close()
    os.remove(setupObject.targetPath)
    os.rename(tempTargetPath, setupObject.targetPath)


def makeAddTargetDict(puLayer, addAbundDict, featIDList):
    puFeatures = puLayer.getFeatures()
    unitIDField = puLayer.fieldNameIndex('Unit_ID')
    unitStatusField = puLayer.fieldNameIndex('Status')

    addTargetDict = {}
    for featID in featIDList:
        addTargetDict[featID] = (0, 0) #[Con amount, total amount]

    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        puID = puAttributes[unitIDField]
        puStatus = puAttributes[unitStatusField]

        for bFeatID in featIDList:
            try:
                puAddAbundDict = addAbundDict[puID]
                featAmount = puAddAbundDict[bFeatID]
                featCon, featTotal = addTargetDict[bFeatID]
                featTotal += featAmount
                if puStatus == "Conserved" or puStatus == "Earmarked":
                    featCon += featAmount
                addTargetDict[bFeatID] = (featCon, featTotal)
            except KeyError:
                pass

    return addTargetDict

def remFeaturesFromPuvspr2(setupObject, selectedFeatIDSet):
    puvspr2Path = setupObject.inputPath + os.sep + "puvspr2.dat"
    tempPuvspr2Path = cluz_setup.returnTempPathName(puvspr2Path, "dat")
    tempPuvspr2File = open(tempPuvspr2Path, "wb")
    writer = csv.writer(tempPuvspr2File)
    writer.writerow(["species", "pu", "amount"])

    with open(puvspr2Path, 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            if int(row[0]) not in selectedFeatIDSet:
                writer.writerow(row)

    tempPuvspr2File.close()
    os.remove(puvspr2Path)
    os.rename(tempPuvspr2Path, puvspr2Path)

def remFeaturesFromTargetCsv_Dict(setupObject, selectedFeatIDSet):
    tempTargetPath = cluz_setup.returnTempPathName(setupObject.targetPath, "csv")
    tempTargetFile = open(tempTargetPath, "wb")
    writer = csv.writer(tempTargetFile)

    with open(setupObject.targetPath, 'rb') as f:
        reader = csv.reader(f)
        rowHeader = True
        for row in reader:
            if rowHeader == True:
                writer.writerow(row)
                rowHeader = False
            else:
                featID = int(row[0])
                if featID in selectedFeatIDSet:
                    pass
                else:
                    writer.writerow(row)

    tempTargetFile.close()
    os.remove(setupObject.targetPath)
    os.rename(tempTargetPath, setupObject.targetPath)

def makeBlankCLUZFiles(shapePath, convFactor, costAsAreaBool, inputPath, targetPath):
    targetWriter = csv.writer(open(targetPath, "wb"))
    targetWriter.writerow(["Id", "Name", "Type", "Target", "Spf", "Conserved", "Total", "PC_target"])

    puvspr2Writer = csv.writer(open(inputPath + os.sep + "puvspr2.dat", "wb"))
    puvspr2Writer.writerow(["species", "pu", "amount"])

    sporderWriter = csv.writer(open(inputPath + os.sep + "sporder.dat", "wb"))
    sporderWriter.writerow(["species", "pu", "amount"])

    puLayer = QgsVectorLayer(shapePath, "Shapefile", "ogr")
    puProvider = puLayer.dataProvider()
    unitIDField = puProvider.addAttributes([QgsField("Unit_ID", QVariant.Int)])
    puAreaField = puProvider.addAttributes([QgsField("Area", QVariant.Double, "real", 10, 2)])
    puCostField = puProvider.addAttributes([QgsField("Cost", QVariant.Double, "real", 10, 2)])
    unitStatusField = puProvider.addAttributes([QgsField("Status", QVariant.String)])
    puLayer.updateFields()

    unitIDFieldIndex = puProvider.fieldNameIndex("Unit_ID")
    puAreaFieldIndex = puProvider.fieldNameIndex("Area")
    puCostFieldIndex = puProvider.fieldNameIndex("Cost")
    statusFieldIndex = puProvider.fieldNameIndex("Status")

    puLayer.startEditing()
    puFeatures = puLayer.getFeatures()
    for puFeature in puFeatures:
        puRow = puFeature.id()
        unitIDValue = puRow + 1
        puGeom = puFeature.geometry()
        puArea = puGeom.area()
        finalPUArea = puArea / convFactor
        if costAsAreaBool is True:
            puCost = finalPUArea
        else:
            puCost = 0

        puLayer.changeAttributeValue(puRow, unitIDFieldIndex, unitIDValue, True)
        puLayer.changeAttributeValue(puRow, puCostFieldIndex, puCost, True)
        puLayer.changeAttributeValue(puRow, puAreaFieldIndex, finalPUArea, True)
        puLayer.changeAttributeValue(puRow, statusFieldIndex, "Available", True)

    puLayer.commitChanges()

def troubleShootCLUZFiles(setupObject):
    cluz_setup.checkStatusObjectValues(setupObject)
    targetFileFine, targetFeatIDSet = checkTargetCsvFile(setupObject)
    puvspr2FileFine, puvspr2PuIDSet, puvspr2FeatIDSet, puvspr2RowNum, puvspr2RecCountDict = checkPuvspr2DatFile(setupObject)
    sporderFileFine, sporderPuIDSet, sporderFeatIDSet, sporderRowNum, sporderRecCountDict = checkSporderDatFile(setupObject)
    puFileFine, puPuIDSet = checkPuShapeFile(setupObject)

    progressMessage = "Comparing the files..."
    qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)
    idValuesNotDuplicated = True

    idValuesNotDuplicated = checkIDsMatchInTargetTableAndPuvspr2(targetFeatIDSet, puvspr2FeatIDSet, idValuesNotDuplicated)
    idValuesNotDuplicated = checkIDsMatchInPULayerAndPuvspr2(puvspr2PuIDSet, puPuIDSet, idValuesNotDuplicated)

    abundDatFilesSame = True
    if puvspr2PuIDSet != sporderPuIDSet or puvspr2FeatIDSet != sporderFeatIDSet or puvspr2RowNum != sporderRowNum or puvspr2RecCountDict != sporderRecCountDict:
        qgis.utils.iface.messageBar().pushMessage("puvspr2.dat and sporder.dat: ", "The two files do not contain the same data. Delete the sporder.dat file in the input folder and CLUZ will create a new one in the correct format.", QgsMessageBar.WARNING)
        abundDatFilesSame = False

    if targetFileFine == True and puvspr2FileFine == True and puFileFine == True and idValuesNotDuplicated == True and abundDatFilesSame == True:
        if setupObject.setupStatus == "files_checked":
            cluz_setup.makeTargetDict(setupObject)
            qgis.utils.iface.messageBar().pushMessage("Status: ", "No problems were found and the Target table has been updated to ensure it reflects the current data.", QgsMessageBar.INFO)
        else:
            qgis.utils.iface.messageBar().pushMessage("Status: ", "No problems were found.", QgsMessageBar.INFO)

    progressMessage = "CLUZ Troubleshoot files completed"
    qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)

def checkIDsMatchInTargetTableAndPuvspr2(targetFeatIDSet, puvspr2FeatIDSet, idValuesNotDuplicated):
    extraTargetFeatIDset, extraAbundFeatIDset = findValuesInOneSet(targetFeatIDSet, puvspr2FeatIDSet)

    if len(extraTargetFeatIDset) > 0:
        errorText = ""
        for aValue in extraTargetFeatIDset:
            errorText += str(aValue) + ", "
        errorText = errorText[: -2]
        qgis.utils.iface.messageBar().pushMessage("Abundance and Target tables: ", "The following Feature IDs appear in the Target Table but not in the puvspr2.dat file: " + errorText, QgsMessageBar.WARNING)
        idValuesNotDuplicated = False
    if len(extraAbundFeatIDset) > 0:
        errorText = ""
        for aValue in extraAbundFeatIDset:
            errorText += str(aValue) + ", "
        errorText = errorText[: -2]
        qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file and Target tables: ", "The following Feature IDs appear in the puvspr2.dat file but not in the Target table: " + errorText, QgsMessageBar.WARNING)
        idValuesNotDuplicated = False

    return idValuesNotDuplicated

def checkIDsMatchInPULayerAndPuvspr2(puvspr2PuIDSet, puPuIDSet, idValuesNotDuplicated):
    extraPuvspr2PuIDSet, extraPUPuIDSet = findValuesInOneSet(puvspr2PuIDSet, puPuIDSet)
    if len(extraPuvspr2PuIDSet) > 0:
        errorText = ""
        for aValue in extraPuvspr2PuIDSet:
            errorText += str(aValue) + ", "
        errorText = errorText[: -2]
        qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file and Planning unit layer: ", "The following planning unit IDs appear in the puvspr2.dat file but not in the planning unit layer: " + errorText, QgsMessageBar.WARNING)
        idValuesNotDuplicated = False

    return idValuesNotDuplicated


def findValuesInOneSet(inputSet1, inputSet2):
    set1 = set()
    set2 = set()
    bigSet = inputSet1.union(inputSet2)
    for aValue in bigSet:
        if aValue in inputSet1 and aValue not in inputSet2:
            set1.add(aValue)
        if aValue not in inputSet1 and aValue in inputSet2:
            set2.add(aValue)

    return set1, set2

def checkTargetCsvFile(setupObject):
    targetCSVFilePath = setupObject.targetPath
    featIDList = []
    progressMessage = "Checking the target table..."
    qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)

    with open(targetCSVFilePath, 'rb') as f:
        targetReader = csv.reader(f)

        origHeaderList = targetReader.next()
        headerList = [] #convert to lowercase so it doesn't matter whether the headers or lowercase, uppercase or a mix
        for aHeader in origHeaderList:
            headerList.append(aHeader.lower())

        errorSet = set()
        for aRow in targetReader:
            featIDString = aRow[headerList.index('id')]
            featNameString = aRow[headerList.index('name')]
            featTypeString = aRow[headerList.index('type')]
            featSpfString = aRow[headerList.index('spf')]
            featTargetString = aRow[headerList.index('target')]
            featConservedString = aRow[headerList.index('conserved')]
            featTotalString = aRow[headerList.index('total')]
            featPc_TargetString = aRow[headerList.index('pc_target')]

            featIDList, errorSet = checkFeatIDString(featIDList, featIDString, errorSet)
            errorSet = checkFeatNameString(featNameString, errorSet)
            errorSet = checkFeatTypeString(featTypeString, errorSet)
            errorSet = checkFeatSpfString(featSpfString, errorSet)
            errorSet = checkFeatTargetString(featTargetString, errorSet)
            errorSet = checkFeatConservedString(featConservedString, errorSet)
            errorSet = checkFeatTotalString(featTotalString, errorSet)
            errorSet = checkFeatPc_TargetString(featPc_TargetString, errorSet)

        errorSet = checkForDuplicateFeatIDs(featIDList, errorSet)

    pushTargetTableErrorMessages(errorSet)

    if len(errorSet) == 0:
        fileFine = True
    else:
        fileFine = False

    return fileFine, set(featIDList)

def checkFeatIDString(featIDList, featIDString, errorSet):
    if featIDString == "":
        errorSet.add("featIDBlank")
    else:
        try:
            featIDList.append(int(featIDString))
            if int(featIDString) < 0:
                errorSet.add("featIDNotInt")
        except ValueError:
            errorSet.add("featIDNotInt")

    return featIDList, errorSet

def checkFeatNameString(featNameString, errorSet):
    if featNameString == "":
        errorSet.add("featNameBlank")
    elif " " in featNameString or any(i.isdigit() for i in featNameString):
        errorSet.add("featNameWrongFormat")

    return errorSet


def checkFeatTypeString(featTypeString, errorSet):
    if featTypeString == "":
        errorSet.add("featTypeBlank")
    else:
        try:
            int(featTypeString)
            if int(featTypeString) < 0:
                errorSet.add("featSpfNotFloat")
        except ValueError:
            errorSet.add("featTypeNotFloat")

    return errorSet

def checkFeatSpfString(featSpfString, errorSet):
    if featSpfString == "":
        errorSet.add("featSpfBlank")
    else:
        try:
            float(featSpfString)
            if float(featSpfString) < 0:
                errorSet.add("featSpfNotFloat")
        except ValueError:
            errorSet.add("featSpfNotFloat")

    return errorSet

def checkFeatTargetString(featTargetString, errorSet):
    if featTargetString == "":
        errorSet.add("featTargetBlank")
    else:
        try:
            float(featTargetString)
            if float(featTargetString) < 0:
                errorSet.add("featTargetNotFloat")
        except ValueError:
            errorSet.add("featTargetNotFloat")

    return errorSet

def checkFeatConservedString(featConservedString, errorSet):
    if featConservedString == "":
        errorSet.add("featConservedBlank")
    else:
        try:
            float(featConservedString)
        except ValueError:
            errorSet.add("featConservedNotFloat")

    return errorSet


def checkFeatTotalString(featTotalString, errorSet):
    if featTotalString == "":
        errorSet.add("featTotalNotFloat")
    else:
        try:
            float(featTotalString)
        except ValueError:
            errorSet.add("featTotalBlank")

    return errorSet


def checkFeatPc_TargetString(featPc_TargetString, errorSet):
    if featPc_TargetString == "":
        errorSet.add("featPc_TargetBlank")
    else:
        try:
            float(featPc_TargetString)
        except ValueError:
            errorSet.add("featPc_TargetNotFloat")

    return errorSet

def checkForDuplicateFeatIDs(featIDList, errorSet):
    if len(featIDList) != len(set(featIDList)):
        errorSet.add("duplicateFeatID")

    return errorSet

def pushTargetTableErrorMessages(errorSet):
    for anError in errorSet:
        if anError == "featIDBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the Feature ID values is blank.", QgsMessageBar.WARNING)
        if anError == "featIDNotInt":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the Feature ID values is not a positive integer.", QgsMessageBar.WARNING)
        if anError == "featNameBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the name values is blank.", QgsMessageBar.WARNING)
        if anError == "featTypeBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the type values is blank.", QgsMessageBar.WARNING)
        if anError == "featTypeNotInt":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the type values is not a positve integer.", QgsMessageBar.WARNING)
        if anError == "featSpfBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the SPF values is blank.", QgsMessageBar.WARNING)
        if anError == "featSpfNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the SPF values is not a positive number.", QgsMessageBar.WARNING)
        if anError == "featTargetBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the target values is blank.", QgsMessageBar.WARNING)
        if anError == "featTargetNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the target values is not a non-negative number.", QgsMessageBar.WARNING)
        if anError == "featConservedBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the conserved values is blank.", QgsMessageBar.WARNING)
        if anError == "featConservedNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the conserved values is not a number.", QgsMessageBar.WARNING)
        if anError == "featTotalBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the total values is blank.", QgsMessageBar.WARNING)
        if anError == "featTotalNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the total values is not a number.", QgsMessageBar.WARNING)
        if anError == "featPc_TargetBlank":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the % target met values is blank.", QgsMessageBar.WARNING)
        if anError == "featPc_TargetNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the % target met values is not a number.", QgsMessageBar.WARNING)

        if anError == "duplicateFeatID":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the Feature IDs appears twice in the Feature ID field.", QgsMessageBar.WARNING)
        if anError == "featNameWrongFormat":
            qgis.utils.iface.messageBar().pushMessage("Target Table: ", "At least one of the Feature names is in the wrong format. They cannot contain spaces or numbers.", QgsMessageBar.WARNING)

def checkPuvspr2DatFile(setupObject):
    puvspr2FilePath = setupObject.inputPath + os.sep + "puvspr2.dat"
    recCountDict = {} #Used to check whether there are the same number of records per feature in puvspr2.dat and sporder.dat files
    errorSet = set()
    unitIDSet = set()
    featIDSet = set()

    errorRowSet = set()
    prevUnitID = -99
    recordCount = 0
    progressCount = 0

    with open(puvspr2FilePath, 'rb') as f:
        puvspr2Reader = csv.reader(f)
        puvspr2Reader.next()

        rowNum = 2
        for aRow in puvspr2Reader:
            recordCount += 1
            progressCount += 1
            if progressCount == 100000:
                progressMessage = "Checking the puvspr2.dat file: records imported = " + str(recordCount)
                qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)
                progressCount = 0

            if len(aRow) != 3:
                errorSet.add("wrongNumColumns")
                errorRowSet.add(rowNum)

            featID = aRow[0]
            unitID = aRow[1]
            featAmount = aRow[2]

            if int(unitID) < int(prevUnitID):
                errorSet.add("notOrderedByPU")
                errorRowSet.add(rowNum)

            if featID == "":
                errorSet.add("featIDBlank")
                errorRowSet.add(rowNum)
            else:
                try:
                    int(featID)
                    featIDSet.add(int(featID))
                    try:
                        recCount = recCountDict[featID]
                        recCount += 1
                        recCountDict[featID] = recCount
                    except KeyError:
                        recCountDict[featID] = 1
                    if int(featID) < 1:
                        errorSet.add("featIDNeg")
                        errorRowSet.add(rowNum)
                except ValueError:
                    errorSet.add("featIDNotInt")
                    errorRowSet.add(rowNum)
            if unitID == "":
                errorSet.add("puIDBlank")
                errorRowSet.add(rowNum)
            try:
                int(unitID)
                unitIDSet.add(int(unitID))
                if int(unitID) < 1:
                    errorSet.add("puIDNeg")
                    errorRowSet.add(rowNum)
            except ValueError:
                errorSet.add("puIDNotInt")
                errorRowSet.add(rowNum)
            if featAmount == "":
                errorSet.add("featAmountBlank")
                errorRowSet.add(rowNum)
            try:
                float(featAmount)
                if float(featAmount) < 0:
                    errorSet.add("featAmountNeg")
                    errorRowSet.add(rowNum)
            except ValueError:
                errorSet.add("featAmountNotFloat")
                errorRowSet.add(rowNum)
            rowNum += 1
            prevunitID = unitID

    if len(errorRowSet) > 0:
        errorRowList = list(errorRowSet)
        errorRowList.sort()
        messageText = ""
        for aErrorRow in errorRowList:
            messageText += str(aErrorRow) + " "
        finalMessageText = messageText[:-1]
        qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "Errors are in the following rows: " + finalMessageText, QgsMessageBar.WARNING)

    for anError in errorSet:
        if anError == "wrongNumColumns":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the rows does not contain 3 values.", QgsMessageBar.WARNING)
        if anError == "notOrderedByPU":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "This file must be ordered by planning unit ID, from smallest to highest value.", QgsMessageBar.WARNING)
        if anError == "featIDBlank":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the feature ID values is missing.", QgsMessageBar.WARNING)
        if anError == "featIDNotInt":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the feature ID values is not an integer.", QgsMessageBar.WARNING)
        if anError == "featIDNeg":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the feature ID values is less than 1.", QgsMessageBar.WARNING)
        if anError == "puIDBlank":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the planning unit ID values is missing.", QgsMessageBar.WARNING)
        if anError == "puIDNotInt":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the planning unit ID values is not an integer.", QgsMessageBar.WARNING)
        if anError == "puIDNeg":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the planning unit ID values is less than 1.", QgsMessageBar.WARNING)
        if anError == "featAmountBlank":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the amount values is missing.", QgsMessageBar.WARNING)
        if anError == "featAmountNotFloat":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the amount values is not a valid number.", QgsMessageBar.WARNING)
        if anError == "featAmountNeg":
            qgis.utils.iface.messageBar().pushMessage("puvspr2.dat file: ", "At least one of the amount values is less than 0.", QgsMessageBar.WARNING)

    if len(errorSet) == 0:
        fileFine = True
    else:
        fileFine = False

    return fileFine, unitIDSet, featIDSet, rowNum, recCountDict

def checkSporderDatFile(setupObject):
    sporderFilePath = setupObject.inputPath + os.sep + "sporder.dat"
    recCountDict = {} #Used to check whether there are the same number of records per feature in puvspr2.dat and sporder.dat files
    errorSet = set()
    unitIDSet = set()
    featIDSet = set()

    errorRowSet = set()
    prevFeatID = -99
    recordCount = 0
    progressCount = 0

    with open(sporderFilePath, 'rb') as f:
        sporderReader = csv.reader(f)
        sporderReader.next()

        rowNum = 2
        for aRow in sporderReader:
            recordCount += 1
            progressCount += 1
            if progressCount == 100000:
                progressMessage = "Checking the sporder.dat file: records imported = " + str(recordCount)
                qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)
                progressCount = 0
            if len(aRow) != 3:
                errorSet.add("wrongNumColumns")
                errorRowSet.add(rowNum)

            featID = aRow[0]
            unitID = aRow[1]
            featAmount = aRow[2]

            if int(featID) < int(prevFeatID):
                errorSet.add("notOrderedByFeature")
                errorRowSet.add(rowNum)

            if featID == "":
                errorSet.add("featIDBlank")
                errorRowSet.add(rowNum)
            else:
                try:
                    int(featID)
                    featIDSet.add(int(featID))
                    try:
                        recCount = recCountDict[featID]
                        recCount += 1
                        recCountDict[featID] = recCount
                    except KeyError:
                        recCountDict[featID] = 1
                    if int(featID) < 1:
                        errorSet.add("featIDNeg")
                        errorRowSet.add(rowNum)
                except ValueError:
                    errorSet.add("featIDNotInt")
                    errorRowSet.add(rowNum)
            if unitID == "":
                errorSet.add("puIDBlank")
                errorRowSet.add(rowNum)
            try:
                int(unitID)
                unitIDSet.add(int(unitID))
                if int(unitID) < 1:
                    errorSet.add("puIDNeg")
                    errorRowSet.add(rowNum)
            except ValueError:
                errorSet.add("puIDNotInt")
                errorRowSet.add(rowNum)
            if featAmount == "":
                errorSet.add("featAmountBlank")
                errorRowSet.add(rowNum)
            try:
                float(featAmount)
                if float(featAmount) < 0:
                    errorSet.add("featAmountNeg")
                    errorRowSet.add(rowNum)
            except ValueError:
                errorSet.add("featAmountNotFloat")
                errorRowSet.add(rowNum)
            rowNum += 1
            prevFeatID = featID

    if len(errorRowSet) > 0:
        errorRowList = list(errorRowSet)
        errorRowList.sort()
        messageText = ""
        for aErrorRow in errorRowList:
            messageText += str(aErrorRow) + " "
        finalMessageText = messageText[:-1]
        qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "Errors are in the following rows: " + finalMessageText, QgsMessageBar.WARNING)

    for anError in errorSet:
        if anError == "wrongNumColumns":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the rows does not contain 3 values.", QgsMessageBar.WARNING)
        if anError == "notOrderedByPU":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "This file must be ordered by planning unit ID, from smallest to highest value.", QgsMessageBar.WARNING)
        if anError == "featIDBlank":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the feature ID values is missing.", QgsMessageBar.WARNING)
        if anError == "featIDNotInt":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the feature ID values is not an integer.", QgsMessageBar.WARNING)
        if anError == "featIDNeg":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the feature ID values is less than 1.", QgsMessageBar.WARNING)
        if anError == "puIDBlank":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the planning unit ID values is missing.", QgsMessageBar.WARNING)
        if anError == "puIDNotInt":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the planning unit ID values is not an integer.", QgsMessageBar.WARNING)
        if anError == "puIDNeg":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the planning unit ID values is less than 1.", QgsMessageBar.WARNING)
        if anError == "featAmountBlank":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the amount values is missing.", QgsMessageBar.WARNING)
        if anError == "featAmountNotFloat":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the amount values is not a valid number.", QgsMessageBar.WARNING)
        if anError == "featAmountNeg":
            qgis.utils.iface.messageBar().pushMessage("sporder.dat file: ", "At least one of the amount values is less than 0.", QgsMessageBar.WARNING)

    if len(errorSet) == 0:
        fileFine = True
    else:
        fileFine = False

    return fileFine, unitIDSet, featIDSet, rowNum, recCountDict


####################################################################http://www.opengis.ch/2015/04/29/performance-for-mass-updating-features-on-layers/
def checkPuShapeFile(setupObject):
    unitIDList = []
    errorSet = set()
    statusList = ["Available", "Conserved", "Earmarked", "Excluded"]
    unitIDErrorDuplText = ""

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puFeatures = puLayer.getFeatures()
    unitIDField = puLayer.fieldNameIndex('Unit_ID')
    puAreaField = puLayer.fieldNameIndex('Area')
    puCostField = puLayer.fieldNameIndex('Cost')
    unitStatusField = puLayer.fieldNameIndex('Status')

    recordCount = 0
    progressCount = 0
    progressMessage = "Checking the planning unit shapefile: records imported = 0"
    qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)


    for puFeature in puFeatures:
        recordCount += 1
        progressCount += 1
        if progressCount == 1000:
            progressMessage = "Checking the planning unit shapefile: records imported = " + str(recordCount)
            qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)
            progressCount = 0

        puAttributes = puFeature.attributes()

        unitID = puAttributes[unitIDField]
        if unitID == NULL:#NULL is used for blank values that return QPyNullVariant
            errorSet.add("puIDBlank")
        else:
            try:
                int(unitID)
                unitIDList.append(unitID)
                if unitIDList.count(unitID) > 1:
                    unitIDErrorDuplText += str(unitID) + ", "
                    errorSet.add("duplicatePuID")
                if int(unitID) < 0:
                    errorSet.add("puIDNotInt")
            except ValueError:
                errorSet.add("puIDNotInt")

        puArea = puAttributes[puAreaField]
        if puArea == NULL:
            errorSet.add("puAreaBlank")
        else:
            try:
                float(puArea)
                if float(puArea) < 0:
                    errorSet.add("puAreaNotFloat")
            except ValueError:
                errorSet.add("puAreaNotFloat")

        puCost = puAttributes[puCostField]
        if puCost == NULL:
            errorSet.add("puCostBlank")
        else:
            try:
                float(puCost)
                if float(puCost) < 0:
                    errorSet.add("puCostNotFloat")
            except ValueError:
                errorSet.add("puCostNotFloat")

        unitStatus = puAttributes[unitStatusField]
        if not unitStatus in statusList:
            errorSet.add("puStatusWrong")

    unitIDErrorDuplMessage = unitIDErrorDuplText[: -2]

    for anError in errorSet:
        if anError == "puIDBlank":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit ID values is blank.", QgsMessageBar.WARNING)
        if anError == "duplicateFeatID":
            qgis.utils.iface.messageBar().pushMessage("Abundance Table: ", "The following planning unit ID values appear more than once in the Unit_ID field: " + unitIDErrorDuplMessage, QgsMessageBar.WARNING)
        if anError == "puIDNotInt":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit ID values is not an integer greater than 0.", QgsMessageBar.WARNING)
        if anError == "puAreaBlank":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit area values is blank.", QgsMessageBar.WARNING)
        if anError == "puAreaNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit area values is not a non-negative number.", QgsMessageBar.WARNING)
        if anError == "puCostBlank":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit cost values is blank", QgsMessageBar.WARNING)
        if anError == "puCostNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit cost values is not a non-negative number.", QgsMessageBar.WARNING)
        if anError == "puCostNotFloat":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit cost values is not a non-negative number.", QgsMessageBar.WARNING)
        if anError == "puStatusWrong":
            qgis.utils.iface.messageBar().pushMessage("Planning unit layer: ", "At least one of the planning unit status values is incorrect. They should either be Available, Conserved, Earmarked or Excluded.", QgsMessageBar.WARNING)

    if len(errorSet) == 0:
        fileFine = True
    else:
        fileFine = False

    return fileFine, set(unitIDList)
