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
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
import qgis

import os


def addPlanningUnit(setupObject, legendPosition):
    canvas = qgis.utils.iface.mapCanvas()
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")

    categoryList = makePULayerLegendCategory()
    myRenderer = QgsCategorizedSymbolRendererV2('', categoryList)
    myRenderer.setClassAttribute("Status")
    puLayer.setRendererV2(myRenderer)
    QgsMapLayerRegistry.instance().addMapLayer(puLayer)

    canvas.refresh()
    qgis.utils.iface.setActiveLayer(puLayer)

def makePULayerLegendCategory():
    categoryList = []
    #Set category 1
    cat1Value = 'Conserved'
    cat1Label = 'Conserved'
    cat1Symbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '#006633', 'color_border': '#006633'})
    myCat1 = QgsRendererCategoryV2(cat1Value, cat1Symbol, cat1Label)
    categoryList.append(myCat1)

    #Set category 2
    cat2Value = 'Excluded'
    cat2Label = 'Excluded'
    cat2Symbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '#730083', 'color_border': '#730083'})
    myCat2 = QgsRendererCategoryV2(cat2Value, cat2Symbol, cat2Label)
    categoryList.append(myCat2)

    #Set category 3
    cat3Value = 'Available'
    cat3Label = 'Available'
    cat3Symbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '#99ff99', 'color_border': '#99ff99'})
    myCat3 = QgsRendererCategoryV2(cat3Value, cat3Symbol, cat3Label)
    categoryList.append(myCat3)

    #Set category 4
    cat4Value = 'Earmarked'
    cat4Label = 'Earmarked'
    cat4Symbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '#33cc33', 'color_border': '#33cc33'})
    myCat4 = QgsRendererCategoryV2(cat4Value, cat4Symbol, cat4Label)
    categoryList.append(myCat4)

    return categoryList

def createDistributionMapShapefile(setupObject, distShapeFilePathName, selectedFeatIDList):
    distFileName = os.path.basename(distShapeFilePathName)
    makeBaseDistributionMapShapefile(setupObject, distShapeFilePathName)

    distrLayer = QgsVectorLayer(distShapeFilePathName, distFileName, "ogr")
    addPUIDValuesToBaseDistributionMapShapefile(distrLayer, selectedFeatIDList)

    abundPUKeyDict = setupObject.abundPUKeyDict
    abundValuesDict = {}
    for aValue in selectedFeatIDList:
        abundValuesDict[aValue] = []

    distrFeatures = distrLayer.getFeatures()
    distrIDFieldIndex = distrLayer.fieldNameIndex('Unit_ID')
    distrLayer.startEditing()
    for distrFeature in distrFeatures:
        distrPURow = distrFeature.id()
        distrGeom = distrFeature.geometry()
        distrArea = distrGeom.area()
        distrAttributes = distrFeature.attributes()
        distrID = distrAttributes[distrIDFieldIndex]
        for featID in selectedFeatIDList:
            featFieldIndex = distrLayer.fieldNameIndex("F_" + str(featID))
            try:
                puAbundDict = abundPUKeyDict[distrID]
                abundValue = puAbundDict[featID]
            except KeyError:
                abundValue = 0
            aFeatAbundValueTupleList = abundValuesDict[featID]
            aFeatAbundValueTupleList.append((abundValue, distrArea))
            abundValuesDict[featID] = aFeatAbundValueTupleList

            distrLayer.changeAttributeValue(distrPURow, featFieldIndex, abundValue, True)

    distrLayer.commitChanges()
    return abundValuesDict

def makeBaseDistributionMapShapefile(setupObject, distShapeFilePathName):
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    puFeatures = puLayer.getFeatures()
    puIDFieldIndex = puLayer.fieldNameIndex('Unit_ID')
    newFields = QgsFields()
    newFields.append(QgsField("Unit_ID", QVariant.Int))
    writer = QgsVectorFileWriter(distShapeFilePathName, "CP1250", newFields, QGis.WKBPolygon, puLayer.dataProvider().crs(), "ESRI Shapefile")

    #Make distribution shapefile copying PU polygons and ID field
    for puFeature in puFeatures:
        puGeom = puFeature.geometry()
        puAttributes = puFeature.attributes()
        puID = puAttributes[puIDFieldIndex]
        featAttribList = [puID]

        distFeat = QgsFeature()
        distFeat.setGeometry(puGeom)
        distFeat.setAttributes(featAttribList)
        writer.addFeature(distFeat)

    del writer

def addPUIDValuesToBaseDistributionMapShapefile(distrLayer, selectedFeatIDList):
    distrProvider = distrLayer.dataProvider()
    for aFeatID in selectedFeatIDList:
        distrProvider.addAttributes([QgsField("F_" + str(aFeatID), QVariant.Double, "double", 12, 3)])
        distrLayer.updateFields()


