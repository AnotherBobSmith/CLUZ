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
        setupObject.targetDict = cluz_setup.makeTargetDict(setupObject)
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
                    limboPCValue = round(float(limboPCValue), decPrec)
                    limboPCValue = format(limboPCValue, "." + str(decPrec) + "f")

                if float(limboPCValue) != float(pcValue):
                    pcValueUpdate = True
                aRow[lowerHeaderList.index("pc_target")] = limboPCValue

                self.targetTableWidget.insertRow(insertRowNumber)
                for aColValue in range(len(targetHeaderList)):
                    headerName = targetHeaderList[aColValue].lower()
                    featValue = aRow[aColValue]
                    if headerName in decPrecHeaderNameList:
                        featValue = round(float(featValue), decPrec)
                        featValue = format(featValue, "." + str(decPrec) + "f")
                    targTableItem = QTableWidgetItem(str(featValue))
                    if headerName == "pc_target" and str(featValue) == "-1":
                        targTableItem.setTextColor(QColor.fromRgb(128, 128, 128))
                    elif headerName == "pc_target" and float(featValue) >= 0:
                        if float(featValue) < 100:
                            targTableItem.setTextColor(QColor.fromRgb(255, 0, 0))
                        elif float(featValue) >= 100:
                            targTableItem.setTextColor(QColor.fromRgb(0, 102, 51))
                    self.targetTableWidget.setItem(insertRowNumber, aColValue, targTableItem)

                insertRowNumber += 1

            self.targetTableWidget.setHorizontalHeaderLabels(targetHeaderList)

        for aColValue in range(len(targetHeaderList)):
            self.targetTableWidget.resizeColumnToContents(aColValue)

        if pcValueUpdate == True:
            cluz_setup.updateTargetCSVFromTargetDict(setupObject, setupObject.targetDict)


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
        statusDict = {-2: "Available",-3: "Earmarked",-4: "Conserved",-5: "Excluded"}
        statusCode = self.statusButtonGroup.checkedId() #get the radio button that was selected
        statusType = statusDict[statusCode]

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
        self.targetDict = setupObject.targetDict
        self.abundPUKeyDict = setupObject.abundPUKeyDict
        self.puPath = setupObject.puPath
        self.iface = iface
        self.setupUi(self)
        self.point = point

        identDict, targetMetDict = self.makeIdentifyData()
        if len(identDict.keys()) > 0:
            self.identDict = identDict
            self.targetMetDict = targetMetDict
            self.showIdentifyData()

        # QObject.connect(self.copyButton, SIGNAL("clicked()"), lambda: self.copyIdentDictToClipboard(identDict))

    def makeIdentifyData(self):
        pntGeom = QgsGeometry.fromPoint(self.point)

        puLayer = QgsVectorLayer(self.puPath, "Planning units", "ogr")
        puProvider = puLayer.dataProvider()
        puIdFieldOrder = puProvider.fieldNameIndex("Unit_ID")

        selectList = []
        for feature in puLayer.getFeatures():
            if feature.geometry().intersects(pntGeom):
                selectList.append(feature.id())

        identDict = {}
        targetMetDict = {}
        if len(selectList) > 0:
            featID = selectList[0]
            puRequest = QgsFeatureRequest().setFilterFids([featID])
            for puFeature in puLayer.getFeatures(puRequest):
                puAttributes = puFeature.attributes()
                puID = puAttributes[puIdFieldOrder]
                puAbundDict = self.abundPUKeyDict[puID]
                for featID in puAbundDict:
                    featAmount = puAbundDict[featID]
                    featName = self.targetDict[featID][0]
                    featTarget = self.targetDict[featID][3]
                    conTotal = self.targetDict[featID][4]
                    featTotal = self.targetDict[featID][5]
                    propOfTotal = featAmount / featTotal
                    pcOfTotal = propOfTotal * 100
                    pcOfTotalString = str(round(pcOfTotal, 2)) + " %"
                    if featTarget > 0:
                        if conTotal < featTarget:
                            targetMetDict[featID] = "Not met"
                        else:
                            targetMetDict[featID] = "Met"

                        propOfTarget = featAmount / featTarget
                        pcOfTarget = propOfTarget * 100
                        pcOfTargetString = str(round(pcOfTarget, 2)) + " %"

                        propTargetMet = self.targetDict[featID][4] / featTarget
                        pcTargetMet = propTargetMet * 100
                        pcTargetMetString = str(round(pcTargetMet, 2)) + " %"
                    else:
                        pcOfTargetString = "No target"
                        pcTargetMetString = "No target"
                        targetMetDict[featID] = "No target"

                    identDict[featID] = [str(featID), featName, str(featAmount), pcOfTotalString, str(featTarget), pcOfTargetString, pcTargetMetString]

                titleString = "Planning unit " + str(puID) + ": list of features"
                self.setWindowTitle(titleString)

        return identDict, targetMetDict

    def showIdentifyData(self):
        self.identifyTableWidget.clear()
        self.identifyTableWidget.setColumnCount(7)

        featIDList = self.identDict.keys()
        featIDList.sort()
        for aRow in range(0, len(featIDList)):
            self.identifyTableWidget.insertRow(aRow)
            aID = featIDList[aRow]
            featIdentifyList = self.identDict[aID]
            for aCol in range(0, len(featIdentifyList)):
                featValue = featIdentifyList[aCol]
                featIDItem = QTableWidgetItem(featValue)
                if aCol == 6:
                    targetMetStatus = self.targetMetDict[aID]
                    if targetMetStatus == "Met":
                        featIDItem.setTextColor(QColor.fromRgb(0, 102, 51))
                    elif targetMetStatus == "Not met":
                        featIDItem.setTextColor(QColor.fromRgb(255, 0, 0))
                    else:
                        featIDItem.setTextColor(QColor.fromRgb(128, 128, 128))
                self.identifyTableWidget.setItem(aRow, aCol, featIDItem)

        headerList = ["ID ", "Name ", "Amount ", "As % of total ", "Target ", "As % of target ", "% of target currently met "]
        self.identifyTableWidget.setHorizontalHeaderLabels(headerList)
        for aColValue in range(len(headerList)):
            self.identifyTableWidget.resizeColumnToContents(aColValue)


    # def copyIdentDictToClipboard(self, identDict):
    #     r = Tkinter.Tk()
    #     r.withdraw()
    #     r.clipboard_clear()
    #     r.clipboard_append('i can has clipboardz?')
    #     r.destroy()

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
