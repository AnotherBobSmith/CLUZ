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

from qgis.core import QgsGeometry, QgsVectorLayer, QgsFeatureRequest
from qgis.utils import iface

from csv import reader
from os import sep

from .cluz_make_file_dicts import update_target_csv_from_target_dict, return_rounded_value, make_lowercase_header_list
from .cluz_functions7 import change_status_pu_layer, update_target_dict_with_changes, undo_status_change_in_pu_layer, calc_change_abund_dict, return_targets_met_tuple, make_ident_dict
from .cluz_messages import warning_message
from .cluz_dialog3_code import return_con_tot_dict, update_con_tot_fields_target_dict
from .cluz_shared import QCustomTableWidgetItem
from .zcluz_dialog7_code import zones_create_target_met_dict
from .zcluz_functions7 import update_zones_target_csv_from_target_dict

# Produce target table ###################################################

def make_zones_target_table_title_text(setup_object):
    zones_target_table_title_text = 'Target table:'
    for zoneID in setup_object.zones_dict:
        zones_target_table_title_text += ' Z' + str(zoneID) + ' = ' + setup_object.zones_dict[zoneID] + ','
    zones_target_table_title_text = zones_target_table_title_text[: -1]

    return zones_target_table_title_text


def add_target_table_data(target_table, setup_object):
    update_csv_file_bool = False
    target_dialog_row_list = setup_object.target_dialog_row_list
    target_header_list = target_dialog_row_list.pop(0)
    target_dialog_row_list.sort()
    lower_header_list = make_lowercase_header_list(target_header_list)

    target_table.targetTableWidget.clear()
    target_table.targetTableWidget.setColumnCount(len(target_header_list))
    insert_row_number = 0
    for a_row in target_dialog_row_list:
        a_row, update_csv_file_bool = check_update_pc_value(setup_object, a_row, lower_header_list, update_csv_file_bool)
        if setup_object.analysis_type == 'MarxanWithZones':
            a_row, update_csv_file_bool = check_update_zones_earlock_values(setup_object, a_row, lower_header_list, update_csv_file_bool)
        add_target_table_row(target_table, setup_object, a_row, target_header_list, [], insert_row_number)
        insert_row_number += 1

    target_table.targetTableWidget.setHorizontalHeaderLabels(target_header_list)

    for aColValue in range(len(target_header_list)):
        target_table.targetTableWidget.resizeColumnToContents(aColValue)

    if update_csv_file_bool:
        if setup_object.analysis_type == 'MarxanWithZones':
            update_zones_target_csv_from_target_dict(setup_object, setup_object.target_dict)
        else:
            update_target_csv_from_target_dict(setup_object, setup_object.target_dict)


def check_update_pc_value(setup_object, a_row, lower_header_list, update_csv_file_bool):
    pc_value = a_row[lower_header_list.index('pc_target')]
    limbo_pc_value = return_limbo_pc_value(setup_object, lower_header_list, a_row)

    if float(limbo_pc_value) != float(pc_value):
        update_csv_file_bool = True
    a_row[lower_header_list.index('pc_target')] = limbo_pc_value

    return a_row, update_csv_file_bool


def return_limbo_pc_value(setup_object, lower_header_list, a_row):
    target_value = float(a_row[lower_header_list.index('target')])
    if setup_object.analysis_type == 'MarxanWithZones':
        cons_value = float(a_row[lower_header_list.index('ear+lock')])
    else:
        cons_value = float(a_row[lower_header_list.index('ear+cons')])
    if target_value <= 0:
        limbo_pc_value = '-1'
    else:
        limbo_pc_value = cons_value / target_value
        limbo_pc_value *= 100
        limbo_pc_value = return_rounded_value(setup_object, limbo_pc_value)

    return limbo_pc_value


def check_update_zones_earlock_values(setup_object, a_row, lower_header_list, update_csv_file_bool):
    earlock_value = 0.0
    for zone_id in setup_object.zones_dict:
        zone_earlock_field_name = 'z' + str(zone_id) + '_ear+lock'
        zone_earlock_value = a_row[lower_header_list.index(zone_earlock_field_name)]
        limbo_earlock_value = return_limbo_earlock_value(setup_object, lower_header_list, a_row, zone_id)

        if float(limbo_earlock_value) != float(zone_earlock_value):
            update_csv_file_bool = True

        a_row[lower_header_list.index(zone_earlock_field_name)] = limbo_earlock_value
        earlock_value += float(limbo_earlock_value)

    a_row[lower_header_list.index('ear+lock')] = return_rounded_value(setup_object, earlock_value)

    return a_row, update_csv_file_bool


