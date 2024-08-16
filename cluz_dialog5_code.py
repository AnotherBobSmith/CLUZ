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

from csv import reader
from os import listdir, path, remove, sep
from subprocess import Popen
from time import sleep

from .cluz_functions5 import check_num_runs_para_dict, make_calibrate_parameter_value_list, add_best_marxan_output_to_pu_shapefile, make_marxan_bat_file
from .cluz_functions5 import check_initial_prop_value_para_dict, check_missing_prop_value_para_dict, make_calibrate_results_dict, add_summed_marxan_output_to_pu_shapefile, waiting_for_marxan
from .cluz_functions5 import return_output_name, make_marxan_input_file, check_num_iter_para_dict, check_permission_to_use_marxan_folder_para_dict, check_blm_value_para_dict
from .cluz_functions5 import make_calibrate_spec_dat_file

from .zcluz_functions5 import make_zones_marxan_input_file, check_if_add_zone_target_dat_needed_bool, make_zones_calibrate_results_dict

from .cluz_display import display_graduated_layer, reload_pu_layer, display_best_output
from .cluz_messages import warning_message


# Marxan Dialog###########################################
def set_dialog_parameters(marxan_dialog, setup_object):
    marxan_dialog.boundLineEdit.setVisible(False)

    marxan_dialog.iterLineEdit.setText(str(setup_object.num_iter))
    marxan_dialog.runLineEdit.setText(str(setup_object.num_runs))
    output_name = return_output_name(setup_object)
    marxan_dialog.outputLineEdit.setText(output_name)
    marxan_dialog.boundLineEdit.setText(str(setup_object.blm_value))

    if setup_object.bound_flag:
        marxan_dialog.boundCheckBox.setChecked(True)
        marxan_dialog.boundLineEdit.setVisible(True)

    if setup_object.extra_outputs_flag:
        marxan_dialog.extraCheckBox.setChecked(True)

    marxan_dialog.missingLineEdit.setText(str(setup_object.target_prop))
    marxan_dialog.propLineEdit.setText(str(setup_object.start_prop))


def make_marxan_raw_parameter_dict(marxan_dialog, setup_object):
    num_iter_string = marxan_dialog.iterLineEdit.text()
    num_run_string = marxan_dialog.runLineEdit.text()
    output_name = str(marxan_dialog.outputLineEdit.text())
    setup_object.output_name = output_name
    if marxan_dialog.boundCheckBox.isChecked():
        blm_value_string = marxan_dialog.boundLineEdit.text()
    else:
        blm_value_string = "0"
    missing_prop_string = marxan_dialog.missingLineEdit.text()
    initial_prop_string = marxan_dialog.propLineEdit.text()
    extra_outputs_bool = marxan_dialog.extraCheckBox.isChecked()

    marxan_raw_parameter_dict = dict()
    marxan_raw_parameter_dict['num_iter_string'] = num_iter_string
    marxan_raw_parameter_dict['num_run_string'] = num_run_string
    marxan_raw_parameter_dict['blm_value_string'] = blm_value_string
    marxan_raw_parameter_dict['missing_prop_string'] = missing_prop_string
    marxan_raw_parameter_dict['initial_prop_string'] = initial_prop_string
    marxan_raw_parameter_dict['extra_outputs_bool'] = extra_outputs_bool
    marxan_raw_parameter_dict['spec_name'] = 'spec.dat'
    marxan_raw_parameter_dict['output_name'] = output_name
    marxan_raw_parameter_dict['marxan_path'] = setup_object.marxan_path

    return marxan_raw_parameter_dict


