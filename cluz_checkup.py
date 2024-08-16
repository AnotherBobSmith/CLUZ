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

from qgis.core import QgsVectorLayer, QgsProject

from os import access, path, sep, W_OK
from csv import reader
from time import ctime

from .cluz_messages import warning_message
from .cluz_display import add_pu_layer
from .cluz_make_file_dicts import change_conserved_field_name_to_ear_cons


def check_files_and_return_setup_file_ok_bool(setup_object, analysis_type, dec_place_text, num_iter_text, num_run_text, num_blm_text, start_prop_text, target_prop_text):
    setup_file_ok = True
    if analysis_type not in ['Marxan', 'MarxanWithZones']:
        warning_message('Setup file incorrect format', 'The analysis type value is not specified as Marxan or MarxanWithZones. Please correct this.')
        setup_file_ok = False
    try:
        setup_object.decimal_places = int(dec_place_text)
        if setup_object.decimal_places > 5:
            setup_object.decimal_places = 5
    except ValueError:
        warning_message('Setup file incorrect format', 'The specified decimal place value in the setup file is not an integer. Please correct this.')
        setup_file_ok = False
    try:
        setup_object.num_iter = int(num_iter_text)
    except ValueError:
        warning_message('Setup file incorrect format', 'The specified number of iterations in the setup file is not an integer. Please correct this.')
        setup_file_ok = False
    try:
        setup_object.num_runs = int(num_run_text)
    except ValueError:
        warning_message('Setup file incorrect format', 'The specified number of runs in the setup file is not an integer. Please correct this.')
        setup_file_ok = False
    try:
        setup_object.blm_value = float(num_blm_text)
    except ValueError:
        warning_message('Setup file incorrect format', 'The BLM value in the setup file is not a number. Please correct this.')
        setup_file_ok = False
    try:
        setup_object.start_prop = float(start_prop_text)
    except ValueError:
        warning_message('Setup file incorrect format', 'The start proportion value in the setup file is not a number. Please correct this.')
        setup_file_ok = False
    try:
        setup_object.target_prop = float(target_prop_text)
    except ValueError:
        warning_message('Setup file incorrect format', 'The target proportion value in the setup file is not a number. Please correct this.')
        setup_file_ok = False

    return setup_file_ok


def check_status_object_values(setup_object):
    setup_file_correct_bool = True

    setup_file_correct_bool = check_dec_places_value(setup_object, setup_file_correct_bool)
    setup_file_correct_bool = check_num_iters_value(setup_object, setup_file_correct_bool)
    setup_file_correct_bool = check_num_runs_value(setup_object, setup_file_correct_bool)
    setup_file_correct_bool = check_blm_value(setup_object, setup_file_correct_bool)
    setup_file_correct_bool = check_start_prop(setup_object, setup_file_correct_bool)
    setup_file_correct_bool = check_cluz_file_paths(setup_object, setup_file_correct_bool)

    folders_ok_bool = check_folder_values(setup_object)

    if setup_file_correct_bool and folders_ok_bool:
        setup_object.setup_status = 'values_checked'

    return setup_object


def check_dec_places_value(setup_object, setup_file_correct_bool):
    try:
        setup_object.decimal_places = int(setup_object.decimal_places)
        if setup_object.decimal_places < 0:
            warning_message('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of decimal places cannot be a negative value. Please correct this.')
            setup_file_correct_bool = False
    except ValueError:
        warning_message('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of decimal places in the Abundance and Target tables is not an integer. Please correct this.')
        setup_file_correct_bool = False

    return setup_file_correct_bool


def check_num_iters_value(setup_object, setup_file_correct_bool):
    try:
        setup_object.num_iter = int(setup_object.num_iter)
        if setup_object.num_iter < 0:
            warning_message('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of Marxan iterations cannot be a negative value. Please correct this.')
            setup_file_correct_bool = False
    except ValueError:
        warning_message('Setup file incorrect format', 'The specified number of iterations in the setup file is not an integer. Please correct this.')
        setup_file_correct_bool = False

    return setup_file_correct_bool


def check_num_runs_value(setup_object, setup_file_correct_bool):
    try:
        setup_object.num_runs = int(setup_object.num_runs)
        if setup_object.num_runs < 0:
            warning_message('Setup file incorrect format', 'The specified value in the CLUZ setup file for number of Marxan runs cannot be a negative value. Please correct this.')
            setup_file_correct_bool = False
    except ValueError:
        warning_message('Setup file incorrect format', 'The specified number of runs in the setup file is not an integer. Please correct this.')
        setup_file_correct_bool = False

    return setup_file_correct_bool


