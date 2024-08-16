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

from .cluz_make_file_dicts import return_pc_target_value_for_target_table

# Update Zones target table ##########


def return_zones_earlock_amount_tot_dict(setup_object):
    zones_earlock_amount_tot_dict = dict()

    for zoneID in list(setup_object.zones_dict):
        pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
        pu_features = pu_layer.getFeatures()
        pu_id_field = pu_layer.fields().indexFromName('Unit_ID')
        status_field_name = 'Z' + str(zoneID) + '_Status'
        pu_status_field = pu_layer.fields().indexFromName(status_field_name)
        a_zones_earlock_amount_tot_dict = dict()

        for puFeature in pu_features:
            pu_attributes = puFeature.attributes()
            pu_id = pu_attributes[pu_id_field]
            pu_status = pu_attributes[pu_status_field]
            try:
                pu_abund_dict = setup_object.abund_pu_key_dict[pu_id]
            except KeyError:
                pu_abund_dict = dict()
            for feat_id in pu_abund_dict:
                try:
                    ear_lock_amount, tot_amount = a_zones_earlock_amount_tot_dict[feat_id]
                except KeyError:
                    ear_lock_amount, tot_amount = [0, 0]
                feat_amount = pu_abund_dict[feat_id]
                new_tot_amount = tot_amount + feat_amount
                if pu_status == 'Earmarked' or pu_status == 'Locked':
                    new_ear_lock_amount = ear_lock_amount + feat_amount
                else:
                    new_ear_lock_amount = ear_lock_amount
                a_zones_earlock_amount_tot_dict[feat_id] = [new_ear_lock_amount, new_tot_amount]

        zones_earlock_amount_tot_dict[zoneID] = a_zones_earlock_amount_tot_dict

    return zones_earlock_amount_tot_dict


def update_zones_ear_lock_tot_fields_target_dict(setup_object, zones_ear_lock_tot_dict):
    target_dict = setup_object.target_dict
    for feat_id in target_dict:
        target_list = target_dict[feat_id]
        try:
            tot_value = zones_ear_lock_tot_dict[list(zones_ear_lock_tot_dict)[1]][feat_id][1]  # This value is in every zone dict, so just chose the Z1 dict
        except KeyError:
            tot_value = 0
        target_list[5] = tot_value

        comb_ear_lock_value = 0
        for zone_id in list(setup_object.zones_dict):
            zone_id_additional_list_pos_value = list(setup_object.zones_dict).index(zone_id) + 1
            value_target_list_pos = 6 + (2 * len(setup_object.zones_dict)) + zone_id_additional_list_pos_value
            try:
                zone_ear_lock_amount = zones_ear_lock_tot_dict[zone_id][feat_id][0]
                feat_zone_prop = setup_object.zones_prop_dict['Z' + str(zone_id) + '_Prop'][feat_id]
                zone_ear_lock_value = zone_ear_lock_amount * feat_zone_prop
            except KeyError:
                zone_ear_lock_value = 0
            target_list[value_target_list_pos] = zone_ear_lock_value
            comb_ear_lock_value += zone_ear_lock_value
        target_list[4] = comb_ear_lock_value

        feat_target = target_list[3]
        pc_target = return_pc_target_value_for_target_table(target_dict, feat_id, feat_target, setup_object.decimal_places)
        target_list[6] = pc_target

        target_dict[feat_id] = target_list

    return target_dict
