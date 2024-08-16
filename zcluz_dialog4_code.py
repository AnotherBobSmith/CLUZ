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
import copy

from qgis.PyQt.QtWidgets import QTableWidgetItem

from qgis.core import QgsVectorLayer, QgsField
from qgis.utils import iface

from .cluz_make_file_dicts import return_rounded_value


# Identify features in selected units #############################################################


def zones_make_selected_avail_ear_excl_lock_dict(setup_object):
    avail_ear_excl_lock_dict = dict()

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    iface.setActiveLayer(pu_layer)
    pu_layer = iface.activeLayer()
    provider = pu_layer.dataProvider()
    selected_pus = pu_layer.selectedFeatures()
    id_field_index = provider.fieldNameIndex('Unit_ID')

    for a_pu in selected_pus:
        pu_id = int(a_pu.attributes()[id_field_index])
        pu_status_dict = zones_make_pu_status_dict(setup_object, provider, a_pu)
        pu_status_list = list(pu_status_dict.values())
        try:
            pu_abund_dict = setup_object.abund_pu_key_dict[pu_id]
        except KeyError:
            pu_abund_dict = dict()

        if 'Earmarked' in pu_status_list or 'Locked' in pu_status_list:
            for zone_id in pu_status_dict:
                pu_zone_status = pu_status_dict[zone_id]
                if pu_zone_status == 'Earmarked':
                    avail_ear_excl_lock_dict[pu_id] = {'Z' + str(zone_id) + ' Earmarked': copy.deepcopy(pu_abund_dict)}
                if pu_zone_status == 'Locked':
                    avail_ear_excl_lock_dict[pu_id] = {'Z' + str(zone_id) + ' Locked': copy.deepcopy(pu_abund_dict)}
        elif set(pu_status_list) == 'Excluded':
            avail_ear_excl_lock_dict[pu_id] = {'Excluded': copy.deepcopy(pu_abund_dict)}
        else:
            avail_ear_excl_lock_dict[pu_id] = {'Available': copy.deepcopy(pu_abund_dict)}

    return avail_ear_excl_lock_dict


def zones_make_pu_status_dict(setup_object, provider, a_pu):
    pu_status_dict = dict()
    for zone_id in setup_object.zones_dict:
        focal_zone_status_field_index = provider.fieldNameIndex('Z' + str(zone_id) + '_Status')
        pu_status = str(a_pu.attributes()[focal_zone_status_field_index])
        pu_status_dict[zone_id] = pu_status

    return pu_status_dict


def zones_return_selected_pu_details_dict(selected_avail_ear_excl_lock_dict):
    selected_abund_details_dict = dict()

    for pu_id in selected_avail_ear_excl_lock_dict:
        pu_avail_ear_excl_lock_dict = selected_avail_ear_excl_lock_dict[pu_id]

        for zone_type in pu_avail_ear_excl_lock_dict:
            zone_type_abund_dict = pu_avail_ear_excl_lock_dict[zone_type]

            for feat_id in zone_type_abund_dict:
                feat_amount = zone_type_abund_dict[feat_id]
                try:
                    selected_abund_zone_details_dict = selected_abund_details_dict[zone_type]
                except KeyError:
                    selected_abund_zone_details_dict = dict()
                try:
                    feat_running_amount = selected_abund_zone_details_dict[feat_id]
                except KeyError:
                    feat_running_amount = 0
                feat_running_amount += feat_amount
                selected_abund_zone_details_dict[feat_id] = feat_running_amount
                selected_abund_details_dict[zone_type] = selected_abund_zone_details_dict

    return selected_abund_details_dict


