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

from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QLabel, QTableWidgetItem

from cluz_form_zones_inputs import Ui_zonesInputsDialog
from cluz_form_zones_marxan import Ui_zonesMarxanDialog
from cluz_form_zones_load import Ui_zonesLoadDialog

from .cluz_display import remove_previous_marxan_layers
from .cluz_functions5 import report_output_success_message, create_bound_dat_file
from .cluz_setup import update_clz_setup_file
from .zcluz_display import display_zones_sf_layer, reload_zones_pu_layer, display_zones_best_output
from .zcluz_functions5 import create_zones_feat_dat_file, create_zones_target_dat_file, create_zones_prop_dat_file
from .zcluz_functions5 import create_zones_pu_dat_file, create_zones_pu_status_dict, create_pu_lock_dat_file, create_pu_zone_dat_file
from .zcluz_functions5 import create_costs_dat_file, create_zones_dat_file, create_zone_cost_dat_file
from .zcluz_functions5 import zones_marxan_update_setup_object, add_best_zones_marxan_output_to_pu_shapefile
from .zcluz_functions5 import add_summed_zones_marxan_output_to_pu_shapefile, zones_load_best_marxan_output_to_pu_shapefile
from .zcluz_functions5 import check_make_zones_bound_cost_dict_from_dialog, zones_load_summed_marxan_output_to_pu_shapefile
from .zcluz_functions5 import make_zoneboundcost_dat_from_zones_bound_cost_dict
from .zcluz_dialog5_code import make_zones_marxan_raw_parameter_dict, check_zones_marxan_input_values_ok_bool, check_zones_marxan_files_exist_bool, launch_zones_marxan_analysis, set_zones_dialog_parameters, make_zones_marxan_parameter_dict
from .zcluz_dialog5_code import zones_return_initial_load_field_names, zones_check_load_best_marxan_result_file, zones_check_load_summed_marxan_result_file
from .zcluz_make_file_dicts import make_zones_bound_cost_dict_from_scratch


