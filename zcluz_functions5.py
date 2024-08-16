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

from qgis.core import QgsVectorLayer, QgsSpatialIndex, QgsField
from qgis.PyQt.QtCore import QVariant

from csv import reader, writer
from os import path, sep
from pathlib import Path
from statistics import median

from .cluz_messages import clear_progress_bar, make_progress_bar, warning_message, set_progress_bar_value


# Produce Marxan input files #######################################################


def create_zones_feat_dat_file(setup_object):
    zones_feat_dat_file = setup_object.input_path + sep + 'feat.dat'
    with open(zones_feat_dat_file, 'w', newline='', encoding='utf-8') as out_file:
        spec_dat_writer = writer(out_file)
        spec_dat_writer.writerow(['id', 'name', 'target', 'spf'])

        target_dict = setup_object.target_dict
        feat_list = list(target_dict)
        feat_list.sort()

        progress_bar = make_progress_bar('Making a new feat.dat file')
        row_total_count = len(feat_list)
        row_count = 1

        for aFeat in feat_list:
            set_progress_bar_value(progress_bar, row_count, row_total_count)
            row_count += 1

            feat_list = target_dict[aFeat]
            raw_feat_name = feat_list[0]
            change_bool, feat_name = convert_feat_name_by_changing_incompatible_text_characters(raw_feat_name)
            feat_target = feat_list[3]
            feat_spf = feat_list[2]
            spec_dat_writer.writerow([aFeat, feat_name, feat_target, feat_spf])
    clear_progress_bar()


def convert_feat_name_by_changing_incompatible_text_characters(raw_feat_name):
    change_bool = False
    feat_name = raw_feat_name.replace(' ', '_')
    feat_name = feat_name.replace('.', '')

    if raw_feat_name != feat_name:
        change_bool = True

    return change_bool, feat_name


def create_zones_target_dat_file(setup_object):
    zones_feat_dat_file = setup_object.input_path + sep + 'zonetarget.dat'
    with open(zones_feat_dat_file, 'w', newline='', encoding='utf-8') as out_file:
        zones_target_dat_writer = writer(out_file)
        zones_target_dat_writer.writerow(['zoneid', 'featureid', 'target'])

        feat_list = list(setup_object.target_dict)
        feat_list.sort()

        progress_bar = make_progress_bar('Making a new feat.dat file')
        row_total_count = len(feat_list)
        row_count = 1

        for zonesTargetTypeName in setup_object.zones_target_dict:
            set_progress_bar_value(progress_bar, row_count, row_total_count)
            row_count += 1

            zones_id_prefix = zonesTargetTypeName.split('_')[0]
            zones_id = int(zones_id_prefix[1:])
            zones_feat_target_dict = setup_object.zones_target_dict[zonesTargetTypeName]
            for featID in zones_feat_target_dict:
                zones_target_dat_writer.writerow([zones_id, featID, zones_feat_target_dict[featID]])
    clear_progress_bar()


def create_zones_prop_dat_file(setup_object):
    zones_prop_dat_file = setup_object.input_path + sep + 'zonecontrib.dat'
    with open(zones_prop_dat_file, 'w', newline='', encoding='utf-8') as out_file:
        zones_prop_dat_writer = writer(out_file)
        zones_prop_dat_writer.writerow(['zoneid', 'featureid', 'fraction'])

        feat_list = list(setup_object.target_dict.keys())
        feat_list.sort()

        progress_bar = make_progress_bar('Making a new feat.dat file')
        row_total_count = len(feat_list)
        row_count = 1

        for zonesPropTypeName in setup_object.zones_prop_dict:
            set_progress_bar_value(progress_bar, row_count, row_total_count)
            row_count += 1

            zones_id_prefix = zonesPropTypeName.split('_')[0]
            zones_id = int(zones_id_prefix[1:])
            zones_prop_target_dict = setup_object.zones_prop_dict[zonesPropTypeName]
            for featID in zones_prop_target_dict:
                zones_prop_dat_writer.writerow([zones_id, featID, zones_prop_target_dict[featID]])
    clear_progress_bar()