def return_limbo_earlock_value(setup_object, lower_header_list, a_row, zone_id):
    zone_prop_field_name = 'z' + str(zone_id) + '_prop'
    zone_el_amount_field_name = 'z' + str(zone_id) + '_ear+lock'
    zone_prop = float(a_row[lower_header_list.index(zone_prop_field_name)])
    zone_el_amount = float(a_row[lower_header_list.index(zone_el_amount_field_name)])

    limbo_earlock_value = zone_el_amount * zone_prop
    limbo_earlock_value = return_rounded_value(setup_object, limbo_earlock_value)

    return limbo_earlock_value


def add_target_table_row(target_table, setup_object, a_row, target_header_list, dec_prec_header_name_list, insert_row_number):
    target_value, conserved_value = 0, 0
    target_table.targetTableWidget.insertRow(insert_row_number)
    for a_col_value in range(len(target_header_list)):
        header_name = target_header_list[a_col_value].lower()
        table_value = return_table_value(setup_object, a_row, a_col_value, header_name, dec_prec_header_name_list)
        if header_name in setup_object.numeric_cols_list:
            targ_table_item = QCustomTableWidgetItem(table_value)
        else:
            targ_table_item = QTableWidgetItem(str(table_value))

        if setup_object.analysis_type != 'MarxanWithZones':
            if header_name == 'target':
                target_value = table_value
            elif header_name == 'ear+cons':
                conserved_value = table_value
        else:
            if header_name == 'target':
                target_value = table_value
            elif header_name == 'ear+lock':
                conserved_value = table_value
        targ_table_item = set_pc_target_item_colour(header_name, targ_table_item, table_value, target_value, conserved_value)
        target_table.targetTableWidget.setItem(insert_row_number, a_col_value, targ_table_item)

        target_table.targetTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
        target_table.targetTableWidget.verticalHeader().hide()


def return_table_value(setup_object, a_row, a_col_value, header_name, dec_prec_header_name_list):
    table_value = a_row[a_col_value]
    if header_name in dec_prec_header_name_list:
        table_value = round(float(table_value), setup_object.decimal_places)
        table_value = format(table_value, '.' + str(setup_object.decimal_places) + 'f')

    return table_value


def set_pc_target_item_colour(header_name, targ_table_item, table_value, target_value, conserved_value):
    if header_name == 'pc_target' and str(table_value) == '-1':
        targ_table_item.setForeground(QColor.fromRgb(128, 128, 128))
    elif header_name == 'pc_target' and float(table_value) >= 0:
        if float(conserved_value) < float(target_value):
            targ_table_item.setForeground(QColor.fromRgb(255, 0, 0))
        else:
            targ_table_item.setForeground(QColor.fromRgb(0, 102, 51))

    return targ_table_item


# Produce abundance table #####################################################################

def load_abund_select_feature_list(abund_select_table, setup_object):
    feat_id_list = list(setup_object.target_dict.keys())
    feat_id_list.sort()
    feat_string_list = list()
    feat_string_dict = dict()
    for aFeat in feat_id_list:
        a_string = str(aFeat) + ' - ' + setup_object.target_dict[aFeat][0]
        feat_string_list.append(a_string)
        feat_string_dict[a_string] = aFeat
    abund_select_table.featListWidget.addItems(feat_string_list)

    return feat_string_dict


