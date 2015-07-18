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

from qgis.gui import QgsMapTool
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from cluz_dialog3 import identifyDialog

class IdentifyTool(QgsMapTool):
    def __init__(self, canvas, setupObject):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.setupObject = setupObject

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def canvasReleaseEvent(self, event):
        #Get the click
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

        self.identifyDialog = identifyDialog(self, self.setupObject, point)
        # show the dialog
        self.identifyDialog.show()
        # Run the dialog event loop
        result = self.identifyDialog.exec_()

    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True
