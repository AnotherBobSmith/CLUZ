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

# def removeUndoField(setupObject):
#     puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
#     provider = puLayer.dataProvider()
#     undoFieldOrder = provider.fieldNameIndex("CLUZ_undo")
#     if undoFieldOrder <> -1:
#         provider.deleteAttributes([undoFieldOrder])
#         puLayer.updateFields()
#         puLayer.commitChanges()

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

        statusType = "Earmarked" # This works out the changes needed to update the Best PUs to Earmarked
        changeAbundDict = calcChangeAbundDict(setupObject, selectedPUIDStatusDict, statusType)
        updateTargetDictWithChanges(setupObject, changeAbundDict)
        cluz_setup.updateTargetCSVFromTargetDict(setupObject, setupObject.targetDict)
        qgis.utils.iface.messageBar().pushMessage("Process completed", "Planning units that were selected in the Best portfolio now have Earmarked status.", QgsMessageBar.INFO)

        puLayer.triggerRepaint()
        canvas.refresh()
