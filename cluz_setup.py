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
from qgis.utils import *

import os
import csv
import re
import time

import cluz_display



def xxxSaveTextToFile(outputName, anItem):
    baseName = 'C:\Users\Bob\.qgis2\python\plugins\Cluz\hope.txt'
    pathName = baseName.replace('hope',outputName)
    textFile = open(pathName,'wb')
    finalString = ""
    finalString += str(anItem)
    textFile.writelines(finalString)
    textFile.close()

def xxxSavePortfolioToFile(outputName, portfolioDict):
    baseName = 'C:\Users\Bob\.qgis2\python\plugins\Cluz\hope.txt'
    pathName = baseName.replace('hope', outputName)
    headerList = ["ID", "Status"]
    portfolioWriter = csv.writer(open(pathName, "wb"))
    portfolioWriter.writerow(headerList)

    for puID in portfolioDict:
        portfolioWriter.writerow([puID, portfolioDict[puID][1]])


def removePrefixMakeIDValue(aString):
    numList = re.findall(r'[0-9]+', aString)
    revNumList = numList[::-1]
    if len(revNumList) > 0:
        idValue = int(revNumList[0])
    else:
        idValue = ""

    return idValue

class CluzSetupObject:
    def __init__(self):

        self.setupStatus = "blank" #Can be "values_set", "values_checked" or "files_checked"
        self.setupAction = "blank" #Can be be "new" or "open"
        self.setupPath = "blank"

        #Specify the field names used in the Marxan outputs
        self.bestHeadingFieldNames = ["planning_unit","solution"]
        self.summedHeadingFieldNames = ["planning_unit","number"]

        self.decimalPlaces = 2
        self.marxanPath = "blank"
        self.inputPath = "blank"
        self.outputPath = "blank"
        self.puPath = "blank"
        self.targetPath = "blank"
        self.abundFileDate = "blank"
        self.targetFileDate = "blank"

        #These are the default values
        self.outputName = "output1"
        self.numIter = 1000000
        self.numRuns = 10
        self.blmValue = 0
        self.boundFlag = "False"
        self.extraOutputsFlag = "False"
        self.startProp = 0.2
        self.targetProp = 1

        self.abundPUKeyDict = "blank"

        #################################################
        self.overRide = False  ###########################
        #################################################


class MinPatchObject:
    def __init__(self):

        self.setupStatus = "blank" #Can be "values_set", "values_checked" or "files_checked"

def makeSetupDictFromSetupFile(setupFilePath):
    setupDict = dict()
    with open(setupFilePath, 'rb') as f:
        setupReader = csv.reader(f)
        for aRow in setupReader:
            aList = aRow[0].split(" = ")
            if len(aList) == 2:
                theKey = aList[0]
                theValue = aList[1]
                setupDict[theKey] = theValue

    return setupDict

def updateSetupObjectFromSetupFile(setupObject, setupFilePath):
    setupDict = makeSetupDictFromSetupFile(setupFilePath)

    try:
        decPlaceText = setupDict["decimal_places"]
        setupObject.setupPath = setupFilePath
        setupObject.marxanPath = setupDict["marxan_path"]
        setupObject.inputPath = setupDict["input_dir"]
        setupObject.outputPath = setupDict["output_dir"]
        setupObject.puPath = setupDict["unit_theme"]
        setupObject.targetPath = setupDict["target_table"]
        setupObject.outputName = setupDict["output_name"]
        numIterText = setupDict["num_iterations"]
        numRunText = setupDict["num_runs"]
        numBlmText = setupDict["blm"]
        setupObject.boundFlag = setupDict["bound_flag"]
        setupObject.extraOutputsFlag = setupDict["extra_flag"]
        startPropText = setupDict["start_prop"]
        targetPropText = setupDict["target_prop"]

        setupFileOK = checkFilesAndReturnSetupFileOKBool(setupObject, decPlaceText, numIterText, numRunText, numBlmText, startPropText, targetPropText)

    except KeyError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified setup file does not contain all of the correct factors. Please correct this.", QgsMessageBar.WARNING)
        setupFileOK = False

    if setupFileOK == True:
        setupObject.setupStatus = "values_set"
        checkStatusObjectValues(setupObject)
        if setupObject.setupStatus == "values_checked":
            setupObject.setupPath = setupFilePath

