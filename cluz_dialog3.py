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
import qgis

import os
import csv

import cluz_setup
import cluz_functions1
import cluz_functions3

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")

from cluz_form_target import Ui_targetDialog
from cluz_form_abund_select import Ui_abundSelectDialog
from cluz_form_abund import Ui_abundDialog
from cluz_form_change import Ui_ChangeStatusDialog
from cluz_form_identify import Ui_identifyDialog
from cluz_form_met import Ui_metDialog

class targetDialog(QDialog, Ui_targetDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        targetDict = cluz_setup.makeTargetDict(setupObject)
        if targetDict != "blank":
            setupObject.targetDict = targetDict
            self.loadTargetDictData(setupObject)

    def loadTargetDictData(self, setupObject):
        decPrec = setupObject.decimalPlaces
        targetCSVFilePath = setupObject.targetPath
        decPrecHeaderNameList = ["target", "spf", "conserved", "total"] # List of columns that will be changed to decimal precision
        pcValueUpdate = False
        with open(targetCSVFilePath, 'rb') as f:
            targetReader = csv.reader(f)
            targetHeaderList = targetReader.next()

            lowerHeaderList = []
            for aHeader in targetHeaderList:
                lowerHeaderList.append(aHeader.lower())

            self.targetTableWidget.clear()
            self.targetTableWidget.setColumnCount(len(targetHeaderList))
            insertRowNumber = 0
            for aRow in targetReader:
                pcValue = aRow[lowerHeaderList.index("pc_target")]
                targetValue = float(aRow[lowerHeaderList.index("target")])
                consValue = float(aRow[lowerHeaderList.index("conserved")])

                if targetValue <= 0:
                    limboPCValue = "-1"
                else:
                    limboPCValue = consValue / targetValue
                    limboPCValue *= 100
                    limboPCValue = cluz_setup.returnRoundedValue(setupObject, limboPCValue)

                if float(limboPCValue) != float(pcValue):
                    pcValueUpdate = True
                aRow[lowerHeaderList.index("pc_target")] = limboPCValue

                addTargetTableRow(self, aRow, targetHeaderList, decPrecHeaderNameList, insertRowNumber, decPrec)
                insertRowNumber += 1

            self.targetTableWidget.setHorizontalHeaderLabels(targetHeaderList)

        for aColValue in range(len(targetHeaderList)):
            self.targetTableWidget.resizeColumnToContents(aColValue)

        if pcValueUpdate == True:
            cluz_setup.updateTargetCSVFromTargetDict(setupObject, setupObject.targetDict)


    # http://stackoverflow.com/questions/24971305/copy-pyqt-table-selection-including-column-and-row-headers
    def keyPressEvent(self, e):
        if (e.modifiers() & Qt.ControlModifier):
            selected = self.targetTableWidget.selectedRanges()

            if e.key() == Qt.Key_C: #copy
                s = ""

                for r in xrange(selected[0].topRow(), selected[0].bottomRow() + 1):
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.targetTableWidget.item(r, c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)


def addTargetTableRow(self, aRow, targetHeaderList, decPrecHeaderNameList, insertRowNumber, decPrec):
    self.targetTableWidget.insertRow(insertRowNumber)
    for aColValue in range(len(targetHeaderList)):
        headerName = targetHeaderList[aColValue].lower()
        tableValue = aRow[aColValue]
        if headerName in decPrecHeaderNameList:
            tableValue = round(float(tableValue), decPrec)
            tableValue = format(tableValue, "." + str(decPrec) + "f")
        targTableItem = QTableWidgetItem(str(tableValue))
        if headerName == "target":
            targetValue = tableValue
        elif headerName == "conserved":
            conservedValue = tableValue
        if headerName == "pc_target" and str(tableValue) == "-1":
            targTableItem.setTextColor(QColor.fromRgb(128, 128, 128))
        elif headerName == "pc_target" and float(tableValue) >= 0:
            if float(conservedValue) < float(targetValue):
                targTableItem.setTextColor(QColor.fromRgb(255, 0, 0))
            else:
                targTableItem.setTextColor(QColor.fromRgb(0, 102, 51))
        self.targetTableWidget.setItem(insertRowNumber, aColValue, targTableItem)

class abundSelectDialog(QDialog, Ui_abundSelectDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        featStringDict = self.loadAbundSelectFeatureList(setupObject)

        QObject.connect(self.okButton, SIGNAL("clicked()"), lambda: self.displayAbundValues(setupObject, featStringDict))

    def loadAbundSelectFeatureList(self, setupObject):
        featIDList = setupObject.targetDict.keys()
        featIDList.sort()
        featStringList = []
        featStringDict = {}
        for aFeat in featIDList:
            aString = str(aFeat) + " - " + setupObject.targetDict[aFeat][0]
            featStringList.append(aString)
            featStringDict[aString] = aFeat
        self.featListWidget.addItems(featStringList)

        return featStringDict

    def displayAbundValues(self, setupObject, featStringDict):
        selectedFeatIDList = [featStringDict[item.text()] for item in self.featListWidget.selectedItems()]
        if len(selectedFeatIDList) == 0:
            selectedFeatIDList = setupObject.targetDict.keys()
        self.close()

        self.abundDialog = abundDialog(self, setupObject, selectedFeatIDList)
        # show the dialog
        self.abundDialog.show()
        # Run the dialog event loop
        result = self.abundDialog.exec_()

class abundDialog(QDialog, Ui_abundDialog):
    def __init__(self, iface, setupObject, selectedFeatIDList):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        self.loadAbundDictData(setupObject, selectedFeatIDList)

    def loadAbundDictData(self, setupObject, selectedFeatIDList):
        decPrec = setupObject.decimalPlaces
        abundPUKeyDict = setupObject.abundPUKeyDict
        featSet = set(selectedFeatIDList)
        abundHeaderList = ["PU_ID"]
        for aFeatID in featSet:
            abundHeaderList.append("F_" + str(aFeatID))
        self.abundTableWidget.clear()
        self.abundTableWidget.setColumnCount(len(abundHeaderList))

        insertRowNumber = 0
        for puID in abundPUKeyDict:
            self.abundTableWidget.insertRow(insertRowNumber)
            zeroValue = round(0.0, decPrec)
            zeroValue = format(zeroValue, "." + str(decPrec) + "f")
            blankString = str(zeroValue)
            puStringList = [blankString] * len(featSet)
            puAbundDict = abundPUKeyDict[puID]
            for featID in puAbundDict:
                if featID in featSet:
                    featAmount = puAbundDict[featID]
                    featAmount = round(float(featAmount), decPrec)
                    featAmount = format(featAmount, "." + str(decPrec) + "f")
                    featIndex = list(featSet).index(featID)
                    puStringList[featIndex] = str(featAmount)
            puStringList.insert(0, str(puID))

            for aColValue in range(len(puStringList)):
                featValue = puStringList[aColValue]
                abundTableItem = QTableWidgetItem(str(featValue))
                self.abundTableWidget.setItem(insertRowNumber, aColValue, abundTableItem)
            insertRowNumber += 1

        self.abundTableWidget.setHorizontalHeaderLabels(abundHeaderList)

        for aColValue in range(len(abundHeaderList)):
            self.abundTableWidget.resizeColumnToContents(aColValue)


    # http://stackoverflow.com/questions/24971305/copy-pyqt-table-selection-including-column-and-row-headers
    def keyPressEvent(self, e):
        if (e.modifiers() & Qt.ControlModifier):
            selected = self.abundTableWidget.selectedRanges()

            if e.key() == Qt.Key_C: #copy
                s = ""
                for r in xrange(selected[0].topRow(), selected[0].bottomRow() + 1):
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.abundTableWidget.item(r, c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)


class changeStatusDialog(QDialog, Ui_ChangeStatusDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.iface = iface
        self.setupUi(self)

        (targetsMetCount, targetCount) = cluz_functions3.returnTargetsMetTuple(setupObject)
        self.targetsMetLabel.setText("Targets met: " + str(targetsMetCount) + " of " + str(targetCount))

        self.undoButton.setEnabled(False)

        QObject.connect(self.changeButton, SIGNAL("clicked()"), lambda: self.changeStatus(setupObject))
        QObject.connect(self.undoButton, SIGNAL("clicked()"), lambda: self.undoStatusChange(setupObject))
        QObject.connect(self.closeButton, SIGNAL("clicked()"), lambda: self.closeStatusDialog(setupObject))

    def changeStatus(self, setupObject):
        if self.availableButton.isChecked():
            statusType = "Available"
        elif self.earmarkedButton.isChecked():
            statusType = "Earmarked"
        elif self.conservedButton.isChecked():
            statusType = "Conserved"
        elif self.excludedButton.isChecked():
            statusType = "Excluded"

        changeLockedPUsBool = self.changeCheckBox.isChecked()

        selectedPUIDStatusDict = cluz_functions3.changeStatusPuLayer(setupObject, statusType, changeLockedPUsBool)
        changeAbundDict = cluz_functions3.calcChangeAbundDict(setupObject, selectedPUIDStatusDict, statusType)
        targetDict = cluz_functions3.updateTargetDictWithChanges(setupObject, changeAbundDict)
        setupObject.targetDict = targetDict
        cluz_setup.updateTargetCSVFromTargetDict(setupObject, targetDict)
        (targetsMetCount, targetCount) = cluz_functions3.returnTargetsMetTuple(setupObject)
        self.targetsMetLabel.setText("Targets met: " + str(targetsMetCount) + " of " + str(targetCount))

        setupObject.selectedPUIDStatusDict = selectedPUIDStatusDict
        self.undoButton.setEnabled(True)

    def undoStatusChange(self, setupObject):
        canvas = qgis.utils.iface.mapCanvas()
        cluz_functions3.undoStatusChangeInPuLayer(setupObject)
        newConTotDict = cluz_functions1.returnConTotDict(setupObject)
        targetDict = cluz_functions1.updateConTotFieldsTargetDict(setupObject, newConTotDict)
        cluz_setup.updateTargetCSVFromTargetDict(setupObject, targetDict)
        setupObject.targetDict = targetDict

        (targetsMetCount, targetCount) = cluz_functions3.returnTargetsMetTuple(setupObject)
        self.targetsMetLabel.setText("Targets met: " + str(targetsMetCount) + " of " + str(targetCount))

        setupObject.selectedPUIDStatusDict = "blank"
        self.undoButton.setEnabled(False)
        canvas.refresh()

    def closeStatusDialog(self, setupObject):
        self.close()

class identifyDialog(QDialog, Ui_identifyDialog):
    def __init__(self, iface, setupObject, point):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        selectedPUIDList = cluz_functions3.returnPointPUIDList(setupObject, point)
        identDict, targetMetDict = cluz_functions3.makeIdentifyData(setupObject, selectedPUIDList)
        titleString = cluz_functions3.setIdentifyDialogWindowTitle(selectedPUIDList, identDict)

        if len(identDict.keys()) > 0:
            self.identDict = identDict
            self.targetMetDict = targetMetDict
            self.showIdentifyData()
            self.setWindowTitle(titleString)

        self.setWindowTitle(titleString)

    def showIdentifyData(self):
        self.identifyTableWidget.clear()
        self.identifyTableWidget.setColumnCount(7)
        cluz_functions3.addIdenitfyDataToTableWidget(self.identifyTableWidget, self.targetMetDict, self.identDict)

        headerList = ["ID ", "Name ", "Amount ", "As % of total ", "Target ", "As % of target ", "% of target currently met "]
        self.identifyTableWidget.setHorizontalHeaderLabels(headerList)
        for aColValue in range(len(headerList)):
            self.identifyTableWidget.resizeColumnToContents(aColValue)


class metDialog(QDialog, Ui_metDialog):
    def __init__(self, iface, setupObject):
        QDialog.__init__(self)
        outputPath = setupObject.outputPath
        outputName = setupObject.outputName + "_mvbest.txt"
        self.metTargetFile = outputPath + os.sep + outputName
        self.iface = iface
        self.setupUi(self)
        self.metLoadTargetDictData()

        self.setWindowTitle("Marxan Targets Met table for analysis " + setupObject.outputName)


    def metLoadTargetDictData(self):
        targetMetDict = {}

        with open(self.metTargetFile, 'rb') as f:
            targetMetReader = csv.reader(f)
            targetMetHeaderList = next(targetMetReader, None)
            for row in targetMetReader:
                puID = int(row.pop(0))
                targetMetDict[puID] = row

        targetIDList = targetMetDict.keys()
        targetIDList.sort()

        self.metTableWidget.clear()
        self.metTableWidget.setColumnCount(len(targetMetHeaderList))

        insertRowNumber = 0
        for aFeat in targetIDList:
            self.metTableWidget.insertRow(insertRowNumber)
            aRowList = targetMetDict[aFeat]
            aRowList.insert(0, aFeat)
            for aColValue in range(len(targetMetHeaderList)):
                featValue = aRowList[aColValue]
                metTableItem = QTableWidgetItem(str(featValue))
                self.metTableWidget.setItem(insertRowNumber,aColValue,metTableItem)

            insertRowNumber += 1

            self.metTableWidget.setHorizontalHeaderLabels(targetMetHeaderList)

        for aColValue in range(len(targetMetHeaderList)):
            self.metTableWidget.resizeColumnToContents(aColValue)