def make_marxan_parameter_dict(setup_object, marxan_raw_parameter_dict):
    marxan_parameter_dict = dict()
    marxan_parameter_dict['num_iter'] = int(marxan_raw_parameter_dict['num_iter_string'])
    marxan_parameter_dict['num_run'] = int(marxan_raw_parameter_dict['num_run_string'])
    marxan_parameter_dict['blm_value'] = float(marxan_raw_parameter_dict['blm_value_string'])
    marxan_parameter_dict['missing_prop'] = float(marxan_raw_parameter_dict['missing_prop_string'])
    marxan_parameter_dict['initial_prop'] = float(marxan_raw_parameter_dict['initial_prop_string'])

    marxan_parameter_dict['extra_outputs_bool'] = marxan_raw_parameter_dict['extra_outputs_bool']
    marxan_parameter_dict['spec_name'] = marxan_raw_parameter_dict['spec_name']
    marxan_parameter_dict['output_name'] = marxan_raw_parameter_dict['output_name']
    marxan_parameter_dict['extra_outputs_bool'] = marxan_raw_parameter_dict['extra_outputs_bool']

    marxan_path = setup_object.marxan_path
    marxan_folder_name = path.dirname(marxan_path)
    marxan_setup_path = str(marxan_folder_name) + sep + 'input.dat'
    marxan_parameter_dict["marxan_path"] = marxan_path
    marxan_parameter_dict["marxan_setup_path"] = marxan_setup_path

    return marxan_parameter_dict


