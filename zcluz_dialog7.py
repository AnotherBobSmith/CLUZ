"""
/***************************************************************************
                                 A QGIS plugin
 CLUZ for QGIS
                             -------------------
        begin                : 2024-07-29
        copyright            : (C) 2024 by Bob Smith, DICE
        email                : r.j.smith@kent.ac.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog, QTableWidgetItem
from qgis.core import *

from os import path
import sys

from .cluz_display import update_pu_layer_to_show_changes_by_shifting_extent
from .cluz_shared import copy_table_contents_to_clipboard
from .zcluz_functions7 import return_zones_main_targets_met_tuple, return_zones_targets_met_tuple, return_selected_zone_id_from_change_status_panel
from .zcluz_dialog7_code import add_zones_table_data, make_zones_name_list, zones_change_status_of_pu_layer_update_target_table, zones_undo_status_of_pu_layer_update_target_table

sys.path.append(path.dirname(path.abspath(__file__)) + "/forms")
from cluz_form_zones import Ui_zonesDialog
from cluz_form_zones_change import Ui_ZonesChangeStatusDialog


# Zones table #################################################


class ZonesDialog(QDialog, Ui_zonesDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        if setup_object.zones_dict != 'blank':
            self.load_zones_dict_data(setup_object)

    def load_zones_dict_data(self, setup_object):
        add_zones_table_data(self, setup_object)

    def keyPressEvent(self, e):
        widget_name = 'zonesTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)


class ZonesChangeStatusDialog(QDialog, Ui_ZonesChangeStatusDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.iface = iface
        self.setupUi(self)

        zones_name_list = make_zones_name_list(setup_object)
        self.zonesNameComboBox.addItems(zones_name_list)
        selected_zone_id = list(setup_object.zones_dict.keys())[0]
        targets_met_count, target_count = return_zones_main_targets_met_tuple(setup_object)
        self.zonesMainTargetsMetLabel.setText("Targets met: " + str(targets_met_count) + " of " + str(target_count))
        (zone_targets_met_count, zone_target_count) = return_zones_targets_met_tuple(setup_object, selected_zone_id)
        self.zonesZoneTargetsMetLabel.setText('Zone ' + str(selected_zone_id) + ' targets met: ' + str(zone_targets_met_count) + ' of ' + str(zone_target_count))
        self.undoButton.setEnabled(False)

        self.zonesNameComboBox.activated.connect(lambda: self.update_zone_target_details(setup_object))
        self.changeButton.clicked.connect(lambda: self.change_status(setup_object))
        self.undoButton.clicked.connect(lambda: self.undo_status_change(setup_object))

    def update_zone_target_details(self, setup_object):
        selected_zone_id = return_selected_zone_id_from_change_status_panel(self)
        (zone_targets_met_count, zone_target_count) = return_zones_targets_met_tuple(setup_object, selected_zone_id)
        self.zonesZoneTargetsMetLabel.setText('Zone ' + str(selected_zone_id) + ' targets met: ' + str(zone_targets_met_count) + ' of ' + str(zone_target_count))

    def change_status(self, setup_object):
        zones_change_status_of_pu_layer_update_target_table(self, setup_object)

    def undo_status_change(self, setup_object):
        zones_undo_status_of_pu_layer_update_target_table(self, setup_object)
        update_pu_layer_to_show_changes_by_shifting_extent()
