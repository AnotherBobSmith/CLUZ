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

import minpat_maketables
import minpat_minsub

def makeSetupDict(filename):
    setupDict = {}
    setupFile = open(filename,'r')
    setupText = setupFile.read()
    setupText.strip
    setupLines = setupText.split('\n')

    for aLine in setupLines:
        aList = aLine.split(" = ",1)
        if len(aList) == 2:
            theKey = aList[0]
            theValue = aList[1]
            setupDict[theKey] = theValue

    return setupDict

def makeInputDataDict(setupDict):
    setupString = setupDict['input_dir']
    dataDict = {}

    dataDict["bound_cost"] = float(setupDict["bound_cost"])
    dataDict["rem_small_patch"] = setupDict["rem_small_patch"]
    dataDict["add_patches"] = setupDict["add_patches"]
    dataDict["whittle_polish"] = setupDict["whittle_polish"]
    dataDict["marxan_polish"] = setupDict["marxan_polish"]
    dataDict["patch_stats"] = setupDict["patch_stats"]
    dataDict["zone_stats"] = setupDict["zone_stats"]

    unitLocString = setupString + '\\unit.dat'
    unitNameList = ["id", "cost","status"]
    unitNameTypeList = ["int","float","int"]
    unitDict = minpat_maketables.makeDataDict(unitLocString,unitNameList,unitNameTypeList)
    dataDict["initialUnitDictionary"] = unitDict

    targetLocString = setupString + '\\target.dat'
    targetNameList = ["id","name","target","spf"]
    targetNameTypeList = ["int","str","float","float","int"]
    targetDict = minpat_maketables.makeDataDict(targetLocString,targetNameList,targetNameTypeList)
    dataDict["targetDictionary"] = targetDict

    abundLocString = setupString + '\\abundance.dat'
    abundDict = minpat_maketables.makeAbundDict(abundLocString,targetDict,unitDict)
    abundanceMatrixDictionary = minpat_maketables.makeAbundMatrixDict(abundLocString,abundDict,unitDict)
    dataDict["abundanceDictionary"] = abundDict
    dataDict["abundanceMatrixDictionary"] = abundanceMatrixDictionary

    boundLocString = setupString + '\\bound.dat'
    boundDict = minpat_maketables.makeBoundDict(boundLocString,unitDict)
    boundMatrixDict = minpat_maketables.makeBoundMatrixDict(boundLocString,boundDict,unitDict)
    dataDict["boundaryDictionary"] = boundDict
    dataDict["boundaryMatrixDictionary"] = boundMatrixDict

    unitLocString = setupString + '\\unit.dat'
    unitNameList = ["id", "status","xloc", "yloc"]
    unitNameTypeList = ["int","int","float","float"]
    cluzanXYDictionary = minpat_maketables.makeDataDict(unitLocString,unitNameList,unitNameTypeList)
    dataDict["cluzanXYDictionary"] = cluzanXYDictionary

    minpLocString = setupString + '\\minpatch.dat'
    minpNameList = ["id","zone","patch_area","radius"]
    minpNameTypeList = ["int","float","float","float"]
    minpDict = minpat_maketables.makeDataDict(minpLocString,minpNameList,minpNameTypeList)
    dataDict["minpatchDictionary"] = minpDict

    unitLocString = setupString + '\\minpatch.dat'
    unitNameList = ["id", "area"]
    unitNameTypeList = ["int","float"]
    rawAreaDictionary = minpat_maketables.makeDataDict(unitLocString,unitNameList,unitNameTypeList)
    areaDictionary = {}
    for puUnitValue in rawAreaDictionary:
        areaDictionary[puUnitValue] = rawAreaDictionary[puUnitValue][0]
    dataDict["areaDictionary"] = areaDictionary

    zonalLocString = setupString + '\\minpatch.dat'
    zonalNameList = ["id","zone","patch_area","radius"]
    zonalNameTypeList  = ["int","int", "float","float"]
    zoneDict = minpat_maketables.makeDataDict(zonalLocString,zonalNameList,zonalNameTypeList)
    dataDict["zoneDictionary"] = zoneDict

    zoneTypeDict = {}
    for aRow in zoneDict:
        zoneList = zoneDict[aRow]
        zoneID = zoneList[0]
        if zoneID in zoneTypeDict:
            continue;
        else:
            patchValue = zoneList[1]
            radiusValue = zoneList[2]
            zoneTypeDict[zoneID] = [float(patchValue), float(radiusValue)]
    dataDict["zoneTypeDictionary"] = zoneTypeDict

    return dataDict

def producePatchDetails(setupDict,dataDict):
    makeTextFileBool = minpat_maketables.checkNeighbPUIDFile(setupDict,dataDict)
##    zoneBool = dataDict["zonal"]
    zoneBool = "true"#Changed to always use the zonal approach
    if makeTextFileBool == 1:
        radiusNeighbDict = minpat_minsub.makeRadiusPUDict(setupDict,dataDict,zoneBool)
        minpat_minsub.makeNeighbPUID(radiusNeighbDict,setupDict,dataDict,zoneBool)

    addNeighbPUIDDict = minpat_maketables.makeNeighbPUIDDict(setupDict,dataDict,"add")
    dataDict["addNeighbPUIDDictionary"] = addNeighbPUIDDict

    whittleNeighbPUIDDict = minpat_maketables.makeNeighbPUIDDict(setupDict,dataDict,"whittle")
    dataDict["whittleNeighbPUIDDict"] = whittleNeighbPUIDDict

    patchAreaDict = minpat_maketables.makePatchAreaDict(setupDict,dataDict)
    dataDict["patchAreaDictionary"] = patchAreaDict

    return dataDict


##
##def makeZoneDict(setupDict):
##    setupString = setupDict['input_dir']
##    zonalLocString = setupString + '\\zonal.dat'
##    zonalNameList = ["id","zone","patch_area","radius"]
##    zonalNameTypeList  = ["int","int", "float","float"]
##    zoneDict = minpat_maketables.makeDataDict(zonalLocString,zonalNameList,zonalNameTypeList)
##
##    return zoneDict

##def makeZoneTypeDict(zoneDict):
##    zoneTypeDict = {}
##    for aRow in zoneDict:
##        zoneList = zoneDict[aRow]
##        zoneID = zoneList[0]
##        if zoneID in zoneTypeDict:
##            continue;
##        else:
##            patchValue = zoneList[1]
##            radiusValue = zoneList[2]
##            zoneTypeDict[zoneID] = [float(patchValue), float(radiusValue)]
##    return zoneTypeDict
