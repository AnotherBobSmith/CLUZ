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

from qgis.core import QgsVectorLayer, NULL

from csv import reader, writer
from os import remove, rename, sep

from .cluz_messages import clear_progress_bar, info_message, make_progress_bar, warning_message, set_progress_bar_value
from .cluz_make_file_dicts import make_target_dict, return_temp_path_name
from .cluz_setup import check_status_object_values, create_and_check_cluz_files

from .zcluz_functions3 import zones_check_pu_shape_file_pu_status_value, check_zones_field_status_list_for_conflicts, check_zones_fields_target_csv_file
from .zcluz_make_file_dicts import make_zones_target_dict


# Remove features ##################################################################################


def rem_features_from_puvspr2(setup_object, selected_feat_id_set):
    puvspr2_path = setup_object.input_path + sep + 'puvspr2.dat'
    temp_puvspr2_path = return_temp_path_name(puvspr2_path, 'dat')
    with open(temp_puvspr2_path, 'w', newline='', encoding='utf-8') as out_file:
        puvspr2_writer = writer(out_file)
        puvspr2_writer.writerow(['species', 'pu', 'amount'])

        with open(puvspr2_path, 'rt') as f:
            puvspr2_reader = reader(f)
            next(puvspr2_reader)
            for row in puvspr2_reader:
                if int(row[0]) not in selected_feat_id_set:
                    puvspr2_writer.writerow(row)

        out_file.close()
        remove(puvspr2_path)
        rename(temp_puvspr2_path, puvspr2_path)


def rem_features_from_target_csv_dict(setup_object, selected_feat_id_set):
    temp_target_path = return_temp_path_name(setup_object.target_path, 'csv')
    with open(temp_target_path, 'w', newline='', encoding='utf-8') as out_file:
        temp_target_writer = writer(out_file)

        with open(setup_object.target_path, 'rt') as f:
            target_reader = reader(f)
            row_header = True
            for row in target_reader:
                if row_header:
                    temp_target_writer.writerow(row)
                    row_header = False
                else:
                    feat_id = int(row[0])
                    if feat_id in selected_feat_id_set:
                        pass
                    else:
                        temp_target_writer.writerow(row)

    out_file.close()
    remove(setup_object.target_path)
    rename(temp_target_path, setup_object.target_path)

# Troubleshoot ##################################################################################


def trouble_shoot_cluz_files(setup_object):
    setup_object = check_status_object_values(setup_object)
    setup_object = create_and_check_cluz_files(setup_object)

    target_error_set, target_feat_id_set = check_target_csv_file(setup_object)
    if setup_object.analysis_type == 'MarxanWithZones':
        target_error_set = check_zones_fields_target_csv_file(setup_object)
    puvspr2_abund_error_set, puvspr2_abund_error_row_set, puvspr2_pu_id_set, puvspr2_feat_id_set, puvspr2_row_num = check_abund_table_dat_file(setup_object)
    shape_error_set, pu_pu_id_set, duplicate_id_text = check_pu_shape_file(setup_object)
    id_values_not_duplicated = check_id_values_not_duplicated(target_feat_id_set, puvspr2_feat_id_set, puvspr2_pu_id_set, pu_pu_id_set)

    push_target_table_error_messages(target_error_set)
    push_abund_table_file_error_messages(puvspr2_abund_error_set)
    push_abund_table_row_error_messages(puvspr2_abund_error_row_set)
    push_pu_shape_file_error_messages(shape_error_set, duplicate_id_text)

    combined_error_set = target_error_set | puvspr2_abund_error_set | puvspr2_abund_error_row_set | shape_error_set

    if len(combined_error_set) == 0 and id_values_not_duplicated:
        if setup_object.analysis_type != 'MarxanWithZones':
            make_target_dict(setup_object)
        else:
            make_zones_target_dict(setup_object)
        info_message('Status: ', 'no problems were found and the Target table has been updated to ensure it reflects the current data.')


