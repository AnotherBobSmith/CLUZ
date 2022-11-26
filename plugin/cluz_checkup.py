# """
# /***************************************************************************
#                                  A QGIS plugin
#  CLUZ for QGIS
#                              -------------------
#         begin                : 2022-26-08
#         copyright            : (C) 2022 by Bob Smith, DICE
#         email                : r.j.smith@kent.ac.uk
#  ***************************************************************************/
#
# /***************************************************************************
#  *                                                                         *
#  *   This program is free software; you can redistribute it and/or modify  *
#  *   it under the terms of the GNU General Public License as published by  *
#  *   the Free Software Foundation; either version 2 of the License, or     *
#  *   (at your option) any later version.                                   *
#  *                                                                         *
#  ***************************************************************************/
# """
#
from qgis.core import QgsVectorLayer, QgsProject

from os import access, path, sep, W_OK
from csv import reader
from time import ctime

from .cluz_messages import warningMessage
from .cluz_display import addPULayer
from .cluz_make_file_dicts import changeConservedFieldNameToEarCons


def checkFilesAndReturnSetupFileOKBool(setupObject, analysisType, decPlaceText, numIterText, numRunText, numBlmText, startPropText, targetPropText):
    setupFileOK = True
    if analysisType not in ['Marxan', 'MarxanWithZones']:
        warningMessage('Setup file incorrect format', 'The analysis type value is not specified as Marxan or MarxanWithZones. Please correct this.')
        setupFileOK = False
    try:
        setupObject.decimalPlaces = int(decPlaceText)
        if setupObject.decimalPlaces > 5:
            setupObject.decimalPlaces = 5
    except ValueError:
        warningMessage('Setup file incorrect format', 'The specified decimal place value in the setup file is not an integer. Please correct this.')
        setupFileOK = False
    try:
        setupObject.numIter = int(numIterText)
    except ValueError:
        warningMessage('Setup file incorrect format', 'The specified number of iterations in the setup file is not an integer. Please correct this.')
        setupFileOK = False
    try:
        setupObject.numRuns = int(numRunText)
    except ValueError:
        warningMessage('Setup file incorrect format', 'The specified number of runs in the setup file is not an integer. Please correct this.')
        setupFileOK = False
    try:
        setupObject.blmValue = float(numBlmText)
    except ValueError:
        warningMessage('Setup file incorrect format', 'The BLM value in the setup file is not a number. Please correct this.')
        setupFileOK = False
    try:
        setupObject.startProp = float(startPropText)
    except ValueError:
        warningMessage('Setup file incorrect format', 'The start proportion value in the setup file is not a number. Please correct this.')
        setupFileOK = False
    try:
        setupObject.targetProp = float(targetPropText)
    except ValueError:
        warningMessage('Setup file incorrect format', 'The target proportion value in the setup file is not a number. Please correct this.')
        setupFileOK = False

    return setupFileOK


def checkStatusObjectValues(setupObject):
    setupFileCorrectBool = True

    setupFileCorrectBool = checkDecPlacesValue(setupObject, setupFileCorrectBool)
    setupFileCorrectBool = checkNumItersValue(setupObject, setupFileCorrectBool)
    setupFileCorrectBool = checkNumRunsValue(setupObject, setupFileCorrectBool)
    setupFileCorrectBool = checkBlmValue(setupObject, setupFileCorrectBool)
    setupFileCorrectBool = checkStartProp(setupObject, setupFileCorrectBool)
    setupFileCorrectBool = checkCLUZFilePaths(setupObject, setupFileCorrectBool)

    foldersOKBool = checkFolderValues(setupObject)

    if setupFileCorrectBool and foldersOKBool:
        setupObject.setupStatus = 'values_checked'

    return setupObject


def checkDecPlacesValue(setupObject, setupFileCorrectBool):
    try:
        setupObject.decimalPlaces = int(setupObject.decimalPlaces)
        if setupObject.decimalPlaces < 0:
            warningMessage('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of decimal places cannot be a negative value. Please correct this.')
            setupFileCorrectBool = False
    except ValueError:
        warningMessage('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of decimal places in the Abundance and Target tables is not an integer. Please correct this.')
        setupFileCorrectBool = False

    return setupFileCorrectBool


def checkNumItersValue(setupObject, setupFileCorrectBool):
    try:
        setupObject.numIter = int(setupObject.numIter)
        if setupObject.numIter < 0:
            warningMessage('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of Marxan iterations cannot be a negative value. Please correct this.')
            setupFileCorrectBool = False
    except ValueError:
        warningMessage('Setup file incorrect format', 'The specified number of iterations in the setup file is not an integer. Please correct this.')
        setupFileCorrectBool = False

    return setupFileCorrectBool