def checkFilesAndReturnSetupFileOKBool(setupObject, decPlaceText, numIterText, numRunText, numBlmText, startPropText, targetPropText):
    setupFileOK = True
    try:
        setupObject.decimalPlaces = int(decPlaceText)
        if setupObject.decimalPlaces > 5:
            setupObject.decimalPlaces = 5
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified decimal place value in the setup file is not an integer. Please correct this.", QgsMessageBar.WARNING)
        setupFileOK = False
    try:
        setupObject.numIter = int(numIterText)
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified number of iterations in the setup file is not an integer. Please correct this.", QgsMessageBar.WARNING)
        setupFileOK = False
    try:
        setupObject.numRuns = int(numRunText)
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified number of runs in the setup file is not an integer. Please correct this.", QgsMessageBar.WARNING)
        setupFileOK = False
    try:
        setupObject.blmValue = float(numBlmText)
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The BLM value in the setup file is not a number. Please correct this.", QgsMessageBar.WARNING)
        setupFileOK = False
    try:
        setupObject.startProp = float(startPropText)
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The start proportion value in the setup file is not a number. Please correct this.", QgsMessageBar.WARNING)
        setupFileOK = False
    try:
        setupObject.targetProp = float(targetPropText)
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The target proportion value in the setup file is not a number. Please correct this.", QgsMessageBar.WARNING)
        setupFileOK = False

    return setupFileOK

