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

import qgis
from qgis.core import QgsVectorLayer, QgsExpression, QgsFeatureRequest
from qgis.utils import iface

from .cluz_messages import success_message, zones_check_change_earmarked_to_available_pu, warning_message
from .cluz_display import update_pu_layer_to_show_changes_by_shifting_extent

from .zcluz_dialog3 import recalc_update_zones_target_table_details
from .zcluz_make_file_dicts import update_zones_target_csv_from_target_dict


def return_zones_main_targets_met_tuple(setup_object):
    num_targets = 0
    num_targets_met = 0
    target_dict = setup_object.target_dict
    for a_feat in target_dict:
        target_list = target_dict[a_feat]
        target_amount = target_list[3]
        con_amount = 0
        for zone_position in range(1, len(setup_object.zones_dict)):
            con_list_pos = 6 + (2 * len(setup_object.zones_dict)) + zone_position
            con_amount += target_list[con_list_pos]
        if target_amount > 0:
            num_targets += 1
            if con_amount >= target_amount:
                num_targets_met += 1

    return num_targets_met, num_targets


def return_zones_targets_met_tuple(setup_object, selected_zone_id):
    num_zone_targets = 0
    num_zones_targets_met = 0
    target_dict = setup_object.target_dict
    zone_id_additional_list_pos_value = list(setup_object.zones_dict).index(selected_zone_id) + 1
    for a_feat in target_dict:
        target_list = target_dict[a_feat]
        target_list_pos = 6 + (1 * len(setup_object.zones_dict)) + zone_id_additional_list_pos_value
        target_amount = target_list[target_list_pos]
        con_list_pos = 6 + (2 * len(setup_object.zones_dict)) + zone_id_additional_list_pos_value
        con_amount = target_list[con_list_pos]
        if target_amount > 0:
            num_zone_targets += 1
            if con_amount >= target_amount:
                num_zones_targets_met += 1

    return num_zones_targets_met, num_zone_targets


def return_selected_zone_id_from_change_status_panel(zones_change_status_dialog):
    zone_string = str(zones_change_status_dialog.zonesNameComboBox.currentText())
    zone_id = int(zone_string.split(' - ')[0][5:])

    return zone_id


def return_before_after_pu_zones_status_dicts(setup_object, change_status_type, change_locked_pus_bool, selected_zone_id):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    qgis.utils.iface.setActiveLayer(pu_layer)
    pu_layer = qgis.utils.iface.activeLayer()
    pu_layer.startEditing()
    before_pu_zones_status_dict = make_before_pu_zones_status_dict(setup_object)
    after_pu_zones_status_dict = make_after_pu_zones_status_dict(before_pu_zones_status_dict, selected_zone_id, change_status_type, change_locked_pus_bool)

    return before_pu_zones_status_dict, after_pu_zones_status_dict


def make_before_pu_zones_status_dict(setup_object):
    before_pu_zones_status_dict = dict()

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    qgis.utils.iface.setActiveLayer(pu_layer)
    pu_layer = qgis.utils.iface.activeLayer()
    provider = pu_layer.dataProvider()
    id_field_order = provider.fieldNameIndex('Unit_ID')

    selected_pus = pu_layer.selectedFeatures()
    pu_layer.startEditing()

    for a_pu in selected_pus:
        pu_zone_status_dict = dict()
        pu_id = a_pu.attributes()[id_field_order]
        for zoneID in list(setup_object.zones_dict):
            status_field_name = 'Z' + str(zoneID) + '_Status'
            zone_status_field_order = provider.fieldNameIndex(status_field_name)
            zone_status = a_pu.attributes()[zone_status_field_order]
            pu_zone_status_dict[zoneID] = zone_status
        before_pu_zones_status_dict[pu_id] = pu_zone_status_dict

    return before_pu_zones_status_dict


