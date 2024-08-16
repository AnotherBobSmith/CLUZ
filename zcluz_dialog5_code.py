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

from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsVectorLayer

from csv import reader
from os import path, sep
from subprocess import Popen

from .cluz_dialog5_code import check_import_best_field_name, check_import_summed_field_name
from .cluz_functions5 import check_num_runs_para_dict, check_initial_prop_value_para_dict, check_missing_prop_value_para_dict
from .cluz_functions5 import check_num_iter_para_dict, check_permission_to_use_marxan_folder_para_dict, check_blm_value_para_dict, make_marxan_bat_file, waiting_for_marxan
from .zcluz_functions5 import make_zones_marxan_input_file, return_zones_output_name, check_if_add_zone_target_dat_needed_bool

from .cluz_messages import warning_message


def set_zones_dialog_parameters(zones_marxan_dialog, setup_object):
    zones_marxan_dialog.iterLineEdit.setText(str(setup_object.num_iter))
    zones_marxan_dialog.runLineEdit.setText(str(setup_object.num_runs))
    zones_output_name = return_zones_output_name(setup_object)
    zones_marxan_dialog.outputLineEdit.setText(zones_output_name)
    zones_marxan_dialog.boundLineEdit.setText(str(setup_object.blm_value))

    if setup_object.bound_flag:
        zones_marxan_dialog.boundCheckBox.setChecked(True)
        zones_marxan_dialog.boundLineEdit.setVisible(True)
    else:
        zones_marxan_dialog.boundLineEdit.setVisible(False)

    if setup_object.extra_outputs_flag:
        zones_marxan_dialog.extraCheckBox.setChecked(True)

    produce_blm_table_widget_content(zones_marxan_dialog, setup_object)
    if setup_object.zones_bound_flag:
        zones_marxan_dialog.boundZoneCheckBox.setChecked(True)
        zones_marxan_dialog.blmTableWidget.setEnabled(True)
    else:
        zones_marxan_dialog.boundZoneCheckBox.setChecked(False)
        zones_marxan_dialog.blmTableWidget.setEnabled(False)

    if setup_object.bound_flag is False:
        zones_marxan_dialog.boundZoneCheckBox.setEnabled(False)
        zones_marxan_dialog.blmTableWidget.setEnabled(False)

    zones_marxan_dialog.missingLineEdit.setText(str(setup_object.target_prop))
    zones_marxan_dialog.propLineEdit.setText(str(setup_object.start_prop))


def produce_blm_table_widget_content(zones_marxan_dialog, setup_object):
    zones_marxan_dialog.blmTableWidget.insertColumn(0)
    zones_marxan_dialog.blmTableWidget.insertColumn(1)
    a_row = 0
    for a_zone_tuple_id in setup_object.zones_bound_cost_dict:
        if a_zone_tuple_id[0] != a_zone_tuple_id[1]:
            zone_combination_text = 'Zone ' + str(a_zone_tuple_id[0]) + ' vs Zone ' + str(a_zone_tuple_id[1])
            label_item = QTableWidgetItem(zone_combination_text)
            blm_value = float(setup_object.zones_bound_cost_dict[a_zone_tuple_id])
            zones_marxan_dialog.blmTableWidget.insertRow(a_row)
            label_item.setFlags(Qt.ItemIsEditable)
            zones_marxan_dialog.blmTableWidget.setItem(a_row, 0, label_item)
            zones_marxan_dialog.blmTableWidget.setItem(a_row, 1, QTableWidgetItem(str(blm_value)))
            a_row += 1

    zones_marxan_dialog.blmTableWidget.horizontalHeader().hide()
    zones_marxan_dialog.blmTableWidget.horizontalHeader().setStretchLastSection(True)
    zones_marxan_dialog.blmTableWidget.verticalHeader().hide()


