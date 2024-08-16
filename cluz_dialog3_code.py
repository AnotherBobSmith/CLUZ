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

from qgis.core import QgsVectorLayer

from .cluz_checkup import return_feat_id_set_from_abund_pu_key_dict
from .cluz_functions3 import rem_features_from_puvspr2, rem_features_from_target_csv_dict
from .cluz_make_file_dicts import make_target_dict, make_abundance_pu_key_dict
from .cluz_messages import critical_message, success_message
from .zcluz_make_file_dicts import make_zones_target_dict, return_pc_target_value_for_target_table


# Remove features ##########################################################################################

def create_feature_list_dict(setup_object):
    target_feat_id_set = set(setup_object.target_dict.keys())
    abund_feat_id_set = return_feat_id_set_from_abund_pu_key_dict(setup_object)
    feat_id_set = target_feat_id_set.union(abund_feat_id_set)
    feat_id_list = list(feat_id_set)
    feat_id_list.sort()

    feat_string_list = list()
    missing_feat_string_list = list()  # This is for features that are missing from one or other of the target or abund tables
    feat_string_dict = dict()
    for aFeat in feat_id_list:
        try:
            a_string = str(aFeat) + ' - ' + setup_object.target_dict[aFeat][0]
            if aFeat in abund_feat_id_set:
                pass
            else:
                a_string = '*Target table only* ' + a_string
        except KeyError:
            a_string = '*Abundance table only * ' + str(aFeat) + ' - blank'
        if a_string[0] == '*':
            missing_feat_string_list.append(a_string)
        else:
            feat_string_list.append(a_string)
        feat_string_dict[a_string] = aFeat
    final_feat_string_list = missing_feat_string_list + feat_string_list

    return final_feat_string_list, feat_string_dict


def remove_selected_features_from_target_abund_files(remove_dialog, setup_object, feat_string_dict):
    selected_feat_id_list = [feat_string_dict[item.text()] for item in remove_dialog.featListWidget.selectedItems()]
    selected_feat_id_set = set(selected_feat_id_list)
    selected_feat_id_list_length = len(selected_feat_id_list)
    if selected_feat_id_list_length > 0:
        rem_features_from_puvspr2(setup_object, selected_feat_id_set)
        setup_object.abund_pu_key_dict = make_abundance_pu_key_dict(setup_object)

        rem_features_from_target_csv_dict(setup_object, selected_feat_id_set)
        if setup_object.analysis_type != 'MarxanWithZones':
            setup_object.target_dict = make_target_dict(setup_object)
        else:
            setup_object.target_dict = make_zones_target_dict(setup_object)

        success_message('Task successfully completed: ', str(selected_feat_id_list_length) + ' features have been removed.')
        remove_dialog.close()
    else:
        critical_message('No features selected', 'No features were selected and so no changes have been made.')
        remove_dialog.close()


# Update target table ##################################################

def update_con_tot_fields_target_dict(setup_object, new_con_tot_dict):
    target_dict = setup_object.target_dict
    decimal_places = setup_object.decimal_places
    for feat_id in target_dict:
        target_list = target_dict[feat_id]
        feat_target = target_list[3]
        try:
            target_list[4] = new_con_tot_dict[feat_id][0]
        except KeyError:
            target_list[4] = 0
        try:
            target_list[5] = new_con_tot_dict[feat_id][1]
        except KeyError:
            target_list[5] = 0

        pc_target = return_pc_target_value_for_target_table(target_dict, feat_id, feat_target, decimal_places)
        target_list[6] = pc_target

        target_dict[feat_id] = target_list

    return target_dict


def return_con_tot_dict(setup_object):
    amount_con_tot_dict = dict()

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_features = pu_layer.getFeatures()
    pu_id_field = pu_layer.fields().indexFromName('Unit_ID')
    pu_status_field = pu_layer.fields().indexFromName('Status')

    for puFeature in pu_features:
        pu_attributes = puFeature.attributes()
        unit_id = pu_attributes[pu_id_field]
        unit_status = pu_attributes[pu_status_field]
        try:
            pu_abund_dict = setup_object.abund_pu_key_dict[unit_id]
            for featID in pu_abund_dict:
                feat_amount = pu_abund_dict[featID]
                try:
                    con_amount, tot_amount = amount_con_tot_dict[featID]
                except KeyError:
                    con_amount, tot_amount = [0, 0]

                tot_amount += feat_amount
                if unit_status == 'Earmarked' or unit_status == 'Conserved':
                    con_amount += feat_amount

                amount_con_tot_dict[featID] = [con_amount, tot_amount]
        except KeyError:
            pass

    return amount_con_tot_dict

# Update target table ############################################################