def create_zones_pu_dat_file(setup_object):
    pu_zones_dat_path_name = setup_object.input_path + sep + 'pu.dat'

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_features = pu_layer.getFeatures()
    pu_id_field = pu_layer.fields().indexFromName('Unit_ID')

    progress_bar = make_progress_bar('Making a new pu.dat file')
    poly_count = 1
    poly_total_count = pu_layer.featureCount()

    with open(pu_zones_dat_path_name, 'w', newline='', encoding='utf-8') as out_file:
        pu_dat_writer = writer(out_file)
        zones_pu_dat_file_header_list = ['id'] + make_zones_header_list(setup_object, '_Cost')
        pu_dat_writer.writerow(zones_pu_dat_file_header_list)

        zones_pu_cost_field_list = make_zones_field_list(setup_object, pu_layer, '_Cost')
        for puFeature in pu_features:
            set_progress_bar_value(progress_bar, poly_count, poly_total_count)
            poly_count += 1
            pu_dat_row_list = make_pu_dat_row_list(setup_object, puFeature, pu_id_field, zones_pu_cost_field_list)
            pu_dat_writer.writerow(pu_dat_row_list)
    clear_progress_bar()


def make_pu_dat_row_list(setup_object, pu_feature, pu_id_field, zones_pu_cost_field_list):
    decimal_places = setup_object.decimal_places
    pu_attributes = pu_feature.attributes()
    pu_id = pu_attributes[pu_id_field]
    pu_dat_row_list = [pu_id]
    for costField in zones_pu_cost_field_list:
        raw_cost_value = pu_attributes[costField]
        cost_value = round(float(raw_cost_value), decimal_places)
        cost_value = format(cost_value, "." + str(decimal_places) + "f")
        pu_dat_row_list.append(cost_value)

    return pu_dat_row_list


def create_zones_pu_status_dict(setup_object):
    zones_pu_status_dict = dict()
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_features = pu_layer.getFeatures()
    pu_id_field = pu_layer.fields().indexFromName('Unit_ID')
    zone_id_list = list(setup_object.zones_dict)

    for pu_feature in pu_features:
        pu_attributes = pu_feature.attributes()
        pu_id = pu_attributes[pu_id_field]
        for zoneID in zone_id_list:
            status_field = pu_layer.fields().indexFromName('Z' + str(zoneID) + '_Status')
            status_value = pu_attributes[status_field]
            try:
                pu_zones_pu_status_dict = zones_pu_status_dict[pu_id]
            except KeyError:
                pu_zones_pu_status_dict = dict()
            pu_zones_pu_status_dict[zoneID] = status_value
            zones_pu_status_dict[pu_id] = pu_zones_pu_status_dict

    return zones_pu_status_dict


def create_pu_lock_dat_file(setup_object, zones_pu_status_dict):
    pu_lock_dat_path_name = setup_object.input_path + sep + 'pulock.dat'

    progress_bar = make_progress_bar('Making a new pulock.dat file')
    line_count = 1
    line_total_count = len(zones_pu_status_dict)

    with open(pu_lock_dat_path_name, 'w', newline='', encoding='utf-8') as out_file:
        pu_lock_dat_writer = writer(out_file)
        pu_lock_dat_writer.writerow(['puid', 'zoneid'])
        pu_id_list = list(zones_pu_status_dict.keys())
        pu_id_list.sort()
        for pu_id in pu_id_list:
            set_progress_bar_value(progress_bar, line_count, line_total_count)
            line_count += 1

            pu_zones_pu_status_dict = zones_pu_status_dict[pu_id]
            for zoneID in pu_zones_pu_status_dict:
                status_value = pu_zones_pu_status_dict[zoneID]
                if status_value == 'Locked' or status_value == 'Earmarked':
                    pu_lock_dat_writer.writerow([pu_id, zoneID])

    clear_progress_bar()


