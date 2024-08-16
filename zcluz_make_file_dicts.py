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

from itertools import combinations
from os import remove, rename, sep
from csv import reader, writer

from .cluz_make_file_dicts import return_temp_path_name, return_pc_target_value_for_target_table
from .cluz_make_file_dicts import make_lowercase_header_list
from .cluz_messages import warning_message, critical_message


def make_zones_target_dict(setup_object):
    target_dict = dict()
    target_csv_file_path = setup_object.target_path
    try:
        with open(target_csv_file_path, 'rt') as f:
            target_reader = reader(f)
            header_list = make_lowercase_header_list(next(target_reader))  # convert to lowercase, so it doesn't matter whether the headers or lowercase, uppercase or a mix

            for a_row in target_reader:
                feat_id = int(a_row[header_list.index('id')])
                feat_list = make_zones_target_dict_row_feat_list(setup_object, a_row, header_list)
                target_dict[feat_id] = feat_list

    # except ValueError:
    except KeyError:
        warning_message('Target table error', 'The Target table is incorrectly formatted. Please use the Troubleshoot all CLUZ files function to identify the problem.')
        target_dict = 'blank'

    return target_dict


def make_zones_target_dict_row_feat_list(setup_object, a_row, header_list):
    feat_name = str(a_row[header_list.index('name')])
    feat_type = int(a_row[header_list.index('type')])
    feat_spf = float(a_row[header_list.index('spf')])
    feat_target = float(a_row[header_list.index('target')])
    feat_ear_lock = float(a_row[header_list.index('ear+lock')])
    feat_total = float(a_row[header_list.index('total')])
    feat_pc_target = float(a_row[header_list.index('pc_target')])
    standard_feat_list = [feat_name, feat_type, feat_spf, feat_target, feat_ear_lock, feat_total, feat_pc_target]
    zones_feat_list = make_zones_feat_list(setup_object, a_row, header_list)
    feat_list = standard_feat_list + zones_feat_list

    return feat_list


def make_zones_feat_list(setup_object, a_row, header_list):
    zones_feat_list = list()
    for zone_id in list(setup_object.zones_dict):
        a_zone_target = float(a_row[header_list.index('z' + str(zone_id) + '_prop')])
        zones_feat_list.append(a_zone_target)

    for zone_id in list(setup_object.zones_dict):
        a_zone_target = float(a_row[header_list.index('z' + str(zone_id) + '_target')])
        zones_feat_list.append(a_zone_target)

    for zone_id in list(setup_object.zones_dict):
        a_zone_target = float(a_row[header_list.index('z' + str(zone_id) + '_ear+lock')])
        zones_feat_list.append(a_zone_target)

    return zones_feat_list


def make_zones_dict(setup_object):
    zones_dict = dict()
    zones_csv_file_path = setup_object.zones_path
    try:
        with open(zones_csv_file_path, 'rt') as f:
            zones_reader = reader(f)
            next(zones_reader)
            for a_row in zones_reader:
                zone_id = int(a_row[0])
                zone_name = a_row[1]
                zones_dict[zone_id] = zone_name

    except ValueError:
        # warning_message('Zones table error', 'The Zones table is incorrectly formatted. Please use the Troubleshoot all CLUZ files function to identify the problem.')
        zones_dict = 'blank'

    return zones_dict


def make_zones_prop_dict(setup_object):
    zones_header_name_list = make_zones_header_name_list(setup_object, '_Prop')
    target_csv_file_path = setup_object.target_path
    try:
        with open(target_csv_file_path, 'rt') as f:
            target_reader = reader(f)
            lowercase_header_list = make_lowercase_header_list(next(target_reader))
            zones_prop_dict = make_generic_zones_dict_from_target_csv(target_reader, zones_header_name_list, lowercase_header_list)

    except ValueError:
        # warning_message('Target table error', 'The Target table is incorrectly formatted. Please use the Troubleshoot all CLUZ files function to identify the problem.')
        zones_prop_dict = 'blank'

    return zones_prop_dict