def make_after_pu_zones_status_dict(before_pu_zones_status_dict, selected_zone_id, change_status_type, change_exc_lock_pus_bool):
    after_pu_zones_status_dict = dict()
    for pu_id in before_pu_zones_status_dict:
        before_pu_id_zone_status_dict = before_pu_zones_status_dict[pu_id]
        other_zones_status_list = make_other_zones_status_list(before_pu_id_zone_status_dict, selected_zone_id)
        orig_zone_status_type = before_pu_id_zone_status_dict[selected_zone_id]
        change_status_p_us_bool = check_change_status_pus_bool(orig_zone_status_type, change_status_type, other_zones_status_list)

        if change_exc_lock_pus_bool is False and change_status_p_us_bool is False:
            pass
        else:
            after_pu_id_zone_status_dict = dict()
            after_pu_id_zone_status_dict[selected_zone_id] = change_status_type
            for zoneID in before_pu_id_zone_status_dict:
                if zoneID != selected_zone_id:
                    orig_other_zone_status_type = before_pu_id_zone_status_dict[zoneID]
                    new_other_zone_status_type = return_other_zone_status_type(change_status_type, orig_other_zone_status_type)
                    after_pu_id_zone_status_dict[zoneID] = new_other_zone_status_type
            after_pu_zones_status_dict[pu_id] = after_pu_id_zone_status_dict

    return after_pu_zones_status_dict


def check_change_status_pus_bool(orig_zone_status_type, change_status_type, other_zones_status_list):
    change_status_pus_bool = True
    if orig_zone_status_type == change_status_type:
        change_status_pus_bool = False
    if orig_zone_status_type == 'Excluded' or orig_zone_status_type == 'Locked':
        change_status_pus_bool = False
    if change_status_type == 'Earmarked' and 'Locked' in other_zones_status_list:
        change_status_pus_bool = False

    return change_status_pus_bool


def return_other_zone_status_type(change_status_type, orig_other_zone_status_type):
    change_zone_status_type_dict = dict()
    change_zone_status_type_dict[('Unassigned', 'Unassigned')] = 'Unassigned'
    change_zone_status_type_dict[('Unassigned', 'Earmarked')] = 'Earmarked'
    change_zone_status_type_dict[('Unassigned', 'Excluded')] = 'Excluded'
    change_zone_status_type_dict[('Unassigned', 'Locked')] = 'Unassigned'
    change_zone_status_type_dict[('Earmarked', 'Unassigned')] = 'Unassigned'
    change_zone_status_type_dict[('Earmarked', 'Earmarked')] = 'Unassigned'
    change_zone_status_type_dict[('Earmarked', 'Excluded')] = 'Excluded'
    change_zone_status_type_dict[('Earmarked', 'Locked')] = 'Unassigned'
    change_zone_status_type_dict[('Excluded', 'Unassigned')] = 'Unassigned'
    change_zone_status_type_dict[('Excluded', 'Earmarked')] = 'Earmarked'
    change_zone_status_type_dict[('Excluded', 'Excluded')] = 'Excluded'
    change_zone_status_type_dict[('Excluded', 'Locked')] = 'Locked'
    change_zone_status_type_dict[('Locked', 'Unassigned')] = 'Unassigned'
    change_zone_status_type_dict[('Locked', 'Earmarked')] = 'Unassigned'
    change_zone_status_type_dict[('Locked', 'Excluded')] = 'Excluded'
    change_zone_status_type_dict[('Locked', 'Locked')] = 'Unassigned'
    new_other_zone_status_type = change_zone_status_type_dict[(change_status_type, orig_other_zone_status_type)]

    return new_other_zone_status_type


def make_other_zones_status_list(before_change_pu_zones_status_dict, selected_zone_id):
    other_zones_status_list = list()
    for zoneID in before_change_pu_zones_status_dict:
        if zoneID != selected_zone_id:
            other_zones_status_list.append(before_change_pu_zones_status_dict[zoneID])

    return other_zones_status_list


def make_zones_selected_status_balance_dict(before_pu_zones_status_dict, after_pu_zones_status_dict):
    zones_selected_status_balance_dict = dict()
    for pu_id in after_pu_zones_status_dict:
        try:
            pu_id_zone_status_balance_dict = zones_selected_status_balance_dict[pu_id]
        except KeyError:
            pu_id_zone_status_balance_dict = dict()
        before_pu_status_dict = before_pu_zones_status_dict[pu_id]
        after_pu_status_dict = after_pu_zones_status_dict[pu_id]
        for zone_id in after_pu_status_dict:
            before_status = before_pu_status_dict[zone_id]
            after_status = after_pu_status_dict[zone_id]
            pu_id_zone_status_balance_dict[zone_id] = return_status_balance_value(before_status, after_status)
        zones_selected_status_balance_dict[pu_id] = pu_id_zone_status_balance_dict

    return zones_selected_status_balance_dict