def check_target_csv_file(setup_object):
    target_csv_file_path = setup_object.target_path
    feat_id_list = list()

    with open(target_csv_file_path, 'rt') as f:
        count_reader = reader(f)
        row_total_count = len(list(count_reader))

    progress_bar = make_progress_bar('Processing target file')
    row_count = 1

    with open(target_csv_file_path, 'rt') as f:
        target_reader = reader(f)
        orig_header_list = next(target_reader)
        header_list = list()  # convert to lowercase so it doesn't matter whether the headers or lowercase, uppercase or a mix
        for aHeader in orig_header_list:
            header_list.append(aHeader.lower())

        target_error_set = set()
        for aRow in target_reader:
            set_progress_bar_value(progress_bar, row_count, row_total_count)
            row_count += 1

            feat_id_string = aRow[header_list.index('id')]
            feat_name_string = aRow[header_list.index('name')]
            feat_type_string = aRow[header_list.index('type')]
            feat_spf_string = aRow[header_list.index('spf')]
            feat_target_string = aRow[header_list.index('target')]
            if setup_object.analysis_type != 'MarxanWithZones':
                feat_conserved_string = aRow[header_list.index('ear+cons')]
            else:
                feat_conserved_string = aRow[header_list.index('ear+lock')]
            feat_total_string = aRow[header_list.index('total')]
            feat_pc_target_string = aRow[header_list.index('pc_target')]

            feat_id_list, target_error_set = check_feat_id_string(feat_id_list, feat_id_string, target_error_set)
            target_error_set = check_feat_name_string(feat_name_string, target_error_set)
            target_error_set = check_feat_type_string(feat_type_string, target_error_set)
            target_error_set = check_feat_spf_string(feat_spf_string, target_error_set)
            target_error_set = check_feat_target_string(feat_target_string, target_error_set)
            target_error_set = check_feat_conserved_string(feat_conserved_string, target_error_set)
            target_error_set = check_feat_total_string(feat_total_string, target_error_set)
            target_error_set = check_feat_pc_target_string(feat_pc_target_string, target_error_set)

        target_error_set = check_for_duplicate_feat_i_ds(feat_id_list, target_error_set)

    clear_progress_bar()

    return target_error_set, set(feat_id_list)


def check_feat_id_string(feat_id_list, feat_id_string, error_set):
    if feat_id_string == '':
        error_set.add('featIDBlank')
    else:
        try:
            feat_id_list.append(int(feat_id_string))
            if int(feat_id_string) < 0:
                error_set.add('featIDNotInt')
        except ValueError:
            error_set.add('featIDNotInt')

    return feat_id_list, error_set


def check_feat_name_string(feat_name_string, error_set):
    if feat_name_string == '':
        error_set.add('featNameBlank')

    feat_name_string_is_a_number_bool = False
    try:
        float(feat_name_string)
        feat_name_string_is_a_number_bool = True
    except ValueError:
        pass

    if feat_name_string_is_a_number_bool is False and any(i.isdigit() for i in feat_name_string):
        error_set.add('featNameWrongFormat')

    return error_set


def check_feat_type_string(feat_type_string, error_set):
    if feat_type_string == '':
        error_set.add('featTypeBlank')
    else:
        try:
            int(feat_type_string)
            if int(feat_type_string) < 0:
                error_set.add('featTypeNotInt')
        except ValueError:
            error_set.add('featTypeNotInt')

    return error_set


def check_feat_spf_string(feat_spf_string, error_set):
    if feat_spf_string == '':
        error_set.add('featSpfBlank')
    else:
        try:
            float(feat_spf_string)
            if float(feat_spf_string) < 0:
                error_set.add('featSpfNotFloat')
        except ValueError:
            error_set.add('featSpfNotFloat')

    return error_set


def check_feat_target_string(feat_target_string, error_set):
    if feat_target_string == '':
        error_set.add('featTargetBlank')
    else:
        try:
            float(feat_target_string)
            if float(feat_target_string) < 0:
                error_set.add('featTargetNotFloat')
        except ValueError:
            error_set.add('featTargetNotFloat')

    return error_set


def check_feat_conserved_string(feat_conserved_string, error_set):
    if feat_conserved_string == '':
        error_set.add('featConservedBlank')
    else:
        try:
            if float(feat_conserved_string) < 0:
                error_set.add('featConservedNotFloat')
        except ValueError:
            error_set.add('featConservedNotFloat')

    return error_set


def check_feat_total_string(feat_total_string, error_set):
    if feat_total_string == '':
        error_set.add('featTotalBlank')
    else:
        try:
            if float(feat_total_string) < 0:
                error_set.add('featTotalNotFloat')
        except ValueError:
            error_set.add('featTotalNotFloat')

    return error_set


def check_feat_pc_target_string(feat_pc_target_string, error_set):
    if feat_pc_target_string == '':
        error_set.add('featPc_TargetBlank')
    elif feat_pc_target_string == '-1':
        pass
    else:
        try:
            if float(feat_pc_target_string) < 0:
                error_set.add('featPc_TargetNotFloat')
        except ValueError:
            error_set.add('featPc_TargetNotFloat')

    return error_set