def displayDistributionMaps(setupObject, distShapeFilePathName, abundValuesDict, legendType, selectedFeatIDList):
    iface = qgis.utils.iface
    canvas = iface.mapCanvas()

    colourDict = {}
    colourDict[1] = ['#FEE1E1','#FE8787','#FF0000','#AE0000','#630000']
    colourDict[2] = ['#FEEEE1','#FEBC87','#FE8828','#D15D00','#863C00']
    colourDict[3] = ['#FEFAE1','#FEEC87','#FEDD28','#D1B100','#867100']
    colourDict[4] = ['#F6FEE1','#DCFE87','#C1FE28','#95D100','#608600']
    colourDict[5] = ['#E1FEFE','#87FEFE','#28FEFE','#00D6D6','#009A9A']
    colourDict[6] = ['#E6FEE6','#88FE87','#00FF00','#02A900','#015400']
    colourDict[7] = ['#E1FEF5','#87FEDA','#28FEBD','#00D192','#00865D']
    colourDict[8] = ['#E1E1FE','#8789FE','#282CFE','#0004D1','#000286']
    colourDict[9] = ['#FAD7FE','#F587FE','#DD00EF','#A500B3','#5C0063']
    colourDict[10] = ['#FEE1F6','#FE87DE','#FE28C4','#D10098','#860062']
    colourDict[11] = ['#F5F5F5','#B9B9B9','#7D7D7D','#414141','#000000']
    colourDict[12] = ['#FFEABE','#E0B986','#BC865D','#8B5445','#5A2D2D']
    colourKey = 1

    for dFeat in selectedFeatIDList:
        rangeList = []
        colourList = colourDict[colourKey]
        colourKey += 1
        if colourKey > len(colourDict.keys()):
            colourKey = 1

        aDistLayerName = setupObject.targetDict[int(dFeat)][0]
        aDistLayer = QgsVectorLayer(distShapeFilePathName, aDistLayerName, "ogr")
        aDistLayerFieldName = "F_" + str(dFeat)
        aFeatAbundValueTupleList = abundValuesDict[dFeat]
        if legendType == "equal_interval":
            legendValCatList = calcEqualIntervalLegendClasses(aFeatAbundValueTupleList)
        if legendType == "equal_area":
            legendValCatList = calcEqualAreaLegendClasses(aFeatAbundValueTupleList)
        for aValue in range(0, 5):
            minValue = legendValCatList[aValue]
            maxValue = legendValCatList[aValue + 1]
            myColour = colourList[aValue]
            mySymbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': myColour, 'color_border': myColour})
            theRange = QgsRendererRangeV2(minValue, maxValue, mySymbol, str(minValue) + " - " + str(maxValue))
            rangeList.insert(0, theRange)

        myRenderer = QgsGraduatedSymbolRendererV2('', rangeList)
        myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
        myRenderer.setClassAttribute(aDistLayerFieldName)
        aDistLayer.setRendererV2(myRenderer)
        QgsMapLayerRegistry.instance().addMapLayer(aDistLayer)

    canvas.refresh()

def calcEqualIntervalLegendClasses(aFeatAbundValueTupleList):
    abundList = []
    for aTuple in aFeatAbundValueTupleList:
        abundValue = aTuple[0]
        if abundValue > 0:
            abundList.append(abundValue)

    if len(abundList) > 0:
        minValue = min(abundList)
        maxValue = max(abundList)
    else:
        minValue = 0
        maxValue = 0

    incValue = (maxValue - minValue) / 5
    legendValCatList = [minValue, minValue + (1 * incValue), minValue + (2 * incValue), minValue + (3 * incValue), minValue + (4 * incValue), maxValue]

    return legendValCatList

def calcEqualAreaLegendClasses(aFeatAbundValueTupleList):
    abundList = []
    abundTupleList = []
    totalArea = 0

    for aTuple in aFeatAbundValueTupleList:
        abundValue = aTuple[0]
        if abundValue > 0:
            abundList.append(aTuple[0])
            totalArea += aTuple[1]
    abundList.sort()
    if len(abundList) > 0:
        minValue = abundList[0]
        maxValue = abundList[-1]
    else:
        minValue = 0
        maxValue = 0

    x = 1
    while len(abundList) > 0:
        abundValue = abundList.pop(0)
        for aTuple in aFeatAbundValueTupleList:
            if aTuple[0] == abundValue:
                abundTupleList.append(aTuple)
                aFeatAbundValueTupleList.remove(aTuple)

    #Produce dictionary that lists the abundance amount and the total area of PUs containing that amount
    combinedAreaDict = {}
    for bTuple in abundTupleList:
        (bAmount, bArea) = bTuple
        try:
            runningArea = combinedAreaDict[bAmount]
            runningArea += bArea
            combinedAreaDict[bAmount] = runningArea
        except KeyError:
            combinedAreaDict[bAmount] = bArea

    abundValueList = combinedAreaDict.keys()
    abundValueList.sort()
    runningTotalArea = 0
    legendValue1 = "blank"
    legendValue2 = "blank"
    legendValue3 = "blank"
    legendValue4 = "blank"
    for aValue in abundValueList:
        areaAmount = combinedAreaDict[aValue]
        runningTotalArea += areaAmount
        runningProp = runningTotalArea / totalArea
        if legendValue1 == "blank" and runningProp >= 0.2:
            legendValue1 = aValue
        if legendValue2 == "blank" and runningProp >= 0.4:
            legendValue2 = aValue
        if legendValue3 == "blank" and runningProp >= 0.6:
            legendValue3 = aValue
        if legendValue4 == "blank" and runningProp >= 0.8:
            legendValue4 = aValue

    legendValCatList = [minValue, legendValue1, legendValue2, legendValue3, legendValue4, maxValue]

    return legendValCatList