def create_pu_zone_dat_file(setup_object, zones_pu_status_dict):
    pu_zones_dat_path_name = setup_object.input_path + sep + 'puzone.dat'

    progress_bar = make_progress_bar('Making a new puzone.dat file')
    line_count = 1
    line_total_count = len(zones_pu_status_dict)

    with open(pu_zones_dat_path_name, 'w', newline='', encoding='utf-8') as out_file:
        pu_zones_dat_writer = writer(out_file)
        pu_zones_dat_writer.writerow(['puid', 'zoneid'])
        pu_id_list = list(zones_pu_status_dict.keys())
        pu_id_list.sort()
        for pu_id in pu_id_list:
            set_progress_bar_value(progress_bar, line_count, line_total_count)
            line_count += 1

            pu_zones_pu_status_dict = zones_pu_status_dict[pu_id]
            pu_zones_pu_status_list = pu_zones_pu_status_dict.values()
            if 'Excluded' in pu_zones_pu_status_list:
                restricted_to_zone_list = make_restricted_to_zone_list(pu_zones_pu_status_dict)
                for zoneID in restricted_to_zone_list:
                    pu_zones_dat_writer.writerow([pu_id, zoneID])

    clear_progress_bar()


def make_restricted_to_zone_list(pu_zones_pu_status_dict):
    restricted_to_zone_list = list()
    for zoneID in pu_zones_pu_status_dict:
        status_value = pu_zones_pu_status_dict[zoneID]
        if status_value != 'Excluded':
            restricted_to_zone_list.append(zoneID)

    return restricted_to_zone_list


def make_zones_header_list(setup_object, name_suffix):
    zones_pu_dat_file_header_list = list()
    for zone_id in setup_object.zones_dict:
        new_zone_header = 'Z' + str(zone_id) + name_suffix
        zones_pu_dat_file_header_list.append(new_zone_header)

    return zones_pu_dat_file_header_list


def make_zones_field_list(setup_object, pu_layer, name_suffix):
    zones_pu_cost_field_list = list()
    for zoneID in setup_object.zones_dict:
        zones_cost_field_name = 'Z' + str(zoneID) + name_suffix
        zones_cost_field = pu_layer.fields().indexFromName(zones_cost_field_name)
        zones_pu_cost_field_list.append(zones_cost_field)

    return zones_pu_cost_field_list


def create_costs_dat_file(setup_object):
    costs_dat_path_name = setup_object.input_path + sep + 'costs.dat'

    progress_bar = make_progress_bar('Making a new costs.dat file')
    row_count = 1
    total_row_count = len(setup_object.zones_dict)

    with open(costs_dat_path_name, 'w', newline='', encoding='utf-8') as out_file:
        costs_dat_writer = writer(out_file)
        costs_dat_writer.writerow(['costid', 'costname'])

        for zone_id in setup_object.zones_dict:
            set_progress_bar_value(progress_bar, row_count, total_row_count)
            row_count += 1
            costs_dat_writer.writerow([zone_id, 'Z' + str(zone_id) + '_Cost'])
    clear_progress_bar()


def create_zones_dat_file(setup_object):
    zones_dat_path_name = setup_object.input_path + sep + 'zones.dat'

    progress_bar = make_progress_bar('Making a new zones.dat file')
    row_count = 1
    total_row_count = len(setup_object.zones_dict)

    with open(zones_dat_path_name, 'w', newline='', encoding='utf-8') as out_file:
        costs_dat_writer = writer(out_file)
        costs_dat_writer.writerow(['zoneid', 'zonename'])

        for zone_id in setup_object.zones_dict:
            set_progress_bar_value(progress_bar, row_count, total_row_count)
            costs_dat_writer.writerow([zone_id, setup_object.zones_dict[zone_id]])
    clear_progress_bar()


def create_zone_cost_dat_file(setup_object):
    zone_cost_dat_path_name = setup_object.input_path + sep + 'zonecost.dat'

    progress_bar = make_progress_bar('Making a new zonecost.dat file')
    row_count = 1
    total_row_count = len(setup_object.zones_dict)

    with open(zone_cost_dat_path_name, 'w', newline='', encoding='utf-8') as out_file:
        zone_cost_dat_writer = writer(out_file)
        zone_cost_dat_writer.writerow(['zoneid', 'costid', 'multiplier'])

        for zone_id in setup_object.zones_dict:
            set_progress_bar_value(progress_bar, row_count, total_row_count)
            for cost_id in setup_object.zones_dict:
                if zone_id == cost_id:
                    zone_cost_dat_writer.writerow([zone_id, cost_id, 1])
                else:
                    zone_cost_dat_writer.writerow([zone_id, cost_id, 0])
    clear_progress_bar()