def return_marxan_input_values_ok_bool(marxan_parameter_dict):
    marxan_input_values_ok_bool = check_num_iter_para_dict(marxan_parameter_dict['num_iter_string'])
    marxan_input_values_ok_bool = check_num_runs_para_dict(marxan_parameter_dict['num_run_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_blm_value_para_dict(marxan_parameter_dict['blm_value_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_missing_prop_value_para_dict(marxan_parameter_dict['missing_prop_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_initial_prop_value_para_dict(marxan_parameter_dict['initial_prop_string'], marxan_input_values_ok_bool)
    marxan_input_values_ok_bool = check_permission_to_use_marxan_folder_para_dict(marxan_parameter_dict, marxan_input_values_ok_bool)

    return marxan_input_values_ok_bool


def check_marxan_files_exist_bool(setup_object):
    marxan_files_exist_bool = True
    pu_dat_path = setup_object.input_path + sep + 'pu.dat'
    spec_dat_path = setup_object.input_path + sep + 'spec.dat'
    puvspr2_dat_path = setup_object.input_path + sep + 'puvspr2.dat'

    if path.exists(pu_dat_path) is False:
        warning_message('Missing Marxan file', 'There is no pu.dat file in the specified Marxan input folder. Please create the file using the Create Marxan input files function')
        marxan_files_exist_bool = False
    if path.exists(spec_dat_path) is False:
        warning_message('Missing Marxan file', 'There is no spec.dat file in the specified Marxan input folder. Please create the file using the Create Marxan input files function')
        marxan_files_exist_bool = False
    if path.exists(puvspr2_dat_path) is False:
        warning_message('Missing Marxan file', 'There is no puvspr2.dat file in the specified Marxan input folder. Please create one')
        marxan_files_exist_bool = False

    return marxan_files_exist_bool


def launch_marxan_analysis(setup_object, marxan_parameter_dict):
    make_marxan_input_file(setup_object, marxan_parameter_dict)
    marxan_bat_file_name = make_marxan_bat_file(setup_object)
    Popen([marxan_bat_file_name])
    waiting_for_marxan(setup_object, marxan_parameter_dict['output_name'])
    best_output_file = setup_object.output_path + sep + marxan_parameter_dict['output_name'] + '_best.txt'
    summed_output_file = setup_object.output_path + sep + marxan_parameter_dict['output_name'] + '_ssoln.txt'

    return best_output_file, summed_output_file


# Load previous results ########################################################

def return_initial_load_field_names(setup_object):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    field_name_list = [field.name() for field in pu_layer.fields()]
    best_name = 'IMP_BEST'
    best_suffix = ''
    if best_name in field_name_list:
        best_suffix = 1
        while (best_name + str(best_suffix)) in field_name_list:
            best_suffix += 1
    final_best_name = best_name + str(best_suffix)

    summed_name = 'IMP_SUM'
    summed_suffix = ''
    if summed_name in field_name_list:
        summed_suffix = 1
        while (summed_name + str(summed_suffix)) in field_name_list:
            summed_suffix += 1
    final_summed_name = summed_name + str(summed_suffix)

    return final_best_name, final_summed_name


def check_load_best_marxan_result(load_dialog, setup_object):
    best_field_name = load_dialog.bestNameLineEdit.text()
    if load_dialog.bestCheckBox.isChecked():
        best_path = load_dialog.bestLineEdit.text()
    else:
        best_path = 'blank'
    progress_bool = check_import_best_field_name(setup_object, best_field_name)
    if progress_bool:
        load_dialog.close()
        if best_path != 'blank':
            if path.isfile(best_path):
                with open(best_path, 'rt') as f:
                    best_reader = reader(f)
                    best_header = next(best_reader, None)  # skip the headers
                if best_header == setup_object.best_heading_field_names:
                    add_best_marxan_output_to_pu_shapefile(setup_object, best_path, best_field_name)
                    best_shapefile_name = best_field_name
                    display_best_output(setup_object, best_field_name, best_shapefile_name)
                else:
                    warning_message('Invalid file', 'The specified Marxan best output file is incorrectly formatted. It must contain only two fields named planning_unit and zone.')
            else:
                warning_message('Incorrect pathname', 'The specified pathname for the Marxan best output is invalid. Please choose another one.')


def check_import_best_field_name(setup_object, best_field_name):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    field_name_list = [field.name() for field in pu_layer.fields()]
    progress_bool = True
    if best_field_name in field_name_list:
        warning_message('Best field name duplication', 'The planning unit theme already contains a field named ' + best_field_name + '. Please choose another name.')
        progress_bool = False
    if len(best_field_name) > 10:
        warning_message('Invalid field name', 'The Best field name cannot be more than 10 characters long.')
        progress_bool = False
        
    return progress_bool


def check_load_summed_marxan_result(load_dialog, setup_object):
    summed_field_name = load_dialog.summedNameLineEdit.text()
    if load_dialog.summedCheckBox.isChecked():
        summed_path = load_dialog.summedLineEdit.text()
    else:
        summed_path = 'blank'
        
    progress_bool = check_import_summed_field_name(setup_object, summed_field_name)
    if progress_bool:
        load_dialog.close()
        if summed_path != 'blank':
            if path.isfile(summed_path):
                with open(summed_path, 'rt') as f:
                    summed_reader = reader(f)
                    summed_header = next(summed_reader, None)  # skip the headers
                if summed_header == setup_object.summed_heading_field_names:
                    add_summed_marxan_output_to_pu_shapefile(setup_object, summed_path, summed_field_name)
                    summed_shapefile_name = summed_field_name
                    display_graduated_layer(setup_object, summed_field_name, summed_shapefile_name, 1)  # 1 is SF legend code
                else:
                    warning_message('Invalid file', 'The specified Marxan summed output file is incorrectly formatted. It must contain only two fields named planning_unit and number')
            else:
                warning_message('Incorrect pathname', 'The specified pathname for the Marxan summed output is invalid. Please choose another one')


def check_import_summed_field_name(setup_object, summed_field_name):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    field_name_list = [field.name() for field in pu_layer.fields()]
    progress_bool = True
    if summed_field_name in field_name_list:
        warning_message('Summed field name duplication', 'The planning unit theme already contains a field named ' + summed_field_name + '. Please choose another name.')
        progress_bool = False
    if len(summed_field_name) > 10:
        warning_message('Invalid field name', 'The Summed field name cannot be more than 10 characters long.')
        progress_bool = False

    return progress_bool


# Calibrate Dialog #######################################################

def set_initial_values_calibrate_dialog(calibrate_dialog, setup_object):
    calibrate_dialog.paraComboBox.addItems(['BLM', 'Number of iterations', 'Number of runs', 'SPF'])
    calibrate_dialog.iterLineEdit.setText(str(setup_object.num_iter))
    calibrate_dialog.runLineEdit.setText(str(setup_object.num_runs))
    calibrate_dialog.boundLineEdit.setText(str(setup_object.blm_value))
    calibrate_dialog.boundLabel.setEnabled(False)
    calibrate_dialog.boundLineEdit.setEnabled(False)
    calibrate_dialog.boundLineEdit.setText('Specified above')
    calibrate_dialog.spfLabel.setEnabled(False)
    calibrate_dialog.spfLineEdit.setEnabled(False)
    calibrate_dialog.spfLineEdit.setText('As specified in spec.dat file')


def make_marxan_calibrate_raw_parameter_dict(calibrate_dialog):
    calibrate_raw_parameter_dict = dict()
    calibrate_raw_parameter_dict['num_analyses_text'] = calibrate_dialog.numberLineEdit.text()
    calibrate_raw_parameter_dict['min_analyses_text'] = calibrate_dialog.minLineEdit.text()
    calibrate_raw_parameter_dict['max_analyses_text'] = calibrate_dialog.maxLineEdit.text()
    calibrate_raw_parameter_dict['iter_analyses_text'] = calibrate_dialog.iterLineEdit.text()
    calibrate_raw_parameter_dict['run_analyses_text'] = calibrate_dialog.runLineEdit.text()
    calibrate_raw_parameter_dict['blm_analyses_text'] = calibrate_dialog.boundLineEdit.text()
    calibrate_raw_parameter_dict['spf_analyses_text'] = calibrate_dialog.spfLineEdit.text()

    calibrate_raw_parameter_dict['output_name_base'] = calibrate_dialog.outputLineEdit.text()
    calibrate_raw_parameter_dict['result_path_text'] = calibrate_dialog.resultsLineEdit.text()
    
    return calibrate_raw_parameter_dict


def check_calibrate_analysis_parameters(calibrate_dialog, calibrate_raw_parameter_dict):
    num_run_list = list()
    num_iter_list = list()
    blm_value_list = list()
    spf_list = list()
    check_bool = True

    check_bool = check_calibrate_output_name_base(calibrate_raw_parameter_dict, check_bool)
    check_bool = check_calibrate_output_num_analyses(calibrate_raw_parameter_dict, check_bool)
    check_bool = check_calibrate_output_min_max_values(calibrate_dialog, calibrate_raw_parameter_dict, check_bool)

    if check_bool:
        exponential_bool = calibrate_dialog.expCheckBox.isChecked()
        parameter_value_list = make_calibrate_parameter_value_list(calibrate_raw_parameter_dict, exponential_bool)
        num_iter_list, check_bool = check_calibrate_num_iter_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool)
        num_run_list, check_bool = check_calibrate_num_run_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool)
        blm_value_list, check_bool = check_calibrate_blm_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool)
        spf_list, check_bool = check_calibrate_spf_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool)

    return check_bool, num_run_list, num_iter_list, blm_value_list, spf_list

        
