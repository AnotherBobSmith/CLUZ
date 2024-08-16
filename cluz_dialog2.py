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

from .cluz_functions2 import make_csv_add_abund_dict, check_conv_factor
from .cluz_dialog2_code import check_make_new_cluz_files, check_add_layer_list_convert_vec_dialog, check_layer_factor, check_add_csv_file_path, create_update_abund_data_from_vec_file
from .cluz_dialog2_code import add_csv_dict_to_abund_dict_update_puvspr2_target_files, check_layer_factor_convert_vec, make_vector_error_layer_string, check_layer_has_same_crs_as_pu_layer
from .cluz_dialog2_code import check_add_layer_list_convert_raster_dialog, check_layer_factor_convert_raster, create_update_abund_data_from_raster_file, make_raster_error_layer_string
from .cluz_dialog2_code import check_return_layer_list, check_layer_list_for_incorrect_fields

from .cluz_messages import critical_message

sys.path.append(path.dirname(path.abspath(__file__)) + "/forms")
from cluz_form_create import Ui_createDialog
from cluz_form_convert_vec import Ui_convertVecDialog
from cluz_form_convert_raster import Ui_convertRasterDialog
from cluz_form_convert_csv import Ui_convertCsvDialog


class CreateDialog(QDialog, Ui_createDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.convLineEdit.setText('1')

        self.puButton.clicked.connect(self.set_shapefile_path)
        self.inputButton.clicked.connect(self.set_input_path)
        self.targetButton.clicked.connect(self.set_target_path)
        self.okButton.clicked.connect(self.create_new_cluz_files)

    def set_shapefile_path(self):
        (shapefilePathNameText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select shapefile', '*.shp')
        if shapefilePathNameText is not None:
            self.puLineEdit.setText(shapefilePathNameText)

    def set_input_path(self):
        input_path_name_raw_text = QFileDialog.getExistingDirectory(self, 'Select input folder')
        input_path_name_text = path.abspath(input_path_name_raw_text)
        if input_path_name_text is not None:
            self.inputLineEdit.setText(input_path_name_text)

    def set_target_path(self):
        (targetPathNameText, fileTypeDetailsText) = QFileDialog.getSaveFileName(self, 'Specify target table name', '*.csv', '*.csv')
        if targetPathNameText is not None:
            self.targetLineEdit.setText(targetPathNameText)

    def create_new_cluz_files(self):
        check_make_new_cluz_files(self)


class ConvertVecDialog(QDialog, Ui_convertVecDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        check_add_layer_list_convert_vec_dialog(self)
        self.idfieldLineEdit.setText("ID")
        self.convLineEdit.setText("1")
        self.convLineEdit.setEnabled(False)
        self.convLabel.setEnabled(False)

        self.okButton.clicked.connect(lambda: self.convert_vec_layers_to_abund_table(setup_object))

    def convert_vec_layers_to_abund_table(self, setup_object):
        layer_list, layer_factor_check = check_return_layer_list(self)
        layer_factor_check = check_layer_list_for_incorrect_fields(self, layer_list, layer_factor_check)
        layer_factor_check = check_layer_factor_convert_vec(self, layer_list, layer_factor_check)
        same_projection_check = check_layer_has_same_crs_as_pu_layer(self, setup_object)
        conv_factor_check = check_conv_factor(self)

        if layer_factor_check and same_projection_check and conv_factor_check:
            error_layer_list = create_update_abund_data_from_vec_file(self, setup_object, layer_list)
            if len(error_layer_list) > 0:
                vector_error_layer_string = make_vector_error_layer_string(error_layer_list)
                critical_message('Error processing layers', vector_error_layer_string)


class ConvertRasterDialog(QDialog, Ui_convertRasterDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        check_add_layer_list_convert_raster_dialog(self)
        self.convLineEdit.setText("1")
        self.convLineEdit.setEnabled(False)
        self.convLabel.setEnabled(False)

        self.okButton.clicked.connect(lambda: self.convert_raster_layers_to_abund_table(setup_object))

    def convert_raster_layers_to_abund_table(self, setup_object):
        layer_list, layer_factor_check = check_layer_factor_convert_raster(self)
        same_projection_check = check_layer_has_same_crs_as_pu_layer(self, setup_object)
        conv_factor_check = check_conv_factor(self)

        if layer_factor_check and same_projection_check and conv_factor_check:

            error_layer_list = create_update_abund_data_from_raster_file(self, setup_object, layer_list)
            if len(error_layer_list) > 0:
                if 'ZonalHistogram failed' in error_layer_list:
                    critical_message('QGIS Zonal histogram function failed', 'Please check the raster file you selected')
                else:
                    error_layer_string = make_raster_error_layer_string(error_layer_list)
                    critical_message('Error processing layers', error_layer_string)


class ConvertCsvDialog(QDialog, Ui_convertCsvDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.idfieldComboBox.setEnabled(False)
        self.convLineEdit.setText("1")
        self.convLineEdit.setEnabled(False)
        self.convLabel.setEnabled(False)
        self.noneRadioButton.setChecked(True)

        self.browseButton.clicked.connect(self.set_csv_file_path)
        self.okButton.clicked.connect(lambda: self.convert_csv_to_abund_table(setup_object))

    def set_csv_file_path(self):
        (csvPathNameText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select CSV file', '*.csv')
        check_add_csv_file_path(self, csvPathNameText)

    def convert_csv_to_abund_table(self, setup_object):
        layer_factor_check = check_layer_factor(self)
        conv_factor_check = check_conv_factor(self)

        if layer_factor_check and conv_factor_check:
            add_abund_dict, feat_id_list, continue_bool = make_csv_add_abund_dict(self, setup_object)
            if continue_bool:
                add_csv_dict_to_abund_dict_update_puvspr2_target_files(setup_object, add_abund_dict, feat_id_list)

        self.close()
