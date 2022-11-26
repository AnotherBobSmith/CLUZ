"""
/***************************************************************************
                                 A QGIS plugin
 CLUZ for QGIS
                             -------------------
        begin                : 2022-26-08
        copyright            : (C) 2022 by Bob Smith, DICE
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

from .cluz_setup import CluzSetupObject

from os import path

from .cluz_setup import updateSetupObjectFromSetupFile, checkStatusObjectValues, createAndCheckCLUZFiles, updateClzSetupFile
from .cluz_checkup import checkAddPULayer
from .zcluz_checkup import checkAddZonesPULayer


def addSetupDialogTextFromSetupObject(setupDialog, setupObject):
    setupDialog.marxanLineEdit.setText(setupObject.marxanPath)
    setupDialog.inputLineEdit.setText(setupObject.inputPath)
    setupDialog.outputLineEdit.setText(setupObject.outputPath)
    setupDialog.puLineEdit.setText(setupObject.puPath)
    setupDialog.targetLineEdit.setText(setupObject.targetPath)
    setupDialog.setPrecValue(setupObject.decimalPlaces)

    if path.isfile(setupObject.setupPath):
        setupPathText = path.abspath(setupObject.setupPath)
    else:
        setupPathText = 'blank'

    if setupObject.analysisType == 'MarxanWithZones':
        setupDialog.mzonesRadioButton.setChecked(True)
        setupDialog.zonesLineEdit.setText(setupObject.zonesPath)
    else:
        setupDialog.mzonesRadioButton.setChecked(False)

    setupPathLabelText = 'Setup file location: ' + setupPathText
    setupDialog.setupPathLabel.setText(setupPathLabelText)


def loadSetupFileCode(setupDialog, setupObject, setupFilePath):
    setupObject = updateSetupObjectFromSetupFile(setupObject, setupFilePath)

    if setupObject.setupStatus == 'values_checked':
        setupObject = createAndCheckCLUZFiles(setupObject)

    if setupObject.setupStatus == "files_checked":
        setupObject.setupAction = "blank"
        setupPathLabelText = path.abspath(setupFilePath)
        setupPathLabelText = "Setup file location: " + str(setupPathLabelText)
        setupDialog.setupPathLabel.setText(setupPathLabelText)

        setupDialog.marxanLineEdit.setText(path.abspath(setupObject.marxanPath))
        setupDialog.inputLineEdit.setText(path.abspath(setupObject.inputPath))
        setupDialog.outputLineEdit.setText(setupObject.outputPath)
        setupDialog.puLineEdit.setText(setupObject.puPath)
        setupDialog.targetLineEdit.setText(setupObject.targetPath)
        setupDialog.setPrecValue(setupObject.decimalPlaces)

        if setupObject.analysisType == 'MarxanWithZones':
            setupDialog.mzonesRadioButton.setChecked(True)
            setupDialog.zonesLineEdit.setText(setupObject.zonesPath)
            setupObject.ZonesAction.setEnabled(True)
            setupObject.ConvertVecAction.setEnabled(False)
            setupObject.ConvertRasterAction.setEnabled(False)
            setupObject.ConvertCsvAction.setEnabled(False)
            setupObject.MinPatchAction.setEnabled(False)
        else:
            setupDialog.mzonesRadioButton.setChecked(False)
            setupObject.ZonesAction.setEnabled(False)
            setupObject.ConvertVecAction.setEnabled(True)
            setupObject.ConvertRasterAction.setEnabled(True)
            setupObject.ConvertCsvAction.setEnabled(True)
            setupObject.MinPatchAction.setEnabled(True)

        if setupObject.analysisType != 'MarxanWithZones':
            checkAddPULayer(setupObject)
        else:
            checkAddZonesPULayer(setupObject)

        if setupObject.analysisType != 'MarxanWithZones':
            checkAddPULayer(setupObject)
        else:
            checkAddZonesPULayer(setupObject)


def saveSetupFileCode(setupDialog, setupObject, setupFilePath):
    limboSetupObject = CluzSetupObject()
    limboSetupObject.TargetsMetAction = setupObject.TargetsMetAction
    limboSetupObject.ZonesAction = setupObject.ZonesAction
    limboSetupObject.MinPatchAction = setupObject.MinPatchAction
    limboSetupObject.setupStatus = 'blank'

    if setupDialog.mzonesRadioButton.isChecked():
        limboSetupObject.analysisType = 'MarxanWithZones'
    else:
        limboSetupObject.analysisType = 'Marxan'
    limboSetupObject.decimalPlaces = int(setupDialog.precComboBox.currentText())
    limboSetupObject.marxanPath = setupDialog.marxanLineEdit.text()
    limboSetupObject.inputPath = setupDialog.inputLineEdit.text()
    limboSetupObject.outputPath = setupDialog.outputLineEdit.text()
    limboSetupObject.puPath = setupDialog.puLineEdit.text()
    limboSetupObject.targetPath = setupDialog.targetLineEdit.text()
    if limboSetupObject.analysisType == 'MarxanWithZones':
        limboSetupObject.zonesPath = setupDialog.zonesLineEdit.text()

    limboSetupObject = checkStatusObjectValues(limboSetupObject)
    saveSuccessfulBool = False

    if limboSetupObject.setupStatus == 'values_checked':
        limboSetupObject = createAndCheckCLUZFiles(limboSetupObject)

    if limboSetupObject.setupStatus == 'files_checked':
        saveSuccessfulBool = True
        copyLimboParametersToSetupObject(setupObject, limboSetupObject)
        saveSuccessfulBool = updateClzSetupFile(setupObject, saveSuccessfulBool)
        if saveSuccessfulBool:
            setupPathLabelText = 'Setup file location: ' + str(setupFilePath)
            setupDialog.setupPathLabel.setText(setupPathLabelText)

            checkAddPULayer(setupObject)

    return saveSuccessfulBool


def copyLimboParametersToSetupObject(setupObject, limboSetupObject):
    setupObject.decimalPlaces = limboSetupObject.decimalPlaces
    setupObject.marxanPath = limboSetupObject.marxanPath
    setupObject.inputPath = limboSetupObject.inputPath
    setupObject.outputPath = limboSetupObject.outputPath
    setupObject.puPath = limboSetupObject.puPath
    setupObject.targetPath = limboSetupObject.targetPath


def saveAsSetupFileCode(setupDialog, setupObject, newSetupFilePath):
    if setupDialog.mzonesRadioButton.isChecked():
        setupObject.analysisType = 'MarxanWithZones'
    else:
        setupObject.analysisType = 'Marxan'
    setupObject.decimalPlaces = int(setupDialog.precComboBox.currentText())
    setupObject.marxanPath = setupDialog.marxanLineEdit.text()
    setupObject.inputPath = setupDialog.inputLineEdit.text()
    setupObject.outputPath = setupDialog.outputLineEdit.text()
    setupObject.puPath = setupDialog.puLineEdit.text()
    setupObject.targetPath = setupDialog.targetLineEdit.text()
    if setupObject.analysisType == 'MarxanWithZones':
        setupObject.zonesPath = setupDialog.zonesLineEdit.text()

    setupObject.setupPath = newSetupFilePath

    setupObject = checkStatusObjectValues(setupObject)
    if setupObject.setupStatus == 'values_checked':
        setupObject = createAndCheckCLUZFiles(setupObject)
    if setupObject.setupStatus == 'files_checked':
        saveSuccessfulBool = True
        saveSuccessfulBool = updateClzSetupFile(setupObject, saveSuccessfulBool)
        if saveSuccessfulBool:
            setupPathLabelText = 'Setup file location: ' + str(newSetupFilePath)
            setupDialog.setupPathLabel.setText(setupPathLabelText)
            checkAddPULayer(setupObject)
