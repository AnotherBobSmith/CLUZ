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

from qgis.PyQt.QtWidgets import QDialog, QFileDialog

from os import path
from sys import platform

from .cluz_setup import update_clz_setup_file
from .cluz_dialog5_code import check_load_summed_marxan_result, make_marxan_parameter_dict, check_load_best_marxan_result, make_marxan_raw_parameter_dict
from .cluz_dialog5_code import return_marxan_input_values_ok_bool, set_dialog_parameters, launch_marxan_analysis, return_initial_load_field_names, check_marxan_files_exist_bool
from .cluz_dialog5_code import set_initial_values_calibrate_dialog, make_marxan_calibrate_raw_parameter_dict, check_calibrate_analysis_parameters, run_calibrate_marxan
from .cluz_display import display_graduated_layer, remove_previous_marxan_layers, reload_pu_layer, display_best_output
from .cluz_functions5 import create_pu_dat_file, marxan_update_setup_object, add_best_marxan_output_to_pu_shapefile, create_bound_dat_file, create_spec_dat_file, add_summed_marxan_output_to_pu_shapefile
from .cluz_functions5 import make_calibrate_output_file, report_output_success_message
from .cluz_messages import critical_message, success_message

from cluz_form_inputs import Ui_inputsDialog
from cluz_form_marxan import Ui_marxanDialog
from cluz_form_load import Ui_loadDialog
from cluz_form_calibrate import Ui_calibrateDialog