def check_calibrate_output_name_base(calibrate_raw_parameter_dict, check_bool):
    if calibrate_raw_parameter_dict['output_name_base'] == '':
        warning_message('Incorrect output basename', 'The specified basename for the Marxan output files is blank. Please choose another one')
        check_bool = False

    return check_bool


def check_calibrate_output_num_analyses(calibrate_raw_parameter_dict, check_bool):
    try:
        num_analyses = int(calibrate_raw_parameter_dict['num_analyses_text'])
        if num_analyses < 1:
            warning_message('Incorrect format', 'The specified number of analysis is incorrectly formatted. It must be an integer and greater than 1.')
            check_bool = False
    except ValueError:
        warning_message('Incorrect format', 'The specified number of analysis is incorrectly formatted. It must be an integer and greater than 1.')
        check_bool = False

    return check_bool


def check_calibrate_output_min_max_values(calibrate_dialog, calibrate_raw_parameter_dict, check_bool):
    if calibrate_dialog.paraComboBox.currentText() == 'BLM' or calibrate_dialog.paraComboBox.currentText() == 'SPF':
        value_floor = 0
        min_warning_message_string = 'The specified minimum value is incorrectly formatted. It must be a number greater than 0.'
        max_warning_message_string = 'The specified maximum value is incorrectly formatted. It must be a number greater than 0.'
    else:
        value_floor = 1
        min_warning_message_string = 'The specified minimum value is incorrectly formatted. It must be a number greater than 1.'
        max_warning_message_string = 'The specified maximum value is incorrectly formatted. It must be a number greater than 1.'
    try:
        test_min_value = float(calibrate_raw_parameter_dict['min_analyses_text'])
        if test_min_value < value_floor:
            warning_message('Incorrect format', min_warning_message_string)
            check_bool = False
        if calibrate_dialog.paraComboBox.currentText() == 'Number of iterations' or calibrate_dialog.paraComboBox.currentText() == 'Number of runs':
            if test_min_value.is_integer() is False:
                warning_message('Incorrect format', 'The specified minimum value has to be an integer.')
                check_bool = False
    except ValueError:
        warning_message('Incorrect format', min_warning_message_string)
        check_bool = False
    try:
        test_max_value = float(calibrate_raw_parameter_dict['max_analyses_text'])
        if test_max_value < value_floor:
            warning_message('Incorrect format', max_warning_message_string)
            check_bool = False
        if calibrate_dialog.paraComboBox.currentText() == 'Number of iterations' or calibrate_dialog.paraComboBox.currentText() == 'Number of runs':
            if test_max_value.is_integer() is False:
                warning_message('Incorrect format', 'The specified maximum value has to be an integer.')
                check_bool = False
    except ValueError:
        warning_message('Incorrect format', max_warning_message_string)
        check_bool = False
    try:
        if float(calibrate_raw_parameter_dict['min_analyses_text']) > float(calibrate_raw_parameter_dict['max_analyses_text']):
            warning_message('Incorrect format', 'The specified minimum value has to be lower than the specified maximum value.')
            check_bool = False
    except ValueError:
        check_bool = False

    return check_bool