# Marxan dialog ###########################


def return_zones_output_name(setup_object):
    old_output_name = setup_object.output_name
    output_path = setup_object.output_path
    old_output_best_name = output_path + sep + old_output_name + '_best.csv'

    old_output_name_stem = ''
    num_value_bool = True
    for a_num in range(len(old_output_name), 0, -1):
        a_char = old_output_name[a_num - 1]
        try:
            int(a_char)
        except ValueError:
            num_value_bool = False
        if num_value_bool is False:
            old_output_name_stem = a_char + old_output_name_stem

    if path.isfile(old_output_best_name):
        name_suffix = 1
        new_name = output_path + sep + old_output_name_stem + str(name_suffix) + '_best.csv'
        while path.isfile(new_name):
            name_suffix += 1
            new_name = output_path + sep + old_output_name_stem + str(name_suffix) + '_best.csv'

        output_name = old_output_name_stem + str(name_suffix)
    else:
        output_name = old_output_name

    return output_name


def make_zoneboundcost_dat_from_zones_bound_cost_dict(setup_object):
    zoneboundcost_dat_path_name = setup_object.input_path + sep + 'zoneboundcost.dat'

    progress_bar = make_progress_bar('Making a new zoneboundcost.dat file')
    line_count = 1
    line_total_count = len(setup_object.zones_bound_cost_dict)

    with open(zoneboundcost_dat_path_name, 'w', newline='', encoding='utf-8') as out_file:
        zoneboundcost_dat_writer = writer(out_file)
        zoneboundcost_dat_writer.writerow(['zoneid1', 'zoneid2', 'cost'])
        for zones_id_tuple in setup_object.zones_bound_cost_dict:
            set_progress_bar_value(progress_bar, line_count, line_total_count)
            zoneboundcost_dat_writer.writerow([zones_id_tuple[0], zones_id_tuple[1], setup_object.zones_bound_cost_dict[zones_id_tuple]])
            line_count += 1

    clear_progress_bar()


def check_make_zones_bound_cost_dict_from_dialog(zones_marxan_dialog, setup_object):
    zones_bound_cost_values_ok_bool = True
    zones_blm_value_dict = copy.deepcopy(setup_object.zones_bound_cost_dict)
    try:
        for a_row in range(0, zones_marxan_dialog.blmTableWidget.rowCount()):
            label_value = zones_marxan_dialog.blmTableWidget.item(a_row, 0).text()
            label_value_list = label_value.split(' vs ')
            zone_id_tuple = (int(label_value_list[0][5:]), int(label_value_list[1][5:]))
            blm_value = float(zones_marxan_dialog.blmTableWidget.item(a_row, 1).text())
            if blm_value < 0:
                zones_bound_cost_values_ok_bool = False
            zones_blm_value_dict[zone_id_tuple] = blm_value
    except ValueError:
        zones_blm_value_dict = dict()
        zones_bound_cost_values_ok_bool = False

    if zones_bound_cost_values_ok_bool is False:
        warning_message('Zone boundary cost error', ' Every cost value must be a positive number. Please correct this to run Marxan with Zones successfully.')

    return zones_blm_value_dict, zones_bound_cost_values_ok_bool


def make_zones_marxan_input_file(setup_object, marxan_parameter_dict, add_zone_target_dat_bool):
    if marxan_parameter_dict['extra_outputs_bool']:
        extra_output_value = '3'
    else:
        extra_output_value = '0'
    if path.isfile(marxan_parameter_dict['marxan_path']):
        write_zones_marxan_input_file(setup_object, marxan_parameter_dict, extra_output_value, add_zone_target_dat_bool)