def zones_add_selected_identify_data_to_table_widget(zones_identify_selected_dialog, setup_object, abund_details_dict):
    feat_id_list = list(setup_object.target_dict.keys())
    feat_id_list.sort()
    for rowNumber in range(0, len(feat_id_list)):
        zones_identify_selected_dialog.zonesIdentifySelectedTableWidget.insertRow(rowNumber)
        feat_id = feat_id_list[rowNumber]
        feat_id_table_item = QTableWidgetItem(str(feat_id))
        feat_name_table_item = QTableWidgetItem(str(setup_object.target_dict[feat_id][0]))
        zone_available_amount = zones_return_string_amount_per_zone_type(setup_object, abund_details_dict, 'Available', feat_id)
        zone_available_table_item = QTableWidgetItem(zone_available_amount)
        zones_identify_selected_table_widget_item_list = [feat_id_table_item, feat_name_table_item, zone_available_table_item]

        for zone_id in setup_object.zones_dict:
            earmarked_amount = zones_return_string_amount_per_zone_type(setup_object, abund_details_dict, 'Z' + str(zone_id) + ' Earmarked', feat_id)
            zone_earmarked_id_table_item = QTableWidgetItem(str(earmarked_amount))
            locked_amount = zones_return_string_amount_per_zone_type(setup_object, abund_details_dict, 'Z' + str(zone_id) + ' Locked', feat_id)
            zone_locked_id_table_item = QTableWidgetItem(str(locked_amount))
            zones_identify_selected_table_widget_item_list += [zone_earmarked_id_table_item, zone_locked_id_table_item]

        feat_target = return_rounded_value(setup_object, setup_object.target_dict[feat_id][3])
        feat_target_table_item = QTableWidgetItem(feat_target)
        feat_shortfall_table_item = QTableWidgetItem(zones_return_string_shortfall(setup_object, feat_id))
        zones_identify_selected_table_widget_item_list += [feat_target_table_item, feat_shortfall_table_item]

        for colNumber in range(0, len(zones_identify_selected_table_widget_item_list)):
            zones_identify_selected_dialog.zonesIdentifySelectedTableWidget.setItem(rowNumber, colNumber, zones_identify_selected_table_widget_item_list[colNumber])


def zones_return_string_amount_per_zone_type(setup_object, abund_details_dict, zone_type, feat_id):
    decimal_places = setup_object.decimal_places
    try:
        feat_amount = abund_details_dict[zone_type][feat_id]
        feat_amount_round = round(float(feat_amount), decimal_places)
        feat_amount_string = format(feat_amount_round, '.' + str(decimal_places) + 'f')
    except KeyError:
        feat_amount = 0
        feat_amount_round = round(float(feat_amount), decimal_places)
        feat_amount_string = format(feat_amount_round, '.' + str(decimal_places) + 'f')

    return feat_amount_string


def zones_add_formatting_headings_to_table_widget(zones_identify_selected_dialog, setup_object):
    header_list = ['ID  ', 'Name  ', 'Available  ']
    for zoneID in setup_object.zones_dict:
        header_list.append('Z' + str(zoneID) + ' Earmarked  ')
        header_list.append('Z' + str(zoneID) + ' Locked     ')
    header_list.append('Target  ')
    header_list.append('Target shortfall  ')

    zones_identify_selected_dialog.zonesIdentifySelectedTableWidget.setHorizontalHeaderLabels(header_list)
    zones_identify_selected_dialog.zonesIdentifySelectedTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
    zones_identify_selected_dialog.zonesIdentifySelectedTableWidget.verticalHeader().hide()
    for aColValue in range(len(header_list)):
        zones_identify_selected_dialog.zonesIdentifySelectedTableWidget.resizeColumnToContents(aColValue)


def zones_return_string_shortfall(setup_object, feat_id):
    decimal_places = setup_object.decimal_places
    target_amount = setup_object.target_dict[feat_id][3]
    con_amount = 0

    zone_count = len(setup_object.zones_dict)
    amount_target_list_pos = 6 + (2 * zone_count)
    for row_pos_value in range(amount_target_list_pos, amount_target_list_pos + zone_count):
        con_amount += setup_object.target_dict[feat_id][row_pos_value]

    if con_amount >= target_amount:
        string_shortfall = 'Target met'
    else:
        short_value = target_amount - con_amount
        short_value_round = round(float(short_value), decimal_places)
        string_shortfall = format(short_value_round, '.' + str(decimal_places) + 'f')

    return string_shortfall