def return_status_balance_value(before_status, after_status):
    recode_dict = {'Unassigned': False, 'Earmarked': True, 'Excluded': False, 'Locked': True}
    before_bool = recode_dict[before_status]
    after_bool = recode_dict[after_status]

    balance_value = 0
    if before_bool and after_bool is False:
        balance_value = -1
    elif before_bool is False and after_bool:
        balance_value = 1

    return balance_value


def change_zones_status_pu_layer(setup_object, after_pu_zones_status_dict):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    qgis.utils.iface.setActiveLayer(pu_layer)
    pu_layer = qgis.utils.iface.activeLayer()
    provider = pu_layer.dataProvider()
    id_field_order = provider.fieldNameIndex('Unit_ID')
    selected_pu_list = list()

    selected_pus = pu_layer.selectedFeatures()
    pu_layer.startEditing()

    for a_pu in selected_pus:
        pu_row = a_pu.id()
        selected_pu_list.append(pu_row)
        pu_id = a_pu.attributes()[id_field_order]
        try:
            after_pu_id_zones_status_dict = after_pu_zones_status_dict[pu_id]
            for zone_id in after_pu_id_zones_status_dict:
                zone_status_field_name = 'Z' + str(zone_id) + '_Status'
                zone_status_field_order = provider.fieldNameIndex(zone_status_field_name)
                final_change_status_type = after_pu_id_zones_status_dict[zone_id]
                pu_layer.changeAttributeValue(pu_row, zone_status_field_order, final_change_status_type)
        except KeyError:
            pass

    setup_object.selectedPUList = selected_pu_list
    pu_layer.commitChanges()
    pu_layer.removeSelection()
    update_pu_layer_to_show_changes_by_shifting_extent()


def calc_zones_change_abund_amount_dict(setup_object, zones_selected_status_balance_dict):
    zones_change_amount_dict = dict()
    for pu_id in zones_selected_status_balance_dict:
        pu_id_zones_status_balance_dict = zones_selected_status_balance_dict[pu_id]
        for zoneID in pu_id_zones_status_balance_dict:
            try:
                zone_id_change_abund_dict = zones_change_amount_dict[zoneID]
            except KeyError:
                zone_id_change_abund_dict = dict()
            try:
                pu_abund_dict = setup_object.abund_pu_key_dict[pu_id]
            except KeyError:
                pu_abund_dict = dict()  # just to leave things blank
            for feat_id in pu_abund_dict:
                abund_value = pu_abund_dict[feat_id]
                try:
                    running_change = zone_id_change_abund_dict[feat_id]
                except KeyError:
                    running_change = 0
                change_amount = abund_value * pu_id_zones_status_balance_dict[zoneID]
                running_change += change_amount
                zone_id_change_abund_dict[feat_id] = running_change
            zones_change_amount_dict[zoneID] = zone_id_change_abund_dict

    return zones_change_amount_dict


def update_zones_target_dict_with_changes(setup_object, zones_change_abund_dict):
    target_dict = setup_object.target_dict
    for zone_id in zones_change_abund_dict:
        focal_zone_change_abund_dict = zones_change_abund_dict[zone_id]
        for feat_id in focal_zone_change_abund_dict:
            target_list = setup_object.target_dict[feat_id]

            zone_id_additional_list_pos_value = list(setup_object.zones_dict).index(zone_id) + 1
            change_amount = zones_change_abund_dict[zone_id][feat_id]
            change_value = change_amount * setup_object.zones_prop_dict['Z' + str(zone_id) + '_Prop'][feat_id]
            earlock_target_list_pos = 6 + (2 * len(setup_object.zones_dict)) + zone_id_additional_list_pos_value
            old_zone_earlock_value = target_list[earlock_target_list_pos]
            new_zone_earlock_value = old_zone_earlock_value + change_value
            target_list[earlock_target_list_pos] = new_zone_earlock_value

            target_dict[feat_id] = target_list

    for feat_id in target_dict:
        combined_earlock_value = return_combined_earlock_values(setup_object, feat_id)
        target_list = setup_object.target_dict[feat_id]
        target_list[4] = combined_earlock_value
        target_dict[feat_id] = target_list

    return target_dict