def check_if_add_zone_target_dat_needed_bool(setup_object):
    zone_count = len(setup_object.zones_dict)
    add_zone_target_dat_bool = False
    for featID in setup_object.target_dict:
        target_list_beg_pos = 6 + (1 * zone_count) + 1
        target_list_end_pos = 6 + (2 * zone_count) + 1
        zone_target_list = setup_object.target_dict[featID][target_list_beg_pos:target_list_end_pos]

        for aValue in zone_target_list:
            if float(aValue) > 0:
                add_zone_target_dat_bool = True

    return add_zone_target_dat_bool


def write_zones_marxan_input_file(setup_object, zones_marxan_parameter_dict, extra_output_value, add_zone_target_dat_bool):
    with open(zones_marxan_parameter_dict['marxan_setup_path'], 'w', newline='', encoding='utf-8') as marxanFile:
        marxan_writer = writer(marxanFile)

        header1 = 'Input file for Marxan program, written by Ian Ball, Hugh Possingham and Matt Watts.'
        header2 = 'This file was generated using CLUZ, written by Bob Smith'
        marxan_writer.writerow([header1])
        marxan_writer.writerow([header2])
        marxan_writer.writerow([])

        marxan_writer.writerow(['General Parameters'])
        marxan_writer.writerow(['BLM ' + str(zones_marxan_parameter_dict['blm_value'])])
        marxan_writer.writerow(['PROP  ' + str(zones_marxan_parameter_dict['initial_prop'])])
        marxan_writer.writerow(['RANDSEED -1'])
        marxan_writer.writerow(['NUMREPS ' + str(zones_marxan_parameter_dict['num_run'])])
        marxan_writer.writerow(['AVAILABLEZONE  1'])  # "The available zone is treated as an unprotected zone in Marxan Z."

        marxan_writer.writerow([])

        marxan_writer.writerow(['Annealing Parameters'])
        marxan_writer.writerow(['NUMITNS ' + str(zones_marxan_parameter_dict['num_iter'])])
        marxan_writer.writerow(['STARTTEMP -1'])
        marxan_writer.writerow(['COOLFAC  -1'])
        marxan_writer.writerow(['NUMTEMP 10000'])
        marxan_writer.writerow([])

        marxan_writer.writerow(['Cost Threshold'])
        marxan_writer.writerow(['COSTTHRESH  0'])
        marxan_writer.writerow(['THRESHPEN1  0'])
        marxan_writer.writerow(['THRESHPEN2  0'])
        marxan_writer.writerow([])

        marxan_writer.writerow(['Input Files'])
        marxan_writer.writerow(['INPUTDIR ' + setup_object.input_path])
        marxan_writer.writerow(['PUNAME pu.dat'])
        marxan_writer.writerow(['FEATNAME feat.dat'])
        marxan_writer.writerow(['PUVSPRNAME puvspr2.dat'])
        marxan_writer.writerow(['ZONESNAME zones.dat'])
        marxan_writer.writerow(['COSTSNAME costs.dat'])
        marxan_writer.writerow(['ZONECOSTNAME zonecost.dat'])
        if setup_object.bound_flag: # The zoneboundcost.dat is only used when the boundary costs are applied
            marxan_writer.writerow(['BOUNDNAME bound.dat'])
            marxan_writer.writerow(['ZONEBOUNDCOSTNAME zoneboundcost.dat'])
        marxan_writer.writerow(['PUZONENAME puzone.dat'])
        marxan_writer.writerow(['PULOCKNAME pulock.dat'])
        if add_zone_target_dat_bool:
            marxan_writer.writerow(['ZONETARGETNAME zonetarget.dat'])
        marxan_writer.writerow(['ZONECONTRIBNAME zonecontrib.dat'])

        marxan_writer.writerow([])

        marxan_writer.writerow(['Save Files'])
        marxan_writer.writerow(['SCENNAME ' + zones_marxan_parameter_dict['output_name']])
        marxan_writer.writerow(['SAVERUN ' + extra_output_value])
        marxan_writer.writerow(['SAVEBEST 3'])
        marxan_writer.writerow(['SAVESUMMARY 3'])
        marxan_writer.writerow(['SAVESCEN ' + extra_output_value])
        marxan_writer.writerow(['SAVETARGMET 3'])
        marxan_writer.writerow(['SAVESUMSOLN 3'])

        marxan_writer.writerow(['SAVESOLUTIONSMATRIX 0'])
        marxan_writer.writerow(['SOLUTIONSMATRIXHEADERS 0'])
        marxan_writer.writerow(['SAVEPENALTY 0'])
        marxan_writer.writerow(['SAVELOG 3'])
        marxan_writer.writerow(['SAVEANNEALINGTRACE 0'])
        marxan_writer.writerow(['ANNEALINGTRACEROWS 0'])
        marxan_writer.writerow(['SAVEITIMPTRACE 0'])
        marxan_writer.writerow(['ITIMPTRACEROWS 0'])
        marxan_writer.writerow(['SAVEZONECONNECTIVITYSUM 0'])
        marxan_writer.writerow(['OUTPUTDIR ' + setup_object.output_path])
        marxan_writer.writerow([])

        marxan_writer.writerow(['Program control.'])
        marxan_writer.writerow(['RUNMODE 1'])
        marxan_writer.writerow(['MISSLEVEL  ' + str(zones_marxan_parameter_dict['missing_prop'])])
        marxan_writer.writerow(['ITIMPTYPE 0'])
        marxan_writer.writerow(['VERBOSITY 3'])
        marxan_writer.writerow([])