def checkNumRunsValue(setupObject, setupFileCorrectBool):
    try:
        setupObject.numRuns = int(setupObject.numRuns)
        if setupObject.numRuns < 0:
            warningMessage('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of Marxan runs cannot be a negative value. Please correct this.')
            setupFileCorrectBool = False
    except ValueError:
        warningMessage('Setup file incorrect format', 'The specified number of runs in the setup file is not an integer. Please correct this.')
        setupFileCorrectBool = False

    return setupFileCorrectBool


def checkBlmValue(setupObject, setupFileCorrectBool):
    try:
        setupObject.blmValue = float(setupObject.blmValue)
        if setupObject.blmValue < 0:
            warningMessage('Setup file incorrect format', 'The specified BLM value in the CLUZ setup file cannot be a negative value. Please correct this.')
            setupFileCorrectBool = False
    except ValueError:
        warningMessage('Setup file incorrect format', 'The BLM value in the setup file is not a number. Please correct this.')
        setupFileCorrectBool = False

    return setupFileCorrectBool


def checkStartProp(setupObject, setupFileCorrectBool):
    try:
        setupObject.startProp = float(setupObject.startProp)
        if setupObject.startProp < 0 or setupObject.startProp > 1:
            warningMessage('Setup file incorrect format', 'The specified proportion of planning units initially selected by Marxan as specified in the CLUZ setup has to be between 0 and 1. Please correct this.')
            setupFileCorrectBool = False
    except ValueError:
        warningMessage('Setup file incorrect format', 'The start proportion value in the setup file is not a number. Please correct this.')
        setupFileCorrectBool = False

    return setupFileCorrectBool


def checkTargetProp(setupObject, setupFileCorrectBool):
    try:
        setupObject.targetProp = float(setupObject.targetProp)
        if setupObject.targetProp < 0 or setupObject.targetProp > 1:
            warningMessage('Setup file incorrect format', 'The specified proportion of a target that needs to be achieved for Marxan to report that the target has been met as specified in the CLUZ setup has to be between 0 and 1. Please correct this.')
            setupFileCorrectBool = False
    except ValueError:
        warningMessage('Setup file incorrect format', 'The target proportion value in the setup file is not a number. Please correct this.')
        setupFileCorrectBool = False

    return setupFileCorrectBool