def make_zones_marxan_raw_parameter_dict(zones_marxan_dialog, setup_object):
    num_iter_string = zones_marxan_dialog.iterLineEdit.text()
    num_run_string = zones_marxan_dialog.runLineEdit.text()
    output_name = str(zones_marxan_dialog.outputLineEdit.text())
    setup_object.output_name = output_name
    if zones_marxan_dialog.boundCheckBox.isChecked():
        blm_value_string = zones_marxan_dialog.boundLineEdit.text()
    else:
        blm_value_string = '0'
    missing_prop_string = zones_marxan_dialog.missingLineEdit.text()
    initial_prop_string = zones_marxan_dialog.propLineEdit.text()
    extra_outputs_bool = zones_marxan_dialog.extraCheckBox.isChecked()

    marxan_raw_parameter_dict = dict()
    marxan_raw_parameter_dict['num_iter_string'] = num_iter_string
    marxan_raw_parameter_dict['num_run_string'] = num_run_string
    marxan_raw_parameter_dict['blm_value_string'] = blm_value_string
    marxan_raw_parameter_dict['missing_prop_string'] = missing_prop_string
    marxan_raw_parameter_dict['initial_prop_string'] = initial_prop_string
    marxan_raw_parameter_dict['extra_outputs_bool'] = extra_outputs_bool
    marxan_raw_parameter_dict['output_name'] = output_name
    marxan_raw_parameter_dict['marxan_path'] = setup_object.marxan_path

    return marxan_raw_parameter_dict


def make_zones_marxan_parameter_dict(setup_object, zones_marxan_raw_parameter_dict):
    zones_marxan_parameter_dict = dict()
    zones_marxan_parameter_dict['num_iter'] = int(zones_marxan_raw_parameter_dict['num_iter_string'])
    zones_marxan_parameter_dict['num_run'] = int(zones_marxan_raw_parameter_dict['num_run_string'])
    zones_marxan_parameter_dict['blm_value'] = float(zones_marxan_raw_parameter_dict['blm_value_string'])
    zones_marxan_parameter_dict['missing_prop'] = float(zones_marxan_raw_parameter_dict['missing_prop_string'])
    zones_marxan_parameter_dict['initial_prop'] = float(zones_marxan_raw_parameter_dict['initial_prop_string'])

    zones_marxan_parameter_dict['extra_outputs_bool'] = zones_marxan_raw_parameter_dict['extra_outputs_bool']
    zones_marxan_parameter_dict['output_name'] = zones_marxan_raw_parameter_dict['output_name']
    zones_marxan_parameter_dict['extra_outputs_bool'] = zones_marxan_raw_parameter_dict['extra_outputs_bool']

    marxan_path = setup_object.marxan_path
    marxan_folder_name = path.dirname(marxan_path)
    marxan_setup_path = str(marxan_folder_name) + sep + 'input.dat'
    zones_marxan_parameter_dict["marxan_path"] = marxan_path
    zones_marxan_parameter_dict["marxan_setup_path"] = marxan_setup_path

    return zones_marxan_parameter_dict