def zones_marxan_update_setup_object(zones_marxan_dialog, setup_object, marxan_parameter_dict):
    setup_object.output_name = marxan_parameter_dict['output_name']
    setup_object.num_iter = marxan_parameter_dict['num_iter']
    setup_object.num_runs = marxan_parameter_dict['num_run']
    setup_object.blm_value = marxan_parameter_dict['blm_value']
    setup_object.bound_flag = zones_marxan_dialog.boundCheckBox.isChecked()
    setup_object.extra_outputs_flag = zones_marxan_dialog.extraCheckBox.isChecked()
    setup_object.zones_bound_flag = zones_marxan_dialog.boundZoneCheckBox.isChecked()
    setup_object.start_prop = marxan_parameter_dict['initial_prop']
    setup_object.target_prop = marxan_parameter_dict['missing_prop']

    return setup_object


def add_best_zones_marxan_output_to_pu_shapefile(setup_object, best_zones_output_file_path, best_zones_field_name):
    best_zones_dict = make_best_zones_dict(best_zones_output_file_path)
    pu_layer = QgsVectorLayer(setup_object.pu_path, "Planning units", "ogr")
    id_field_index = pu_layer.fields().indexFromName("Unit_ID")

    best_zones_field_index = pu_layer.fields().indexFromName(best_zones_field_name)
    provider = pu_layer.dataProvider()
    if best_zones_field_index == -1:
        provider.addAttributes([QgsField(best_zones_field_name, QVariant.Int)])
        pu_layer.updateFields()
    best_zones_field_index = provider.fieldNameIndex(best_zones_field_name)

    progress_bar = make_progress_bar('Loading best output results')
    poly_total_count = pu_layer.featureCount()
    poly_count = 1

    pu_features = pu_layer.getFeatures()
    pu_layer.startEditing()
    for pu_feature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_row = pu_feature.id()
        pu_attributes = pu_feature.attributes()
        pu_id = pu_attributes[id_field_index]
        best_zone = best_zones_dict[pu_id]
        pu_layer.changeAttributeValue(pu_row, best_zones_field_index, best_zone)
    pu_layer.commitChanges()
    clear_progress_bar()


def make_best_zones_dict(best_output_file_path):
    best_zones_dict = dict()
    with open(best_output_file_path, 'rt') as f:
        best_output_reader = reader(f)
        next(best_output_reader, None)  # skip the headers
        for row in best_output_reader:
            pu_id = int(float(row[0]))
            best_zone = int(float(row[1]))
            best_zones_dict[pu_id] = best_zone

    return best_zones_dict