def check_blm_value(setup_object, setup_file_correct_bool):
    try:
        setup_object.blm_value = float(setup_object.blm_value)
        if setup_object.blm_value < 0:
            warning_message('Setup file incorrect format', 'The specified BLM value in the CLUZ setup file cannot be a negative value. Please correct this.')
            setup_file_correct_bool = False
    except ValueError:
        warning_message('Setup file incorrect format', 'The BLM value in the setup file is not a number. Please correct this.')
        setup_file_correct_bool = False

    return setup_file_correct_bool


def check_start_prop(setup_object, setup_file_correct_bool):
    try:
        setup_object.start_prop = float(setup_object.start_prop)
        if setup_object.start_prop < 0 or setup_object.start_prop > 1:
            warning_message('Setup file incorrect format', 'The specified proportion of planning units initially selected by Marxan as specified in the CLUZ setup has to be between 0 and 1. Please correct this.')
            setup_file_correct_bool = False
    except ValueError:
        warning_message('Setup file incorrect format', 'The start proportion value in the setup file is not a number. Please correct this.')
        setup_file_correct_bool = False

    return setup_file_correct_bool


def check_target_prop(setup_object, setup_file_correct_bool):
    try:
        setup_object.target_prop = float(setup_object.target_prop)
        if setup_object.target_prop < 0 or setup_object.target_prop > 1:
            warning_message('Setup file incorrect format', 'The specified proportion of a target that needs to be achieved for Marxan to report that the target has been met as specified in the CLUZ setup has to be between 0 and 1. Please correct this.')
            setup_file_correct_bool = False
    except ValueError:
        warning_message('Setup file incorrect format', 'The target proportion value in the setup file is not a number. Please correct this.')
        setup_file_correct_bool = False

    return setup_file_correct_bool