def make_zones_target_zones_dict(setup_object):
    zones_header_name_list = make_zones_header_name_list(setup_object, '_Target')
    target_csv_file_path = setup_object.target_path
    try:
        with open(target_csv_file_path, 'rt') as f:
            target_reader = reader(f)
            lowercase_header_list = make_lowercase_header_list(next(target_reader))
            zones_target_dict = make_generic_zones_dict_from_target_csv(target_reader, zones_header_name_list, lowercase_header_list)

    except ValueError:
        # warning_message('Target table error', 'The Target table is incorrectly formatted. Please use the Troubleshoot all CLUZ files function to identify the problem.')
        zones_target_dict = 'blank'

    return zones_target_dict


def make_generic_zones_dict_from_target_csv(target_reader, zones_header_name_list, lowercase_header_list):
    feat_id_col_value = lowercase_header_list.index('id')
    zones_col_value_dict = make_zones_col_value_dict(lowercase_header_list, zones_header_name_list)

    generic_zones_dict = dict()
    for a_row in target_reader:
        feat_id = int(a_row[feat_id_col_value])
        for zones_header_name in zones_header_name_list:
            try:
                zones_value_dict = generic_zones_dict[zones_header_name]
            except KeyError:
                zones_value_dict = dict()
            zones_col_value = zones_col_value_dict[zones_header_name]
            zones_value_dict[feat_id] = float(a_row[zones_col_value])
            generic_zones_dict[zones_header_name] = zones_value_dict

    return generic_zones_dict


def make_zones_header_name_list(setup_object, header_suffix_text):
    header_col_num_list = list()
    for zoneID in setup_object.zones_dict:
        header_col_num_list.append('Z' + str(zoneID) + header_suffix_text)

    return header_col_num_list


def make_zones_col_value_dict(lowercase_header_list, zones_header_name_list):
    zones_col_dict = dict()
    for zonesHeaderName in zones_header_name_list:
        lowercase_zones_header_name = zonesHeaderName.lower()
        zones_col_dict[zonesHeaderName] = lowercase_header_list.index(lowercase_zones_header_name)

    return zones_col_dict


def make_zones_bound_cost_dict_from_zoneboundcost_dat(setup_object):
    zoneboundcost_dat_file_path = setup_object.input_path + sep + 'zoneboundcost.dat'
    zones_blm_value_dict = dict()
    try:
        with open(zoneboundcost_dat_file_path, 'rt') as f:
            zoneboundcost_dat_reader = reader(f)
            next(zoneboundcost_dat_reader)
            for a_row in zoneboundcost_dat_reader:
                tuple_id = (int(a_row[0]), int(a_row[1]))
                zones_blm_value_dict[tuple_id] = float(a_row[2])
    except FileNotFoundError:
        zones_blm_value_dict = make_zones_bound_cost_dict_from_scratch(setup_object)

    return zones_blm_value_dict


def make_zones_bound_cost_dict_from_scratch(setup_object):
    zones_blm_value_dict = dict()
    for a_zone_id in list(setup_object.zones_dict.keys()):
        tuple_id = (a_zone_id, a_zone_id)
        zones_blm_value_dict[tuple_id] = 0.0

    combinations_set = set(combinations(list(setup_object.zones_dict.keys()), 2))
    combinations_list = list(combinations_set)
    combinations_list.sort()
    for a_combination in combinations_list:
        tuple_id = (a_combination[0], a_combination[1])
        zones_blm_value_dict[tuple_id] = 1.0

    return zones_blm_value_dict