def add_summed_zones_marxan_output_to_pu_shapefile(setup_object, summed_output_file_path):
    summed_score_dict = make_zones_summed_scores_dict(summed_output_file_path)

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    provider = pu_layer.dataProvider()
    id_field_index = provider.fieldNameIndex('Unit_ID')

    for zone_id in list(setup_object.zones_dict):
        zones_summed_field_name = 'Z' + str(zone_id) + '_' + 'SFreq'
        summed_field_index = provider.fieldNameIndex(zones_summed_field_name)
        if summed_field_index == -1:
            provider.addAttributes([QgsField(zones_summed_field_name, QVariant.Int)])
            pu_layer.updateFields()

    progress_bar = make_progress_bar('Loading summed solution output results')
    poly_total_count = pu_layer.featureCount()
    poly_count = 1

    pu_features = pu_layer.getFeatures()
    pu_layer.startEditing()
    for puFeature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_row = puFeature.id()
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[id_field_index]
        for zone_id in list(setup_object.zones_dict):
            zones_summed_field_name = 'Z' + str(zone_id) + '_' + 'SFreq'
            zone_sf_score_field_index = provider.fieldNameIndex(zones_summed_field_name)
            zone_name_text = setup_object.zones_dict[zone_id]
            sf_score = summed_score_dict[zone_name_text][pu_id]

            pu_layer.changeAttributeValue(pu_row, zone_sf_score_field_index, sf_score)

    pu_layer.commitChanges()
    clear_progress_bar()


def make_zones_summed_scores_dict(summed_output_file):
    zones_summed_score_dict = dict()
    with open(summed_output_file, 'rt') as f:
        zones_sf_file_reader = reader(f)
        zones_sf_file_header = next(zones_sf_file_reader)
        zones_sf_file_zone_name_list = zones_sf_file_header[2:]
        for row in zones_sf_file_reader:
            pu_id = int(row[0])
            zones_sf_file_zone_sf_score_list = row[2:]
            for a_col in range(0, len(zones_sf_file_zone_name_list)):
                header_name = zones_sf_file_zone_name_list[a_col]
                sf_score = int(zones_sf_file_zone_sf_score_list[a_col])

                try:
                    a_zone_summed_score_dict = zones_summed_score_dict[header_name]
                except KeyError:
                    a_zone_summed_score_dict = dict()
                a_zone_summed_score_dict[pu_id] = sf_score
                zones_summed_score_dict[header_name] = a_zone_summed_score_dict

    return zones_summed_score_dict


def zones_load_best_marxan_output_to_pu_shapefile(zones_load_dialog, setup_object):
    zones_load_best_output_file_path = zones_load_dialog.zonesBestLineEdit.text()
    zones_load_best_csv_file_name = Path(zones_load_best_output_file_path).stem
    zones_load_best_field_name = zones_load_dialog.zonesBestNameLineEdit.text()
    zones_load_best_dict = zones_make_best_values_dict(zones_load_best_output_file_path)
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', "ogr")
    id_field_index = pu_layer.fields().indexFromName('Unit_ID')

    provider = pu_layer.dataProvider()
    provider.addAttributes([QgsField(zones_load_best_field_name, QVariant.String)])
    pu_layer.updateFields()
    best_load_field_index = provider.fieldNameIndex(zones_load_best_field_name)

    progress_bar = make_progress_bar('Loading best output results')
    poly_total_count = pu_layer.featureCount()
    poly_count = 1

    pu_features = pu_layer.getFeatures()
    pu_layer.startEditing()
    for puFeature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_row = puFeature.id()
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[id_field_index]
        best_zone_value = zones_load_best_dict[pu_id]
        pu_layer.changeAttributeValue(pu_row, best_load_field_index, best_zone_value)
    pu_layer.commitChanges()
    clear_progress_bar()

    return zones_load_best_csv_file_name, zones_load_best_field_name


def zones_make_best_values_dict(best_output_file_path):
    zones_best_scores_dict = dict()
    with open(best_output_file_path, 'rt') as f:
        best_output_reader = reader(f)
        next(best_output_reader, None)  # skip the headers
        for row in best_output_reader:
            pu_id = int(float(row[0]))
            best_zone_value = int(float(row[1]))
            zones_best_scores_dict[pu_id] = best_zone_value

    return zones_best_scores_dict