def checkCLUZFilePaths(setupObject, setupFileCorrectBool):
    inputPath = setupObject.inputPath
    if inputPath == 'blank':
        warningMessage('Missing input folder', 'The input folder has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False
    elif path.exists(inputPath) is False:
        warningMessage('Incorrect input folder', 'The specified input folder cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False

    outputPath = setupObject.outputPath
    if outputPath == 'blank':
        warningMessage('Missing output folder', 'The output folder has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False
    elif path.exists(outputPath) is False:
        warningMessage('Incorrect output folder', 'The specified output folder cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False

    puPath = setupObject.puPath
    if puPath == 'blank':
        warningMessage('Missing planning unit shapefile', 'The planning unit shapefile has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False
    elif path.exists(puPath) is False:
        warningMessage('Incorrect planning unit shapefile path', 'The specified planning unit shapefile cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False

    puvspr2Path = setupObject.inputPath + sep + 'puvspr2.dat'
    if path.exists(puvspr2Path) is False:
        warningMessage('Incorrect puvspr2 path', 'The puvspr2.dat file cannot be found. Please add it to the specified input folder.')
        setupFileCorrectBool = False

    targetPath = setupObject.targetPath
    if targetPath == 'blank':
        warningMessage('Missing target table', 'The target table has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False
    elif path.exists(targetPath) is False:
        warningMessage('Incorrect target table path', 'The specified target table cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setupFileCorrectBool = False

    return setupFileCorrectBool


def checkFolderValues(setupObject):
    foldersOKBool = True
    if path.isfile(setupObject.marxanPath) is False:
        warningMessage('Setup file incorrect format', 'The specified Marxan file cannot be found. Please correct this.')
        foldersOKBool = False
    else:
        marxanDirPath = path.dirname(setupObject.marxanPath)
        if setupObject.marxanPath == 'blank' or setupObject.marxanPath == '':
            warningMessage('Marxan path invalid', 'The Marxan path is missing.')
            foldersOKBool = False
        elif path.isdir(marxanDirPath) is False:
            warningMessage('Marxan path invalid', 'The specified folder containing Marxan does not exist.')
            foldersOKBool = False
        elif access(marxanDirPath, W_OK) is False:
            warningMessage('Marxan path invalid', 'Running Marxan involves CLUZ creating a new input file in the folder where Marxan is stored. You do not have permission to save files into the specified folder so please move Marxan to a folder where you do have permission.')
            foldersOKBool = False

    return foldersOKBool


def createAndCheckTargetFile(setupObject, checkBool):
    targetCSVFilePath = setupObject.targetPath
    setupObject.targetFileDate = ctime(path.getmtime(targetCSVFilePath))
    targetFileFieldNameList = ['id', 'name', 'type', 'spf', 'target', 'ear+cons', 'total', 'pc_target']
    try:
        with open(targetCSVFilePath, 'rt') as f:
            targetReader = reader(f)
            origHeaderList = next(targetReader)

        lowercaseHeaderList = list()
        for aHeader in origHeaderList:
            lowercaseHeader = aHeader.lower()
            lowercaseHeaderList.append(lowercaseHeader)

        for aHeader in targetFileFieldNameList:
            if lowercaseHeaderList.count(aHeader) == 0:
                if aHeader != 'ear+cons':
                    warningMessage('Formatting error:', 'the Target table is missing a ' + aHeader + ' field. Please select a table with the correct format.')
                    checkBool = False
                elif aHeader == 'ear+cons' and lowercaseHeaderList.count('conserved') == 0:
                    warningMessage('Formatting error:', 'the Target table is missing a ' + aHeader + ' field. Please select a table with the correct format.')
                    checkBool = False
                else:
                    warningMessage('Formatting error:', 'the Conserved field in the Target table is now known as the Ear+Cons field, as it shows how much of each feature is Earmarked and Conserved. CLUZ will now rename the Conserved field in your table.')
                    changeConservedFieldNameToEarCons(setupObject)
                    checkBool = False
    except FileNotFoundError:
        checkBool = False

    return checkBool


def createAndCheckPuvspr2File(setupObject, checkBool):
    puvspr2FilePath = setupObject.inputPath + sep + 'puvspr2.dat'
    with open(puvspr2FilePath, 'rt') as f:
        puvspr2Reader = reader(f)
        puvspr2HeaderList = next(puvspr2Reader)
        if puvspr2HeaderList != ['species', 'pu', 'amount']:
            warningMessage('Formatting error: ', 'the puvspr2.dat file in the input folder is incorrectly formatted and should only have the following header names: species, pu, amount.')
            checkBool = False

    return checkBool


def createAndCheckPuLayerFile(setupObject, checkBool):
    puLayer = QgsVectorLayer(setupObject.puPath, 'Planning units', 'ogr')
    fields = puLayer.fields()
    fieldDetailsList = list()
    titleText = 'Formatting error: '
    mainText = 'the planning unit shapefile must contain a field named '
    for aField in fields:
        fieldDetailsList.append((str(aField.name()), str(aField.typeName())))
    if fieldDetailsList.count(('Unit_ID', 'Integer')) == 0 and fieldDetailsList.count(('Unit_ID', 'Integer64')) == 0:
        warningMessage(titleText, mainText + 'Unit_ID containing integer values.')
        checkBool = False
    if fieldDetailsList.count(('Area', 'Real')) == 0:
        warningMessage(titleText, mainText + 'Area containing real number values.')
        checkBool = False
    if fieldDetailsList.count(('Cost', 'Real')) == 0:
        warningMessage(titleText, mainText + 'Cost containing real number values.')
        checkBool = False
    if fieldDetailsList.count(('Status', 'String')) == 0:
        warningMessage(titleText, mainText + 'Status containing text values.')
        checkBool = False

    return checkBool


def checkPULayerPresent():
    allLayers = QgsProject.instance().mapLayers().values()
    puLayerPresentBool = False
    for aLayer in allLayers:
        if aLayer.name() == 'Planning units':
            puLayerPresentBool = True

    return puLayerPresentBool


def checkAddPULayer(setupObject):
    if setupObject.setupStatus == 'files_checked':
        if not checkPULayerPresent():
            addPULayer(setupObject, 0)  # 0 = Position


def returnFeatIDSetFromAbundPUKeyDict(setupObject):
    featIDSet = set()
    abundPUKeyDict = setupObject.abundPUKeyDict
    for puID in abundPUKeyDict:
        featIDList = abundPUKeyDict[puID].keys()
        for featID in featIDList:
            featIDSet.add(featID)

    return featIDSet