def check_calibrate_num_iter_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool):
    num_iter_list = parameter_value_list
    if calibrate_dialog.iterLineEdit.isEnabled():
        num_iter_text = calibrate_dialog.iterLineEdit.text()
        try:
            num_iter = int(num_iter_text)
            num_iter_list = [num_iter] * int(calibrate_raw_parameter_dict['run_analyses_text'])
            if num_iter < 10000:
                warning_message('Incorrect format', 'The specified number of iterations is incorrectly formatted. It must be an integer greater than 10000 (Marxan uses 10000 temperature drops in the simulated annealing process in these analyses and the number of iterations must be greater than the number of temperature drops).')
                check_bool = False
        except ValueError:
            warning_message('Incorrect format', 'The specified number of iterations is incorrectly formatted. It must be a positive integer.')
            check_bool = False

    return num_iter_list, check_bool


def check_calibrate_num_run_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool):
    num_run_list = parameter_value_list
    if calibrate_dialog.runLineEdit.isEnabled():
        num_run_text = calibrate_dialog.runLineEdit.text()
        try:
            num_run = int(num_run_text)
            num_run_list = [num_run] * int(calibrate_raw_parameter_dict['run_analyses_text'])
            if num_run < 1:
                warning_message('Incorrect format', 'The specified number of runs is incorrectly formatted. It must be a positive integer.')
                check_bool = False
        except ValueError:
            warning_message('Incorrect format', 'The specified number of runs is incorrectly formatted. It must be a positive integer.')
            check_bool = False
        
    return num_run_list, check_bool


def check_calibrate_blm_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool):
    blm_value_list = parameter_value_list
    if calibrate_dialog.boundLineEdit.isEnabled():
        blm_value_text = calibrate_dialog.boundLineEdit.text()
        try:
            blm_value = float(blm_value_text)
            blm_value_list = [blm_value] * int(calibrate_raw_parameter_dict['run_analyses_text'])
            if blm_value < 0:
                warning_message('Incorrect format', 'The specified BLM value is incorrectly formatted. It must be a positive number.')
                check_bool = False
        except ValueError:
            warning_message('Incorrect format', 'The specified BLM value is incorrectly formatted. It must be a positive number.')
            check_bool = False

    return blm_value_list, check_bool


