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
from qgis.core import *
from qgis.gui import *
import qgis

from cluz_form_distribution import Ui_distributionDialog
from cluz_form_identify_selected import Ui_identifySelectedDialog
from cluz_form_richness import Ui_richnessDialog
from cluz_form_portfolio import Ui_portfolioDialog
from cluz_form_portfolio_results import Ui_portfolioResultsDialog
from cluz_form_inputs import Ui_inputsDialog
from cluz_form_marxan import Ui_marxanDialog
from cluz_form_load import Ui_loadDialog
from cluz_form_calibrate import Ui_calibrateDialog
from cluz_form_minpatch import Ui_minpatchDialog
from cluz_form_patches import Ui_patchesDialog

import os
import csv
import subprocess
import time

import cluz_setup
import cluz_functions2
import cluz_display
import cluz_mpmain
import cluz_mpsetup

from cluz_setup import MinPatchObject

class distributionDialog(QDialog, Ui_distributionDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.loadFeatureList(setupObject)
        self.setInitialShapeFilePath(setupObject)

        QObject.connect(self.filePathButton, SIGNAL("clicked()"), self.setDistShapeFile)
        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.runDisplayDistributionMaps(setupObject))

    def setDistShapeFile(self):
        distShapefilePathNameText = QFileDialog.getSaveFileName(self, 'Save new shapefile', '*.shp')
        self.filePathlineEdit.setText(distShapefilePathNameText)

    def loadFeatureList(self, setupObject):
        featList = setupObject.targetDict.keys()
        featList.sort()
        featStringList = []
        for aFeat in featList:
            aString = str(aFeat) + " - " + setupObject.targetDict[aFeat][0]
            featStringList.append(aString)
        self.featListWidget.addItems(featStringList)

    def setInitialShapeFilePath(self, setupObject):
        dirPath = os.path.dirname(setupObject.puPath)
        distShapeFileNameNumber = cluz_setup.returnLowestUnusedFileNameNumber(dirPath, "cluz_dist", ".shp")
        distShapeFileFullPath = dirPath + os.sep + "cluz_dist" + str(distShapeFileNameNumber) + ".shp"
        self.filePathlineEdit.setText(distShapeFileFullPath)

    def runDisplayDistributionMaps(self, setupObject):
        if self.intervalRadioButton.isChecked():
            legendType = "equal_interval"
        elif self.areaRadioButton.isChecked():
            legendType = "equal_area"
        distShapeFilePathName = self.filePathlineEdit.text()
        selectedFeatList = [item.text() for item in self.featListWidget.selectedItems()]
        selectedFeatIDList = [int(item.split(" - ")[0]) for item in selectedFeatList]

        abundValuesDict = cluz_display.createDistributionMapShapefile(setupObject, distShapeFilePathName, selectedFeatIDList)
        cluz_display.displayDistributionMaps(setupObject, distShapeFilePathName, abundValuesDict, legendType, selectedFeatIDList)

        self.close()