def update_zones_target_csv_from_target_dict(setup_object, target_dict):
    update_target_csv_success_bool = True
    target_csv_file_path = setup_object.target_path
    text_rows = list()
    with open(target_csv_file_path, 'rt') as in_file:
        target_reader = reader(in_file)
        orig_header_list = next(target_reader)
        text_rows.append(orig_header_list)
        lower_header_list = make_lowercase_header_list(orig_header_list)

        for a_row in target_reader:
            feat_id = int(a_row[lower_header_list.index('id')])
            feat_target = float(a_row[lower_header_list.index('target')])
            pc_target = return_pc_target_value_for_target_table(target_dict, feat_id, feat_target, setup_object.decimal_places)

            a_row[lower_header_list.index('ear+lock')] = target_dict[feat_id][4]
            a_row[lower_header_list.index('total')] = target_dict[feat_id][5]
            a_row[lower_header_list.index('pc_target')] = pc_target

            zone_count = len(setup_object.zones_dict)
            zone_id_list = list(setup_object.zones_dict)
            for zone_id in setup_object.zones_dict:
                value_target_list_pos = 6 + (2 * zone_count) + zone_id_list.index(zone_id) + 1
                a_row[lower_header_list.index('z' + str(zone_id) + '_ear+lock')] = target_dict[feat_id][value_target_list_pos]
            text_rows.append(a_row)
    try:
        with open(target_csv_file_path, 'w', newline='', encoding='utf-8') as out_file:
            target_writer = writer(out_file)
            for b_row in text_rows:
                target_writer.writerow(b_row)
    except PermissionError:
        critical_message('Update error', 'Cannot update target csv file. This is often because the file is open in another software package.')
        update_target_csv_success_bool = False

    return update_target_csv_success_bool


# Add data to target table from Add data from Vec, raster, csv files #######################################

def zones_add_features_to_target_csv_file(setup_object, feat_id_list):
    temp_target_path = return_temp_path_name(setup_object.target_path, 'csv')
    with open(temp_target_path, 'w', newline='', encoding='utf-8') as temp_target_file:
        temp_target_writer = writer(temp_target_file)
        with open(setup_object.target_path, 'rt') as f:
            target_reader = reader(f)
            target_file_header_list = next(target_reader)
            temp_target_writer.writerow(target_file_header_list)
            for row in target_reader:
                temp_target_writer.writerow(row)

            add_target_list = feat_id_list
            add_target_list.sort()
            for featID in add_target_list:
                row = zones_make_new_row_target_csv_from_add_target_list(target_file_header_list, featID)
                temp_target_writer.writerow(row)

    temp_target_file.close()
    remove(setup_object.target_path)
    rename(temp_target_path, setup_object.target_path)


def zones_make_new_row_target_csv_from_add_target_list(target_file_header_list, feat_id):
    new_row_list = [''] * len(target_file_header_list)
    for a_target_header_col in range(0, len(target_file_header_list)):
        a_target_header_name = target_file_header_list[a_target_header_col]
        if a_target_header_name.lower() == 'id':
            new_row_list[a_target_header_col] = str(feat_id)
        elif a_target_header_name.lower() == 'name':
            new_row_list[a_target_header_col] = 'blank'
        elif a_target_header_name.lower() == 'ear+lock':
            new_row_list[a_target_header_col] = '0'
        elif a_target_header_name.lower() == 'total':
            new_row_list[a_target_header_col] = '0'
        elif a_target_header_name.lower() == 'pc_target':
            new_row_list[a_target_header_col] = '-1'
        elif a_target_header_name.lower() in ['type', 'target', 'spf']:
            new_row_list[a_target_header_col] = '0'
        elif '_prop' in a_target_header_name.lower():
            new_row_list[a_target_header_col] = '1'
        elif '_target' in a_target_header_name.lower():
            new_row_list[a_target_header_col] = '0'
        elif '_ear+lock' in a_target_header_name.lower():
            new_row_list[a_target_header_col] = '0'
        elif '_e+l_amount' in a_target_header_name.lower():
            new_row_list[a_target_header_col] = '0'

    return new_row_list
