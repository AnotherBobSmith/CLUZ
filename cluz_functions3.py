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
import cluz_messages

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
    statusBoolDict = {"Available": False, "Conserved": True, "Earmarked": True, "Excluded": False}
    changeStatusBoolType = statusBoolDict[statusType]

    changeAbundDict = dict()
    for puID in selectedPUIDStatusDict:
        puStatus = selectedPUIDStatusDict[puID]
        currentStatusBoolType = statusBoolDict[puStatus]

        if currentStatusBoolType is False and changeStatusBoolType:
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

        if currentStatusBoolType and changeStatusBoolType is False:
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
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puProvider = puLayer.dataProvider()
    idFieldOrder = puProvider.fieldNameIndex("Unit_ID")
    statusFieldOrder = puProvider.fieldNameIndex("Status")
    bestFieldOrder = puProvider.fieldNameIndex("Best")
    changeBool = True

    if bestFieldOrder == -1:
        cluz_messages.changeBestToEarmarkedPU_NoBestField()
        changeBool = False

    if changeBool:
        selectedPUIDStatusDict = changeStatus_makeSelectedPUIDStatusDict(puLayer, idFieldOrder, statusFieldOrder, bestFieldOrder)
        cluz_setup.updatePULayerToShowChangesByShiftingExtent()
        statusType = "Earmarked" # This works out the changes needed to update the Best PUs to Earmarked
        changeAbundDict = calcChangeAbundDict(setupObject, selectedPUIDStatusDict, statusType)
        updateTargetDictWithChanges(setupObject, changeAbundDict)
        cluz_setup.updateTargetCSVFromTargetDict(setupObject, setupObject.targetDict)
        cluz_messages.changeBestToEarmarkedPU_Completed()
        cluz_setup.removeThenAddPULayer(setupObject)


def changeStatus_makeSelectedPUIDStatusDict(puLayer, idFieldOrder, statusFieldOrder, bestFieldOrder):
    selectedPUIDStatusDict = dict()
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

    return selectedPUIDStatusDict


def changeEarmarkedToAvailablePUs(setupObject):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puProvider = puLayer.dataProvider()
    idFieldOrder = puProvider.fieldNameIndex("Unit_ID")
    statusFieldOrder = puProvider.fieldNameIndex("Status")
    changeBool = cluz_messages.checkChangeEarmarkedToAvailablePU()

    if changeBool:
        earmakedPUIDStatusDict = changeStatus_makeEarmakedPUIDStatusDict(puLayer, idFieldOrder, statusFieldOrder)
        cluz_setup.updatePULayerToShowChangesByShiftingExtent()
        changeAbundDict = calcChangeAbundDict(setupObject, earmakedPUIDStatusDict, "Available")
        updateTargetDictWithChanges(setupObject, changeAbundDict)
        cluz_setup.updateTargetCSVFromTargetDict(setupObject, setupObject.targetDict)
        cluz_messages.changeEarmarkedToAvailablePU_Completed()
        cluz_setup.removeThenAddPULayer(setupObject)


def changeStatus_makeEarmakedPUIDStatusDict(puLayer, idFieldOrder, statusFieldOrder):
    earmarkedPUIDStatusDict = dict()
    puLayer.startEditing()
    puFeatures = puLayer.getFeatures()
    for puFeature in puFeatures:
        puRow = puFeature.id()
        puID = puFeature.attributes()[idFieldOrder]
        puStatus = puFeature.attributes()[statusFieldOrder]
        if puStatus == "Earmarked":
            puLayer.changeAttributeValue(puRow, statusFieldOrder, "Available")
            earmarkedPUIDStatusDict[puID] = puStatus
    puLayer.commitChanges()

    return earmarkedPUIDStatusDict


def returnPointPUIDList(setupObject, point):
    pointPUIDList = list()
    pntGeom = QgsGeometry.fromPoint(point)

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puProvider = puLayer.dataProvider()
    puIdFieldOrder = puProvider.fieldNameIndex("Unit_ID")

    selectList = list()
    for feature in puLayer.getFeatures():
        if feature.geometry().intersects(pntGeom):
            selectList.append(feature.id())
    if len(selectList) > 0:
        featID = selectList[0]
        puRequest = QgsFeatureRequest().setFilterFids([featID])
        for puFeature in puLayer.getFeatures(puRequest):
            puAttributes = puFeature.attributes()
            puID = puAttributes[puIdFieldOrder]
            pointPUIDList.append(puID)

    return pointPUIDList


def makeIdentifyData(setupObject, selectedPUIDList):
    identDict = dict()
    targetMetDict = dict()
    for puID in selectedPUIDList:
        try:
            puAbundDict = setupObject.abundPUKeyDict[puID]
            identDict, targetMetDict = makeIdentDict(setupObject.targetDict, puAbundDict)
        except KeyError:
            pass

    return identDict, targetMetDict


def makeIdentDict(targetDict, puAbundDict):
    identDict = dict()
    targetMetDict = dict()
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

    return identDict, targetMetDict

def setIdentifyDialogWindowTitle(selectedPUIDList, identDict):
    titleString = "No planning unit selected"
    if len(selectedPUIDList) > 0:
        puID = selectedPUIDList[0]
        if len(identDict) > 0:
            titleString = "Planning unit " + str(puID) + ": list of features"
        else:
            titleString = "Planning unit " + str(puID) + ": does not contain any features"

    return titleString


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

