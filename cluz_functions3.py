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

from PyQt4.QtGui import *

import qgis
from qgis.core import *
from qgis.gui import *
import cluz_setup

def returnTargetsMetTuple(setupObject):
    numTargets = 0
    numTargetsMet = 0
    targetDict = setupObject.targetDict
    for aFeat in targetDict:
        targetList = targetDict[aFeat]
        targetAmount = targetList[3]
        conAmount = targetList[4]
        if targetAmount > 0:
            numTargets += 1
            if conAmount >= targetAmount:
                numTargetsMet += 1

    return (numTargetsMet, numTargets)

def changeStatusPuLayer(setupObject, changeStatusType, changeLockedPUsBool):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    qgis.utils.iface.setActiveLayer(puLayer)
    puLayer = qgis.utils.iface.activeLayer()
    provider = puLayer.dataProvider()
    idFieldOrder = provider.fieldNameIndex("Unit_ID")
    statusFieldOrder = provider.fieldNameIndex("Status")

    selectedPUs = puLayer.selectedFeatures()
    puLayer.startEditing()

    selectedPUIDStatusDict = {}
    for aPU in selectedPUs:
        puRow = aPU.id()
        puID = aPU.attributes()[idFieldOrder]
        puStatus = aPU.attributes()[statusFieldOrder]
        if changeLockedPUsBool == True:
            selectedPUIDStatusDict[puID] = puStatus
            puLayer.changeAttributeValue(puRow, statusFieldOrder, changeStatusType)
        else:
            if puStatus == "Available" or puStatus == "Earmarked":
                if puStatus <> changeStatusType:
                    selectedPUIDStatusDict[puID] = str(puStatus)
                    puLayer.changeAttributeValue(puRow, statusFieldOrder, changeStatusType)

    puLayer.commitChanges()
    puLayer.setSelectedFeatures([])

    return selectedPUIDStatusDict

def calcChangeAbundDict(setupObject, selectedPUIDStatusDict, statusType):
    statusBoolDict = {"Available": False, "Conserved": True, "Earmarked": True, "Excluded": "False"}
    changeStatusBoolType = statusBoolDict[statusType]

    changeAbundDict = {}
    for puID in selectedPUIDStatusDict:
        puStatus = selectedPUIDStatusDict[puID]
        currentStatusBoolType = statusBoolDict[puStatus]

        if currentStatusBoolType == False and changeStatusBoolType == True:
            try:
                puAbundDict = setupObject.abundPUKeyDict[puID]
                for featID in puAbundDict:
                    abundValue = puAbundDict[featID]
                    try:
                        runningChange = changeAbundDict[featID]
                    except KeyError:
                        runningChange = 0
                    runningChange += abundValue
                    changeAbundDict[featID] = runningChange
            except KeyError:
                pass

        if currentStatusBoolType == True and changeStatusBoolType == False:
            try:
                puAbundDict = setupObject.abundPUKeyDict[puID]
                for featID in puAbundDict:
                    abundValue = puAbundDict[featID]
                    try:
                        runningChange = changeAbundDict[featID]
                    except KeyError:
                        runningChange = 0
                    runningChange -= abundValue
                    changeAbundDict[featID] = runningChange
            except KeyError:
                pass

    return changeAbundDict

def updateTargetDictWithChanges(setupObject, changeAbundDict):
    targetDict = setupObject.targetDict
    for theFeatID in changeAbundDict:
        changeAmount = changeAbundDict[theFeatID]
        targetList = setupObject.targetDict[theFeatID]
        conAmount = targetList[4]
        newAmount = conAmount + changeAmount
        targetList[4] = newAmount
        targetDict[theFeatID] = targetList

    return targetDict

####################################################################http://www.opengis.ch/2015/04/29/performance-for-mass-updating-features-on-layers/
def undoStatusChangeInPuLayer(setupObject):
    canvas = qgis.utils.iface.mapCanvas()
    selectedPUIDStatusDict = setupObject.selectedPUIDStatusDict
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    provider = puLayer.dataProvider()
    puIDFieldOrder = provider.fieldNameIndex("Unit_ID")
    statusFieldOrder = provider.fieldNameIndex("Status")

    puLayer.startEditing()
    if statusFieldOrder <> -1:
        puFeatures = puLayer.getFeatures()
        for puFeature in puFeatures:
            puRow = puFeature.id()
            puAttributes = puFeature.attributes()
            puID = puAttributes[puIDFieldOrder]
            try:
                backupPuStatus = selectedPUIDStatusDict[puID]
                if backupPuStatus == "Available" or backupPuStatus == "Earmarked" or backupPuStatus == "Conserved" or backupPuStatus == "Excluded":
                    puLayer.changeAttributeValue(puRow, statusFieldOrder, backupPuStatus)
            except KeyError:
                pass

    puLayer.commitChanges()
    canvas.refresh()


