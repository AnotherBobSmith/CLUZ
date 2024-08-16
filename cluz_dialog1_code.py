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

from .cluz_setup import CluzSetupObject

from os import path

from .cluz_setup import update_setup_object_from_setup_file, check_status_object_values, create_and_check_cluz_files, update_clz_setup_file
from .cluz_checkup import check_add_pu_layer
from .zcluz_checkup import check_add_zones_pu_layer


def add_setup_dialog_text_from_setup_object(setup_dialog, setup_object):
    setup_dialog.marxanLineEdit.setText(setup_object.marxan_path)
    setup_dialog.inputLineEdit.setText(setup_object.input_path)
    setup_dialog.outputLineEdit.setText(setup_object.output_path)
    setup_dialog.puLineEdit.setText(setup_object.pu_path)
    setup_dialog.targetLineEdit.setText(setup_object.target_path)
    setup_dialog.set_prec_value(setup_object.decimal_places)

    if path.isfile(setup_object.setup_path):
        setup_path_text = path.abspath(setup_object.setup_path)
    else:
        setup_path_text = 'blank'

    if setup_object.analysis_type == 'MarxanWithZones':
        setup_dialog.mzonesRadioButton.setChecked(True)
        setup_dialog.zonesLineEdit.setText(setup_object.zones_path)
    else:
        setup_dialog.mzonesRadioButton.setChecked(False)

    setup_path_label_text = 'Setup file location: ' + setup_path_text
    setup_dialog.setupPathLabel.setText(setup_path_label_text)


def load_setup_file_code(setup_dialog, setup_object, setup_file_path):
    setup_object = update_setup_object_from_setup_file(setup_object, setup_file_path)

    if setup_object.setup_status == 'values_checked':
        setup_object = create_and_check_cluz_files(setup_object)

    if setup_object.setup_status == "files_checked":
        setup_object.setup_action = "blank"
        setup_path_label_text = path.abspath(setup_file_path)
        setup_path_label_text = "Setup file location: " + str(setup_path_label_text)
        setup_dialog.setupPathLabel.setText(setup_path_label_text)

        setup_dialog.marxanLineEdit.setText(path.abspath(setup_object.marxan_path))
        setup_dialog.inputLineEdit.setText(path.abspath(setup_object.input_path))
        setup_dialog.outputLineEdit.setText(setup_object.output_path)
        setup_dialog.puLineEdit.setText(setup_object.pu_path)
        setup_dialog.targetLineEdit.setText(setup_object.target_path)
        setup_dialog.set_prec_value(setup_object.decimal_places)

        if setup_object.analysis_type == 'MarxanWithZones':
            setup_dialog.mzonesRadioButton.setChecked(True)
            setup_dialog.zonesLineEdit.setText(setup_object.zones_path)
            setup_object.ZonesAction.setEnabled(True)
            setup_object.ConvertVecAction.setEnabled(False)
            setup_object.ConvertRasterAction.setEnabled(False)
            setup_object.ConvertCsvAction.setEnabled(False)
            setup_object.MinPatchAction.setEnabled(False)
        else:
            setup_dialog.mzonesRadioButton.setChecked(False)
            setup_object.ZonesAction.setEnabled(False)
            setup_object.ConvertVecAction.setEnabled(True)
            setup_object.ConvertRasterAction.setEnabled(True)
            setup_object.ConvertCsvAction.setEnabled(True)
            setup_object.MinPatchAction.setEnabled(True)

        if setup_object.analysis_type != 'MarxanWithZones':
            check_add_pu_layer(setup_object)
        else:
            check_add_zones_pu_layer(setup_object)


def save_setup_file_code(setup_dialog, setup_object, setup_file_path):
    limbo_setup_object = CluzSetupObject()
    limbo_setup_object.TargetsMetAction = setup_object.TargetsMetAction
    limbo_setup_object.ZonesAction = setup_object.ZonesAction
    limbo_setup_object.MinPatchAction = setup_object.MinPatchAction
    limbo_setup_object.setup_status = 'blank'

    limbo_setup_object = add_details_to_setup_object(setup_dialog, limbo_setup_object)

    limbo_setup_object = check_status_object_values(limbo_setup_object)
    save_successful_bool = False

    if limbo_setup_object.setup_status == 'values_checked':
        limbo_setup_object = create_and_check_cluz_files(limbo_setup_object)

    if limbo_setup_object.setup_status == 'files_checked':
        save_successful_bool = True
        copy_limbo_parameters_to_setup_object(setup_object, limbo_setup_object)
        save_successful_bool = update_clz_setup_file(setup_object, save_successful_bool)
        if save_successful_bool:
            setup_path_label_text = 'Setup file location: ' + str(setup_file_path)
            setup_dialog.setupPathLabel.setText(setup_path_label_text)

            check_add_pu_layer(setup_object)

    return save_successful_bool


def copy_limbo_parameters_to_setup_object(setup_object, limbo_setup_object):
    setup_object.decimal_places = limbo_setup_object.decimal_places
    setup_object.marxan_path = limbo_setup_object.marxan_path
    setup_object.input_path = limbo_setup_object.input_path
    setup_object.output_path = limbo_setup_object.output_path
    setup_object.pu_path = limbo_setup_object.pu_path
    setup_object.target_path = limbo_setup_object.target_path


def save_as_setup_file_code(setup_dialog, setup_object, new_setup_file_path):
    setup_object = add_details_to_setup_object(setup_dialog, setup_object)
    setup_object.setup_path = new_setup_file_path

    setup_object = check_status_object_values(setup_object)
    if setup_object.setup_status == 'values_checked':
        setup_object = create_and_check_cluz_files(setup_object)
    if setup_object.setup_status == 'files_checked':
        save_successful_bool = True
        save_successful_bool = update_clz_setup_file(setup_object, save_successful_bool)
        if save_successful_bool:
            setup_path_label_text = 'Setup file location: ' + str(new_setup_file_path)
            setup_dialog.setupPathLabel.setText(setup_path_label_text)
            check_add_pu_layer(setup_object)


def add_details_to_setup_object(setup_dialog, setup_object):
    if setup_dialog.mzonesRadioButton.isChecked():
        setup_object.analysis_type = 'MarxanWithZones'
    else:
        setup_object.analysis_type = 'Marxan'
    setup_object.decimal_places = int(setup_dialog.precComboBox.currentText())
    setup_object.marxan_path = setup_dialog.marxanLineEdit.text()
    setup_object.input_path = setup_dialog.inputLineEdit.text()
    setup_object.output_path = setup_dialog.outputLineEdit.text()
    setup_object.pu_path = setup_dialog.puLineEdit.text()
    setup_object.target_path = setup_dialog.targetLineEdit.text()
    if setup_object.analysis_type == 'MarxanWithZones':
        setup_object.zones_path = setup_dialog.zonesLineEdit.text()

    return setup_object