def checkStatusObjectValues(setupObject):
    setupFileCorrect = True
    try:
        setupObject.decimalPlaces = int(setupObject.decimalPlaces)
        if setupObject.decimalPlaces < 0:
            qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified value in the CLUZ setup file for number of decimal places cannot be a negative value. Please correct this.", QgsMessageBar.WARNING)
            setupFileCorrect = False
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified value in the CLUZ setup file for number of decimal places in the Abundance and Target tables is not an integer. Please correct this.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    try:
        setupObject.numIter = int(setupObject.numIter)
        if setupObject.numIter < 0:
            qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified value in the CLUZ setup file for number of Marxan iterations cannot be a negative value. Please correct this.", QgsMessageBar.WARNING)
            setupFileCorrect = False
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format","The specified number of Marxan run iterations in the CLUZ setup is not an integer. Please correct this.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    try:
        setupObject.numRuns = int(setupObject.numRuns)
        if setupObject.numRuns < 0:
            qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified value in the CLUZ setup file for number of Marxan runs cannot be a negative value. Please correct this.", QgsMessageBar.WARNING)
            setupFileCorrect = False
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format","The specified number of Marxan runs in the CLUZ setup is not an integer. Please correct this.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    try:
        setupObject.blmValue = float(setupObject.blmValue)
        if setupObject.blmValue < 0:
            qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified BLM value in the CLUZ setup cannot be a negative value. Please correct this.", QgsMessageBar.WARNING)
            setupFileCorrect = False
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format","The specified BLM value in the CLUZ setup is not a valid number. Please correct this.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    if setupObject.boundFlag == "True" or setupObject.boundFlag == "False":
        pass
    else:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The BLM flag value in the CLUZ setup is not specified as True or False. Please correct this.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    if setupObject.extraOutputsFlag == "True" or setupObject.extraOutputsFlag == "False":
        pass
    else:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The extra outputs flag value in the CLUZ setup is not specified as True or False. Please correct this.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    try:
        setupObject.startProp = float(setupObject.startProp)
        if setupObject.startProp < 0 or setupObject.startProp > 1:
            qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified proportion of planning units initially selected by Marxan as specified in the CLUZ setup has to be between 0 and 1. Please correct this.", QgsMessageBar.WARNING)
            setupFileCorrect = False
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified proportion of planning units initially selected by Marxan as specified in the CLUZ setup is not a number. Please correct this.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    try:
        setupObject.targetProp = float(setupObject.targetProp)
        if setupObject.targetProp < 0 or setupObject.targetProp > 1:
            qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified proportion of a target that needs to be achieved for Marxan to report that the target has been met as specified in the CLUZ setup has to be between 0 and 1. Please correct this.", QgsMessageBar.WARNING)
            setupFileCorrect = False
    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Setup file incorrect format", "The specified proportion of a target that needs to be achieved for Marxan to report that the target has been met as specified in the CLUZ setup is not a number.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    puPath = setupObject.puPath
    if puPath == "blank":
        qgis.utils.iface.messageBar().pushMessage("Missing planning unit shapefile","The planning unit shapefile has not been specified. Please open the View and Edit CLUZ setup file function and update the information.", QgsMessageBar.WARNING)
        setupFileCorrect = False
    elif os.path.exists(puPath) == False:
        qgis.utils.iface.messageBar().pushMessage("Incorrect planning unit shapefile path", "The specified planning unit shapefile cannot be found. Please open the View and Edit CLUZ setup file function and update the information.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    puvspr2Path = setupObject.inputPath + os.sep + "puvspr2.dat"
    if os.path.exists(puvspr2Path) == False:
        qgis.utils.iface.messageBar().pushMessage("Incorrect puvspr2 path", "The puvspr2.dat file cannot be found. Please add it to the specified input folder.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    targetPath = setupObject.targetPath
    if targetPath == "blank":
        qgis.utils.iface.messageBar().pushMessage("Missing target table","The target table has not been specified. Please open the View and Edit CLUZ setup file function and update the information.", QgsMessageBar.WARNING)
        setupFileCorrect = False
    elif os.path.exists(targetPath) == False:
        qgis.utils.iface.messageBar().pushMessage("Incorrect target table path", "The specified target table cannot be found. Please open the View and Edit CLUZ setup file function and update the information.", QgsMessageBar.WARNING)
        setupFileCorrect = False

    foldersOKBool = checkFolderValues(setupObject.marxanPath, setupObject.inputPath, setupObject.outputPath)
    if setupFileCorrect == True and foldersOKBool == True:
        setupObject.setupStatus = "values_checked"

def checkFolderValues(marxanPath, inputPath, outputPath):
    foldersOKBool = True
    marxanDirPath = os.path.dirname(marxanPath)
    if marxanPath == "blank" or marxanPath == "":
        qgis.utils.iface.messageBar().pushMessage("Marxan path invalid", "The Marxan path is missing.", QgsMessageBar.WARNING)
        foldersOKBool = False
    elif os.path.isdir(marxanDirPath) == False:
        qgis.utils.iface.messageBar().pushMessage("Marxan path invalid", "The specified folder containing Marxan does not exist.", QgsMessageBar.WARNING)
        foldersOKBool = False
    elif os.access(marxanDirPath, os.W_OK) == False:
        qgis.utils.iface.messageBar().pushMessage("Marxan path invalid", "Running Marxan involves CLUZ creating a new input file in the folder where Marxan is stored. You do not have permission to save files into the specified folder so please move Marxan to a folder where you do have permission.", QgsMessageBar.WARNING)
        foldersOKBool = False

    return foldersOKBool

def updateClzSetupFile(setupObject):
    setupFilePath = setupObject.setupPath
    try:
        setupWriter = csv.writer(open(setupFilePath, "wb"))

        setupWriter.writerow(["decimal_places = " + str(setupObject.decimalPlaces)])
        setupWriter.writerow(["marxan_path = " + setupObject.marxanPath])
        setupWriter.writerow(["input_dir = " + setupObject.inputPath])
        setupWriter.writerow(["output_dir = " + setupObject.outputPath])
        setupWriter.writerow(["unit_theme = " + setupObject.puPath])
        setupWriter.writerow(["target_table = " + setupObject.targetPath])
        setupWriter.writerow(["output_name = " + setupObject.outputName])
        setupWriter.writerow(["num_iterations = " + str(setupObject.numIter)])
        setupWriter.writerow(["num_runs = " + str(setupObject.numRuns)])
        setupWriter.writerow(["blm = " + str(setupObject.blmValue)])
        setupWriter.writerow(["bound_flag = " + str(setupObject.boundFlag)])
        setupWriter.writerow(["extra_flag = " + str(setupObject.extraOutputsFlag)])
        setupWriter.writerow(["start_prop = " + str(setupObject.startProp)])
        setupWriter.writerow(["target_prop = " + str(setupObject.targetProp)])
    except:
        qgis.utils.iface.messageBar().pushMessage("Failed to save", "The new CLUZ setup file failed to save.", QgsMessageBar.WARNING)

def createAndCheckCLUZFiles(setupObject):
    if setupObject.setupStatus == "values_checked":
        checkBool = True

        createAndCheckTargetFile(setupObject, checkBool)
        createAndCheckPuvspr2File(setupObject, checkBool)
        createAndCheckPuLayerFile(setupObject, checkBool)

        if checkBool == True:
            setupObject.targetDict = makeTargetDict(setupObject)
            setupObject.setupStatus = "files_checked"


def createAndCheckTargetFile(setupObject, checkBool):
    targetCSVFilePath = setupObject.targetPath
    setupObject.targetFileDate = time.ctime(os.path.getmtime(targetCSVFilePath))
    targetFileFieldNameList = ["id", "name", "type", "spf", "target", "conserved", "total", "pc_target"]
    with open(targetCSVFilePath, 'rb') as f:
        targetReader = csv.reader(f)
        origHeaderList = targetReader.next()

    lowercaseHeaderList = []
    for aHeader in origHeaderList:
        lowercaseHeader = aHeader.lower()
        lowercaseHeaderList.append(lowercaseHeader)

    for aHeader in targetFileFieldNameList:
        if lowercaseHeaderList.count(aHeader) == 0:
            qgis.utils.iface.messageBar().pushMessage("Formatting error: ","The Target table is missing a " + aHeader + " field. Please select a table with the correct format.", QgsMessageBar.WARNING)
            checkBool = False

    return checkBool


def createAndCheckPuvspr2File(setupObject, checkBool):
    puvspr2FilePath = setupObject.inputPath + os.sep + "puvspr2.dat"
    puvspr2ErrorSet = set()
    with open(puvspr2FilePath, 'rb') as f:
        puvspr2Reader = csv.reader(f)
        puvspr2HeaderList = puvspr2Reader.next()
        if puvspr2HeaderList != ["species", "pu", "amount"]:
            puvspr2ErrorSet.add("abundHeaderFormat")
            checkBool = False

    for anErrorValue in puvspr2ErrorSet:
        if anErrorValue == "abundHeaderFormat":
            qgis.utils.iface.messageBar().pushMessage("Formatting error: ", "The puvspr2.dat file in the input folder is incorrectly formatted and should only have the following header names: species, pu, amount.", QgsMessageBar.WARNING)

    return checkBool


def createAndCheckPuLayerFile(setupObject, checkBool):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    fields = puLayer.pendingFields()
    fieldDetailsList = []
    for aField in fields:
        fieldDetailsList.append((str(aField.name()), str(aField.typeName())))
    if fieldDetailsList.count(('Unit_ID', 'Integer')) == 0 and fieldDetailsList.count(('Unit_ID', 'Integer64')) == 0:
        qgis.utils.iface.messageBar().pushMessage("Formatting error: ", "The planning unit shapefile must contain a field named Unit_ID containing integer values.", QgsMessageBar.WARNING)
        checkBool = False
    if fieldDetailsList.count(('Area', 'Real')) == 0:
        qgis.utils.iface.messageBar().pushMessage("Formatting error: ", "The planning unit shapefile must contain a field named Area containing real number values.", QgsMessageBar.WARNING)
        checkBool = False
    if fieldDetailsList.count(('Cost', 'Real')) == 0:
        qgis.utils.iface.messageBar().pushMessage("Formatting error: ", "The planning unit shapefile must contain a field named Cost containing real number values.", QgsMessageBar.WARNING)
        checkBool = False
    if fieldDetailsList.count(('Status', 'String')) == 0:
        qgis.utils.iface.messageBar().pushMessage("Formatting error: ", "The planning unit shapefile must contain a field named Status containing text values.", QgsMessageBar.WARNING)
        checkBool = False

    return checkBool


def makeTargetDict(setupObject):
    targetDict = {}
    targetCSVFilePath = setupObject.targetPath
    try:
        with open(targetCSVFilePath, 'rb') as f:
            targetReader = csv.reader(f)

            origHeaderList = targetReader.next()
            headerList = [] #convert to lowercase so it doesn't matter whether the headers or lowercase, uppercase or a mix
            for aHeader in origHeaderList:
                headerList.append(aHeader.lower())

            for aRow in targetReader:
                featID = int(aRow[headerList.index('id')])
                featList = makeTargetDictRowFeatList(aRow, headerList)
                targetDict[featID] = featList

    except ValueError:
        qgis.utils.iface.messageBar().pushMessage("Target table error", "The Target table is incorrectly formatted. Please use the Troubleshoot all CLUZ files function to identify the problem.", QgsMessageBar.WARNING)
        targetDict = "blank"

    return targetDict

def makeTargetDictRowFeatList(aRow, headerList):
    featName = str(aRow[headerList.index('name')])
    featType = int(aRow[headerList.index('type')])
    featSpf = float(aRow[headerList.index('spf')])
    featTarget = float(aRow[headerList.index('target')])
    featConserved = float(aRow[headerList.index('conserved')])
    featTotal = float(aRow[headerList.index('total')])
    featPc_Target = float(aRow[headerList.index('pc_target')])
    featList = [featName, featType, featSpf, featTarget, featConserved, featTotal, featPc_Target]

    return featList

def makeAbundancePUKeyDict(setupObject):
    abundPUKeyDict = {}
    abundPUKeyDictCorrect = True
    puvspr2FilePath = setupObject.inputPath + os.sep + "puvspr2.dat"
    progressMessage = "Reading in the puvspr2.dat data: records imported = 0"
    qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)
    recordCount = 0
    with open(puvspr2FilePath, 'rb') as f:
        abundReader = csv.reader(f)
        abundReader.next()
        for aRow in abundReader:
            try:
                featID = int(aRow[0])
                puID = int(aRow[1])
                abundValue = float(aRow[2])
                try:
                    puAbundDict = abundPUKeyDict[puID]
                except KeyError:
                    puAbundDict = {}
                puAbundDict[featID] = abundValue
                abundPUKeyDict[puID] = puAbundDict
                recordCount += 1
            except ValueError:
                abundPUKeyDictCorrect = False

        progressMessage = "Reading in the puvspr2.dat data: records imported = " + str(recordCount)
        qgis.utils.iface.mainWindow().statusBar().showMessage(progressMessage)

    if abundPUKeyDictCorrect == False:
        qgis.utils.iface.messageBar().pushMessage("puvspr2.dat error", "The puvspr2.dat file is incorrectly formated. Please use the Troubleshoot all CLUZ files function to identify the problem.", QgsMessageBar.WARNING)
        abundPUKeyDict = "blank"

    return abundPUKeyDict


def makePuvspr2DatFile(setupObject):
    qgis.utils.iface.messageBar().pushMessage("Processing files", "Making a new puvspr2.dat file.", QgsMessageBar.INFO, 2)
    inputPathName = setupObject.inputPath
    puvspr2DatName = inputPathName + os.sep + "puvspr2.dat"
    puvspr2DatWriter = csv.writer(open(puvspr2DatName, "wb"))
    puvspr2DatWriter.writerow(["species", "pu", "amount"])

    abundPUKeyDict = setupObject.abundPUKeyDict
    puList = abundPUKeyDict.keys()
    puList.sort()
    for aPUID in puList:
        aPUAbundDict = abundPUKeyDict[aPUID]
        aFeatList = aPUAbundDict.keys()
        aFeatList.sort()
        for aFeat in aFeatList:
            aAmount = aPUAbundDict[aFeat]
            puvspr2DatWriter.writerow([aFeat, aPUID, aAmount])

def checkCreateSporderDat(setupObject):
    if setupObject.setupStatus == "files_checked":
        inputPathName = setupObject.inputPath
        sporderDatName = inputPathName + os.sep + "sporder.dat"
        if os.path.isfile(sporderDatName)  == False:
            makeSporderDatFile(setupObject)

def makeSporderDatFile(setupObject):
    qgis.utils.iface.messageBar().pushMessage("Processing files", "Making a new sporder.dat file.", QgsMessageBar.INFO, 2)
    if setupObject.abundPUKeyDict == "blank":
        setupObject.abundPUKeyDict = makeAbundancePUKeyDict(setupObject)
    inputPathName = setupObject.inputPath
    sporderDatName = inputPathName + os.sep + "sporder.dat"
    sporderDatWriter = csv.writer(open(sporderDatName, "wb"))
    sporderDatWriter.writerow(["species", "pu", "amount"])

    sporderDict = makeSporderDict(setupObject)
    featList = sporderDict.keys()
    featList.sort()
    for aFeat in featList:
        aPUDict = sporderDict[aFeat]
        aPUList = aPUDict.keys()
        aPUList.sort()
        for aPUID in aPUList:
            aAmount = aPUDict[aPUID]
            sporderDatWriter.writerow([aFeat, aPUID, aAmount])

def makeSporderDict(setupObject):
    sporderDict = {}
    abundPUKeyDict = setupObject.abundPUKeyDict
    for puID in abundPUKeyDict:
        featDict = abundPUKeyDict[puID]
        for featID in featDict:
            featAmount = featDict[featID]
            try:
                puDict = sporderDict[featID]
            except KeyError:
                puDict = {}
            puDict[puID] = featAmount
            sporderDict[featID] = puDict

    return sporderDict

def checkPULayerPresent():
    canvas = qgis.utils.iface.mapCanvas()
    allLayers = canvas.layers()
    puLayerPresentBool = False
    for aLayer in allLayers:
        if aLayer.name() == "Planning units":
            puLayerPresentBool = True

    return puLayerPresentBool


def checkAddPULayer(setupObject):
    if setupObject.setupStatus == "files_checked":
        if not checkPULayerPresent():
            cluz_display.addPULayer(setupObject, 0) # 0 = Position


def removeThenAddPULayer(setupObject): # This is a way of refreshing PU Layer so it shows newly added fields
    canvas = qgis.utils.iface.mapCanvas()
    allLayers = canvas.layers()
    puLayerPositionInTOC = 0
    for aLayer in allLayers:
        if aLayer.name() == "Planning units":
            puLayer = aLayer
            QgsMapLayerRegistry.instance().removeMapLayers([puLayer.id()])
            canvas.refresh()
            cluz_display.addPULayer(setupObject, puLayerPositionInTOC)
        puLayerPositionInTOC += 1


def updatePULayerToShowChangesByShiftingExtent():# This is a way of refreshing PU Layer so it displays changes in values
    canvas = qgis.utils.iface.mapCanvas()

    canvasExtent = canvas.extent()
    extMinX, extMaxX = canvasExtent.xMinimum(), canvasExtent.xMaximum()
    extMinY, extMaxY = canvasExtent.yMinimum(), canvasExtent.yMaximum()
    xShift = (extMaxX - extMinX) * 0.005
    shiftMinX, shiftMaxX = extMinX + xShift, extMaxX + xShift
    canvas.setExtent(QgsRectangle(shiftMinX, extMinY, shiftMaxX, extMaxY))
    canvas.refresh()


def returnTempPathName(pathString, fileType):
    suffixString = "." + fileType
    tempNumber = 0
    while os.path.exists(pathString.replace(suffixString, "_tmp" + str(tempNumber) + suffixString)):
        tempNumber += 1
    tempPath = pathString.replace(suffixString, "_tmp" + str(tempNumber) + suffixString)

    return tempPath

def returnFeatIDListFromAbundPUKeyDict(setupObject):
    keyDict = {}
    abundPUKeyDict = setupObject.abundPUKeyDict
    for aPUID in abundPUKeyDict:
        featIDList = abundPUKeyDict[aPUID].keys()
        for aFeat in featIDList:
            keyDict[aFeat] = 0

    return keyDict.keys()

def updateTargetCSVFromTargetDict(setupObject, targetDict):
    decPrec = setupObject.decimalPlaces
    targetCSVFilePath = setupObject.targetPath
    textRows = []
    with open(targetCSVFilePath, 'rb') as in_file:
        targetReader = csv.reader(in_file)
        origHeaderList = targetReader.next()
        textRows.append(origHeaderList)
        lowerHeaderList = [] #convert to lowercase so it doesn't matter whether the headers or lowercase, uppercase or a mix
        for aHeader in origHeaderList:
            lowerHeaderList.append(aHeader.lower())

        for aRow in targetReader:
            featID = int(aRow[lowerHeaderList.index('id')])
            featTarget = float(aRow[lowerHeaderList.index('target')])
            pcTarget = returnPCTargetValueForTargetTable(targetDict, featID, featTarget, decPrec)

            aRow[lowerHeaderList.index('conserved')] = targetDict[featID][4]
            aRow[lowerHeaderList.index('total')] = targetDict[featID][5]
            aRow[lowerHeaderList.index('pc_target')] = pcTarget
            textRows.append(aRow)

    with open(targetCSVFilePath, 'wb') as out_file:
        targetWriter = csv.writer(out_file)
        for bRow in textRows:
            targetWriter.writerow(bRow)

def returnPCTargetValueForTargetTable(targetDict, featID, featTarget, decPrec):
    if featTarget > 0:
        pcTarget = targetDict[featID][4] / featTarget
        pcTarget *= 100
        pcTarget = round(float(pcTarget), decPrec)
        pcTarget = format(pcTarget, "." + str(decPrec) + "f")
    else:
        pcTarget = -1

    return pcTarget

def returnLowestUnusedFileNameNumber(dirPath, fileNameBase, extTypeText):
    fileNameNumber = 1
    while os.path.exists(dirPath + os.sep + fileNameBase + str(fileNameNumber) + extTypeText):
        fileNameNumber += 1

    return fileNameNumber


def returnRoundedValue(setupObject, rawValue):
    decPrec = setupObject.decimalPlaces
    limboValue = round(float(rawValue), decPrec)
    finalValue = format(limboValue, "." + str(decPrec) + "f")

    return finalValue