def return_combined_earlock_values(setup_object, feat_id):
    combined_earlock_value = 0
    target_list = setup_object.target_dict[feat_id]
    for zone_id in setup_object.zones_dict:
        zone_id_additional_list_pos_value = list(setup_object.zones_dict).index(zone_id) + 1
        earlock_value_target_list_pos = 6 + (2 * len(setup_object.zones_dict)) + zone_id_additional_list_pos_value
        zone_earlock_value = target_list[earlock_value_target_list_pos]
        combined_earlock_value += zone_earlock_value

    return combined_earlock_value


def zones_select_undo_planning_units(setup_object):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    qgis.utils.iface.setActiveLayer(pu_layer)
    pu_layer = qgis.utils.iface.activeLayer()
    pu_layer.selectByIds(setup_object.selectedPUList)


# # ####################################################################

def zones_change_best_to_earmarked_pus(setup_object):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_provider = pu_layer.dataProvider()
    status_field_order_dict = make_status_field_order_dict(setup_object, pu_provider)
    best_field_order = pu_provider.fieldNameIndex('Best')

    if best_field_order == -1:
        warning_message('Incorrect format', 'The planning unit layer has no field named Best (which is produced by running Marxan with Zones). This process will terminate.')
    else:
        zones_change_zones_status_from_best_field(setup_object, pu_layer, status_field_order_dict, best_field_order)
        recalc_update_zones_target_table_details(setup_object)
        update_zones_target_csv_from_target_dict(setup_object, setup_object.target_dict)
        success_message('Process completed', 'Planning units that were selected in the Best portfolio for each zone now have Earmarked status and the target table has been updated accordingly.')
    update_pu_layer_to_show_changes_by_shifting_extent()


def make_status_field_order_dict(setup_object, pu_provider):
    status_field_order_dict = dict()
    for zoneID in setup_object.zones_dict:
        status_field_order_dict[zoneID] = pu_provider.fieldNameIndex('Z' + str(zoneID) + '_Status')

    return status_field_order_dict


def zones_change_zones_status_from_best_field(setup_object, pu_layer, status_field_order_dict, best_field_order):
    pu_layer.startEditing()
    pu_features = pu_layer.getFeatures()
    for puFeature in pu_features:
        pu_row = puFeature.id()
        pu_best_zone_value = puFeature.attributes()[best_field_order]
        for zone_id in setup_object.zones_dict:
            pu_zone_status = puFeature.attributes()[status_field_order_dict[zone_id]]
            if pu_zone_status == 'Unassigned' and pu_best_zone_value == zone_id:
                pu_layer.changeAttributeValue(pu_row, status_field_order_dict[zone_id], 'Earmarked')
            if pu_zone_status == 'Earmarked' and pu_best_zone_value != zone_id:
                pu_layer.changeAttributeValue(pu_row, status_field_order_dict[zone_id], 'Unassigned')

    pu_layer.commitChanges()


def zones_change_earmarked_to_available_pus(setup_object):
    pu_layer = QgsVectorLayer(setup_object.pu_path, "Planning units", "ogr")
    pu_provider = pu_layer.dataProvider()
    status_field_order_dict = make_status_field_order_dict(setup_object, pu_provider)
    change_bool = zones_check_change_earmarked_to_available_pu()

    if change_bool:
        zones_updated_zones_fields_from_earmarked_to_unassigned(setup_object, pu_layer, status_field_order_dict)
        recalc_update_zones_target_table_details(setup_object)
        update_zones_target_csv_from_target_dict(setup_object, setup_object.target_dict)
        success_message('Process completed', 'Planning units with Earmarked status in each zone have been changed to Unassigned status and the target table has been updated accordingly.')
    update_pu_layer_to_show_changes_by_shifting_extent()


def zones_updated_zones_fields_from_earmarked_to_unassigned(setup_object, pu_layer, status_field_order_dict):
    pu_layer.startEditing()
    pu_features = pu_layer.getFeatures()
    for puFeature in pu_features:
        pu_row = puFeature.id()
        for zone_id in setup_object.zones_dict:
            pu_zone_status = puFeature.attributes()[status_field_order_dict[zone_id]]
            if pu_zone_status == 'Earmarked':
                pu_layer.changeAttributeValue(pu_row, status_field_order_dict[zone_id], 'Unassigned')

    pu_layer.commitChanges()