class InputsDialog(QDialog, Ui_inputsDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.boundextBox.setEnabled(False)
        self.okButton.clicked.connect(lambda: self.set_create_marxan_input_files(setup_object))

    def set_create_marxan_input_files(self, setup_object):
        message_string_list = list()
        if self.targetBox.isChecked():
            create_spec_dat_file(setup_object)
            message_string_list.append('spec.dat')

        if self.puBox.isChecked():
            create_pu_dat_file(setup_object)
            message_string_list.append('pu.dat')

        if self.boundBox.isChecked():
            if self.boundextBox.isChecked() and self.boundextBox.isEnabled():
                ext_edge_bool = True
            else:
                ext_edge_bool = False
            create_bound_dat_file(setup_object, ext_edge_bool)
            message_string_list.append('bound.dat')

        report_output_success_message(message_string_list)

        self.close()


def check_cluz_is_not_running_on_mac():
    marxan_bool = True
    if platform.startswith('darwin'):
        critical_message('CLUZ and MacOS', 'The current version of CLUZ cannot run Marxan on Mac computers. Sorry about that. Instead, you can run Marxan independently and load the results into CLUZ.')
        marxan_bool = False
        
    return marxan_bool


def check_marxan_path(setup_object, marxan_bool):
    if setup_object.marxan_path == 'blank':
        critical_message('Marxan path missing', 'The location of Marxan has not been specified. CLUZ will now open the CLUZ setup dialog box, so please specify a correct version.')
        marxan_bool = False
    if path.exists(setup_object.marxan_path) is False:
        critical_message('Incorrect Marxan path', 'Marxan cannot be found at the specified pathway. CLUZ will now open the CLUZ setup dialog box, so please specify a correct version.')
        marxan_bool = False
        
    return marxan_bool


class MarxanDialog(QDialog, Ui_marxanDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        set_dialog_parameters(self, setup_object)
        self.startButton.clicked.connect(lambda: self.run_marxan(setup_object))

    def run_marxan(self, setup_object):
        marxan_raw_parameter_dict = make_marxan_raw_parameter_dict(self, setup_object)
        marxan_input_values_ok_bool = return_marxan_input_values_ok_bool(marxan_raw_parameter_dict)
        marxan_files_exist_bool = check_marxan_files_exist_bool(setup_object)
        if marxan_input_values_ok_bool and marxan_files_exist_bool:
            marxan_parameter_dict = make_marxan_parameter_dict(setup_object, marxan_raw_parameter_dict)
            create_spec_dat_file(setup_object)

            setup_object = marxan_update_setup_object(self, setup_object, marxan_parameter_dict)
            update_clz_setup_file(setup_object, True)  # saveSuccessfulBool = True
            self.close()

            best_layer_name = 'Best (' + marxan_parameter_dict['output_name'] + ')'
            summed_layer_name = 'SF_Score (' + marxan_parameter_dict['output_name'] + ')'
            best_output_file, summed_output_file = launch_marxan_analysis(setup_object, marxan_parameter_dict)

            add_best_marxan_output_to_pu_shapefile(setup_object, best_output_file, 'Best')
            add_summed_marxan_output_to_pu_shapefile(setup_object, summed_output_file, 'SF_Score')

            remove_previous_marxan_layers()
            reload_pu_layer(setup_object)
            display_graduated_layer(setup_object, 'SF_Score', summed_layer_name, 1)  # 1 is SF legend code
            display_best_output(setup_object, 'Best', best_layer_name)  # Added second to be on top

            setup_object.TargetsMetAction.setEnabled(True)


class LoadDialog(QDialog, Ui_loadDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.bestLabel.setVisible(False)
        self.bestLineEdit.setVisible(False)
        self.bestNameLineEdit.setVisible(False)
        self.bestButton.setVisible(False)
        self.summedLabel.setVisible(False)
        self.summedLineEdit.setVisible(False)
        self.summedNameLineEdit.setVisible(False)
        self.summedButton.setVisible(False)

        best_name, summed_name = return_initial_load_field_names(setup_object)
        self.bestNameLineEdit.setText(best_name)
        self.summedNameLineEdit.setText(summed_name)

        self.bestButton.clicked.connect(self.set_best_path)
        self.summedButton.clicked.connect(self.set_summed_path)
        self.okButton.clicked.connect(lambda: self.load_previous_marxan_results(setup_object))

    def set_best_path(self):
        (bestPathNameText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select Marxan best portfolio output', '*.txt')
        if bestPathNameText is not None:
            self.bestLineEdit.setText(bestPathNameText)

    def set_summed_path(self):
        (summedPathNameText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select Marxan summed solution output', '*.txt')
        if summedPathNameText is not None:
            self.summedLineEdit.setText(summedPathNameText)

    def load_previous_marxan_results(self, setup_object):
        reload_pu_layer(setup_object)
        check_load_best_marxan_result(self, setup_object)
        check_load_summed_marxan_result(self, setup_object)


class CalibrateDialog(QDialog, Ui_calibrateDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        set_initial_values_calibrate_dialog(self, setup_object)
        self.paraComboBox.activated.connect(lambda: self.combo_chosen(setup_object))
        if setup_object.analysis_type == 'MarxanWithZones':
            self.setWindowTitle('Calibrate Marxan with Zones parameters')
            self.outputLabel.setText('Marxan with Zones output files base name     ')

        self.saveResultsButton.clicked.connect(self.save_results_file)
        self.runButton.clicked.connect(lambda: self.run_calibrate_analysis(setup_object))

    def combo_chosen(self, setup_object):
        self.iterLineEdit.setText(str(setup_object.num_iter))
        self.runLineEdit.setText(str(setup_object.num_runs))
        self.boundLineEdit.setText(str(setup_object.blm_value))
        self.iterLabel.setEnabled(True)
        self.iterLineEdit.setEnabled(True)
        self.runLabel.setEnabled(True)
        self.runLineEdit.setEnabled(True)
        self.boundLabel.setEnabled(True)
        self.boundLineEdit.setEnabled(True)
        parameter_text = self.paraComboBox.currentText()
        if parameter_text == 'Number of iterations':
            self.iterLabel.setEnabled(False)
            self.iterLineEdit.setEnabled(False)
            self.iterLineEdit.setText('Specified above')
            self.spfLineEdit.setText('As specified in spec.dat file')
        elif parameter_text == 'Number of runs':
            self.runLabel.setEnabled(False)
            self.runLineEdit.setEnabled(False)
            self.runLineEdit.setText('Specified above')
            self.spfLineEdit.setText('As specified in spec.dat file')
        elif parameter_text == 'BLM':
            self.boundLabel.setEnabled(False)
            self.boundLineEdit.setEnabled(False)
            self.boundLineEdit.setText('Specified above')
            self.spfLineEdit.setText('As specified in spec.dat file')
        elif parameter_text == 'SPF':
            self.spfLabel.setEnabled(False)
            self.spfLineEdit.setEnabled(False)
            self.spfLineEdit.setText('Specified above')

    def save_results_file(self):
        (resultsFilePath, fileTypeDetailsText) = QFileDialog.getSaveFileName(self, 'Save Calibration results file', '*.csv')
        self.resultsLineEdit.setText(resultsFilePath)

    def run_calibrate_analysis(self, setup_object):
        calibrate_raw_parameter_dict = make_marxan_calibrate_raw_parameter_dict(self)
        check_bool, num_run_list, num_iter_list, blm_value_list, spf_list = check_calibrate_analysis_parameters(self, calibrate_raw_parameter_dict)
        if check_bool:
            calibrate_results_dict = run_calibrate_marxan(setup_object, calibrate_raw_parameter_dict, num_run_list, num_iter_list, blm_value_list, spf_list)
            make_calibrate_output_file(calibrate_raw_parameter_dict['result_path_text'], calibrate_results_dict)
            self.close()