def check_for_duplicate_feat_i_ds(feat_id_list, error_set):
    if len(feat_id_list) != len(set(feat_id_list)):
        error_set.add('duplicateFeatID')

    return error_set


def check_id_values_not_duplicated(target_feat_id_set, puvspr2_feat_id_set, puvspr2_pu_id_set, pu_pu_id_set):
    id_values_not_duplicated = True
    id_values_not_duplicated = check_ids_match_in_target_table_and_puvspr2(target_feat_id_set, puvspr2_feat_id_set, id_values_not_duplicated)
    id_values_not_duplicated = check_ids_match_in_pu_layer_and_puvspr2(puvspr2_pu_id_set, pu_pu_id_set, id_values_not_duplicated)

    return id_values_not_duplicated


def push_target_table_error_messages(target_error_set):
    for anError in target_error_set:
        if anError == 'featIDBlank':
            warning_message('Target Table: ', 'at least one of the Feature ID values is blank.')
        if anError == 'featIDNotInt':
            warning_message('Target Table: ', 'at least one of the Feature ID values is not a positive integer.')
        if anError == 'featNameBlank':
            warning_message('Target Table: ', 'at least one of the Name values is blank.')
        if anError == 'featTypeBlank':
            warning_message('Target Table: ', 'at least one of the Type values is blank.')
        if anError == 'featTypeNotInt':
            warning_message('Target Table: ', 'at least one of the Type values is not a positive integer.')
        if anError == 'featSpfBlank':
            warning_message('Target Table: ', 'at least one of the SPF values is blank.')
        if anError == 'featSpfNotFloat':
            warning_message('Target Table: ', 'at least one of the SPF values is not a positive number.')
        if anError == 'featTargetBlank':
            warning_message('Target Table: ', 'at least one of the Target values is blank.')
        if anError == 'featTargetNotFloat':
            warning_message('Target Table: ', 'at least one of the Target values is not a positive number.')
        if anError == 'featConservedBlank':
            warning_message('Target Table: ', 'at least one of the Conserved values is blank.')
        if anError == 'featConservedNotFloat':
            warning_message('Target Table: ', 'at least one of the Conserved values is not a positive number.')
        if anError == 'featTotalBlank':
            warning_message('Target Table: ', 'at least one of the Total values is blank.')
        if anError == 'featTotalNotFloat':
            warning_message('Target Table: ', 'at least one of the Total values is not a positive number.')
        if anError == 'featPc_TargetBlank':
            warning_message('Target Table: ', 'at least one of the % target met values is blank.')
        if anError == 'featPc_TargetNotFloat':
            warning_message('Target Table: ', 'at least one of the % target met values is not a positive number (not including features with a target of 0, which are automatically given a % target of -1).')
        if anError == 'duplicateFeatID':
            warning_message('Target Table: ', 'at least one of the Feature IDs appears twice in the Feature ID field.')
        if anError == 'featNameWrongFormat':
            warning_message('Target Table: ', 'at least one of the Feature names is in the wrong format. They cannot contain letters and numbers.')


def check_abund_table_dat_file(setup_object):
    abund_file_path = setup_object.input_path + sep + 'puvspr2.dat'
    abund_error_set, unit_id_set, feat_id_set = set(), set(), set()
    row_num = 2
    abund_error_row_set = set()
    prev_id_value_for_checking = -99

    with open(abund_file_path, 'rt') as f:
        count_reader = reader(f)
        progress_bar = make_progress_bar('Processing ' + 'Puvspr2 file')
        row_total_count = len(list(count_reader))
        row_count = 1

    with open(abund_file_path, 'rt') as f:
        abund_file_reader = reader(f)
        next(abund_file_reader)

        for aRow in abund_file_reader:
            set_progress_bar_value(progress_bar, row_count, row_total_count)
            row_count += 1
            feat_id, unit_id, feat_amount = aRow[0:3]
            abund_error_set, abund_error_row_set = check_abund_table_file_wrong_num_columns(abund_error_set, abund_error_row_set, aRow, row_num)
            abund_error_set, abund_error_row_set = check_abund_table_file_not_ordered(abund_error_set, abund_error_row_set, unit_id, prev_id_value_for_checking, row_num)
            abund_error_set, abund_error_row_set, feat_id_set = check_abund_table_file_feat_id(abund_error_set, abund_error_row_set, feat_id, feat_id_set, row_num)
            abund_error_set, abund_error_row_set, unit_id_set = check_abund_table_file_pu_id(abund_error_set, abund_error_row_set, unit_id, unit_id_set, row_num)
            abund_error_set, abund_error_row_set = check_abund_table_file_feat_amount(abund_error_set, abund_error_row_set, feat_amount, row_num)

            row_num += 1
            prev_id_value_for_checking = unit_id
    clear_progress_bar()

    return abund_error_set, abund_error_row_set, unit_id_set, feat_id_set, row_num