def load_abund_dict_data(abund_table, setup_object, selected_feat_id_list):
    decimal_places = setup_object.decimal_places
    abund_pu_key_dict = setup_object.abund_pu_key_dict
    feat_set = set(selected_feat_id_list)
    abund_header_list = ['PU_ID']
    for aFeatID in feat_set:
        abund_header_list.append('F_' + str(aFeatID))
    abund_table.abundTableWidget.clear()
    abund_table.abundTableWidget.setColumnCount(len(abund_header_list))

    insert_row_number = 0
    for pu_id in abund_pu_key_dict:
        abund_table.abundTableWidget.insertRow(insert_row_number)
        zero_value = round(0.0, decimal_places)
        zero_value = format(zero_value, '.' + str(decimal_places) + 'f')
        blank_string = str(zero_value)
        pu_string_list = [blank_string] * len(feat_set)
        pu_abund_dict = abund_pu_key_dict[pu_id]
        for featID in pu_abund_dict:
            if featID in feat_set:
                feat_amount = pu_abund_dict[featID]
                feat_amount = round(float(feat_amount), decimal_places)
                feat_amount = format(feat_amount, '.' + str(decimal_places) + 'f')
                feat_index = list(feat_set).index(featID)
                pu_string_list[feat_index] = str(feat_amount)
        pu_string_list.insert(0, str(pu_id))

        for aColValue in range(len(pu_string_list)):
            feat_value = pu_string_list[aColValue]
            abund_table_item = QCustomTableWidgetItem(feat_value)
            abund_table.abundTableWidget.setItem(insert_row_number, aColValue, abund_table_item)
        insert_row_number += 1

    abund_table.abundTableWidget.setHorizontalHeaderLabels(abund_header_list)

    for aColValue in range(len(abund_header_list)):
        abund_table.abundTableWidget.resizeColumnToContents(aColValue)

        abund_table.abundTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
        abund_table.abundTableWidget.verticalHeader().hide()


def change_status_of_pu_layer_update_target_table(change_status_dialog, setup_object):
    if change_status_dialog.availableButton.isChecked():
        status_type = 'Available'
    elif change_status_dialog.earmarkedButton.isChecked():
        status_type = 'Earmarked'
    elif change_status_dialog.conservedButton.isChecked():
        status_type = 'Conserved'
    else:
        status_type = 'Excluded'

    change_locked_pus_bool = change_status_dialog.changeCheckBox.isChecked()

    selected_pu_id_status_dict = change_status_pu_layer(setup_object, status_type, change_locked_pus_bool)
    change_abund_dict = calc_change_abund_dict(setup_object, selected_pu_id_status_dict, status_type)
    target_dict = update_target_dict_with_changes(setup_object, change_abund_dict)
    setup_object.target_dict = target_dict
    update_target_csv_from_target_dict(setup_object, target_dict)
    (targetsMetCount, targetCount) = return_targets_met_tuple(setup_object)
    change_status_dialog.targetsMetLabel.setText('Targets met: ' + str(targetsMetCount) + ' of ' + str(targetCount))

    setup_object.selected_pu_id_status_dict = selected_pu_id_status_dict
    change_status_dialog.undoButton.setEnabled(True)


def undo_status_of_pu_layer_update_target_table(change_status_dialog, setup_object):
    undo_status_change_in_pu_layer(setup_object)
    new_con_tot_dict = return_con_tot_dict(setup_object)
    target_dict = update_con_tot_fields_target_dict(setup_object, new_con_tot_dict)
    update_target_csv_from_target_dict(setup_object, target_dict)
    setup_object.target_dict = target_dict

    (targetsMetCount, targetCount) = return_targets_met_tuple(setup_object)
    change_status_dialog.targetsMetLabel.setText('Targets met: ' + str(targetsMetCount) + ' of ' + str(targetCount))

    setup_object.selected_pu_id_status_dict = 'blank'
    change_status_dialog.undoButton.setEnabled(False)
    iface.mapCanvas().refresh()


# Produce Met dialog ########################################################################

def load_marxan_results_met_dialog(met_dialog, setup_object):
    if setup_object.analysis_type == 'MarxanWithZones':
        target_met_dict, target_met_header_list = zones_create_target_met_dict(setup_object)
    else:
        target_met_dict, target_met_header_list = create_target_met_dict(setup_object)

    target_met_dict = check_add_feature_names_to_marxan_results_met_dialog(setup_object, target_met_dict)

    target_id_list = list(target_met_dict.keys())
    target_id_list.sort()

    met_dialog.metTableWidget.clear()
    met_dialog.metTableWidget.setColumnCount(len(target_met_header_list))

    insert_row_number = 0
    for aFeat in target_id_list:
        met_dialog.metTableWidget.insertRow(insert_row_number)
        a_row_list = target_met_dict[aFeat]
        a_row_list.insert(0, aFeat)
        for aColValue in range(len(target_met_header_list)):
            a_col_name = target_met_header_list[aColValue]
            feat_value = a_row_list[aColValue]
            if a_col_name in ['Feature Name', 'Target Met']:
                met_table_item = QTableWidgetItem(str(feat_value))
            else:
                met_table_item = QCustomTableWidgetItem(feat_value)
            met_dialog.metTableWidget.setItem(insert_row_number, aColValue, met_table_item)

        insert_row_number += 1

        met_dialog.metTableWidget.setHorizontalHeaderLabels(target_met_header_list)

    for aColValue in range(len(target_met_header_list)):
        met_dialog.metTableWidget.resizeColumnToContents(aColValue)

    met_dialog.metTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
    met_dialog.metTableWidget.verticalHeader().hide()


