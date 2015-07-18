# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Cluz
                                 A QGIS plugin
 CLUZ for QGIS
                             -------------------
        begin                : 2013-12-19
        copyright            : (C) 2013 by Bob Smith, DICE
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load Cluz class from file Cluz
    from cluz_menu import Cluz
    return Cluz(iface)
