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
import sys

from .cluz_messages import warning_message, success_message
from .cluz_dialog1_code import load_setup_file_code, save_as_setup_file_code, save_setup_file_code, add_setup_dialog_text_from_setup_object
from .cluz_display import remove_then_add_pu_layer

sys.path.append(path.dirname(path.abspath(__file__)) + "/forms")
from cluz_form_start import Ui_startDialog
from cluz_form_setup import Ui_setupDialog


class StartDialog(QDialog, Ui_startDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.okButton.clicked.connect(lambda: self.return_start_bool(setup_object))
        self.cancelButton.clicked.connect(self.close_start_dialog)

    def return_start_bool(self, setup_object):
        if self.openRadioButton.isChecked():
            setup_object.setup_action = 'open'
        elif self.createButton.isChecked():
            setup_object.setup_action = 'new'
        self.close()

    def close_start_dialog(self):
        self.close()


class SetupDialog(QDialog, Ui_setupDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        add_setup_dialog_text_from_setup_object(self, setup_object)

        if setup_object.analysis_type == 'Marxan':
            self.marxanRadioButton.setChecked(True)
            self.mzonesRadioButton.setChecked(False)
            self.zonesLabel.setVisible(False)
            self.zonesLineEdit.setVisible(False)
            self.zonesButton.setVisible(False)
        else:
            self.marxanRadioButton.setChecked(False)
            self.mzonesRadioButton.setChecked(True)
            self.zonesLabel.setVisible(True)
            self.zonesLineEdit.setVisible(True)
            self.zonesButton.setVisible(True)

        self.marxanButton.clicked.connect(self.set_marxan_path)
        self.inputButton.clicked.connect(self.set_input_path)
        self.outputButton.clicked.connect(self.set_output_path)
        self.puButton.clicked.connect(self.set_pu_path)
        self.targetButton.clicked.connect(self.set_target_path)
        self.zonesButton.clicked.connect(self.set_zones_path)

        self.loadButton.clicked.connect(lambda: self.load_setup_file(setup_object))
        self.saveButton.clicked.connect(lambda: self.save_setup_file(setup_object))
        self.saveAsButton.clicked.connect(lambda: self.save_as_setup_file(setup_object))

    def set_marxan_path(self):
        (marxanPathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select Marxan file', '*.exe')
        marxan_path_name_text = path.abspath(marxanPathNameRawText)
        if marxan_path_name_text is not None:
            self.marxanLineEdit.setText(marxan_path_name_text)

    def set_input_path(self):
        input_path_name_raw_text = QFileDialog.getExistingDirectory(self, 'Select input folder')
        input_path_name_text = path.abspath(input_path_name_raw_text)
        if input_path_name_text is not None:
            self.inputLineEdit.setText(input_path_name_text)

    def set_output_path(self):
        output_path_name_raw_text = QFileDialog.getExistingDirectory(self, 'Select output folder')
        output_path_name_text = path.abspath(output_path_name_raw_text)
        if output_path_name_text is not None:
            self.outputLineEdit.setText(output_path_name_text)

    def set_pu_path(self):
        (puPathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select planning unit shapefile', '*.shp')
        pu_path_name_text = path.abspath(puPathNameRawText)
        if pu_path_name_text is not None:
            self.puLineEdit.setText(pu_path_name_text)

    def set_target_path(self):
        (targetPathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select target table', '*.csv')
        target_path_name_text = path.abspath(targetPathNameRawText)
        if target_path_name_text is not None:
            self.targetLineEdit.setText(target_path_name_text)

    def set_zones_path(self):
        (zonePathNameRawText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select zone table', '*.csv')
        zone_path_name_text = path.abspath(zonePathNameRawText)
        if zone_path_name_text is not None:
            self.zonesLineEdit.setText(zone_path_name_text)

    def set_prec_value(self, prec_value):
        self.precComboBox.addItems(['0', '1', '2', '3', '4', '5'])
        number_list = [0, 1, 2, 3, 4, 5]
        if prec_value > 5:
            title_text = 'Decimal precision value problem'
            main_text = 'The number of decimal places specified in the CLUZ setup file cannot be more than 5. The specified value has been changed to 5.'
            warning_message(title_text, main_text)
            prec_value = 5
        index_value = number_list.index(prec_value)
        self.precComboBox.setCurrentIndex(index_value)

    def load_setup_file(self, setup_object):
        (setupPathLabelText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select CLUZ setup file', '*.clz')
        if setupPathLabelText != '':
            load_setup_file_code(self, setup_object, setupPathLabelText)
            remove_then_add_pu_layer(setup_object, 0)

    def save_setup_file(self, setup_object):
        setup_file_path = setup_object.setup_path
        if path.isfile(setup_file_path):
            save_successful_bool = save_setup_file_code(self, setup_object, setup_file_path)
            if save_successful_bool:
                success_message('File saved', 'The CLUZ setup file has been saved successfully.')
        elif setup_file_path == 'blank':
            warning_message("No CLUZ setup file name", "The CLUZ setup file name has not been set. Please use the Save As... option instead.")
        else:
            warning_message("CLUZ setup file name error", "The current CLUZ setup file path is incorrect.")

    def save_as_setup_file(self, setup_object):
        (newSetupFilePath, fileTypeDetailsText) = QFileDialog.getSaveFileName(self, 'Save new CLUZ setup file', '*.clz')
        if newSetupFilePath != '':
            save_as_setup_file_code(self, setup_object, newSetupFilePath)
            if setup_object.setup_status:
                success_message('File saved', 'The CLUZ setup file has been saved successfully.')
        else:
            warning_message("CLUZ setup file name error", "The current CLUZ setup file path is incorrect.")