def displayBestOutput(setupObject, bestFieldName, bestShapefileName):
    iface = qgis.utils.iface
    canvas = iface.mapCanvas()
    bestLayer = QgsVectorLayer(setupObject.puPath, bestShapefileName, "ogr")

    categoryList = []
    #Set category 1
    cat1Value = 'Selected'
    cat1Label = 'Selected'
    cat1Symbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': '#ff00ff', 'color_border': '#ff00ff'})
    myCat1 = QgsRendererCategoryV2(cat1Value, cat1Symbol, cat1Label)
    categoryList.append(myCat1)

    myRenderer = QgsCategorizedSymbolRendererV2('', categoryList)
    myRenderer.setClassAttribute(bestFieldName)
    bestLayer.setRendererV2(myRenderer)
    QgsMapLayerRegistry.instance().addMapLayer(bestLayer)

    canvas.refresh()


def reloadPULayer(setupObject):
    root = QgsProject.instance().layerTreeRoot()

    layers = QgsMapLayerRegistry.instance().mapLayers()
    nameList = []
    for QGISFullname, layer in layers.iteritems():
        layerName = str(layer.name())
        nameList.append(layerName)
        if layerName == "Planning units":
            QgsMapLayerRegistry.instance().removeMapLayer(layer.id())

    puLayerPosition = nameList.index("Planning units")
    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    categoryList = makePULayerLegendCategory()
    myRenderer = QgsCategorizedSymbolRendererV2('', categoryList)
    myRenderer.setClassAttribute("Status")
    puLayer.setRendererV2(myRenderer)

    QgsMapLayerRegistry.instance().addMapLayer(puLayer, False)
    root.insertLayer(puLayerPosition, puLayer)

def removePreviousMarxanLayers():
    layers = QgsMapLayerRegistry.instance().mapLayers()
    for QGISFullname, layer in layers.iteritems():
        layerName = layer.name()
        if str(layerName)[0:6] == "Best (" or str(layerName)[0:10] == "SF_Score (":
            QgsMapLayerRegistry.instance().removeMapLayer(layer.id())

def removePreviousMinPatchLayers():
    layers = QgsMapLayerRegistry.instance().mapLayers()
    for QGISFullname, layer in layers.iteritems():
        layerName = layer.name()
        if str(layerName)[0:9] == "MP Best (" or str(layerName)[0:13] == "MP SF_Score (":
            QgsMapLayerRegistry.instance().removeMapLayer(layer.id())

def displayGraduatedLayer(setupObject, fieldName, layerName, legendCode):
    colourDict = {}
    colourDict[1] = ['#C5C2C5', '#CDCEB4', '#DEDEA3', '#EEE894', '#FFFA8B', '#FFE273', '#FFAA52', '#FF8541', '#FF6D31', '#FF0000']
    colourDict[2] = ['#FFFFCC', '#E3F3B5', '#C8E89E', '#A9DB8E', '#88CD80', '#68BE70', '#48AE60', '#2B9C50', '#158243', '#006837']

    colourList = colourDict[legendCode]

    puLayer = QgsVectorLayer(setupObject.puPath, "Planning units", "ogr")
    iface = qgis.utils.iface
    canvas = iface.mapCanvas()
    graduatedLayer = QgsVectorLayer(setupObject.puPath, layerName, "ogr")
    provider = puLayer.dataProvider()

    puFeatures = puLayer.getFeatures()
    graduatedFieldOrder = provider.fieldNameIndex(fieldName)

    maxCountScore = 0 #This will be used to set highest value in legend
    for puFeature in puFeatures:
        puAttributes = puFeature.attributes()
        puCountScore = puAttributes[graduatedFieldOrder]
        if puCountScore > maxCountScore:
            maxCountScore = puCountScore

    rangeList = []
    minValue = 0
    incValue = float(maxCountScore) / 10


    for aValue in range(0, 10):
        maxValue = minValue + incValue
        if aValue == 9:
            maxValue = maxCountScore
        myColour = colourList[aValue]
        mySymbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': myColour, 'color_border': myColour})
        theRange = QgsRendererRangeV2(minValue, maxValue, mySymbol, str(minValue) + " - " + str(maxValue))
        minValue = maxValue
        rangeList.insert(0, theRange)


    myRenderer = QgsGraduatedSymbolRendererV2('', rangeList)
    myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
    myRenderer.setClassAttribute(fieldName)
    graduatedLayer.setRendererV2(myRenderer)
    QgsMapLayerRegistry.instance().addMapLayer(graduatedLayer)

    canvas.refresh()

