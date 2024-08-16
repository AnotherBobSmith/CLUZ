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

from csv import reader
from os import listdir, path

from .cluz_messages import warning_message


def make_marxan_file_list(setup_object):
    marxan_file_list = list()

    file_list = listdir(setup_object.output_path)
    analysis_set = set()
    for fileNameString in file_list:
        portfolio_identifier_string = fileNameString[-11:-9]
        if portfolio_identifier_string == '_r':
            analysis_set.add(fileNameString[0:-11])

    for aPathName in analysis_set:
        run_path = aPathName + '_r'
        file_count = 0
        for bFile in file_list:
            if bFile.startswith(run_path):
                file_count += 1
        if file_count > 0:
            marxan_file_list.append(aPathName + ' - ' + str(file_count) + ' files')

    return marxan_file_list


def check_min_patch_file(minpatch_dialog, minpatch_object):
    run_min_patch_bool = True
    details_dat_path = minpatch_dialog.detailsLineEdit.text()
    if path.isfile(details_dat_path):
        with open(details_dat_path, 'rt') as f:
            details_reader = reader(f)
            details_header = next(details_reader, None)  # skip the headers
        if details_header == ['id', 'area', 'zone', 'patch_area', 'radius']:
            minpatch_object.detailsDatPath = details_dat_path
        else:
            warning_message('Incorrect format', 'The specified MinPatch details file is incorrectly formatted. It must contain five fields named id, area, zone, patch_area and radius.')
            run_min_patch_bool = False
    else:
        warning_message('Incorrect pathname', 'The specified pathname for the MinPatch details file is invalid. Please choose another one.')
        run_min_patch_bool = False
        
    return run_min_patch_bool, minpatch_object


def check_min_patch_blm_value(minpatch_dialog, minpatch_object, run_minpatch_bool):
    blm_text = minpatch_dialog.blmLineEdit.text()
    try:
        blm_number = float(blm_text)
        if blm_number >= 0:
            minpatch_object.blm = blm_number
        else:
            warning_message('Incorrect BLM format', 'The BLM value must be a non-negative number.')
            run_minpatch_bool = False
    except ValueError:
        warning_message('Incorrect BLM format', 'The BLM value must be a non-negative number.')
        run_minpatch_bool = False
        
    return run_minpatch_bool, minpatch_object


def check_minpatch_selected_items_list(minpatch_dialog, minpatch_object, run_minpatch_bool):
    selected_items_list = minpatch_dialog.fileListWidget.selectedItems()
    if len(selected_items_list) > 0:
        selected_marxan_file_text = [item.text() for item in minpatch_dialog.fileListWidget.selectedItems()][0]

        suffix_text = selected_marxan_file_text.split(' - ')[-1]
        number_text = suffix_text.split(' ')[0]
        run_number_len = len(number_text) + 9  # Calcs length of text to remove from end of string
        minpatch_object.marxanFileName = selected_marxan_file_text[0: -run_number_len]
    else:
        warning_message('No files selected', 'Please select one of the sets of files before proceeding.')
        run_minpatch_bool = False
        
    return run_minpatch_bool, minpatch_object