def check_cluz_file_paths(setup_object, setup_file_correct_bool):
    input_path = setup_object.input_path
    if input_path == 'blank':
        warning_message('Missing input folder', 'The input folder has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False
    elif path.exists(input_path) is False:
        warning_message('Incorrect input folder', 'The specified input folder cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False

    output_path = setup_object.output_path
    if output_path == 'blank':
        warning_message('Missing output folder', 'The output folder has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False
    elif path.exists(output_path) is False:
        warning_message('Incorrect output folder', 'The specified output folder cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False

    pu_path = setup_object.pu_path
    if pu_path == 'blank':
        warning_message('Missing planning unit shapefile', 'The planning unit shapefile has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False
    elif path.exists(pu_path) is False:
        warning_message('Incorrect planning unit shapefile path', 'The specified planning unit shapefile cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False

    puvspr2_path = setup_object.input_path + sep + 'puvspr2.dat'
    if path.exists(puvspr2_path) is False:
        warning_message('Incorrect puvspr2 path', 'The puvspr2.dat file cannot be found. Please add it to the specified input folder.')
        setup_file_correct_bool = False

    target_path = setup_object.target_path
    if target_path == 'blank':
        warning_message('Missing target table', 'The target table has not been specified. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False
    elif path.exists(target_path) is False:
        warning_message('Incorrect target table path', 'The specified target table cannot be found. Please open the View and Edit CLUZ setup file function and update the information.')
        setup_file_correct_bool = False

    return setup_file_correct_bool


def check_folder_values(setup_object):
    folders_ok_bool = True
    if path.isfile(setup_object.marxan_path) is False:
        warning_message('Setup file incorrect format', 'The specified Marxan file cannot be found. Please correct this.')
        folders_ok_bool = False
    else:
        marxan_dir_path = path.dirname(setup_object.marxan_path)
        if setup_object.marxan_path == 'blank' or setup_object.marxan_path == '':
            warning_message('Marxan path invalid', 'The Marxan path is missing.')
            folders_ok_bool = False
        elif path.isdir(marxan_dir_path) is False:
            warning_message('Marxan path invalid', 'The specified folder containing Marxan does not exist.')
            folders_ok_bool = False
        elif access(marxan_dir_path, W_OK) is False:
            warning_message('Marxan path invalid', 'Running Marxan involves CLUZ creating a new input file in the folder where Marxan is stored. You do not have permission to save files into the specified folder so please move Marxan to a folder where you do have permission.')
            folders_ok_bool = False

    return folders_ok_bool


def create_and_check_target_file(setup_object, check_bool):
    target_csv_file_path = setup_object.target_path
    setup_object.target_file_date = ctime(path.getmtime(target_csv_file_path))
    target_file_field_name_list = ['id', 'name', 'type', 'spf', 'target', 'ear+cons', 'total', 'pc_target']
    try:
        # with open(target_csv_file_path, mode='rt') as f:
        with open(target_csv_file_path, mode='rt', encoding='utf-8-sig') as f:
            target_reader = reader(f)
            orig_header_list = next(target_reader)

        lowercase_header_list = list()
        for aHeader in orig_header_list:
            lowercase_header = aHeader.lower()
            lowercase_header_list.append(lowercase_header)

        for aHeader in target_file_field_name_list:
            if lowercase_header_list.count(aHeader) == 0:
                if aHeader != 'ear+cons':
                    warning_message('Formatting error:', 'the Target table is missing the ' + aHeader + ' field. Please select a table with the correct format.')
                    check_bool = False
                elif aHeader == 'ear+cons' and lowercase_header_list.count('conserved') == 0:
                    warning_message('Formatting error:', 'the Target table is missing the ' + aHeader + ' field. Please select a table with the correct format.')
                    check_bool = False
                else:
                    warning_message('Formatting error:', 'the Conserved field in the Target table is now known as the Ear+Cons field, as it shows how much of each feature is Earmarked and Conserved. CLUZ will now rename the Conserved field in your table.')
                    change_conserved_field_name_to_ear_cons(setup_object)
                    check_bool = False
    except FileNotFoundError:
        check_bool = False

    return check_bool


def create_and_check_puvspr2_file(setup_object, check_bool):
    puvspr2_file_path = setup_object.input_path + sep + 'puvspr2.dat'
    with open(puvspr2_file_path, 'rt') as f:
        puvspr2_reader = reader(f)
        puvspr2_header_list = next(puvspr2_reader)
        if puvspr2_header_list != ['species', 'pu', 'amount']:
            warning_message('Formatting error: ', 'the puvspr2.dat file in the input folder is incorrectly formatted and should only have the following header names: species, pu, amount.')
            check_bool = False

    return check_bool


def create_and_check_pu_layer_file(setup_object, check_bool):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    fields = pu_layer.fields()
    field_details_list = list()
    title_text = 'Formatting error: '
    main_text = 'the planning unit shapefile must contain a field named '
    for aField in fields:
        field_details_list.append((str(aField.name()), str(aField.typeName())))
    if field_details_list.count(('Unit_ID', 'Integer')) == 0 and field_details_list.count(('Unit_ID', 'Integer64')) == 0:
        warning_message(title_text, main_text + 'Unit_ID containing integer values.')
        check_bool = False
    if field_details_list.count(('Area', 'Real')) == 0:
        warning_message(title_text, main_text + 'Area containing real number values.')
        check_bool = False
    if setup_object.analysis_type == 'Marxan':
        if field_details_list.count(('Cost', 'Real')) == 0:
            warning_message(title_text, main_text + 'Cost containing real number values.')
            check_bool = False
        if field_details_list.count(('Status', 'String')) == 0:
            warning_message(title_text, main_text + 'Status containing text values.')
            check_bool = False
    elif setup_object.analysis_type == 'MarxanWithZones':
        for aZoneNum in list(setup_object.zones_dict):
            cost_field_name = 'Z' + str(aZoneNum) + '_Cost'
            status_field_name = 'Z' + str(aZoneNum) + '_Status'
            if field_details_list.count((cost_field_name, 'Real')) == 0:
                warning_message(title_text, main_text + cost_field_name + ' containing real number values.')
                check_bool = False
            if field_details_list.count((status_field_name, 'String')) == 0:
                warning_message(title_text, main_text + status_field_name + ' containing text values.')
                check_bool = False

    return check_bool



def check_pu_layer_present():
    all_layers = QgsProject.instance().mapLayers().values()
    pu_layer_present_bool = False
    for a_layer in all_layers:
        if a_layer.name() == 'Planning units':
            pu_layer_present_bool = True

    return pu_layer_present_bool


def check_add_pu_layer(setup_object):
    if setup_object.setup_status == 'files_checked':
        if not check_pu_layer_present():
            add_pu_layer(setup_object, 0)  # 0 = Position


def return_feat_id_set_from_abund_pu_key_dict(setup_object):
    feat_id_set = set()
    for pu_id in setup_object.abund_pu_key_dict:
        feat_id_list = setup_object.abund_pu_key_dict[pu_id].keys()
        for feat_id in feat_id_list:
            feat_id_set.add(feat_id)

    return feat_id_set