def zones_load_summed_marxan_output_to_pu_shapefile(zones_load_dialog, setup_object):
    summed_output_file_path = zones_load_dialog.zonesSummedLineEdit.text()
    summed_score_dict = make_zones_summed_scores_dict(summed_output_file_path)
    zones_load_sf_name_prefix = zones_load_dialog.zonesSummedNameLineEdit.text()
    zones_load_sf_csv_file_name = Path(summed_output_file_path).stem

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    provider = pu_layer.dataProvider()
    id_field_index = provider.fieldNameIndex('Unit_ID')

    for zone_id in list(setup_object.zones_dict):
        zones_summed_field_name = zones_load_sf_name_prefix + '_Z' + str(zone_id) + '_' + 'SF'
        provider.addAttributes([QgsField(zones_summed_field_name, QVariant.Int)])
        pu_layer.updateFields()

    progress_bar = make_progress_bar('Loading summed solution output results')
    poly_total_count = pu_layer.featureCount()
    poly_count = 1

    pu_features = pu_layer.getFeatures()
    pu_layer.startEditing()
    max_sf_score = 0
    for pu_feature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_row = pu_feature.id()
        pu_attributes = pu_feature.attributes()
        pu_id = pu_attributes[id_field_index]
        for zone_id in list(setup_object.zones_dict):
            zones_summed_field_name = zones_load_sf_name_prefix + '_Z' + str(zone_id) + '_SF'
            zone_sf_score_field_index = provider.fieldNameIndex(zones_summed_field_name)
            zone_name_text = setup_object.zones_dict[zone_id]
            sf_score = summed_score_dict[zone_name_text][pu_id]
            if sf_score > max_sf_score:
                max_sf_score = sf_score

            pu_layer.changeAttributeValue(pu_row, zone_sf_score_field_index, sf_score)
    pu_layer.commitChanges()
    clear_progress_bar()

    return zones_load_sf_csv_file_name, zones_load_sf_name_prefix, max_sf_score


def make_zones_calibrate_results_dict(setup_object, marxan_parameter_dict):
    zones_calibrate_results_dict = dict()
    score_list = list()
    cost_list = list()
    connectivity_cost_list = list()
    penalty_list = list()
    mpm_list = list()

    summary_text_path = setup_object.output_path + sep + marxan_parameter_dict['output_name'] + '_sum.csv'
    if path.isfile(summary_text_path):
        with open(summary_text_path, 'rt') as f:
            summary_reader = reader(f)
            header_list = next(summary_reader)
            for a_row in summary_reader:
                score_value = float(a_row[header_list.index('Score')])
                cost_value = float(a_row[header_list.index('Cost')])
                connectivity_cost_value = float(a_row[header_list.index('Connection Strength')])
                penalty_value = float(a_row[header_list.index('Penalty')])
                mpm_value = float(a_row[header_list.index('MPM')])

                score_list.append(score_value)
                cost_list.append(cost_value)
                connectivity_cost_list.append(connectivity_cost_value)
                penalty_list.append(penalty_value)
                mpm_list.append(mpm_value)

        median_score = median(score_list)
        median_cost = median(cost_list)
        median_connectivity = median(connectivity_cost_list)
        median_penalty = median(penalty_list)
        median_mpm = median(mpm_list)

        zones_calibrate_results_dict['num_iter'] = marxan_parameter_dict['num_iter']
        zones_calibrate_results_dict['num_run'] = marxan_parameter_dict['num_run']
        zones_calibrate_results_dict['blm_value'] = marxan_parameter_dict['blm_value']
        zones_calibrate_results_dict['spf_value'] = marxan_parameter_dict['spf_value']
        zones_calibrate_results_dict['output_name'] = str(marxan_parameter_dict['output_name'])

        zones_calibrate_results_dict['median_score'] = median_score
        zones_calibrate_results_dict['median_cost'] = median_cost
        zones_calibrate_results_dict['median_connectivity'] = median_connectivity
        zones_calibrate_results_dict['median_penalty'] = median_penalty
        zones_calibrate_results_dict['median_mpm'] = median_mpm

    else:
        warning_message('No files found', 'The Marxan summary file was not found and so this process will terminate.')

    return zones_calibrate_results_dict