class identifySelectedDialog(QDialog, Ui_identifySelectedDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()

        returnSelectedPUIDDict = cluz_functions2.returnSelectedPUIDDict(setupObject)
        selectedPUDetailsDict = cluz_functions2.returnSelectedPUDetailsDict(setupObject, returnSelectedPUIDDict)

        if len(returnSelectedPUIDDict) > 0:
            self.showSelectedIdentifyData(setupObject, selectedPUDetailsDict)
            self.setWindowTitle('Details of ' + str(len(returnSelectedPUIDDict)) + ' planning units.')
        else:
            self.setWindowTitle('No planning units selected')


    def showSelectedIdentifyData(self, setupObject, selectedPUDetailsDict):
        self.identifySelectedTableWidget.clear()
        self.identifySelectedTableWidget.setColumnCount(8)
        self.addSelectedIdenitfyDataToTableWidget(setupObject, selectedPUDetailsDict)

        headerList = ["ID  ", "Name  ", "Available  ", "Conserved  ", "Earmarked  ", "Excluded  ", "Target  ", "Target shortfall  "]
        self.identifySelectedTableWidget.setHorizontalHeaderLabels(headerList)
        for aColValue in range(len(headerList)):
            self.identifySelectedTableWidget.resizeColumnToContents(aColValue)


    def addSelectedIdenitfyDataToTableWidget(self, setupObject, selectedPUDetailsDict):
        featIDList = setupObject.targetDict.keys()
        featIDList.sort()
        for rowNumber in range(0, len(featIDList)):
            featID = featIDList[rowNumber]
            self.identifySelectedTableWidget.insertRow(rowNumber)
            featIDTableItem = QTableWidgetItem(str(featID))
            featNameTableItem = QTableWidgetItem(str(setupObject.targetDict[featID][0]))
            avaIDTableItem = QTableWidgetItem(str(cluz_functions2.returnStringAmountPerStatus(setupObject, selectedPUDetailsDict, 'Available', featID)))
            conIDTableItem = QTableWidgetItem(str(cluz_functions2.returnStringAmountPerStatus(setupObject, selectedPUDetailsDict, 'Conserved', featID)))
            earIDTableItem = QTableWidgetItem(str(cluz_functions2.returnStringAmountPerStatus(setupObject, selectedPUDetailsDict, 'Earmarked', featID)))
            exlIDTableItem = QTableWidgetItem(str(cluz_functions2.returnStringAmountPerStatus(setupObject, selectedPUDetailsDict, 'Excluded', featID)))
            featTarget = cluz_setup.returnRoundedValue(setupObject, setupObject.targetDict[featID][3])
            featTargetTableItem = QTableWidgetItem(featTarget)
            featShortfallTableItem = QTableWidgetItem(cluz_functions2.returnStringShortfall(setupObject, featID))

            self.identifySelectedTableWidget.setItem(rowNumber, 0, featIDTableItem)
            self.identifySelectedTableWidget.setItem(rowNumber, 1, featNameTableItem)
            self.identifySelectedTableWidget.setItem(rowNumber, 2, avaIDTableItem)
            conIDTableItem.setTextColor(QColor.fromRgb(0, 153, 51))
            self.identifySelectedTableWidget.setItem(rowNumber, 3, conIDTableItem)
            earIDTableItem.setTextColor(QColor.fromRgb(51, 204, 51))
            self.identifySelectedTableWidget.setItem(rowNumber, 4, earIDTableItem)
            self.identifySelectedTableWidget.setItem(rowNumber, 5, exlIDTableItem)
            self.identifySelectedTableWidget.setItem(rowNumber, 6, featTargetTableItem)
            if cluz_functions2.returnStringShortfall(setupObject, featID) == 'Target met':
                featShortfallTableItem.setTextColor(QColor.fromRgb(128, 128, 128))
            self.identifySelectedTableWidget.setItem(rowNumber, 7, featShortfallTableItem)

    # http://stackoverflow.com/questions/24971305/copy-pyqt-table-selection-including-column-and-row-headers
    def keyPressEvent(self, e):
        if (e.modifiers() & Qt.ControlModifier):
            selected = self.identifySelectedTableWidget.selectedRanges()

            if e.key() == Qt.Key_C: #copy
                s = ""
                for r in xrange(selected[0].topRow(), selected[0].bottomRow() + 1):
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.identifySelectedTableWidget.item(r, c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)


class richnessDialog(QDialog, Ui_richnessDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        (countName, rangeName, irrepName) = self.returnInitialFieldNames(setupObject)
        self.countLineEdit.setText(countName)
        self.rangeLineEdit.setText(rangeName)
        self.irrepLineEdit.setText(irrepName)

        self.irrepBox.setVisible(False)
        self.irrepLabel.setVisible(False)
        self.irrepLineEdit.setVisible(False)

        typeList = self.produceTypeTextList(setupObject)
        self.typeListWidget.addItems(typeList)

        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.createRichnessResults(setupObject))

    def returnInitialFieldNames(self, setupObject):
        puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
        fieldNameList = [field.name() for field in puLayer.pendingFields()]

        countName = "F_COUNT"
        countSuffix = ""
        if countName in fieldNameList:
            countSuffix = 1
            while (countName + str(countSuffix)) in fieldNameList:
                countSuffix += 1
        finalCountName = countName + str(countSuffix)

        rangeName = "R_RICH"
        rangeSuffix = ""
        if rangeName in fieldNameList:
            rangeSuffix = 1
            while (rangeName + str(rangeSuffix)) in fieldNameList:
                rangeSuffix += 1
        finalRangeName = rangeName + str(rangeSuffix)

        irrepName = "IRREP"
        irrepSuffix = ""
        if irrepName in fieldNameList:
            irrepSuffix = 1
            while (irrepName + str(irrepSuffix)) in fieldNameList:
                irrepSuffix += 1
        finalIrrepName = irrepName + str(irrepSuffix)

        return (finalCountName, finalRangeName, finalIrrepName)

    def produceTypeTextList(self, setupObject):
        typeTextList = []
        typeDict = {}
        for featID in setupObject.targetDict:
            featType = setupObject.targetDict[featID][1]
            try:
                featCount = typeDict[featType]
                featCount += 1
            except KeyError:
                featCount = 1
            typeDict[featType] = featCount

        typeList = typeDict.keys()
        typeList.sort()
        for aType in typeList:
            typeText = "Type " + str(aType) + " (" + str(typeDict[aType]) + " features)"
            typeTextList.append(typeText)

        return typeTextList

    def createRichnessResults(self, setupObject):
        selectedTypeTextList = [item.text() for item in self.typeListWidget.selectedItems()]
        selectedTypeList = [int(item.split(" ")[1]) for item in selectedTypeTextList]
        puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
        fieldNameList = [field.name() for field in puLayer.pendingFields()]
        progressString = "details_fine"

        if len(selectedTypeList) == 0:
            qgis.utils.iface.messageBar().pushMessage("Calculating richness", "No type codes have been selected.", QgsMessageBar.WARNING, 3)
            progressString = "stop"
        if self.countBox.isChecked() is False and self.rangeBox.isChecked() is False and self.irrepBox.isChecked() is False:
            qgis.utils.iface.messageBar().pushMessage("Calculating richness", "No options have been selected.", QgsMessageBar.WARNING, 3)
            progressString = "stop"

        if self.countBox.isChecked() and progressString == "details_fine":
            countFieldName = self.countLineEdit.text()
            if countFieldName in fieldNameList:
                qgis.utils.iface.messageBar().pushMessage("Feature Count field name duplication", "The planning unit layer already contains a field named " + countFieldName + ". Please choose another name.", QgsMessageBar.WARNING)
            elif countFieldName == "":
                qgis.utils.iface.messageBar().pushMessage("Feature Count field name blank", "The Feature Count name field is blank. Please choose a name.", QgsMessageBar.WARNING)
            elif len(countFieldName) > 10:
                qgis.utils.iface.messageBar().pushMessage("Invalid field name", "The Feature Count field name cannot be more than 10 characters long.", QgsMessageBar.WARNING)
            else:
                cluz_functions2.produceCountField(setupObject, countFieldName, selectedTypeList)
                cluz_setup.removeThenAddPULayer(setupObject)
                cluz_display.displayGraduatedLayer(setupObject, countFieldName, "Feature count", 2) #2 is yellow to green QGIS legend code

                qgis.utils.iface.messageBar().pushMessage("Richness results", "The fields have been successfully added to the planning unit layer attribute table.", QgsMessageBar.INFO, 3)
                self.close()

        if self.rangeBox.isChecked() and progressString == "details_fine":
            rangeFieldName = self.rangeLineEdit.text()
            if rangeFieldName in fieldNameList:
                qgis.utils.iface.messageBar().pushMessage("Restricted Range Richness field name duplication", "The planning unit layer already contains a field named " + rangeFieldName + ". Please choose another name.", QgsMessageBar.WARNING)
            elif rangeFieldName == "":
                qgis.utils.iface.messageBar().pushMessage("Restricted Range Richness field name blank", "The Restricted Range Richness name field is blank. Please choose a name.", QgsMessageBar.WARNING)
            elif len(rangeFieldName) > 10:
                qgis.utils.iface.messageBar().pushMessage("Invalid field name", "The Restricted Range Richness field name cannot be more than 10 characters long.", QgsMessageBar.WARNING)
            else:
                cluz_functions2.produceRestrictedRangeField(setupObject, rangeFieldName, selectedTypeList)
                cluz_display.displayGraduatedLayer(setupObject, rangeFieldName, "Restricted Range score", 2) #2 is yellow to green QGIS legend code

                qgis.utils.iface.messageBar().pushMessage("Richness results", "The fields have been successfully added to the planning unit layer attribute table.", QgsMessageBar.INFO, 3)
                self.close()

        if self.irrepBox.isChecked() and progressString == "details_fine":
            irrepFieldName = self.irrepLineEdit.text()
            if irrepFieldName in fieldNameList:
                qgis.utils.iface.messageBar().pushMessage("Irreplaceability field name duplication", "The planning unit layer already contains a field named " + irrepFieldName + ". Please choose another name.", QgsMessageBar.WARNING)
            elif irrepFieldName == "":
                qgis.utils.iface.messageBar().pushMessage("Irreplaceability field name blank", "The Restricted Range Richness name field is blank. Please choose a name.", QgsMessageBar.WARNING)
            elif len(irrepFieldName) > 10:
                qgis.utils.iface.messageBar().pushMessage("Invalid field name", "The Irreplaceability field name cannot be more than 10 characters long.", QgsMessageBar.WARNING)
            else:
                combSize, puSize = cluz_functions2.calcIrrepCombinationSize(setupObject, selectedTypeList)
                cluz_functions2.produceIrrepField(setupObject, irrepFieldName, selectedTypeList, combSize, puSize)
                cluz_display.displayGraduatedLayer(setupObject, irrepFieldName, "Irreplaceability score", 2) #2 is yellow to green QGIS legend code

                qgis.utils.iface.messageBar().pushMessage("Irreplaceability results", "The fields have been successfully added to the planning unit layer attribute table.", QgsMessageBar.INFO, 3)
                self.close()

class inputsDialog(QDialog, Ui_inputsDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.boundextBox.setEnabled(False)

        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.setCreateMarxanInputFiles(setupObject))

    def setCreateMarxanInputFiles(self, setupObject):
        messageStringList = []
        if self.targetBox.isChecked():
            cluz_functions2.createSpecDatFile(setupObject)
            messageStringList.append("spec.dat")

        if self.puBox.isChecked():
            cluz_functions2.createPuDatFile(setupObject)
            messageStringList.append("pu.dat")

        if self.boundBox.isChecked():
            if self.boundextBox.isChecked() and self.boundextBox.isEnabled():
                extEdgeBool = True
            else:
                extEdgeBool = False
            cluz_functions2.createBoundDatFile(setupObject, extEdgeBool)
            qgis.utils.iface.mainWindow().statusBar().showMessage("")
            messageStringList.append("bound.dat")

        if len(messageStringList) > 0:
            messageString = ""
            for aString in messageStringList:
                messageString += aString + ", "
            finalMessageString = messageString[:-2]

            qgis.utils.iface.messageBar().pushMessage("Marxan files:", "The following files have been produced: " + finalMessageString, QgsMessageBar.INFO, 3)

        self.close()

class marxanDialog(QDialog, Ui_marxanDialog):
    def __init__(self, iface, setupObject, targetsMetAction):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.boundLineEdit.setVisible(False)

        self.iterLineEdit.setText(str(setupObject.numIter))
        self.runLineEdit.setText(str(setupObject.numRuns))
        outputName = cluz_functions2.returnOutputName(setupObject)
        self.outputLineEdit.setText(outputName)
        self.boundLineEdit.setText(str(setupObject.blmValue))
        self.parallelListWidget.addItems(["2", "3", "4", "5"])
        self.parallelListWidget.setCurrentRow(0)

        if setupObject.boundFlag == True:
            self.boundCheckBox.setChecked(True)
            self.boundLineEdit.setVisible(True)

        if setupObject.extraOutputsFlag == True:
            self.extraCheckBox.setChecked(True)

        self.missingLineEdit.setText(str(setupObject.targetProp))
        self.propLineEdit.setText(str(setupObject.startProp))

        QObject.connect(self.startButton, SIGNAL("clicked()"), lambda: self.runMarxan(setupObject, targetsMetAction))

    def runMarxan(self, setupObject, targetsMetAction):
        numIterString = self.iterLineEdit.text()
        numRunString = self.runLineEdit.text()
        outputName = str(self.outputLineEdit.text())
        setupObject.outputName = outputName
        if self.boundCheckBox.isChecked():
            blmValueString = self.boundLineEdit.text()
        else:
            blmValueString = "0"
        missingPropString = self.missingLineEdit.text()
        initialPropString = self.propLineEdit.text()

        extraOutputsBool = self.extraCheckBox.isChecked()

        if self.parallelCheckBox.isChecked():
            numParallelAnalyses = int(self.parallelListWidget.selectedItems()[0].text())
        else:
            numParallelAnalyses = 1

        checkMarxanInputValuesBool = cluz_functions2.checkMarxanInputValuesBool(numIterString, numRunString, blmValueString, missingPropString, initialPropString, numParallelAnalyses)
        if checkMarxanInputValuesBool == True:
            numIter = int(numIterString)
            numRun = int(numRunString)
            blmValue = float(blmValueString)
            missingProp = float(missingPropString)
            initialProp = float(initialPropString)

            cluz_functions2.createSpecDatFile(setupObject)
            setupObject = cluz_functions2.marxanUpdateSetupObject(setupObject, outputName, numIter, numRun, blmValue, extraOutputsBool, missingProp, initialProp)
            cluz_setup.updateClzSetupFile(setupObject)
            self.close()

            if numParallelAnalyses == 1:
                bestOutputFile, summedOutputFile = launchSingleMarxanAnalysis(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool)
            else:
                bestOutputFile, summedOutputFile = launchMultiMarxanAnalysis(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool, numParallelAnalyses)

            cluz_functions2.addBestMarxanOutputToPUShapefile(setupObject, bestOutputFile, "Best")
            cluz_functions2.addSummedMarxanOutputToPUShapefile(setupObject, summedOutputFile, "SF_Score")

            cluz_display.reloadPULayer(setupObject)
            cluz_display.removePreviousMarxanLayers()
            bestLayerName = "Best (" + outputName + ")"
            summedLayerName = "SF_Score (" + outputName + ")"
            cluz_display.displayBestOutput(setupObject, "Best", bestLayerName)
            cluz_display.displayGraduatedLayer(setupObject, "SF_Score", summedLayerName, 1) #1 is SF legend code

            targetsMetAction.setEnabled(True)

def launchSingleMarxanAnalysis(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool):
    marxanInputDict = cluz_functions2.marxanInputDict(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool)
    cluz_functions2.makeMarxanInputFile(setupObject, marxanInputDict)
    marxanBatFileName = cluz_functions2.makeMarxanBatFile(setupObject)
    subprocess.Popen([marxanBatFileName])
    cluz_functions2.waitingForMarxan(setupObject, outputName)
    bestOutputFile = setupObject.outputPath + os.sep + outputName + "_best.txt"
    summedOutputFile = setupObject.outputPath + os.sep + outputName + "_ssoln.txt"

    return bestOutputFile, summedOutputFile

def launchMultiMarxanAnalysis(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool, numParallelAnalyses):
    parallelAnalysesDetailsList = cluz_functions2.makeParallelAnalysesDetailsList(numParallelAnalyses, outputName, numRun)
    for (numRun, parallelOutputName) in parallelAnalysesDetailsList:
        marxanInputDict = cluz_functions2.marxanInputDict(setupObject, numIter, numRun, blmValue, missingProp, initialProp, parallelOutputName, extraOutputsBool)
        cluz_functions2.makeMarxanInputFile(setupObject, marxanInputDict)
        marxanBatFileName = cluz_functions2.makeMarxanBatFile(setupObject)
        subprocess.Popen([marxanBatFileName])
        time.sleep(2)

    cluz_functions2.waitingForParallelMarxan(setupObject, parallelAnalysesDetailsList)

    cluz_functions2.makeBestParralelFile(setupObject, outputName, parallelAnalysesDetailsList)
    bestOutputFile = setupObject.outputPath + os.sep + outputName + "_best.txt"

    cluz_functions2.makeSummedParralelFile(setupObject, outputName, parallelAnalysesDetailsList)
    summedOutputFile = setupObject.outputPath + os.sep + outputName + "_ssoln.txt"

    return bestOutputFile, summedOutputFile

class loadDialog(QDialog, Ui_loadDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.bestLabel.setVisible(False)
        self.bestLineEdit.setVisible(False)
        self.bestNameLineEdit.setVisible(False)
        self.bestButton.setVisible(False)

        self.summedLabel.setVisible(False)
        self.summedLineEdit.setVisible(False)
        self.summedNameLineEdit.setVisible(False)
        self.summedButton.setVisible(False)

        (bestName, summedName) = self.returnInitialFieldNames(setupObject)
        self.bestNameLineEdit.setText(bestName)
        self.summedNameLineEdit.setText(summedName)

        QObject.connect(self.bestButton, SIGNAL("clicked()"), self.setBestPath)
        QObject.connect(self.summedButton, SIGNAL("clicked()"), self.setSummedPath)
        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.loadPreviousMarxanResults(setupObject))

    def setBestPath(self):
        bestPathNameText = QFileDialog.getOpenFileName(self, 'Select Marxan best portfolio output', '*.txt')
        if bestPathNameText != None:
            self.bestLineEdit.setText(bestPathNameText)

    def setSummedPath(self):
        summedPathNameText = QFileDialog.getOpenFileName(self, 'Select Marxan summed solution output', '*.txt')
        if summedPathNameText != None:
            self.summedLineEdit.setText(summedPathNameText)

    def returnInitialFieldNames(self, setupObject):
        puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
        fieldNameList = [field.name() for field in puLayer.pendingFields()]
        bestName = "IMP_BEST"
        bestSuffix = ""
        if bestName in fieldNameList:
            bestSuffix = 1
            while (bestName + str(bestSuffix)) in fieldNameList:
                bestSuffix += 1
        finalBestName = bestName + str(bestSuffix)

        summedName = "IMP_SUM"
        summedSuffix = ""
        if summedName in fieldNameList:
            summedSuffix = 1
            while (summedName + str(summedSuffix)) in fieldNameList:
                summedSuffix += 1
        finalSummedName = summedName + str(summedSuffix)

        return (finalBestName, finalSummedName)

    def loadPreviousMarxanResults(self, setupObject):
        bestFieldName = self.bestNameLineEdit.text()
        summedFieldName = self.summedNameLineEdit.text()
        if self.bestCheckBox.isChecked():
            bestPath = self.bestLineEdit.text()
        else:
            bestPath = "blank"
        if self.summedCheckBox.isChecked():
            summedPath = self.summedLineEdit.text()
        else:
            summedPath = "blank"
        puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
        fieldNameList = [field.name() for field in puLayer.pendingFields()]
        progressString = "check_files"
        if bestFieldName in fieldNameList:
            QMessageBox.warning(self,"Best field name duplication", "The planning unit theme already contains a field named " + bestFieldName + ". Please choose another name.")
            progressString = "stop"
        if summedFieldName in fieldNameList:
            QMessageBox.warning(self,"Summed field name duplication", "The planning unit theme already contains a field named " + summedFieldName + ". Please choose another name.")
            progressString = "stop"
        if len(bestFieldName) > 10:
            QMessageBox.warning(self,"Invalid field name", "The Best field name cannot be more than 10 characters long.")
            progressString = "stop"
        if len(summedFieldName) > 10:
            QMessageBox.warning(self,"Invalid field name", "The Summed field name cannot be more than 10 characters long.")
            progressString = "stop"
        if progressString == "check_files":
            self.close()
            if bestPath <> "blank":
                if os.path.isfile(bestPath):
                    with open(bestPath, 'rb') as f:
                        bestReader = csv.reader(f)
                        bestHeader = next(bestReader, None)  # skip the headers
                    if bestHeader == setupObject.bestHeadingFieldNames:
                        cluz_functions2.addBestMarxanOutputToPUShapefile(setupObject, bestPath, bestFieldName)
                        cluz_setup.removeThenAddPULayer(setupObject)
                        bestShapefileName = bestFieldName
                        cluz_display.displayBestOutput(setupObject, bestFieldName, bestShapefileName)
                    else:
                        QMessageBox.warning(self,"Invalid file","The specified Marxan best output file is incorrectly formatted. It must contain only two fields named planning_unit and solution.")
                else:
                    QMessageBox.warning(self,"Incorrect pathname","The specified pathname for the Marxan best output is invalid. Please choose another one.")
            if summedPath <> "blank":
                if os.path.isfile(summedPath):
                    with open(summedPath, 'rb') as f:
                        summedReader = csv.reader(f)
                        summedHeader = next(summedReader, None)  # skip the headers
                    if summedHeader == setupObject.summedHeadingFieldNames:
                        cluz_functions2.addSummedMarxanOutputToPUShapefile(setupObject, summedPath, summedFieldName)
                        cluz_setup.removeThenAddPULayer(setupObject)
                        summedShapefileName = summedFieldName
                        cluz_display.displayGraduatedLayer(setupObject, summedFieldName, summedShapefileName, 1) #1 is SF legend code
                    else:
                        QMessageBox.warning(self,"Invalid file","The specified Marxan summed output file is incorrectly formatted. It must contain only two fields named planning_unit and number")
                else:
                    QMessageBox.warning(self,"Incorrect pathname","The specified pathname for the Marxan summed output is invalid. Please choose another one")
            if bestPath <> "blank" or summedPath <> "blank":
                cluz_display.reloadPULayer(setupObject)

class calibrateDialog(QDialog, Ui_calibrateDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        parameterList = ["BLM", "Number of iterations", "Number of runs", "SPF"]
        self.paraComboBox.addItems(parameterList)
        self.paraComboBox.activated.connect(self.combo_chosen)

        self.iterLineEdit.setText(str(setupObject.numIter))
        self.runLineEdit.setText(str(setupObject.numRuns))
        self.boundLineEdit.setText(str(setupObject.blmValue))
        self.boundLabel.setEnabled(False)
        self.boundLineEdit.setEnabled(False)

        QObject.connect(self.saveResultsButton, SIGNAL("clicked()"), self.saveResultsFile)
        QObject.connect(self.runButton, SIGNAL("clicked()"), lambda: self.runSimpleCalibrateAnalysis(setupObject))

    def combo_chosen(self):
        self.iterLabel.setEnabled(True)
        self.iterLineEdit.setEnabled(True)
        self.runLabel.setEnabled(True)
        self.runLineEdit.setEnabled(True)
        self.boundLabel.setEnabled(True)
        self.boundLineEdit.setEnabled(True)

        parameterText = self.paraComboBox.currentText()
        if parameterText == "Number of iterations":
            self.iterLabel.setEnabled(False)
            self.iterLineEdit.setEnabled(False)
        elif parameterText == "Number of runs":
            self.runLabel.setEnabled(False)
            self.runLineEdit.setEnabled(False)
        elif parameterText == "BLM":
            self.boundLabel.setEnabled(False)
            self.boundLineEdit.setEnabled(False)

    def saveResultsFile(self):
        resultsFilePath = QFileDialog.getSaveFileName(self, 'Save Calibration results file', '*.csv')
        self.resultsLineEdit.setText(resultsFilePath)

    def runSimpleCalibrateAnalysis(self, setupObject):
        numAnalysesText = self.numberLineEdit.text()
        minAnalysesText = self.minLineEdit.text()
        maxAnalysesText = self.maxLineEdit.text()
        outputNameBase = self.outputLineEdit.text()
        resultPathText = self.resultsLineEdit.text()
        checkBool = True

        if outputNameBase == "":
            qgis.utils.iface.messageBar().pushMessage("Incorrect output basename", "The specified basename for the Marxan output files is blank. Please choose another one", QgsMessageBar.WARNING)
            checkBool = False

        try:
            numAnalyses = int(numAnalysesText)
            if numAnalyses < 1:
                qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified number of analysis is incorrectly formatted. It must be an integer and greater than 0.", QgsMessageBar.WARNING)
                checkBool = False
        except:
            qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified number of analysis is incorrectly formatted. It must be an integer and greater than 0.", QgsMessageBar.WARNING)
            checkBool = False
        try:
            minAnalyses = float(minAnalysesText)
            if minAnalyses < 0:
                qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified minimum value is incorrectly formatted. It must be a number and greater than 0.", QgsMessageBar.WARNING)
                checkBool = False
        except:
            qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified minimum value is incorrectly formatted. It must be a number and greater than 0.", QgsMessageBar.WARNING)
            checkBool = False
        try:
            maxAnalyses = int(maxAnalysesText)
            if maxAnalyses < 0:
                qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified maximum value is incorrectly formatted. It must be a number and greater than 0.", QgsMessageBar.WARNING)
                checkBool = False
        except:
            qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified maximum value is incorrectly formatted. It must be a number and greater than 0.", QgsMessageBar.WARNING)
            checkBool = False
        if checkBool == True:
            if maxAnalyses <= minAnalyses:
                qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified maximum value is incorrectly formatted. It must be greater than the specified minimum value.", QgsMessageBar.WARNING)
                checkBool = False

        if checkBool == True:
            exponentialBool = self.expCheckBox.isChecked()
            parameterValueList = cluz_functions2.makeParameterValueList(numAnalyses, minAnalyses, maxAnalyses, exponentialBool)

            if self.iterLineEdit.isEnabled():
                numIterText = self.iterLineEdit.text()
                try:
                    numIter = int(numIterText)
                    numIterList = [numIter] * numAnalyses
                    if numIter < 10000:
                        qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified number of iterations is incorrectly formatted. It must be an integer greater than 10000 (Marxan uses 10000 temperature drops in the simulated annealing process in these analyses and the number of iterations must be greater than the number of temperature drops).", QgsMessageBar.WARNING)
                        checkBool = False
                except:
                    qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified number of iterations is incorrectly formatted. It must be a positive integer.", QgsMessageBar.WARNING)
                    checkBool = False
            else:
                numIterList = parameterValueList

            if self.runLineEdit.isEnabled():
                numRunText = self.runLineEdit.text()
                try:
                    numRun = int(numRunText)
                    numRunList = [numRun] * numAnalyses
                    if numRun < 1:
                        qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified number of runs is incorrectly formatted. It must be a positive integer.", QgsMessageBar.WARNING)
                        checkBool = False
                except:
                    qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified number of runs is incorrectly formatted. It must be a positive integer.", QgsMessageBar.WARNING)
                    checkBool = False
            else:
                numRunList = parameterValueList

            if self.boundLineEdit.isEnabled():
                blmValueText = self.boundLineEdit.text()
                try:
                    blmValue = float(blmValueText)
                    blmValueList = [blmValue] * numAnalyses
                    if blmValue < 0:
                        qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified BLM value is incorrectly formatted. It must be a positive number.", QgsMessageBar.WARNING)
                        checkBool = False
                except:
                    qgis.utils.iface.messageBar().pushMessage("Incorrect format", "The specified BLM value is incorrectly formatted. It must be a positive number.", QgsMessageBar.WARNING)
                    checkBool = False
            else:
                blmValueList = parameterValueList

        if checkBool == True:
            runCalibrateMarxan(setupObject, numAnalyses, numRunList, numIterList, blmValueList, outputNameBase, resultPathText)
            self.close()

def runCalibrateMarxan(setupObject, numAnalyses, numRunList, numIterList, blmValueList, outputNameBase, resultPathText):
    missingPropList = [1.0] * numAnalyses
    initialPropList = [0.2] * numAnalyses
    calibrateResultsDict = {}
    for analysisNumber in range(0, numAnalyses):
        numIter = numIterList[analysisNumber]
        numRun = numRunList[analysisNumber]
        blmValue = blmValueList[analysisNumber]
        missingProp = missingPropList[analysisNumber]
        initialProp = initialPropList[analysisNumber]
        outputName = outputNameBase + str(analysisNumber + 1)
        extraOutputsBool = True
        marxanInputDict = cluz_functions2.marxanInputDict(setupObject, numIter, numRun, blmValue, missingProp, initialProp, outputName, extraOutputsBool)
        cluz_functions2.makeMarxanInputFile(setupObject, marxanInputDict)
        marxanBatFileName = cluz_functions2.makeMarxanBatFile(setupObject)
        subprocess.Popen([marxanBatFileName])
        time.sleep(2)
        cluz_functions2.waitingForMarxan(setupObject, outputName)

        calibrateResultsDict[analysisNumber] = cluz_functions2.makeAnalysisResultsDict(setupObject, marxanInputDict)

    cluz_functions2.makeCalibrateOutputFile(resultPathText, calibrateResultsDict)


class minpatchDialog(QDialog, Ui_minpatchDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        inputText = "Marxan input folder: " + setupObject.inputPath
        self.inputLabel.setText(inputText)
        outputText = "Marxan output folder: " + setupObject.outputPath
        self.outputLabel.setText(outputText)

        marxanFileList = self.makeMarxanFileList(setupObject)
        if len(marxanFileList) > 0:
            self.fileListWidget.addItems(marxanFileList)
        else:
            self.startButton.setEnabled(False)
            qgis.utils.iface.messageBar().pushMessage("No files found", "The specified Marxan output folder does not contain any individual portfolio files that can be analysed in MinPatch.", QgsMessageBar.WARNING)

        QObject.connect(self.browseButton, SIGNAL("clicked()"), self.setminpatchDetailFile)
        QObject.connect(self.startButton, SIGNAL("clicked()"), lambda: self.startMinPatch(setupObject))

    def setminpatchDetailFile(self):
        minpatchDetailPathNameText = QFileDialog.getOpenFileName(self, 'Select MinPatch details file', '*.dat')
        self.detailsLineEdit.setText(minpatchDetailPathNameText)

    def makeMarxanFileList(self, setupObject):
        marxanFileList = []

        fileList = os.listdir(setupObject.outputPath)
        analysisSet = set()
        for fileNameString in fileList:
            portfolioIdentifierString = fileNameString[-11:-9]
            if portfolioIdentifierString == "_r":
                analysisSet.add(fileNameString[0:-11])

        for aPathName in analysisSet:
            runPath = aPathName + "_r"
            fileCount = 0
            for bFile in fileList:
                if bFile.startswith(runPath):
                    fileCount += 1
            if fileCount > 0:
                marxanFileList.append(aPathName + " - " + str(fileCount) + " files")

        return marxanFileList

    def startMinPatch(self, setupObject):
        minpatchObject = MinPatchObject()
        runMinPatchBool = True

        detailsDatPath = self.detailsLineEdit.text()
        if os.path.isfile(detailsDatPath):
            with open(detailsDatPath, 'rb') as f:
                detailsReader = csv.reader(f)
                detailsHeader = next(detailsReader, None)  # skip the headers
            if detailsHeader == ["id", "area", "zone", "patch_area", "radius"]:
                minpatchObject.detailsDatPath = detailsDatPath
            else:
                qgis.utils.iface.messageBar().pushMessage("The specified MinPatch details file is incorrectly formatted. It must contain five fields named id, area ,zone ,patch_area and radius.", QgsMessageBar.WARNING)
                runMinPatchBool = False
        else:
            qgis.utils.iface.messageBar().pushMessage("Incorrect pathname", "The specified pathname for the MinPatch details file is invalid. Please choose another one", QgsMessageBar.WARNING)
            runMinPatchBool = False

        blmText = self.blmLineEdit.text()
        try:
            blmNumber = float(blmText)
            if blmNumber >= 0:
                minpatchObject.blm = blmNumber
            else:
                qgis.utils.iface.messageBar().pushMessage("Incorrect BLM format", "The BLM value must be a non-negative number.", QgsMessageBar.WARNING)
                runMinPatchBool = False
        except:
            qgis.utils.iface.messageBar().pushMessage("Incorrect BLM format", "The BLM value must be a non-negative number.", QgsMessageBar.WARNING)
            runMinPatchBool = False

        selectedItemsList = self.fileListWidget.selectedItems()
        if len(selectedItemsList) > 0:
            selectedMarxanFileText = [item.text() for item in self.fileListWidget.selectedItems()][0]

            suffixText = selectedMarxanFileText.split(" - ")[-1]
            numberText = suffixText.split(" ")[0]
            runNumberLen = len(numberText) + 9 #Calcs length of text to remove from end of string
            minpatchObject.marxanFileName = selectedMarxanFileText[0: -runNumberLen]
        else:
            qgis.utils.iface.messageBar().pushMessage("No files selected", "Please select one of the sets of files before proceeding.", QgsMessageBar.WARNING)
            runMinPatchBool = False

        minpatchObject.removeBool = self.removeCheckBox.isChecked()
        minpatchObject.addBool = self.addCheckBox.isChecked()
        minpatchObject.whittleBool = self.whittleCheckBox.isChecked()

        if runMinPatchBool:
            minpatchDataDict, setupOKBool = cluz_mpsetup.makeMinpatchDataDict(setupObject, minpatchObject)
            self.close()
            if setupOKBool:
                cluz_mpmain.runMinPatch(setupObject, minpatchObject, minpatchDataDict)


class patchesDialog(QDialog, Ui_patchesDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        QObject.connect(self.browseButton, SIGNAL("clicked()"), self.setPortfolioFilePath)
        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.makePatchShapefile(setupObject))

    def setPortfolioFilePath(self):
        portfolioPathNameText = QFileDialog.getOpenFileName(self, 'Select Marxan or MinPatch portfolio file', '*.txt')
        if portfolioPathNameText != "":
            self.filePathlineEdit.setText(portfolioPathNameText)

    def makePatchShapefile(self, setupObject):
        portfolioPathNameText = self.filePathlineEdit.text()
        portfolioOKBool, portfolioDict = cluz_functions2.makePatchPortfolioDict(portfolioPathNameText)
        if portfolioOKBool:
            cluz_functions2.makePatchPortfolioShapefile(setupObject, portfolioDict)
        else:
            cluz_functions2.portfolioNotOKErrorMessage()


class portfolioDialog(QDialog, Ui_portfolioDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        sfFieldList = cluz_functions2.makeSFFieldList(setupObject)
        self.sfComboBox.addItems(sfFieldList)
        self.sfComboBox.setEnabled(False)
        self.sfFieldLabel.setEnabled(False)
        self.sfRunsLabel.setVisible(False)
        self.sfRunsLineEdit.setVisible(False)
        self.equalityCheckBox.setVisible(False)

        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.runReturnPortfolioDetails(setupObject))


    def runReturnPortfolioDetails(self, setupObject):
        portfolioPUDetailsDict = cluz_functions2.makePortfolioPUDetailsDict()
        sfRunsValueIsOKBool = sfRunsValueIsOK(self)
        if sfRunsValueIsOKBool:
            if self.puDetailsCheckBox.isChecked():
                portfolioPUDetailsDict = cluz_functions2.addStatusDetailsToPortfolioDict(setupObject, portfolioPUDetailsDict)
            if self.spatialCheckBox.isChecked():
                portfolioPUDetailsDict = cluz_functions2.addSpatialDetailsToPortfolioDict(setupObject, portfolioPUDetailsDict)
            if self.patchTargetCheckBox.isChecked():
                portfolioPUDetailsDict = cluz_functions2.addPatchFeatDetailsToPortfolioDict(setupObject, portfolioPUDetailsDict)
            if self.sfCheckBox.isChecked():
                sfFieldName = self.sfComboBox.currentText()
                sfRunsValue = int(self.sfRunsLineEdit.text())
                sfValueList = cluz_functions2.makeFullSFValueList(setupObject, sfFieldName)
                if sfRunsValueNotLowerThanMaxSFValue(sfValueList, sfRunsValue):
                    portfolioPUDetailsDict = cluz_functions2.addSFDetailsToPortfolioDict(portfolioPUDetailsDict, sfValueList, sfRunsValue)
                else:
                    sfRunsValueIsOKBool = False


        if sfRunsValueIsOKBool:
            self.close()

            if len(portfolioPUDetailsDict) > 0:
                self.portfolioResultsDialog = portfolioResultsDialog(self, portfolioPUDetailsDict, setupObject)
                # show the dialog
                self.portfolioResultsDialog.show()
                # Run the dialog event loop
                result = self.portfolioResultsDialog.exec_()


def sfRunsValueIsOK(self):
    sfRunsValueIsOK = True
    if self.sfCheckBox.isChecked():
        try:
            sfRunsValue = int(self.sfRunsLineEdit.text())
            if sfRunsValue < 1:
                qgis.utils.iface.messageBar().pushMessage("Value error", "The number of runs value must be an integer greater than 0.", QgsMessageBar.WARNING)
                sfRunsValueIsOK = False
        except ValueError:
            qgis.utils.iface.messageBar().pushMessage("Value error", "The number of runs value must be an integer greater than 0.", QgsMessageBar.WARNING)
            sfRunsValueIsOK = False

    return sfRunsValueIsOK


def sfRunsValueNotLowerThanMaxSFValue(sfValueList, sfRunsValue):
    sfRunsValueNotLowerThanMaxSFValue = True

    if max(sfValueList) > sfRunsValue:
        qgis.utils.iface.messageBar().pushMessage("Value error", "The specified number of runs value is less than the highest selection frequency value in the specified selection frequency field. Please check the number of runs used in the analysis and update this figure.", QgsMessageBar.WARNING)
        sfRunsValueNotLowerThanMaxSFValue = False

    return sfRunsValueNotLowerThanMaxSFValue


class portfolioResultsDialog(QDialog, Ui_portfolioResultsDialog):
    def __init__(self, iface, portfolioPUDetailsDict, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        self.removeSuperfluousTabs(portfolioPUDetailsDict)
        if portfolioPUDetailsDict["statusDetailsBool"]:
            statusDataDict = portfolioPUDetailsDict["statusDataDict"]
            self.makeStatusTab(setupObject, statusDataDict)
        if portfolioPUDetailsDict["spatialDetailsBool"]:
            spatialDataDict = portfolioPUDetailsDict["spatialDataDict"]
            self.makeSpatialTab(setupObject, spatialDataDict)
        if portfolioPUDetailsDict["sfDetailsBool"]:
            sfDataDict = portfolioPUDetailsDict["sfDataDict"]
            self.makeSfTab(sfDataDict)
        if portfolioPUDetailsDict["patchFeatDetailsBool"]:
            patchFeatDataDict = portfolioPUDetailsDict["patchFeatDataDict"]
            self.makePatchFeatTab(setupObject, patchFeatDataDict)
        if portfolioPUDetailsDict["peDetailsBool"]:
            peDataDict = portfolioPUDetailsDict["peDataDict"]
            self.makePETab(peDataDict)

    def makeStatusTab(self, setupObject, statusDataDict):
        self.statusTabTableWidget.clear()
        self.statusTabTableWidget.setColumnCount(4)
        rowNumber = 0
        statusTypeList = ['Available', 'Conserved', 'Earmarked', 'Excluded', 'Portfolio', 'Region']
        for statusType in statusTypeList:
            self.statusTabTableWidget.insertRow(rowNumber)
            statusTableItem = QTableWidgetItem(statusType)
            costString, areaString, countString = cluz_functions2.returnStatusTabStringValues(setupObject, statusDataDict, statusType)
            costTableItem = QTableWidgetItem(costString)
            areaTableItem = QTableWidgetItem(areaString)
            countTableItem = QTableWidgetItem(countString)
            self.statusTabTableWidget.setItem(rowNumber, 0, statusTableItem)
            self.statusTabTableWidget.setItem(rowNumber, 1, costTableItem)
            self.statusTabTableWidget.setItem(rowNumber, 2, areaTableItem)
            self.statusTabTableWidget.setItem(rowNumber, 3, countTableItem)
            rowNumber += 1

        statusHeaderList = ['Status', 'Total cost', 'Total area', 'No. of planning units']
        self.statusTabTableWidget.setHorizontalHeaderLabels(statusHeaderList)
        for aColValue in range(len(statusHeaderList)):
            self.statusTabTableWidget.resizeColumnToContents(aColValue)

    def makeSpatialTab(self, setupObject, spatialDataDict):
        self.spatialTabTableWidget.clear()
        self.spatialTabTableWidget.setColumnCount(2)
        rowNumber = 0
        spatialTableItemDict = cluz_functions2.makeSpatialTableItemDict(setupObject, spatialDataDict)
        for spatialRowOrder in range(0, 5):
            self.spatialTabTableWidget.insertRow(rowNumber)
            descTableItem = QTableWidgetItem(spatialTableItemDict[spatialRowOrder][0])
            valueTableItem = QTableWidgetItem(spatialTableItemDict[spatialRowOrder][1])
            self.spatialTabTableWidget.setItem(rowNumber, 0, descTableItem)
            self.spatialTabTableWidget.setItem(rowNumber, 1, valueTableItem)
            rowNumber += 1

        spatialHeaderList = ['Metric', 'Value']
        self.spatialTabTableWidget.setHorizontalHeaderLabels(spatialHeaderList)
        for aColValue in range(len(spatialHeaderList)):
            self.spatialTabTableWidget.resizeColumnToContents(aColValue)


    def makeSfTab(self, sfDataDict):
        self.sfTabTableWidget.clear()
        self.sfTabTableWidget.setColumnCount(2)
        rowNumber = 0
        sfDictKeyList = range(0, len(sfDataDict))
        for sfDictKey in sfDictKeyList:
            self.sfTabTableWidget.insertRow(rowNumber)
            descTableItem = QTableWidgetItem(sfDataDict[sfDictKey][0])
            valueTableItem = QTableWidgetItem(sfDataDict[sfDictKey][1])
            self.sfTabTableWidget.setItem(rowNumber, 0, descTableItem)
            self.sfTabTableWidget.setItem(rowNumber, 1, valueTableItem)
            rowNumber += 1

        sfHeaderList = ['Selection frequency value range', 'Number of planning units']
        self.sfTabTableWidget.setHorizontalHeaderLabels(sfHeaderList)
        for aColValue in range(len(sfHeaderList)):
            self.sfTabTableWidget.resizeColumnToContents(aColValue)


    def makePatchFeatTab(self, setupObject, patchFeatDataDict):
        self.patchFeatTabTableWidget.clear()
        self.patchFeatTabTableWidget.setColumnCount(3)
        rowNumber = 0
        featIDList = setupObject.targetDict.keys()
        featIDList.sort()
        for featID in featIDList:
            self.patchFeatTabTableWidget.insertRow(rowNumber)
            featIDTableItem = QTableWidgetItem(str(featID))
            featNameTableItem = QTableWidgetItem(setupObject.targetDict[featID][0])
            try:
                countTableItem = QTableWidgetItem(str(patchFeatDataDict[featID]))
            except KeyError:
                countTableItem = QTableWidgetItem(str(0))
            self.patchFeatTabTableWidget.setItem(rowNumber, 0, featIDTableItem)
            self.patchFeatTabTableWidget.setItem(rowNumber, 1, featNameTableItem)
            self.patchFeatTabTableWidget.setItem(rowNumber, 2, countTableItem)
            rowNumber += 1

        sfHeaderList = ['Feature ID', 'Feature name', "Number of patches"]
        self.patchFeatTabTableWidget.setHorizontalHeaderLabels(sfHeaderList)
        for aColValue in range(len(sfHeaderList)):
            self.patchFeatTabTableWidget.resizeColumnToContents(aColValue)


    def makePETab(self, sfDataDict):
        self.peTabTableWidget.clear()
        # self.sfTabTableWidget.setColumnCount(2)
        # rowNumber = 0
        # sfDictKeyList = range(0, len(sfDataDict))
        # for sfDictKey in sfDictKeyList:
        #     self.sfTabTableWidget.insertRow(rowNumber)
        #     descTableItem = QTableWidgetItem(sfDataDict[sfDictKey][0])
        #     valueTableItem = QTableWidgetItem(sfDataDict[sfDictKey][1])
        #     self.sfTabTableWidget.setItem(rowNumber, 0, descTableItem)
        #     self.sfTabTableWidget.setItem(rowNumber, 1, valueTableItem)
        #     rowNumber += 1
        #
        # sfHeaderList = ['Selection frequency value range', 'Number of planning units']
        # self.sfTabTableWidget.setHorizontalHeaderLabels(sfHeaderList)
        # for aColValue in range(len(sfHeaderList)):
        #     self.sfTabTableWidget.resizeColumnToContents(aColValue)



    def removeSuperfluousTabs(self, portfolioPUDetailsDict):
        tabNameRemoveList = list()
        if not portfolioPUDetailsDict["statusDetailsBool"]:
            tabNameRemoveList.append('Status results')
        if not portfolioPUDetailsDict["spatialDetailsBool"]:
            tabNameRemoveList.append('Spatial results')
        if not portfolioPUDetailsDict["sfDetailsBool"]:
            tabNameRemoveList.append('Selection frequency results')
        if not portfolioPUDetailsDict["patchFeatDetailsBool"]:
            tabNameRemoveList.append('Patches per feature')
        if not portfolioPUDetailsDict["peDetailsBool"]:
            tabNameRemoveList.append('Protection equality')

        for aIter in range(0, len(tabNameRemoveList)):
            for tabIndex in range(0, self.tabWidget.count()):
                tabName = self.tabWidget.tabText(tabIndex)
                if tabName in tabNameRemoveList:
                    self.tabWidget.removeTab(tabIndex)
                    tabNameRemoveList.remove(tabName)


    # http://stackoverflow.com/questions/24971305/copy-pyqt-table-selection-including-column-and-row-headers
    def keyPressEvent(self, e):
        if (e.modifiers() & Qt.ControlModifier):
            tabName = self.tabWidget.tabText(self.tabWidget.currentIndex())
            if tabName == 'Status results':
                selected = self.statusTabTableWidget.selectedRanges()
            elif tabName == 'Spatial results':
                selected = self.spatialTabTableWidget.selectedRanges()
            elif tabName == 'Selection frequency results':
                selected = self.sfTabTableWidget.selectedRanges()
            elif tabName == 'Patches per feature':
                selected = self.patchFeatTabTableWidget.selectedRanges()

            if e.key() == Qt.Key_C: #copy
                s = ""
                for r in xrange(selected[0].topRow(), selected[0].bottomRow() + 1):
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            if tabName == 'Status results':
                                s += str(self.statusTabTableWidget.item(r, c).text()) + "\t"
                            elif tabName == 'Spatial results':
                                s += str(self.spatialTabTableWidget.item(r, c).text()) + "\t"
                            elif tabName == 'Selection frequency results':
                                s += str(self.sfTabTableWidget.item(r, c).text()) + "\t"
                            elif tabName == 'Patches per feature':
                                s += str(self.patchFeatTabTableWidget.item(r, c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)
