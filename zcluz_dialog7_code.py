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

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog, QTableWidgetItem
from qgis.PyQt.QtGui import QColor
from PyQt5 import QtCore, QtGui, QtWidgets

from qgis.utils import iface

from csv import reader
from os import sep

from .zcluz_checkup import create_and_check_zones_file
from .zcluz_make_file_dicts import update_zones_target_csv_from_target_dict
from .zcluz_dialog3_code import return_zones_earlock_amount_tot_dict, update_zones_ear_lock_tot_fields_target_dict
from .zcluz_functions7 import change_zones_status_pu_layer, return_selected_zone_id_from_change_status_panel
from .zcluz_functions7 import return_before_after_pu_zones_status_dicts, make_zones_selected_status_balance_dict
from .zcluz_functions7 import calc_zones_change_abund_amount_dict, update_zones_target_dict_with_changes
from .zcluz_functions7 import return_zones_main_targets_met_tuple, return_zones_targets_met_tuple, zones_select_undo_planning_units


class QCustomTableWidgetItem(QtWidgets.QTableWidgetItem):  # Designed so column sort is based on value of number, not string of number
    def __init__ (self, value):
        super(QCustomTableWidgetItem, self).__init__(str('%s' % value))

    def __lt__ (self, other):
        if isinstance(other, QCustomTableWidgetItem):
            self_data_value = float(self.data(QtCore.Qt.EditRole))
            other_data_value = float(other.data(QtCore.Qt.EditRole))
            return self_data_value < other_data_value
        else:
            return QtGui.QTableWidgetItem.__lt__(self, other)


# Produce zones table ##################################

def add_zones_table_data(zones_table, setup_object):
    check_bool = create_and_check_zones_file(setup_object, True)
    if check_bool:
        zones_header_list = ['Id', 'Name']

        zones_table.zonesTableWidget.clear()
        zones_table.zonesTableWidget.setColumnCount(len(zones_header_list))
        insert_row_number = 0
        for zoneID in setup_object.zones_dict:
            zones_table.zonesTableWidget.insertRow(insert_row_number)
            zone_name = setup_object.zones_dict[zoneID]
            zones_table.zonesTableWidget.setItem(insert_row_number, 0, QCustomTableWidgetItem(str(zoneID)))
            zones_table.zonesTableWidget.setItem(insert_row_number, 1, QCustomTableWidgetItem(zone_name))
            insert_row_number += 1

        zones_table.zonesTableWidget.setHorizontalHeaderLabels(zones_header_list)

        for aColValue in range(len(zones_header_list)):
            zones_table.zonesTableWidget.resizeColumnToContents(aColValue)

        zones_table.zonesTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
        zones_table.zonesTableWidget.verticalHeader().hide()

# Produce Met dialog #################################################


def make_zones_name_list(setup_object):
    zones_name_list = list()
    for zoneID in list(setup_object.zones_dict):
        zone_layer_name = 'Zone ' + str(zoneID) + ' - ' + setup_object.zones_dict[zoneID]
        zones_name_list.append(zone_layer_name)

    return zones_name_list


def zones_change_status_of_pu_layer_update_target_table(zones_change_status_dialog, setup_object):
    if zones_change_status_dialog.zonesUnassignedButton.isChecked():
        status_type = 'Unassigned'
    elif zones_change_status_dialog.zonesEarmarkedButton.isChecked():
        status_type = 'Earmarked'
    elif zones_change_status_dialog.zonesLockedButton.isChecked():
        status_type = 'Locked'
    else:
        status_type = 'Excluded'

    change_locked_pus_bool = zones_change_status_dialog.zonesChangeCheckBox.isChecked()
    selected_zone_id = return_selected_zone_id_from_change_status_panel(zones_change_status_dialog)

    before_pu_zones_status_dict, after_pu_zones_status_dict = return_before_after_pu_zones_status_dicts(setup_object, status_type, change_locked_pus_bool, selected_zone_id)
    zones_selected_status_balance_dict = make_zones_selected_status_balance_dict(before_pu_zones_status_dict, after_pu_zones_status_dict)
    change_zones_status_pu_layer(setup_object, after_pu_zones_status_dict)
    zones_change_abund_dict = calc_zones_change_abund_amount_dict(setup_object, zones_selected_status_balance_dict)
    target_dict = update_zones_target_dict_with_changes(setup_object, zones_change_abund_dict)
    setup_object.target_dict = target_dict
    update_zones_target_csv_from_target_dict(setup_object, target_dict)

    set_zones_zone_targets_met_label(zones_change_status_dialog, setup_object, selected_zone_id)

    setup_object.before_pu_zones_status_dict = before_pu_zones_status_dict
    zones_change_status_dialog.undoButton.setEnabled(True)


def set_zones_zone_targets_met_label(zones_change_status_dialog, setup_object, selected_zone_id):
    (main_targets_met_count, main_target_count) = return_zones_main_targets_met_tuple(setup_object)
    zones_change_status_dialog.zonesMainTargetsMetLabel.setText('Targets met: ' + str(main_targets_met_count) + ' of ' + str(main_target_count))
    (zone_targets_met_count, zone_target_count) = return_zones_targets_met_tuple(setup_object, selected_zone_id)
    zones_change_status_dialog.zonesZoneTargetsMetLabel.setText('Zone ' + str(selected_zone_id) + ' targets met: ' + str(zone_targets_met_count) + ' of ' + str(zone_target_count))


def zones_undo_status_of_pu_layer_update_target_table(zones_change_status_dialog, setup_object):
    selected_zone_id = return_selected_zone_id_from_change_status_panel(zones_change_status_dialog)
    zones_select_undo_planning_units(setup_object)
    change_zones_status_pu_layer(setup_object, setup_object.before_pu_zones_status_dict)
    new_con_tot_dict = return_zones_earlock_amount_tot_dict(setup_object)
    target_dict = update_zones_ear_lock_tot_fields_target_dict(setup_object, new_con_tot_dict)
    update_zones_target_csv_from_target_dict(setup_object, target_dict)
    setup_object.target_dict = target_dict

    set_zones_zone_targets_met_label(zones_change_status_dialog, setup_object, selected_zone_id)

    setup_object.before_pu_zones_status_dict = 'blank'
    zones_change_status_dialog.undoButton.setEnabled(False)
    iface.mapCanvas().refresh()


def zones_create_target_met_dict(setup_object):
    zones_target_met_dict = dict()
    zones_target_met_header_list = ['Feature ID', 'Feature name', 'Total Amount', 'Overall target', 'Target Prop']

    with open(setup_object.output_path + sep + setup_object.output_name + '_mvbest.csv', 'rt') as f:
        target_met_reader = reader(f)
        next(target_met_reader)
        for row in target_met_reader:
            feat_id = int(row[0])
            feat_name = row[1]
            feat_target = float(row[2])
            feat_total_amount = float(row[3])
            feat_total_ear_lock_amount = float(row[4])
            try:
                feat_target_prop = round(feat_total_ear_lock_amount / feat_target, 3)
            except ZeroDivisionError:
                feat_target_prop = 0
            zones_target_met_data_row = [feat_name, feat_total_amount, feat_target, feat_target_prop]
            zones_target_met_dict[feat_id] = zones_target_met_data_row

    return zones_target_met_dict, zones_target_met_header_list