class ZonesInputsDialog(QDialog, Ui_zonesInputsDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.boundextBox.setEnabled(False)
        self.okButton.clicked.connect(lambda: self.set_create_zones_marxan_input_files(setup_object))

    def set_create_zones_marxan_input_files(self, setup_object):
        message_string_list = list()
        if self.targetBox.isChecked():
            create_zones_feat_dat_file(setup_object)
            message_string_list.append('feat.dat')
            create_zones_target_dat_file(setup_object)
            message_string_list.append('zonetarget.dat')
            create_zones_prop_dat_file(setup_object)
            message_string_list.append('zonecontrib.dat')

        if self.puBox.isChecked():
            create_zones_pu_dat_file(setup_object)
            message_string_list.append('pu.dat')
            zones_pu_status_dict = create_zones_pu_status_dict(setup_object)
            create_pu_lock_dat_file(setup_object, zones_pu_status_dict)
            message_string_list.append('pulock.dat')
            create_pu_zone_dat_file(setup_object, zones_pu_status_dict)
            message_string_list.append('puzone.dat')

        if self.zonesBox.isChecked():
            create_zones_dat_file(setup_object)
            message_string_list.append('zones.dat')
            create_costs_dat_file(setup_object)
            message_string_list.append('costs.dat')
            create_zone_cost_dat_file(setup_object)
            message_string_list.append('zonecost.dat')

        if self.boundBox.isChecked():
            if self.boundextBox.isChecked() and self.boundextBox.isEnabled():
                ext_edge_bool = True
            else:
                ext_edge_bool = False
            create_bound_dat_file(setup_object, ext_edge_bool)
            message_string_list.append('bound.dat')

            make_zoneboundcost_dat_from_zones_bound_cost_dict(setup_object)
            message_string_list.append('zoneboundcost.dat')

        report_output_success_message(message_string_list)

        self.close()


class ZonesMarxanDialog(QDialog, Ui_zonesMarxanDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        set_zones_dialog_parameters(self, setup_object)

        self.boundCheckBox.clicked['bool'].connect(self.boundZoneCheckBox.setEnabled)
        self.boundCheckBox.stateChanged.connect(self.update_blm_table_widget_enabled_state)
        self.startButton.clicked.connect(lambda: self.run_zones_marxan(setup_object))


    def update_blm_table_widget_enabled_state(self, checkbox_state):
        if checkbox_state == 0:
            self.blmTableWidget.setEnabled(False)
        else:
            if self.boundZoneCheckBox.isChecked():
                self.blmTableWidget.setEnabled(True)


    def run_zones_marxan(self, setup_object):
        zones_marxan_raw_parameter_dict = make_zones_marxan_raw_parameter_dict(self, setup_object)
        zones_marxan_input_values_ok_bool = check_zones_marxan_input_values_ok_bool(zones_marxan_raw_parameter_dict)

        zones_bound_cost_values_ok_bool = True
        if self.boundZoneCheckBox.isChecked():
            run_zones_bound_cost_dict, zones_bound_cost_values_ok_bool = check_make_zones_bound_cost_dict_from_dialog(self, setup_object)
        else: #  if the tick box is unselected, then all boundary costs between zones = 0
            run_zones_bound_cost_dict = make_zones_bound_cost_dict_from_scratch(setup_object)

        zones_marxan_files_exist_bool = check_zones_marxan_files_exist_bool(setup_object)

        if zones_marxan_input_values_ok_bool and zones_marxan_files_exist_bool and zones_bound_cost_values_ok_bool:
            zones_marxan_parameter_dict = make_zones_marxan_parameter_dict(setup_object, zones_marxan_raw_parameter_dict)
            create_zones_feat_dat_file(setup_object)
            setup_object.zones_bound_cost_dict = run_zones_bound_cost_dict
            make_zoneboundcost_dat_from_zones_bound_cost_dict(setup_object)
            setup_object = zones_marxan_update_setup_object(self, setup_object, zones_marxan_parameter_dict)
            update_clz_setup_file(setup_object, True)  # saveSuccessfulBool = True
            self.close()

            best_output_file, summed_output_file = launch_zones_marxan_analysis(setup_object, zones_marxan_parameter_dict)

            add_best_zones_marxan_output_to_pu_shapefile(setup_object, best_output_file, 'Best')
            add_summed_zones_marxan_output_to_pu_shapefile(setup_object, summed_output_file)

            remove_previous_marxan_layers()
            reload_zones_pu_layer(setup_object)
            display_zones_sf_layer(setup_object, zones_marxan_parameter_dict['num_run'], zones_marxan_parameter_dict['output_name'], 'Z', '_' + 'SFreq')
            display_zones_best_output(setup_object, 'Best (' + zones_marxan_parameter_dict['output_name'] + ')', 'Best')

            setup_object.TargetsMetAction.setEnabled(True)


class ZonesLoadDialog(QDialog, Ui_zonesLoadDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.zonesBestLabel.setVisible(False)
        self.zonesBestLineEdit.setVisible(False)
        self.zonesBestNameLineEdit.setVisible(False)
        self.zonesBestButton.setVisible(False)
        self.zonesSummedLabel.setVisible(False)
        self.zonesSummedLineEdit.setVisible(False)
        self.zonesSummedNameLineEdit.setVisible(False)
        self.zonesSummedButton.setVisible(False)

        zones_import_best_name, zones_import_summed_name = zones_return_initial_load_field_names(setup_object)
        self.zonesBestNameLineEdit.setText(zones_import_best_name)
        self.zonesSummedNameLineEdit.setText(zones_import_summed_name)

        self.zonesBestButton.clicked.connect(self.zones_set_best_path)
        self.zonesSummedButton.clicked.connect(self.zones_set_summed_path)
        self.okButton.clicked.connect(lambda: self.zones_load_previous_marxan_results(setup_object))

    def zones_set_best_path(self):
        (zonesBestPathNameText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select Marxan with Zones best portfolio output', '*.csv')
        if zonesBestPathNameText is not None:
            self.zonesBestLineEdit.setText(zonesBestPathNameText)

    def zones_set_summed_path(self):
        (summedPathNameText, fileTypeDetailsText) = QFileDialog.getOpenFileName(self, 'Select Marxan with Zones summed solution output', '*.csv')
        if summedPathNameText is not None:
            self.zonesSummedLineEdit.setText(summedPathNameText)

    def zones_load_previous_marxan_results(self, setup_object):
        reload_zones_pu_layer(setup_object)
        if self.zonesSummedCheckBox.isChecked() and zones_check_load_summed_marxan_result_file(self, setup_object):  # add SF first so Best is then on top
            zones_load_sf_csv_file_name, zones_load_sf_name_prefix, max_sf_score = zones_load_summed_marxan_output_to_pu_shapefile(self, setup_object)
            run_number = max_sf_score
            display_zones_sf_layer(setup_object, run_number, zones_load_sf_csv_file_name, zones_load_sf_name_prefix + '_Z', '_SF')

        if self.zonesBestCheckBox.isChecked() and zones_check_load_best_marxan_result_file(self, setup_object):
            zones_load_best_csv_file_name, zones_load_best_field_name = zones_load_best_marxan_output_to_pu_shapefile(self, setup_object)
            display_zones_best_output(setup_object, 'Best (' + zones_load_best_csv_file_name + ')', zones_load_best_field_name)