def check_abund_table_file_wrong_num_columns(error_set, error_row_set, a_row, row_num):
    if len(a_row) != 3:
        error_set.add('wrongNumColumns')
        error_row_set.add(row_num)
        
    return error_set, error_row_set
        
        
def check_abund_table_file_not_ordered(error_set, error_row_set, unit_id, prev_id_value_for_checking, row_num):
    try:
        if int(unit_id) < int(prev_id_value_for_checking):
            error_set.add('notOrderedByPU')
            error_row_set.add(row_num)
    except ValueError:
        pass  # Format error is picked up elsewhere

    return error_set, error_row_set


def check_abund_table_file_feat_id(error_set, error_row_set, feat_id, feat_id_set, row_num):
    if feat_id == '':
        error_set.add('featIDBlank')
        error_row_set.add(row_num)
    else:
        try:
            int(feat_id)
            feat_id_set.add(int(feat_id))
            if int(feat_id) < 1:
                error_set.add('featIDNeg')
                error_row_set.add(row_num)
        except ValueError:
            error_set.add('featIDNotInt')
            error_row_set.add(row_num)

    return error_set, error_row_set, feat_id_set


def check_abund_table_file_pu_id(error_set, error_row_set, unit_id, unit_id_set, row_num):
    if unit_id == '':
        error_set.add('puIDBlank')
        error_row_set.add(row_num)
    else:
        try:
            int(unit_id)
            unit_id_set.add(int(unit_id))
            if int(unit_id) < 1:
                error_set.add('puIDNeg')
                error_row_set.add(row_num)
        except ValueError:
            error_set.add('puIDNotInt')
            error_row_set.add(row_num)
        
    return error_set, error_row_set, unit_id_set


def check_abund_table_file_feat_amount(error_set, error_row_set, feat_amount, row_num):
    if feat_amount == '':
        error_set.add('featAmountBlank')
        error_row_set.add(row_num)
    else:
        try:
            float(feat_amount)
            if float(feat_amount) < 0:
                error_set.add('featAmountNeg')
                error_row_set.add(row_num)
        except ValueError:
            error_set.add('featAmountNotFloat')
            error_row_set.add(row_num)
        
    return error_set, error_row_set


def push_abund_table_file_error_messages(abund_error_set):
    for anError in abund_error_set:
        if anError == 'wrongNumColumns':
            warning_message('Puvspr2 file: ', 'at least one of the rows does not contain 3 values.')
        if anError == 'notOrderedByPU':
            warning_message('Puvspr2 file: ', 'this file must be ordered by planning unit ID, from smallest to highest value.')
        if anError == 'notOrderedByFeat':
            warning_message('Puvspr2 file: ', 'this file must be ordered by feature ID, from smallest to highest value.')
        if anError == 'featIDBlank':
            warning_message('Puvspr2 file: ', 'at least one of the feature ID values is missing.')
        if anError == 'featIDNotInt':
            warning_message('Puvspr2 file: ', 'at least one of the feature ID values is not an integer.')
        if anError == 'featIDNeg':
            warning_message('Puvspr2 file: ', 'at least one of the feature ID values is less than 1.')
        if anError == 'puIDBlank':
            warning_message('Puvspr2 file: ', 'at least one of the planning unit ID values is missing.')
        if anError == 'puIDNotInt':
            warning_message('Puvspr2 file: ', 'at least one of the planning unit ID values is not an integer.')
        if anError == 'puIDNeg':
            warning_message('Puvspr2 file: ', 'at least one of the planning unit ID values is less than 1.')
        if anError == 'featAmountBlank':
            warning_message('Puvspr2 file: ', 'at least one of the amount values is missing.')
        if anError == 'featAmountNotFloat':
            warning_message('Puvspr2 file: ', 'at least one of the amount values is not a valid number.')
        if anError == 'featAmountNeg':
            warning_message('Puvspr2 file: ', 'at least one of the amount values is less than 0.')

    return abund_error_set