def check_zones_marxan_input_values_ok_bool(marxan_parameter_dict):
    marxan_input_values_ok_bool = check_num_iter_para_dict(marxan_parameter_dict['num_iter_string'])
    marxan_input_values_ok_bool = check_num_runs_para_dict(marxan_parameter_dict['num_run_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_blm_value_para_dict(marxan_parameter_dict['blm_value_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_missing_prop_value_para_dict(marxan_parameter_dict['missing_prop_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_initial_prop_value_para_dict(marxan_parameter_dict['initial_prop_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_permission_to_use_marxan_folder_para_dict(marxan_parameter_dict, marxan_input_values_ok_bool)

    return marxan_input_values_ok_bool


def check_zones_marxan_files_exist_bool(setup_object):
    marxan_files_exist_bool = True
    pu_dat_path = setup_object.input_path + sep + 'pu.dat'
    spec_dat_path = setup_object.input_path + sep + 'feat.dat'
    puvspr2_dat_path = setup_object.input_path + sep + 'puvspr2.dat'

    if path.exists(pu_dat_path) is False:
        warning_message('Missing Marxan file', 'There is no pu.dat file in the specified Marxan input folder. Please create the file using the Create Marxan input files function')
        marxan_files_exist_bool = False
    if path.exists(spec_dat_path) is False:
        warning_message('Missing Marxan file', 'There is no feat.dat file in the specified Marxan input folder. Please create the file using the Create Marxan input files function')
        marxan_files_exist_bool = False
    if path.exists(puvspr2_dat_path) is False:
        warning_message('Missing Marxan file', 'There is no puvspr2.dat file in the specified Marxan input folder. Please create one')
        marxan_files_exist_bool = False

    return marxan_files_exist_bool


def launch_zones_marxan_analysis(setup_object, zones_marxan_parameter_dict):
    add_zone_target_dat_bool = check_if_add_zone_target_dat_needed_bool(setup_object)
    make_zones_marxan_input_file(setup_object, zones_marxan_parameter_dict, add_zone_target_dat_bool)
    zones_marxan_bat_file_name = make_marxan_bat_file(setup_object)
    Popen([zones_marxan_bat_file_name])
    waiting_for_marxan(setup_object, zones_marxan_parameter_dict['output_name'])
    best_output_file = setup_object.output_path + sep + zones_marxan_parameter_dict['output_name'] + '_best.csv'
    summed_output_file = setup_object.output_path + sep + zones_marxan_parameter_dict['output_name'] + '_ssoln.csv'

    return best_output_file, summed_output_file


# Load previous results ########################################################

def zones_return_initial_load_field_names(setup_object):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    field_name_list = [field.name() for field in pu_layer.fields()]
    zones_best_name = 'IMP_BEST'
    best_suffix = ''
    if zones_best_name in field_name_list:
        best_suffix = 1
        while (zones_best_name + str(best_suffix)) in field_name_list:
            best_suffix += 1
    final_best_name = zones_best_name + str(best_suffix)

    zones_summed_name = 'I'
    summed_suffix_number = 1
    prefix_suffix_name_list = list()
    for aName in field_name_list:
        prefix_suffix_name_list.append([aName[0:4], aName[-2:]])
    name_loop_bool = True

    while name_loop_bool:
        prefix_suffix_name_count = 0
        for prefixSuffixNameElement in prefix_suffix_name_list:
            if prefixSuffixNameElement[0] == zones_summed_name + str(summed_suffix_number) + '_Z' and prefixSuffixNameElement[1] == 'SF':
                prefix_suffix_name_count += 1
        if prefix_suffix_name_count == 0:
            name_loop_bool = False
        else:
            summed_suffix_number += 1

    final_summed_name = zones_summed_name + str(summed_suffix_number)

    return final_best_name, final_summed_name


def zones_check_load_best_marxan_result_file(zones_load_dialog, setup_object):
    zones_best_field_name = zones_load_dialog.zonesBestNameLineEdit.text()
    if zones_load_dialog.zonesBestCheckBox.isChecked():
        load_best_path = zones_load_dialog.zonesBestLineEdit.text()
    else:
        load_best_path = 'blank'
    zones_check_bool = check_import_best_field_name(setup_object, zones_best_field_name)
    if zones_check_bool:
        zones_load_dialog.close()
        if load_best_path != 'blank':
            if path.isfile(load_best_path):
                with open(load_best_path, 'rt') as f:
                    zones_best_reader = reader(f)
                    best_header = next(zones_best_reader, None)  # skip the headers
                if best_header != setup_object.zones_best_heading_field_names:
                    zones_check_bool = False
                    warning_message('Invalid file', 'The specified Marxan with Zones best output file is incorrectly formatted. It must contain only two fields named planning_unit and zone.')
            else:
                zones_check_bool = False
                warning_message('Incorrect pathname', 'The specified pathname for the Marxan with Zones best output is invalid. Please choose another one.')

    return zones_check_bool


def zones_check_load_summed_marxan_result_file(load_dialog, setup_object):
    summed_field_name = load_dialog.zonesSummedNameLineEdit.text()
    if load_dialog.zonesSummedCheckBox.isChecked():
        load_summed_path = load_dialog.zonesSummedLineEdit.text()
    else:
        load_summed_path = 'blank'
    zones_check_bool = check_import_summed_field_name(setup_object, summed_field_name)
    if zones_check_bool:
        load_dialog.close()
        if load_summed_path != 'blank':
            if path.isfile(load_summed_path):
                with open(load_summed_path, 'rt') as f:
                    summed_reader = reader(f)
                    summed_header_list = next(summed_reader, None)  # skip the headers
                if summed_header_list.count('planning unit') + summed_header_list.count('number') != 2:
                    zones_check_bool = False
                    warning_message('Invalid file', 'The specified Marxan with Zones summed output file is incorrectly formatted. It must include two fields named planning unit and number')
            else:
                zones_check_bool = False
                warning_message('Incorrect pathname', 'The specified pathname for the Marxan with Zones summed output is invalid. Please choose another one')

    return zones_check_bool
