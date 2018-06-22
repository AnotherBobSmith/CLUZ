from qgis.core import *
from qgis.gui import *
import qgis
from PyQt4 import QtGui



def irrepCalcPortfolioSizeWarning():
    titleText = "Targets cannot be met"
    mainText = "At least one target cannot be met because the amount of that feature in the Available, Conserved and Earmarked planning units is less than its target. This process will terminate."
    warningMessage(titleText, mainText)


def changeBestToEarmarkedPU_NoBestField():
    titleText = "Incorrect format"
    mainText = "The planning unit layer has no field named Best (which is produced by running Marxan). This process will terminate."
    warningMessage(titleText, mainText)


def changeBestToEarmarkedPU_Completed():
    titleText = "Process completed"
    mainText = "Planning units that were selected in the Best portfolio now have Earmarked status and the target table has been updated accordingly."
    infoMessage(titleText, mainText)


def checkChangeEarmarkedToAvailablePU():
    warningTitleText = "Confirm changes to planning unit status"
    warningMainText = "This will change the status of the Earmaked planning units to Avaialable. Do you want to continue?"
    warningBool = runYesCancelWarningDialogBox(warningTitleText, warningMainText)
    return warningBool


def changeEarmarkedToAvailablePU_Completed():
    titleText = "Process completed"
    mainText = "Planning units with Earmarked status have been changed to Available status and the target table has been updated accordingly."
    infoMessage(titleText, mainText)


def runYesCancelWarningDialogBox(titleText, mainText):
    answer = QtGui.QMessageBox.warning(None, titleText, mainText, QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
    if answer == QtGui.QMessageBox.Yes:
        warningBool = True
    else:
        warningBool = False

    return warningBool


def warningMessage(titleText, mainText):
    qgis.utils.iface.messageBar().pushMessage(titleText, mainText, QgsMessageBar.WARNING)


def infoMessage(titleText, mainText):
    qgis.utils.iface.messageBar().pushMessage(titleText, mainText, QgsMessageBar.INFO)


