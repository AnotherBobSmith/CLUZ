from qgis.core import *
from qgis.gui import *
import qgis



def changeBestToEarmarkedPU_NoBestField():
    titleText = "Incorrect format"
    mainText = "The planning unit layer has no field named Best (which is produced by running Marxan). This process will terminate."
    warningMessage(titleText, mainText)

def changeBestToEarmarkedPU_Completed():
    titleText = "Process completed"
    mainText = "Planning units that were selected in the Best portfolio now have Earmarked status."
    infoMessage(titleText, mainText)


def warningMessage(titleText, mainText):
    qgis.utils.iface.messageBar().pushMessage(titleText, mainText, QgsMessageBar.WARNING)


def infoMessage(titleText, mainText):
    qgis.utils.iface.messageBar().pushMessage(titleText, mainText, QgsMessageBar.INFO)

