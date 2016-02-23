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
from PyQt4.QtGui import *
from qgis.gui import *
import qgis
from qgis.core import *

import os
import csv
import copy

import cluz_setup
import cluz_functions1

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")

from cluz_form_start import Ui_startDialog
from cluz_form_setup import Ui_setupDialog
from cluz_form_create import Ui_createDialog
from cluz_form_convert_vec import Ui_convertVecDialog
from cluz_form_convert_csv import Ui_convertCsvDialog
from cluz_form_remove import Ui_removeDialog

class startDialog(QDialog, Ui_startDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.returnStartBool(self, setupObject))
        QObject.connect(self.cancelButton, SIGNAL("clicked()"), self.closeStartDialog)


    def returnStartBool(self, dialog, setupObject):
        statusCode = self.startButtonGroup.checkedId()
        if statusCode == -2:
            setupObject.setupAction = "open"
        if statusCode == -3:
            setupObject.setupAction = "new"
        self.close()

    def closeStartDialog(self):
        self.close()


class setupDialog(QDialog, Ui_setupDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.marxanLineEdit.setText(setupObject.marxanPath)
        self.inputLineEdit.setText(setupObject.inputPath)
        self.outputLineEdit.setText(setupObject.outputPath)
        self.puLineEdit.setText(setupObject.puPath)
        self.targLineEdit.setText(setupObject.targetPath)

        numberList = ["0", "1", "2", "3", "4", "5"]
        self.precComboBox.addItems(numberList)
        numberList = [0, 1, 2, 3, 4, 5]
        precValue = setupObject.decimalPlaces
        if precValue > 5:
            qgis.utils.iface.messageBar().pushMessage("Decimal precision value problem", "The number of decimal places specified in the CLUZ setup file cannot be more than 5. The specified value has been changed to 5.", QgsMessageBar.WARNING)
            precValue = 5
        indexValue = numberList.index(precValue)
        self.precComboBox.setCurrentIndex(indexValue)

        if os.path.isfile(setupObject.setupPath):
            setupPathText = os.path.abspath(setupObject.setupPath)
        else:
            setupPathText = "blank"
        setupPathLabelText = "Setup file location: " + setupPathText
        self.setupPathLabel.setText(setupPathLabelText)

        QObject.connect(self.marxanButton, SIGNAL("clicked()"), self.setMarxanPath)
        QObject.connect(self.inputButton, SIGNAL("clicked()"), self.setInputPath)
        QObject.connect(self.outputButton, SIGNAL("clicked()"), self.setOutputPath)
        QObject.connect(self.puButton, SIGNAL("clicked()"), self.setPuPath)
        QObject.connect(self.targButton, SIGNAL("clicked()"), self.setTargPath)

        QObject.connect(self.loadButton, SIGNAL("clicked()"), lambda: self.loadSetupFile(setupObject))
        QObject.connect(self.saveButton, SIGNAL("clicked()"), lambda: self.saveSetupFile(setupObject))
        QObject.connect(self.saveasButton, SIGNAL("clicked()"), lambda: self.saveAsSetupFile(setupObject))

    def setMarxanPath(self):
        marxanPathNameRawText = QFileDialog.getOpenFileName(self, 'Select Marxan file', '*.exe')
        marxanPathNameText = os.path.abspath(marxanPathNameRawText)
        if marxanPathNameText != None:
            self.marxanLineEdit.setText(marxanPathNameText)

    def setInputPath(self):
        inputPathNameText = QFileDialog.getExistingDirectory(self, 'Select input folder')
        inputPathNameText = os.path.abspath(inputPathNameText)
        if inputPathNameText != None:
            self.inputLineEdit.setText(inputPathNameText)

    def setOutputPath(self):
        outputPathNameText = QFileDialog.getExistingDirectory(self, 'Select output folder')
        outputPathNameText = os.path.abspath(outputPathNameText)
        if outputPathNameText != None:
            self.outputLineEdit.setText(outputPathNameText)

    def setPuPath(self):
        puPathNameText = QFileDialog.getOpenFileName(self, 'Select planning unit shapefile', '*.shp')
        puPathNameText = os.path.abspath(puPathNameText)
        if puPathNameText != None:
            self.puLineEdit.setText(puPathNameText)

    def setTargPath(self):
        targPathNameText = QFileDialog.getOpenFileName(self, 'Select target table', '*.csv')
        targPathNameText = os.path.abspath(targPathNameText)
        if targPathNameText != None:
            self.targLineEdit.setText(targPathNameText)

    def loadSetupFile(self, setupObject):
        setupPathLabelText = QFileDialog.getOpenFileName(self, 'Select CLUZ setup file', '*.clz')
        if setupPathLabelText != "":

            cluz_setup.updateSetupObjectFromSetupFile(setupObject, setupPathLabelText)
            cluz_setup.checkStatusObjectValues(setupObject)
            if setupObject.setupStatus == "values_checked":
                cluz_setup.createAndCheckCLUZFiles(setupObject)

            if setupObject.setupStatus == "files_checked":
                setupObject.setupAction = "blank"
                setupPathLabelText = os.path.abspath(setupPathLabelText)
                setupPathLabelText = "Setup file location: " + str(setupPathLabelText)
                self.setupPathLabel.setText(setupPathLabelText)

                self.marxanLineEdit.setText(os.path.abspath(setupObject.marxanPath))
                self.inputLineEdit.setText(os.path.abspath(setupObject.inputPath))
                self.outputLineEdit.setText(setupObject.outputPath)
                self.puLineEdit.setText(setupObject.puPath)
                self.targLineEdit.setText(setupObject.targetPath)

                numberList = [0, 1, 2, 3, 4, 5]
                precValue = setupObject.decimalPlaces
                if precValue > 5:
                    qgis.utils.iface.messageBar().pushMessage("Decimal precision value problem", "The number of decimal places specified in the CLUZ setup file cannot be more than 5. The specified value has been changed to 5.", QgsMessageBar.WARNING)
                    precValue = 5
                indexValue = numberList.index(precValue)
                self.precComboBox.setCurrentIndex(indexValue)

                cluz_setup.checkAddPlanningUnit(setupObject)

    def saveSetupFile(self, setupObject):
        setupFilePath = setupObject.setupPath

        if os.path.isfile(setupFilePath):
            limboSetupObject = copy.deepcopy(setupObject)
            limboSetupObject.decimalPlaces = int(self.precComboBox.currentText())
            limboSetupObject.marxanPath = self.marxanLineEdit.text()
            limboSetupObject.inputPath = self.inputLineEdit.text()
            limboSetupObject.outputPath = self.outputLineEdit.text()
            limboSetupObject.puPath = self.puLineEdit.text()
            limboSetupObject.targetPath = self.targLineEdit.text()

            cluz_setup.checkStatusObjectValues(limboSetupObject)
            if limboSetupObject.setupStatus == "values_checked":
                cluz_setup.createAndCheckCLUZFiles(limboSetupObject)
                setupObject = copy.deepcopy(limboSetupObject)

            if setupObject.setupStatus == "files_checked":
                cluz_setup.updateClzSetupFile(setupObject)
                setupPathLabelText = "Setup file location: " + str(setupFilePath)
                self.setupPathLabel.setText(setupPathLabelText)
                cluz_setup.checkAddPlanningUnit(setupObject)

        elif setupFilePath == "blank":
            qgis.utils.iface.messageBar().pushMessage("No CLUZ setup file name", "The CLUZ setup file name has not been set. Please use the Save As... option instead.", QgsMessageBar.WARNING)
        else:
            qgis.utils.iface.messageBar().pushMessage("CLUZ setup file name error", "The current CLUZ setup file path is incorrect.", QgsMessageBar.WARNING)

    def saveAsSetupFile(self, setupObject):
        newSetupFilePath = QFileDialog.getSaveFileName(self, 'Save new CLUZ setup file', '*.clz')
        if newSetupFilePath != "":
            setupObject.decimalPlaces = int(self.precComboBox.currentText())
            setupObject.marxanPath = self.marxanLineEdit.text()
            setupObject.inputPath = self.inputLineEdit.text()
            setupObject.outputPath = self.outputLineEdit.text()
            setupObject.puPath = self.puLineEdit.text()
            setupObject.targetPath = self.targLineEdit.text()

            setupObject.setupPath = newSetupFilePath

            cluz_setup.checkStatusObjectValues(setupObject)
            if setupObject.setupStatus == "values_checked":
                cluz_setup.createAndCheckCLUZFiles(setupObject)
            if setupObject.setupStatus == "files_checked":
                cluz_setup.updateClzSetupFile(setupObject)
                setupPathLabelText = "Setup file location: " + str(newSetupFilePath)
                self.setupPathLabel.setText(setupPathLabelText)
                cluz_setup.checkAddPlanningUnit(setupObject)

        else:
            qgis.utils.iface.messageBar().pushMessage("CLUZ setup file name error", "The current CLUZ setup file path is incorrect.", QgsMessageBar.WARNING)

class createDialog(QDialog, Ui_createDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.convLineEdit.setText("1")

        QObject.connect(self.puButton, SIGNAL("clicked()"), self.setShapefilePath)
        QObject.connect(self.inputButton, SIGNAL("clicked()"), self.setInputPath)
        QObject.connect(self.targetButton, SIGNAL("clicked()"), self.setTargetPath)
        QObject.connect(self.okButton, SIGNAL("clicked()"), self.createNewCLUZFiles)

    def setShapefilePath(self):
        shapefilePathNameText = QFileDialog.getOpenFileName(self, 'Select shapefile', '*.shp')
        if shapefilePathNameText != None:
            self.puLineEdit.setText(shapefilePathNameText)

    def setInputPath(self):
        inputPathNameText = QFileDialog.getExistingDirectory(self, 'Select input folder')
        if inputPathNameText != None:
            self.inputLineEdit.setText(inputPathNameText)

    def setTargetPath(self):
        targetPathNameText = QFileDialog.getSaveFileName(self, 'Specify target table name', '*.csv', '*.csv')
        if targetPathNameText != None:
            self.targetLineEdit.setText(targetPathNameText)

    def createNewCLUZFiles(self):
        createFiles = True
        costAsAreaBool = self.equalCheckBox.isChecked()
        try:
            convFactor = float(self.convLineEdit.text())
        except:
            qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified conversion format is in an incorrect format. It should be a number greater than 0.", QgsMessageBar.WARNING)
            createFiles = False
        if convFactor <= 0:
            qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified conversion format is in an incorrect format. It should be a number greater than 0.", QgsMessageBar.WARNING)
            createFiles = False

        puLayer = QgsVectorLayer(self.puLineEdit.text(), "Shapefile", "ogr")
        layerGeomType = puLayer.geometryType()
        puProvider = puLayer.dataProvider()
        puIdFieldOrder = puProvider.fieldNameIndex("Unit_ID")
        puCostFieldOrder = puProvider.fieldNameIndex("Area")
        puAreaFieldOrder = puProvider.fieldNameIndex("Cost")
        puStatusFieldOrder = puProvider.fieldNameIndex("Status")

        if layerGeomType != 2:
            qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified shapefile is not a polygon layer.", QgsMessageBar.WARNING)
            createFiles = False

        if puIdFieldOrder != -1 or puCostFieldOrder != -1 or puAreaFieldOrder != -1 or puStatusFieldOrder != -1:
            qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified shapefile cannot contain fields named Unit_ID, Area, Cost or Status as these will be created here. Please rename these fields and try again.", QgsMessageBar.WARNING)
            createFiles = False

        if self.inputLineEdit.text() == "":
            qgis.utils.iface.messageBar().pushMessage("No file specified", "You need to specify the input folder where the puvspr2.dat file will be saved.", QgsMessageBar.WARNING)
            createFiles = False
        else:
            if os.access(os.path.dirname(self.inputLineEdit.text()), os.W_OK):
                pass
            else:
                qgis.utils.iface.messageBar().pushMessage("Incorrect format", "You do not have access to the specified input folder.", QgsMessageBar.WARNING)
                createFiles = False

        if self.targetLineEdit.text() == "":
            qgis.utils.iface.messageBar().pushMessage("No file specified", "You need to specify the name and path for the new target file.", QgsMessageBar.WARNING)
            createFiles = False
        else:
            if os.access(os.path.dirname(self.targetLineEdit.text()), os.W_OK):
                pass
            else:
                qgis.utils.iface.messageBar().pushMessage("Incorrect format", "You cannot save the target table into the specified folder because you do not have access.", QgsMessageBar.WARNING)
                createFiles = False

        if createFiles == True:
            cluz_functions1.makeBlankCLUZFiles(self.puLineEdit.text(), convFactor, costAsAreaBool, self.inputLineEdit.text(), self.targetLineEdit.text())
            qgis.utils.iface.messageBar().pushMessage("Task completed", "The CLUZ planning unit layer, blank abundance and target tables have been created. You can now use them when creating the CLUZ setup file.", QgsMessageBar.INFO)
            self.close()

class convertVecDialog(QDialog, Ui_convertVecDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        layerNameList = self.loadThemesList(setupObject)
        if len(layerNameList) == 0:
            qgis.utils.iface.messageBar().pushMessage("No suitable layers", "Please add to the project the polyline or polygon shapefiles that you want to import.", QgsMessageBar.WARNING)
            self.okButton.setEnabled(False)
        self.selectListWidget.addItems(layerNameList)
        self.idfieldLineEdit.setText("ID")
        self.convLineEdit.setText("1")
        self.convLineEdit.setEnabled(False)
        self.convLabel.setEnabled(False)

        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.convertLayersToAbundTable(setupObject))

    def loadThemesList(self, setupObject):
        listMapItems = QgsMapLayerRegistry.instance().mapLayers()
        layerNameList = []
        for nameCode, layer in listMapItems.iteritems():
            layerName = layer.name()
            layerGeomType = layer.geometryType()
            if layerName != "Planning units" and layerGeomType != 0:
                layerNameList.append(str(layerName))

        return layerNameList

    def convertLayersToAbundTable(self, setupObject):
        layerFactorCheck = True
        convFactorCheck = True

        idFieldName = self.idfieldLineEdit.text()
        selectedLayerNameList = [item.text() for item in self.selectListWidget.selectedItems()]
        if len(selectedLayerNameList) == 0:
            self.close()
            QMessageBox.critical(None, "No layers selected", "No layers were selected.")
            layerFactorCheck = False
        else:
            listMapItems = QgsMapLayerRegistry.instance().mapLayers()
            layerList = []
            for nameCode, layer in listMapItems.iteritems():
                layerName = layer.name()
                if layerName in selectedLayerNameList:
                    layerList.append(layer)
            for aLayer in layerList:
                provider = aLayer.dataProvider()
                aLayerName = aLayer.name()
                idFieldOrder = provider.fieldNameIndex(idFieldName)
                if idFieldOrder == -1:
                    self.close()
                    QMessageBox.critical(None, "Layer format error with " + aLayerName, "The specified ID field " + idFieldName + " is not in the layer " + aLayerName + ".")
                    layerFactorCheck = False
                else:
                    idField = provider.fields().field(idFieldOrder)
                    idFieldType = idField.typeName()
                    if idFieldType != "Integer":
                        self.close()
                        QMessageBox.critical(None, "Layer format error" + aLayerName, "The specified ID field " + idFieldName + " does not contain integer values.")
                        layerFactorCheck = False

        if layerFactorCheck == True:
            convFactor = 1
            if self.userRadioButton.isChecked():
                try:
                    convFactor = float(self.convLineEdit.text())
                    if convFactor <= 0:
                        self.close()
                        QMessageBox.critical(None, "Incorrect conversion value", "The conversion value must be a number greater than 0.")
                        convFactorCheck = False

                except:
                    self.close()
                    QMessageBox.critical(None, "Incorrect conversion value", "The conversion value must be a number greater than 0.")
                    convFactorCheck = False

        if layerFactorCheck == True and convFactorCheck == True:
            addAbundDict, featIDList = cluz_functions1.makeVecAddAbundDict(setupObject, layerList, idFieldName, convFactor)
            existingIDSet = set(featIDList).intersection(set(setupObject.targetDict.keys()))
            if len(existingIDSet) > 0:
                self.close()
                listText = ""
                for aID in existingIDSet:
                    listText += str(aID) + ", "
                    finalListText = listText[0 : -2]
                QMessageBox.critical(None, "Existing features", "The abundance table already contains features with ID values of " + finalListText + ". This process will terminate without adding the new values.")
            else:
                cluz_functions1.addFeaturesToPuvspr2File(setupObject, addAbundDict)
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)
                cluz_setup.makeSporderDatFile(setupObject)

                cluz_functions1.addFeaturesToTargetCsvFile(setupObject, addAbundDict, featIDList)
                setupObject.targetDict = cluz_setup.makeTargetDict(setupObject)

                self.close()

class convertCsvDialog(QDialog, Ui_convertCsvDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.idfieldComboBox.setEnabled(False)
        self.convLineEdit.setText("1")
        self.convLineEdit.setEnabled(False)
        self.convLabel.setEnabled(False)
        self.noneRadioButton.setChecked(True)

        QObject.connect(self.browseButton, SIGNAL("clicked()"), self.setCsvFilePath)
        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.convertCSVToAbundTable(setupObject))

    def setCsvFilePath(self):
        csvPathNameText = QFileDialog.getOpenFileName(self, 'Select CSV file', '*.csv')
        if csvPathNameText != "":
            self.csvFileLineEdit.setText(csvPathNameText)
            csvFile =  open(csvPathNameText, 'rb')
            reader = csv.reader(csvFile)
            fileHeaderList = reader.next()
            self.idfieldComboBox.addItems(fileHeaderList)
            self.idfieldComboBox.setEnabled(True)

    def convertCSVToAbundTable(self, setupObject):
        layerFactorCheck = True
        convFactorCheck = True

        unitIDFieldName = self.idfieldComboBox.currentText()
        csvFilePath = self.csvFileLineEdit.text()
        if csvFilePath == "":
            self.close()
            QMessageBox.critical(None, "No file specified", "Please specify a csv file to import.")
            layerFactorCheck = False
        elif os.path.isfile(csvFilePath) == False:
            self.close()
            QMessageBox.critical(None, "Incorrect format", "The specified csv file does not exist.")
            layerFactorCheck = False
        else:
            pass

        if layerFactorCheck == True:
            convFactor = 1 # Default value
            if self.userRadioButton.isChecked():
                try:
                    convFactor = float(self.convLineEdit.text())
                    if convFactor <= 0:
                        self.close()
                        QMessageBox.critical(None, "Incorrect conversion value", "The conversion value must be a number greater than 0.")
                        convFactorCheck = False

                except:
                    self.close()
                    QMessageBox.critical(None, "Incorrect conversion value", "The conversion value must be a number greater than 0.")
                    convFactorCheck = False

        if layerFactorCheck == True and convFactorCheck == True:
            addAbundDict, featIDList, warningStatus = cluz_functions1.makeCsvAddAbundDict(setupObject, csvFilePath, unitIDFieldName, convFactor)
            if warningStatus == "ExistingFeatures":
                self.close()
                QMessageBox.critical(None, "Duplicate features", "The feature ID values in the table duplicate some of those in the abundance table. This process will terminate.")
            elif warningStatus == "HeaderWithNoID":
                self.close()
                QMessageBox.critical(None, "Missing ID code", "One of the fields containing abundance data in the specified table does not contain any numerical characters and so does not specify the feature ID. This process will terminate.")
            else:
                setupObject.abundPUKeyDict = cluz_functions1.addAbundDictToAbundPUKeyDict(setupObject, addAbundDict)
                cluz_setup.makePuvspr2DatFile(setupObject)
                cluz_setup.makeSporderDatFile(setupObject)

                cluz_functions1.addFeaturesToTargetCsvFile(setupObject, addAbundDict, featIDList)
                setupObject.targetDict = cluz_setup.makeTargetDict(setupObject)

                self.close()

class removeDialog(QDialog, Ui_removeDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        featStringDict = self.loadFeatureList(setupObject)

        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.removeSelectedFeatures(setupObject, featStringDict))

    def loadFeatureList(self, setupObject):
        targetFeatIDSet = set(setupObject.targetDict.keys())
        abundFeatIDSet = cluz_setup.returnFeatIDListFromAbundPUKeyDict(setupObject)
        featIDSet = targetFeatIDSet.union(abundFeatIDSet)
        featIDList = list(featIDSet)
        featIDList.sort()

        featStringList = []
        missingFeatStringList = [] #This is for features that are missing the from the target or abund tables
        featStringDict = {}
        for aFeat in featIDList:
            try:
                aString = str(aFeat) + " - " + setupObject.targetDict[aFeat][0]
                if aFeat in abundFeatIDSet:
                    pass
                else:
                    aString = "*Target table only* " + aString
            except KeyError:
                aString = "*Abundance table only * " + str(aFeat) + " - blank"
            if aString[0] == "*":
                missingFeatStringList.append(aString)
            else:
                featStringList.append(aString)
            featStringDict[aString] = aFeat
        finalFeatStringList = missingFeatStringList + featStringList
        self.featListWidget.addItems(finalFeatStringList)

        return featStringDict

    def removeSelectedFeatures(self, setupObject, featStringDict):
        selectedFeatIDList = [featStringDict[item.text()] for item in self.featListWidget.selectedItems()]
        selectedFeatIDSet = set(selectedFeatIDList)
        selectedFeatIDListLength = len(selectedFeatIDList)
        if selectedFeatIDListLength > 0:
            qgis.utils.iface.mainWindow().statusBar().showMessage("Updating puvspr2.dat.")
            cluz_functions1.remFeaturesFromPuvspr2(setupObject, selectedFeatIDSet)
            setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)
            cluz_setup.makeSporderDatFile(setupObject)

            qgis.utils.iface.mainWindow().statusBar().showMessage("Updating target table.")
            cluz_functions1.remFeaturesFromTargetCsv_Dict(setupObject, selectedFeatIDSet)
            setupObject.targetDict = cluz_setup.makeTargetDict(setupObject)

            qgis.utils.iface.mainWindow().statusBar().showMessage("Task successfully completed: " + str(selectedFeatIDListLength) + " features have been removed.")
            self.close()
        else:
            self.close()
            QMessageBox.critical(None, "No features selected", "No features were selected and so no changes have been made.")
