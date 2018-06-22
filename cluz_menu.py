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

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import qgis

import os.path
import sys

import cluz_setup
import cluz_functions1
import cluz_functions3

# Import the code for the Setup Object
from cluz_setup import CluzSetupObject

# Import the code for the dialog
from cluz_dialog1 import startDialog
from cluz_dialog1 import setupDialog
from cluz_dialog1 import createDialog
from cluz_dialog1 import convertVecDialog
from cluz_dialog1 import convertCsvDialog
from cluz_dialog1 import removeDialog
from cluz_dialog2 import distributionDialog
from cluz_dialog2 import identifySelectedDialog
from cluz_dialog2 import richnessDialog
from cluz_dialog2 import irrepDialog
from cluz_dialog2 import portfolioDialog
from cluz_dialog2 import inputsDialog
from cluz_dialog2 import marxanDialog
from cluz_dialog2 import loadDialog
from cluz_dialog2 import calibrateDialog
from cluz_dialog2 import minpatchDialog
from cluz_dialog2 import patchesDialog
from cluz_dialog3 import targetDialog
from cluz_dialog3 import abundSelectDialog
from cluz_dialog3 import metDialog
from cluz_dialog3 import changeStatusDialog
from cluz_tools import IdentifyTool

# Initialize Qt resources from file resources.py
import resources_rc