def push_abund_table_row_error_messages(error_row_set):
    if len(error_row_set) > 0:
        error_row_list = list(error_row_set)
        error_row_list.sort()
        message_text = ''
        for aErrorRow in error_row_list:
            message_text += str(aErrorRow) + ' '
        final_message_text = message_text[:-1]
        warning_message('Puvspr2 file: ', 'errors are in the following rows: ' + final_message_text)


def check_pu_shape_file(setup_object):
    pu_id_list, shape_error_set, = list(), set()

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_features = pu_layer.getFeatures()
    unit_id_field = pu_layer.fields().indexFromName('Unit_ID')
    pu_area_field = pu_layer.fields().indexFromName('Area')
    pu_cost_field = pu_layer.fields().indexFromName('Cost')
    pu_status_field = pu_layer.fields().indexFromName('Status')

    progress_bar = make_progress_bar('Processing planning unit shapefile')
    poly_count = 1
    poly_total_count = pu_layer.featureCount()

    for puFeature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[unit_id_field]
        pu_id_list.append(pu_id)
        shape_error_set = check_pu_shape_file_pu_id_value(shape_error_set, pu_id)
        shape_error_set = check_pu_shape_file_pu_area_value(shape_error_set, pu_attributes, pu_area_field)
        if setup_object.analysis_type != 'MarxanWithZones':
            shape_error_set = check_pu_shape_file_pu_cost_value(shape_error_set, pu_attributes, pu_cost_field)
            shape_error_set = check_pu_shape_file_pu_status_value(shape_error_set, pu_attributes, pu_status_field)
        else:
            zones_field_status_list = list()
            for zoneID in setup_object.zones_dict:
                cost_field_name = 'Z' + str(zoneID) + '_Cost'
                status_field_name = 'Z' + str(zoneID) + '_Status'
                pu_cost_field = pu_layer.fields().indexFromName(cost_field_name)
                pu_status_field = pu_layer.fields().indexFromName(status_field_name)
                shape_error_set = check_pu_shape_file_pu_cost_value(shape_error_set, pu_attributes, pu_cost_field)
                shape_error_set = zones_check_pu_shape_file_pu_status_value(shape_error_set, pu_attributes, pu_status_field)
                zones_field_status_list.append(pu_attributes[pu_status_field])
            shape_error_set = check_zones_field_status_list_for_conflicts(shape_error_set, zones_field_status_list)
    clear_progress_bar()

    shape_error_set, pu_id_set, duplicate_id_text = check_pu_shape_file_duplicate_pu_id_value(shape_error_set, pu_id_list)

    return shape_error_set, pu_id_set, duplicate_id_text


def check_pu_shape_file_pu_id_value(shape_error_set, pu_id):
    if pu_id == NULL:  # NULL is used for blank values that return QPyNullVariant
        shape_error_set.add('puIDBlank')
    else:
        try:
            int(pu_id)
            if int(pu_id) < 0:
                shape_error_set.add('puIDNotInt')
        except ValueError:
            shape_error_set.add('puIDNotInt')

    return shape_error_set


def check_pu_shape_file_pu_area_value(shape_error_set, pu_attributes, pu_area_field):
    pu_area = pu_attributes[pu_area_field]
    if pu_area == NULL:
        shape_error_set.add('puAreaBlank')
    else:
        try:
            float(pu_area)
            if float(pu_area) < 0:
                shape_error_set.add('puAreaNotFloat')
        except ValueError:
            shape_error_set.add('puAreaNotFloat')

    return shape_error_set


def check_pu_shape_file_pu_cost_value(shape_error_set, pu_attributes, pu_cost_field):
    pu_cost = pu_attributes[pu_cost_field]
    if pu_cost == NULL:
        shape_error_set.add('puCostBlank')
    else:
        try:
            float(pu_cost)
            if float(pu_cost) < 0:
                shape_error_set.add('puCostNotFloat')
        except ValueError:
            shape_error_set.add('puCostNotFloat')

    return shape_error_set


def check_pu_shape_file_pu_status_value(shape_error_set, pu_attributes, unit_status_field):
    pu_status = pu_attributes[unit_status_field]
    if pu_status not in ['Available', 'Conserved', 'Earmarked', 'Excluded']:
        shape_error_set.add('puStatusWrong')

    return shape_error_set


