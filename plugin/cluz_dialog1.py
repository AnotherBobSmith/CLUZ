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

from qgis.PyQt.QtWidgets import QDialog, QFileDialog

from os import path
import sys

from .cluz_messages import warningMessage, successMessage
from .cluz_dialog1_code import loadSetupFileCode, saveAsSetupFileCode, saveSetupFileCode, addSetupDialogTextFromSetupObject
from .cluz_display import removeThenAddPULayer

sys.path.append(path.dirname(path.abspath(__file__)) + "/forms")
from cluz_form_start import Ui_startDialog
from cluz_form_setup import Ui_setupDialog


class startDialog(QDialog, Ui_startDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.okButton.clicked.connect(lambda: self.returnStartBool(setupObject))
        self.cancelButton.clicked.connect(self.closeStartDialog)

    def returnStartBool(self, setupObject):
        if self.openRadioButton.isChecked():
            setupObject.setupAction = 'open'
        elif self.createButton.isChecked():
            setupObject.setupAction = 'new'
        self.close()

    def closeStartDialog(self):
        self.close()


class setupDialog(QDialog, Ui_setupDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        addSetupDialogTextFromSetupObject(self, setupObject)

        if setupObject.analysisType == 'Marxan':
            self.marxanRadioButton.setChecked(True)
            self.mzonesRadioButton.setChecked(False)
            self.zonesLabel.setVisible(False)
            self.zonesLineEdit.setVisible(False)
            self.zonesButton.setVisible(False)
        else:
            self.marxanRadioButton.setChecked(False)
            self.mzonesRadioButton.setChecked(True)
            self.zonesLabel.setVisible(True)
            self.zonesLineEdit.setVisible(True)
            self.zonesButton.setVisible(True)

        self.marxanButton.clicked.connect(self.setMarxanPath)
        self.inputButton.clicked.connect(self.setInputPath)
        self.outputButton.clicked.connect(self.setOutputPath)
        self.puButton.clicked.connect(self.setPuPath)
        self.targetButton.clicked.connect(self.setTargetPath)
        self.zonesButton.clicked.connect(self.setZonesPath)

        self.loadButton.clicked.connect(lambda: self.loadSetupFile(setupObject))
        self.saveButton.clicked.connect(lambda: self.saveSetupFile(setupObject))
        self.saveAsButton.clicked.connect(lambda: self.saveAsSetupFile(setupObject))

    def setMarxanPath(self):
        (marxanPathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select Marxan file', '*.exe')
        marxanPathNameText = path.abspath(marxanPathNameRawText)
        if marxanPathNameText is not None:
            self.marxanLineEdit.setText(marxanPathNameText)

    def setInputPath(self):
        inputPathNameRawText = QFileDialog.getExistingDirectory(self, 'Select input folder')
        inputPathNameText = path.abspath(inputPathNameRawText)
        if inputPathNameText is not None:
            self.inputLineEdit.setText(inputPathNameText)

    def setOutputPath(self):
        outputPathNameRawText = QFileDialog.getExistingDirectory(self, 'Select output folder')
        outputPathNameText = path.abspath(outputPathNameRawText)
        if outputPathNameText is not None:
            self.outputLineEdit.setText(outputPathNameText)

    def setPuPath(self):
        (puPathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select planning unit shapefile', '*.shp')
        puPathNameText = path.abspath(puPathNameRawText)
        if puPathNameText is not None:
            self.puLineEdit.setText(puPathNameText)

    def setTargetPath(self):
        (targetPathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select target table', '*.csv')
        targetPathNameText = path.abspath(targetPathNameRawText)
        if targetPathNameText is not None:
            self.targetLineEdit.setText(targetPathNameText)

    def setZonesPath(self):
        (zonePathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select zone table', '*.csv')
        zonePathNameText = path.abspath(zonePathNameRawText)
        if zonePathNameText is not None:
            self.zonesLineEdit.setText(zonePathNameText)

    def setPrecValue(self, precValue):
        self.precComboBox.addItems(['0', '1', '2', '3', '4', '5'])
        numberList = [0, 1, 2, 3, 4, 5]
        if precValue > 5:
            titleText = 'Decimal precision value problem'
            mainText = 'The number of decimal places specified in the CLUZ setup file cannot be more than 5. The specified value has been changed to 5.'
            warningMessage(titleText, mainText)
            precValue = 5
        indexValue = numberList.index(precValue)
        self.precComboBox.setCurrentIndex(indexValue)

    def loadSetupFile(self, setupObject):
        (setupPathLabelText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select CLUZ setup file', '*.clz')
        if setupPathLabelText != '':
            loadSetupFileCode(self, setupObject, setupPathLabelText)
            removeThenAddPULayer(setupObject, 0)

    def saveSetupFile(self, setupObject):
        setupFilePath = setupObject.setupPath
        if path.isfile(setupFilePath):
            saveSuccessfulBool = saveSetupFileCode(self, setupObject, setupFilePath)
            if saveSuccessfulBool:
                successMessage('File saved', 'The CLUZ setup file has been saved successfully.')
        elif setupFilePath == 'blank':
            warningMessage("No CLUZ setup file name", "The CLUZ setup file name has not been set. Please use the Save As... option instead.")
        else:
            warningMessage("CLUZ setup file name error", "The current CLUZ setup file path is incorrect.")

    def saveAsSetupFile(self, setupObject):
        (newSetupFilePath, fileTypeDetailsText) = QFileDialog.getSaveFileName(self, 'Save new CLUZ setup file', '*.clz')
        if newSetupFilePath != '':
            saveAsSetupFileCode(self, setupObject, newSetupFilePath)
            if setupObject.setupStatus:
                successMessage('File saved', 'The CLUZ setup file has been saved successfully.')
        else:
            warningMessage("CLUZ setup file name error", "The current CLUZ setup file path is incorrect.")