####################################################################http://www.opengis.ch/2015/04/29/performance-for-mass-updating-features-on-layers/
def changeBestToEarmarkedPUs(setupObject):
    canvas = qgis.utils.iface.mapCanvas()
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puProvider = puLayer.dataProvider()
    idFieldOrder = puProvider.fieldNameIndex("Unit_ID")
    statusFieldOrder = puProvider.fieldNameIndex("Status")
    bestFieldOrder = puProvider.fieldNameIndex("Best")
    changeBool = True

    if bestFieldOrder == -1:
        QMessageBox.warning(None, "Incorrect format", "The planning unit layer has no field named Best (which is produced by running Marxan). This process will terminate.")
        changeBool = False

    if changeBool == True:
        selectedPUIDStatusDict = {}
        puLayer.startEditing()
        puFeatures = puLayer.getFeatures()
        for puFeature in puFeatures:
            puRow = puFeature.id()
            puID = puFeature.attributes()[idFieldOrder]
            puStatus = puFeature.attributes()[statusFieldOrder]
            bestStatus = puFeature.attributes()[bestFieldOrder]
            if bestStatus == "Selected":
                puLayer.changeAttributeValue(puRow, statusFieldOrder, "Earmarked")
                selectedPUIDStatusDict[puID] = puStatus
        puLayer.commitChanges()
        puLayer.triggerRepaint()
        canvas.refresh()

        statusType = "Earmarked" # This works out the changes needed to update the Best PUs to Earmarked
        changeAbundDict = calcChangeAbundDict(setupObject, selectedPUIDStatusDict, statusType)
        updateTargetDictWithChanges(setupObject, changeAbundDict)
        cluz_setup.updateTargetCSVFromTargetDict(setupObject, setupObject.targetDict)
        qgis.utils.iface.messageBar().pushMessage("Process completed", "Planning units that were selected in the Best portfolio now have Earmarked status.", QgsMessageBar.INFO)


def makeIdentDict(targetDict, targetMetDict, puAbundDict):
    identDict = {}
    for featID in puAbundDict:
        featAmount = puAbundDict[featID]
        featName = targetDict[featID][0]
        featTarget = targetDict[featID][3]
        conTotal = targetDict[featID][4]
        featTotal = targetDict[featID][5]
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

            propTargetMet = targetDict[featID][4] / featTarget
            pcTargetMet = propTargetMet * 100
            pcTargetMetString = str(round(pcTargetMet, 2)) + " %"
        else:
            pcOfTargetString = "No target"
            pcTargetMetString = "No target"
            targetMetDict[featID] = "No target"

        identDict[featID] = [str(featID), featName, str(featAmount), pcOfTotalString, str(featTarget), pcOfTargetString, pcTargetMetString]

    return identDict


def addIdenitfyDataToTableWidget(identifyTableWidget, targetMetDict, identDict):
    featIDList = identDict.keys()
    featIDList.sort()
    for aRow in range(0, len(featIDList)):
        identifyTableWidget.insertRow(aRow)
        aID = featIDList[aRow]
        featIdentifyList = identDict[aID]
        for aCol in range(0, len(featIdentifyList)):
            featValue = featIdentifyList[aCol]
            featIDItem = QTableWidgetItem(featValue)
            if aCol == 6:
                targetMetStatus = targetMetDict[aID]
                if targetMetStatus == "Met":
                    featIDItem.setTextColor(QColor.fromRgb(0, 102, 51))
                elif targetMetStatus == "Not met":
                    featIDItem.setTextColor(QColor.fromRgb(255, 0, 0))
                else:
                    featIDItem.setTextColor(QColor.fromRgb(128, 128, 128))
            identifyTableWidget.setItem(aRow, aCol, featIDItem)