def check_pu_shape_file_duplicate_pu_id_value(shape_error_set, pu_id_list):
    pu_id_set = set(pu_id_list)
    duplicate_id_text = 'The following planning unit ID values appear more than once in the Unit_ID field: '
    if len(pu_id_list) != len(pu_id_set):
        shape_error_set.add('duplicateFeatID')
        duplicate_set = set([x for x in pu_id_list if pu_id_list.count(x) > 1])
        duplicate_list = list(duplicate_set)
        duplicate_list.sort()
        for aNum in duplicate_list:
            duplicate_id_text += str(aNum) + ', '
        duplicate_id_text = duplicate_id_text[0:-2]

    return shape_error_set, pu_id_set, duplicate_id_text


def push_pu_shape_file_error_messages(shape_error_set, duplicate_id_text):
    for anError in shape_error_set:
        if anError == 'puIDBlank':
            warning_message('Planning unit layer: ', 'at least one of the planning unit ID values is blank.')
        if anError == 'duplicateFeatID':
            warning_message('Planning unit layer: ', duplicate_id_text)
        if anError == 'puIDNotInt':
            warning_message('Planning unit layer: ', 'at least one of the planning unit ID values is not an integer greater than 0.')
        if anError == 'puAreaBlank':
            warning_message('Planning unit layer: ', 'at least one of the planning unit area values is blank.')
        if anError == 'puAreaNotFloat':
            warning_message('Planning unit layer: ', 'at least one of the planning unit area values is not a non-negative number.')
        if anError == 'puCostBlank':
            warning_message('Planning unit layer: ', 'at least one of the planning unit cost values is blank')
        if anError == 'puCostNotFloat':
            warning_message('Planning unit layer: ', 'at least one of the planning unit cost values is not a non-negative number.')
        if anError == 'puCostNotFloat':
            warning_message('Planning unit layer: ', 'at least one of the planning unit cost values is not a non-negative number.')
        if anError == 'puStatusWrong':
            warning_message('Planning unit layer: ', 'at least one of the planning unit status values is incorrect. They should either be Available, Conserved, Earmarked or Excluded.')
        if anError == 'puZonesStatusWrong':
            warning_message('Planning unit layer: ', 'at least one of the planning unit status values is incorrect. They should either be Available, Earmarked, Excluded or Locked.')


def check_ids_match_in_target_table_and_puvspr2(target_feat_id_set, puvspr2_feat_id_set, id_values_not_duplicated):
    extra_target_feat_id_set, extra_abund_feat_id_set = find_values_in_one_set(target_feat_id_set, puvspr2_feat_id_set)
    if len(extra_target_feat_id_set) > 0:
        error_text = ''
        for aValue in extra_target_feat_id_set:
            error_text += str(aValue) + ', '
        error_text = error_text[: -2]
        warning_message('Abundance and Target tables: ', 'the following Feature IDs appear in the Target Table but not in the puvspr2.dat file: ' + error_text)
        id_values_not_duplicated = False
    if len(extra_abund_feat_id_set) > 0:
        error_text = ''
        for aValue in extra_abund_feat_id_set:
            error_text += str(aValue) + ', '
        error_text = error_text[: -2]
        warning_message('puvspr2.dat file and Target tables: ', 'the following Feature IDs appear in the puvspr2.dat file but not in the Target table: ' + error_text)
        id_values_not_duplicated = False

    return id_values_not_duplicated


def check_ids_match_in_pu_layer_and_puvspr2(puvspr2_pu_id_set, pu_pu_id_set, id_values_not_duplicated):
    extra_puvspr2_pu_id_set, extra_pu_pu_id_set = find_values_in_one_set(puvspr2_pu_id_set, pu_pu_id_set)
    if len(extra_puvspr2_pu_id_set) > 0:
        error_text = ''
        for aValue in extra_puvspr2_pu_id_set:
            error_text += str(aValue) + ', '
        error_text = error_text[: -2]
        warning_message('puvspr2.dat file and Planning unit layer: ', 'the following planning unit IDs appear in the puvspr2.dat file but not in the planning unit layer: ' + error_text)
        id_values_not_duplicated = False

    return id_values_not_duplicated


def find_values_in_one_set(input_set1, input_set2):
    set1 = set()
    set2 = set()
    big_set = input_set1.union(input_set2)
    for aValue in big_set:
        if aValue in input_set1 and aValue not in input_set2:
            set1.add(aValue)
        if aValue not in input_set1 and aValue in input_set2:
            set2.add(aValue)

    return set1, set2