class Cluz:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'cluz_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        self.cluz_menu = QMenu(self.iface.mainWindow())
        self.cluz_menu.setTitle("CLUZ")
        cluzMenuBar = self.iface.mainWindow().menuBar()
        cluzMenuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.cluz_menu)

        # Create the Setup Object
        setupObject = CluzSetupObject()

        self.cluz_toolbar = self.iface.addToolBar("CLUZ")

        # Create action that will start plugin configuration
        self.SetupAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_setup.png"), "View and edit CLUZ setup file", self.iface.mainWindow())
        self.CreateAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_create.png"), "Create initial CLUZ files", self.iface.mainWindow())
        self.ConvertVecAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_convpoly.png"), "Convert polyline or polygon themes to Marxan abundance data", self.iface.mainWindow())
        self.ConvertCsvAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_convcsv.png"), "Import fields from table to Marxan abundance file", self.iface.mainWindow())

        self.RemoveAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_rem.png"), "Remove features from CLUZ tables", self.iface.mainWindow())
        self.RecalcAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_recalc.png"), "Recalculate target table data", self.iface.mainWindow())
        self.TroubleAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_trouble.png"), "Troubleshoot all CLUZ files", self.iface.mainWindow())

        self.DistributionAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_dist.png"), "Display distributions of conservation features", self.iface.mainWindow())
        self.IdentifySelectedAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_selident.png"), "Identify features in selected units", self.iface.mainWindow())
        self.RichnessAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_richness.png"), "Calculate richness scores", self.iface.mainWindow())
        self.IrrepAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_irrep.png"), "Calculate irreplaceability values", self.iface.mainWindow())
        self.PortfolioAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_portfolio.png"), "Calculate portfolio characteristics", self.iface.mainWindow())

        self.InputsAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_marxcreate.png"), "Create Marxan input files", self.iface.mainWindow())
        self.MarxanAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_marxan.png"), "Launch Marxan", self.iface.mainWindow())
        self.LoadAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_load.png"), "Load previous Marxan outputs", self.iface.mainWindow())
        self.CalibrateAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_calibrate.png"), "Calibrate Marxan parameters", self.iface.mainWindow())

        self.MinPatchAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_minpatch.png"), "Launch MinPatch", self.iface.mainWindow())
        # self.PatchesAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_menu_portfolio.png"), "Show patches from Marxan or MinPatch output file", self.iface.mainWindow())

        self.TargetAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_target.png"), "Open target table", self.iface.mainWindow())
        self.AbundAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_abund.png"), "Open abundance table", self.iface.mainWindow())
        self.TargetsMetAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_target_met.png"), "Open Marxan results table", self.iface.mainWindow())
        self.BestToEarmarkedAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_best_ear.png"), "Change the status of the Best units to Earmarked", self.iface.mainWindow())
        self.EarmarkedToAvailableAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_ear_avail.png"), "Change the status of the Earmarked units to Available", self.iface.mainWindow())
        self.TargetsMetAction.setEnabled(False)
        self.ChangeAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_change.png"), "Change planning unit status", self.iface.mainWindow())
        self.IdentifyAction = QAction(QIcon(os.path.dirname(__file__) + "/icons/cluz_identify.png"), "Identify features in planning unit", self.iface.mainWindow())

        # connect the action to the run method
        self.SetupAction.triggered.connect(lambda: self.runSetupDialog(setupObject))
        self.CreateAction.triggered.connect(self.runCreateDialog)
        self.ConvertVecAction.triggered.connect(lambda: self.convertPolylinePolygonToAbundanceData(setupObject))
        self.ConvertCsvAction.triggered.connect(lambda: self.convertCsvToAbundanceData(setupObject))

        self.RemoveAction.triggered.connect(lambda: self.runRemoveFeatures(setupObject))
        self.RecalcAction.triggered.connect(lambda: self.recalcTargetTable(setupObject))
        self.TroubleAction.triggered.connect(lambda: self.runTroubleShoot(setupObject))

        self.DistributionAction.triggered.connect(lambda: self.runShowDistributionFeatures(setupObject))
        self.IdentifySelectedAction.triggered.connect(lambda: self.runIdentifyFeaturesInSelected(setupObject))
        self.RichnessAction.triggered.connect(lambda: self.calcRichness(setupObject))
        self.IrrepAction.triggered.connect(lambda: self.calcIrrepValues(setupObject))
        self.PortfolioAction.triggered.connect(lambda: self.calcPortfolioDetails(setupObject))

        self.InputsAction.triggered.connect(lambda: self.runCreateMarxanInputFiles(setupObject))
        self.MarxanAction.triggered.connect(lambda: self.runMarxan(setupObject, self.TargetsMetAction))
        self.LoadAction.triggered.connect(lambda: self.loadPrevMarxanResults(setupObject))
        self.CalibrateAction.triggered.connect(lambda: self.runCalibrate(setupObject))

        self.MinPatchAction.triggered.connect(lambda: self.runMinPatch(setupObject))
        # self.PatchesAction.triggered.connect(lambda: self.runShowPatches(setupObject))

        self.TargetAction.triggered.connect(lambda: self.runTargetDialog(setupObject))
        self.AbundAction.triggered.connect(lambda: self.runAbundSelectDialog(setupObject))
        self.BestToEarmarkedAction.triggered.connect(lambda: self.changeBestToEarmarked(setupObject))
        self.TargetsMetAction.triggered.connect(lambda: self.targetsMetDialog(setupObject))
        self.EarmarkedToAvailableAction.triggered.connect(lambda: self.changeEarmarkedToAvailable(setupObject))
        self.ChangeAction.triggered.connect(lambda: self.runChangeStatusDialog(setupObject))
        self.IdentifyAction.triggered.connect(lambda: self.showFeaturesInPU(setupObject))

        # Add actions to CLUZ menu
        self.cluz_menu.addAction(self.SetupAction)
        self.cluz_menu.addAction(self.CreateAction)
        self.cluz_menu.addAction(self.ConvertVecAction)
        self.cluz_menu.addAction(self.ConvertCsvAction)
        self.cluz_menu.addSeparator()
        self.cluz_menu.addAction(self.RemoveAction)
        self.cluz_menu.addAction(self.RecalcAction)
        self.cluz_menu.addAction(self.TroubleAction)
        self.cluz_menu.addSeparator()
        self.cluz_menu.addAction(self.DistributionAction)
        self.cluz_menu.addAction(self.IdentifySelectedAction)
        self.cluz_menu.addAction(self.RichnessAction)
        # self.cluz_menu.addAction(self.IrrepAction)
        self.cluz_menu.addAction(self.PortfolioAction)
        self.cluz_menu.addSeparator()
        self.cluz_menu.addAction(self.InputsAction)
        self.cluz_menu.addAction(self.MarxanAction)
        self.cluz_menu.addAction(self.LoadAction)
        self.cluz_menu.addAction(self.CalibrateAction)
        self.cluz_menu.addSeparator()
        self.cluz_menu.addAction(self.MinPatchAction)
        # self.cluz_menu.addAction(self.PatchesAction)

        # Add actions as buttons on menu bar
        self.cluz_toolbar.addAction(self.TargetAction)
        self.cluz_toolbar.addAction(self.AbundAction)
        self.cluz_toolbar.addAction(self.EarmarkedToAvailableAction)
        self.cluz_toolbar.addAction(self.TargetsMetAction)
        self.cluz_toolbar.addAction(self.BestToEarmarkedAction)
        self.cluz_toolbar.addSeparator()
        self.cluz_toolbar.addAction(self.ChangeAction)
        self.cluz_toolbar.addAction(self.IdentifyAction)
        self.cluz_toolbar.addSeparator()

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&CLUZ", self.SetupAction)
        del self.cluz_toolbar

    def runAddPULayerToView(self, setupObject):
        if cluz_setup.checkPULayerPresent() == False:
            cluz_setup.addPULayer(self, setupObject)

    def runStartDialog(self, setupObject):
        self.startDialog = startDialog(self, setupObject)
        # show the dialog
        self.startDialog.show()
        # Run the dialog event loop
        result = self.startDialog.exec_()

    def runSetupDialog(self, setupObject):
        self.setupDialog = setupDialog(self, setupObject)
        # show the dialog
        self.setupDialog.show()
        # Run the dialog event loop
        result = self.setupDialog.exec_()

    def runCreateDialog(self):
        self.createDialog = createDialog(self)
        # show the dialog
        self.createDialog.show()
        # Run the dialog event loop
        result = self.createDialog.exec_()

    def convertPolylinePolygonToAbundanceData(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.convertVecDialog = convertVecDialog(self, setupObject)
            # show the dialog
            self.convertVecDialog.show()
            # Run the dialog event loop
            result = self.convertVecDialog.exec_()

    def convertCsvToAbundanceData(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.convertCsvDialog = convertCsvDialog(self, setupObject)
            # show the dialog
            self.convertCsvDialog.show()
            # Run the dialog event loop
            result = self.convertCsvDialog.exec_()

    def runRemoveFeatures(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.removeDialog = removeDialog(self, setupObject)
            # show the dialog
            self.removeDialog.show()
            # Run the dialog event loop
            result = self.removeDialog.exec_()

    def recalcTargetTable(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            cluz_setup.createAndCheckCLUZFiles(setupObject)
            cluz_setup.checkAddPULayer(setupObject)
            newConTotDict = cluz_functions1.returnConTotDict(setupObject)
            targetDict = cluz_functions1.updateConTotFieldsTargetDict(setupObject, newConTotDict)
            setupObject.targetDict = targetDict
            cluz_setup.updateTargetCSVFromTargetDict(setupObject, targetDict)
            qgis.utils.iface.messageBar().pushMessage("Target table updated: ", "Process completed.", QgsMessageBar.INFO, 3)

    def runTroubleShoot(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            cluz_setup.checkCreateSporderDat(setupObject)
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)
            cluz_functions1.troubleShootCLUZFiles(setupObject)

    def runShowDistributionFeatures(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.distributionDialog = distributionDialog(self, setupObject)
            # show the dialog
            self.distributionDialog.show()
            # Run the dialog event loop
            result = self.distributionDialog.exec_()


    def runIdentifyFeaturesInSelected(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.Ui_identifySelectedDialog = identifySelectedDialog(self, setupObject)
            # show the dialog
            self.Ui_identifySelectedDialog.show()
            # Run the dialog event loop
            result = self.Ui_identifySelectedDialog.exec_()


    def calcRichness(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.richnessDialog = richnessDialog(self, setupObject)
            # show the dialog
            self.richnessDialog.show()
            # Run the dialog event loop
            result = self.richnessDialog.exec_()

    def calcIrrepValues(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.irrepDialog = irrepDialog(self, setupObject)
            # show the dialog
            self.irrepDialog.show()
            # Run the dialog event loop
            result = self.irrepDialog.exec_()

    def calcPortfolioDetails(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            self.portfolioDialog = portfolioDialog(self, setupObject)
            # show the dialog
            self.portfolioDialog.show()
            # Run the dialog event loop
            result = self.portfolioDialog.exec_()

    def runCreateMarxanInputFiles(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            self.inputsDialog = inputsDialog(self, setupObject)
            # show the dialog
            self.inputsDialog.show()
            # Run the dialog event loop
            result = self.inputsDialog.exec_()

    def runMarxan(self, setupObject, targetsMetAction):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            cluz_setup.checkCreateSporderDat(setupObject)
            marxanBool = True
            marxanPath = setupObject.marxanPath
            if sys.platform.startswith('darwin'):
                QMessageBox.critical(None, "CLUZ and MacOS", "The current version of CLUZ cannot run Marxan on Mac computers. Sorry about that. Instead, you can run Marxan indepedently and load the results into CLUZ.")
            else:
                if marxanPath == "blank":
                    QMessageBox.critical(None, "Marxan path missing", "The location of Marxan has not been specified. CLUZ will now open the CLUZ setup dialog box, so please specify a correct version.")
                    marxanBool = False
                if os.path.exists(marxanPath) == False:
                    QMessageBox.critical(None, "Incorrect Marxan path", "Marxan cannot be found at the specified pathway. CLUZ will now open the CLUZ setup dialog box, so please specify a correct version.")
                    marxanBool = False

                if marxanBool == False:
                    self.setupDialog = setupDialog(self, setupObject)
                    # show the dialog
                    self.setupDialog.show()
                    # Run the dialog event loop
                    result = self.setupDialog.exec_()

                if marxanBool == True and setupObject.setupStatus == "files_checked":
                    self.marxanDialog = marxanDialog(self, setupObject, targetsMetAction)
                    # show the dialog
                    self.marxanDialog.show()
                    # Run the dialog event loop
                    result = self.marxanDialog.exec_()

    def loadPrevMarxanResults(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            self.loadDialog = loadDialog(self, setupObject)
            # show the dialog
            self.loadDialog.show()
            # Run the dialog event loop
            result = self.loadDialog.exec_()

    def runCalibrate(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            cluz_setup.checkCreateSporderDat(setupObject)
            marxanBool = True
            marxanPath = setupObject.marxanPath
            if marxanPath == "blank":
                QMessageBox.critical(None, "Marxan path missing", "The location of Marxan has not been specified. CLUZ will now open the CLUZ setup dialog box, so please specify a correct version.")
                marxanBool = False
            if os.path.exists(marxanPath) == False:
                QMessageBox.critical(None, "Incorrect Marxan path", "Marxan cannot be found at the specified pathway. CLUZ will now open the CLUZ setup dialog box, so please specify a correct version.")
                marxanBool = False

            if marxanBool == False:
                self.setupDialog = setupDialog(self, setupObject)
                # show the dialog
                self.setupDialog.show()
                # Run the dialog event loop
                result = self.setupDialog.exec_()

            if marxanBool == True and setupObject.setupStatus == "files_checked":
                self.calibrateDialog = calibrateDialog(self, setupObject)
                # show the dialog
                self.calibrateDialog.show()
                # Run the dialog event loop
                result = self.calibrateDialog.exec_()

    def runMinPatch(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            self.minpatchDialog = minpatchDialog(self, setupObject)
            # show the dialog
            self.minpatchDialog.show()
            # Run the dialog event loop
            result = self.minpatchDialog.exec_()


    def runShowPatches(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            self.patchesDialog = patchesDialog(self, setupObject)
            # show the dialog
            self.patchesDialog.show()
            # Run the dialog event loop
            result = self.patchesDialog.exec_()


    def runTargetDialog(self,setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            self.targetDialog = targetDialog(self, setupObject)
            # show the dialog
            self.targetDialog.show()
            # Run the dialog event loop
            result = self.targetDialog.exec_()

    def runAbundSelectDialog(self,setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.abundSelectDialog = abundSelectDialog(self, setupObject)
            # show the dialog
            self.abundSelectDialog.show()
            # Run the dialog event loop
            result = self.abundSelectDialog.exec_()

    def targetsMetDialog(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            self.metDialog = metDialog(self, setupObject)
            # show the dialog
            self.metDialog.show()
            # Run the dialog event loop
            result = self.metDialog.exec_()

    def changeBestToEarmarked(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            cluz_functions3.changeBestToEarmarkedPUs(setupObject)


    def changeEarmarkedToAvailable(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            cluz_functions3.changeEarmarkedToAvailablePUs(setupObject)


    def runChangeStatusDialog(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            self.changeStatusDialog = changeStatusDialog(self, setupObject)
            # show the dialog
            self.changeStatusDialog.show()
            # Run the dialog event loop
            result = self.changeStatusDialog.exec_()

    def showFeaturesInPU(self, setupObject):
        checkSetupFileLoaded(self, setupObject)
        openSetupDialogIfSetupFilesIncorrect(self, setupObject)
        checkCreateAddFiles(setupObject)

        if setupObject.setupStatus == "files_checked":
            if setupObject.abundPUKeyDict == "blank":
                setupObject.abundPUKeyDict = cluz_setup.makeAbundancePUKeyDict(setupObject)

            identifyTool = IdentifyTool(self.iface.mapCanvas(), setupObject)
            self.iface.mapCanvas().setMapTool(identifyTool)

# Checks whether setup file has been loaded
def checkSetupFileLoaded(self, setupObject):
    if setupObject.overRide:
        cluz_setup.updateSetupObjectFromSetupFile(setupObject, "C:\\Users\\Bob\\.qgis2\\python\\plugins\\cluz\\ex1.clz")
    else:
        if setupObject.setupPath == "blank":
            self.startDialog = startDialog(self, setupObject)
            # show the dialog
            self.startDialog.show()
            # Run the dialog event loop
            result = self.startDialog.exec_()

            if setupObject.setupAction == "new":
                self.setupDialog = setupDialog(self, setupObject)
                # show the dialog
                self.setupDialog.show()
                # Run the dialog event loop
                result = self.setupDialog.exec_()
            elif setupObject.setupAction == "open":
                setupPathNameText = QFileDialog.getOpenFileName(None, 'Open existing CLUZ setup file', '*.clz')
                try:
                    cluz_setup.updateSetupObjectFromSetupFile(setupObject, setupPathNameText)
                except IOError:
                    pass
            else:
                self.startDialog.close()

# Checks whether setup, pu, target and abundance file paths are correct. If they 
def openSetupDialogIfSetupFilesIncorrect(self, setupObject):
    if setupObject.setupStatus == "values_set":
        self.setupDialog = setupDialog(self, setupObject)
        # show the dialog
        self.setupDialog.show()
        # Run the dialog event loop
        result = self.setupDialog.exec_()

def checkCreateAddFiles(setupObject):
    cluz_setup.createAndCheckCLUZFiles(setupObject)
    cluz_setup.makeTargetDict(setupObject)
    cluz_setup.checkAddPULayer(setupObject)