def check_add_feature_names_to_marxan_results_met_dialog(setup_object, target_met_dict):
    warning_bool = False
    for featID in target_met_dict:
        feat_list = target_met_dict[featID]
        if feat_list != setup_object.target_dict[featID][0]:
            feat_list[0] = setup_object.target_dict[featID][0]
            target_met_dict[featID] = feat_list
            warning_bool = True

    if warning_bool:
        warning_message('Updated Marxan results output', 'The Marxan results ("..._mvbest.txt") file did not include the feature names so these have been added from the CLUZ target file.')

    return target_met_dict


def create_target_met_dict(setup_object):
    target_met_dict = dict()
    with open(setup_object.output_path + sep + setup_object.output_name + '_mvbest.txt', 'rt') as f:
        target_met_reader = reader(f)
        target_met_header_list = next(target_met_reader, None)
        for row in target_met_reader:
            feat_id = int(row.pop(0))
            target_met_dict[feat_id] = row

    return target_met_dict, target_met_header_list


# Identify features in planning unit ################################################################################
def return_point_pu_id_list(setup_object, point):
    point_pu_id_list = list()
    pnt_geom = QgsGeometry.fromPointXY(point)

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_provider = pu_layer.dataProvider()
    pu_id_field_order = pu_provider.fieldNameIndex('Unit_ID')

    select_list = list()
    for feature in pu_layer.getFeatures():
        if feature.geometry().intersects(pnt_geom):
            select_list.append(feature.id())
    if len(select_list) > 0:
        feat_id = select_list[0]
        pu_request = QgsFeatureRequest().setFilterFids([feat_id])
        for puFeature in pu_layer.getFeatures(pu_request):
            pu_attributes = puFeature.attributes()
            pu_id = pu_attributes[pu_id_field_order]
            point_pu_id_list.append(pu_id)

    return point_pu_id_list


def make_identify_data(setup_object, selected_pu_id_list):
    ident_dict = dict()
    target_met_dict = dict()
    for pu_id in selected_pu_id_list:
        try:
            pu_abund_dict = setup_object.abund_pu_key_dict[pu_id]
            ident_dict, target_met_dict = make_ident_dict(setup_object.target_dict, pu_abund_dict)
        except KeyError:
            pass

    return ident_dict, target_met_dict


def set_identify_dialog_window_title(selected_pu_id_list, ident_dict):
    title_string = 'No planning unit selected'
    if len(selected_pu_id_list) > 0:
        pu_id = selected_pu_id_list[0]
        if len(ident_dict) > 0:
            title_string = 'Planning unit ' + str(pu_id) + ': list of features'
        else:
            title_string = 'Planning unit ' + str(pu_id) + ': does not contain any features'

    return title_string


def add_identify_data_to_table_widget(identify_table_widget, setup_object, target_met_dict, ident_dict):
    feat_id_list = list(ident_dict.keys())
    feat_id_list.sort()
    for aRow in range(0, len(feat_id_list)):
        identify_table_widget.insertRow(aRow)
        feat_id = feat_id_list[aRow]
        feat_identify_list = ident_dict[feat_id]
        for aCol in range(0, len(feat_identify_list)):
            feat_value = feat_identify_list[aCol]
            feat_id_item = QTableWidgetItem(feat_value)
            if aCol == 6:
                target_met_status = target_met_dict[feat_id]
                if target_met_status == 'Met':
                    feat_id_item.setForeground(QColor.fromRgb(0, 102, 51))
                elif target_met_status == 'Not met':
                    feat_id_item.setForeground(QColor.fromRgb(255, 0, 0))
                else:
                    feat_id_item.setForeground(QColor.fromRgb(128, 128, 128))
            identify_table_widget.setItem(aRow, aCol, feat_id_item)

    identify_table_widget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
    identify_table_widget.verticalHeader().hide()