def check_calibrate_spf_value(calibrate_dialog, calibrate_raw_parameter_dict, parameter_value_list, check_bool):
    if calibrate_dialog.spfLineEdit.text() == 'As specified in spec.dat file':
        spf_value_list = ['As specified in spec.dat file'] * int(calibrate_raw_parameter_dict['run_analyses_text'])
    else:
        spf_value_list = parameter_value_list

    return spf_value_list, check_bool


def run_calibrate_marxan(setup_object, calibrate_raw_parameter_dict, num_run_list, num_iter_list, blm_value_list, spf_value_list):
    calibrate_results_dict = dict()
    for analysis_number in range(0, int(calibrate_raw_parameter_dict['num_analyses_text'])):
        marxan_parameter_dict = make_calibrate_marxan_parameter_dict(setup_object, calibrate_raw_parameter_dict, num_iter_list, num_run_list, blm_value_list, spf_value_list, analysis_number)
        if len(set(spf_value_list)) != 1:
            spf_value = spf_value_list[analysis_number]
            calibrate_spec_dat_file_name = 'calib_del_later_spec' + str(analysis_number) + '.dat'
            marxan_parameter_dict['spec_name'] = calibrate_spec_dat_file_name
            make_calibrate_spec_dat_file(setup_object, calibrate_spec_dat_file_name, spf_value)
        if setup_object.analysis_type != 'MarxanWithZones':
            make_marxan_input_file(setup_object, marxan_parameter_dict)
        else:
            add_zone_target_dat_bool = check_if_add_zone_target_dat_needed_bool(setup_object)
            make_zones_marxan_input_file(setup_object, marxan_parameter_dict, add_zone_target_dat_bool)
        marxan_bat_file_name = make_marxan_bat_file(setup_object)
        Popen([marxan_bat_file_name])
        sleep(2)
        waiting_for_marxan(setup_object, calibrate_raw_parameter_dict['output_name_base'] + str(analysis_number + 1))

        if setup_object.analysis_type != 'MarxanWithZones':
            calibrate_results_dict[analysis_number] = make_calibrate_results_dict(setup_object, marxan_parameter_dict)
        else:
            calibrate_results_dict[analysis_number] = make_zones_calibrate_results_dict(setup_object, marxan_parameter_dict)
        if len(set(spf_value_list)) != 1:
            remove_calibrate_spec_dat_file(setup_object)

    return calibrate_results_dict


def make_calibrate_marxan_parameter_dict(setup_object, calibrate_raw_parameter_dict, num_iter_list, num_run_list, blm_value_list, spf_value_list, analysis_number):
    missing_prop_value = 1.0
    initial_prop_value = 0.2
    calibrate_marxan_parameter_dict = dict()
    calibrate_marxan_parameter_dict['num_iter'] = num_iter_list[analysis_number]
    calibrate_marxan_parameter_dict['num_run'] = num_run_list[analysis_number]
    calibrate_marxan_parameter_dict['blm_value'] = blm_value_list[analysis_number]
    calibrate_marxan_parameter_dict['spf_value'] = spf_value_list[analysis_number]
    calibrate_marxan_parameter_dict['missing_prop'] = missing_prop_value
    calibrate_marxan_parameter_dict['initial_prop'] = initial_prop_value

    calibrate_marxan_parameter_dict['output_name'] = calibrate_raw_parameter_dict['output_name_base'] + str(analysis_number + 1)
    calibrate_marxan_parameter_dict['extra_outputs_bool'] = True
    calibrate_marxan_parameter_dict['spec_name'] = 'spec.dat'

    marxan_path = setup_object.marxan_path
    marxan_folder_name = path.dirname(marxan_path)
    marxan_setup_path = str(marxan_folder_name) + sep + 'input.dat'
    calibrate_marxan_parameter_dict['marxan_path'] = marxan_path
    calibrate_marxan_parameter_dict['marxan_setup_path'] = marxan_setup_path

    return calibrate_marxan_parameter_dict


def remove_calibrate_spec_dat_file(setup_object):
    input_file_list = listdir(setup_object.input_path)
    for aFile in input_file_list:
        if 'calib_del_later_spec' in aFile:
            remove_file_path = setup_object.input_path + sep + aFile
            remove(remove_file_path)
