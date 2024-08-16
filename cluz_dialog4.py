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
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QApplication

from .cluz_dialog4_code import add_details_to_sf_tab, remove_superfluous_tabs, set_initial_distribution_shapefile_path, load_distribution_feature_list, return_selected_pu_id_details_dict
from .cluz_dialog4_code import check_if_sf_runs_value_is_ok, return_richness_restricted_range_results, make_selected_feat_id_set, create_display_distribution_maps, add_details_to_spatial_tab
from .cluz_dialog4_code import make_sf_field_list, return_selected_pu_id_dict, add_selected_identify_data_to_table_widget, return_initial_field_name, produce_type_text_list, add_patch_feat_details_to_portfolio_dict
from .cluz_dialog4_code import add_formatting_headings_to_table_widget, add_sf_details_to_portfolio_dict, return_richness_count_results
from .cluz_dialog4_code import check_richness_type_codes_selected_options_selected, add_details_to_patch_feat_tab, add_details_to_status_tab
from .cluz_display import remove_then_add_pu_layer
from .cluz_functions4 import add_status_details_to_portfolio_dict, make_portfolio_pu_details_dict, add_spatial_details_to_portfolio_dict
from .cluz_messages import success_message
from .cluz_shared import copy_table_contents_to_clipboard


from cluz_form_distribution import Ui_distributionDialog
from cluz_form_identify_selected import Ui_identifySelectedDialog
from cluz_form_richness import Ui_richnessDialog
from cluz_form_portfolio import Ui_portfolioDialog
from cluz_form_portfolio_results import Ui_portfolioResultsDialog


class DistributionDialog(QDialog, Ui_distributionDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        load_distribution_feature_list(self, setup_object)
        set_initial_distribution_shapefile_path(self, setup_object)

        self.filePathButton.clicked.connect(self.set_dist_shapefile)
        self.okButton.clicked.connect(lambda: self.run_display_distribution_maps(setup_object))

    def set_dist_shapefile(self):
        (distShapefilePathNameText, fileTypeDetailsText) = QFileDialog.getSaveFileName(self, 'Save new shapefile', '*.shp')
        self.filePathlineEdit.setText(distShapefilePathNameText)

    def run_display_distribution_maps(self, setup_object):
        create_display_distribution_maps(self, setup_object)


class IdentifySelectedDialog(QDialog, Ui_identifySelectedDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        selected_pu_id_dict = return_selected_pu_id_dict(setup_object)
        selected_pu_details_dict = return_selected_pu_id_details_dict(setup_object, selected_pu_id_dict)
        self.show_selected_identify_data(setup_object, selected_pu_details_dict)

    def show_selected_identify_data(self, setup_object, selected_pu_details_dict):
        if len(selected_pu_details_dict) > 0:
            self.identifySelectedTableWidget.clear()
            self.identifySelectedTableWidget.setColumnCount(8)
            add_selected_identify_data_to_table_widget(self, setup_object, selected_pu_details_dict)
            add_formatting_headings_to_table_widget(self, setup_object)
            self.setWindowTitle('Details of ' + str(len(selected_pu_details_dict)) + ' planning units.')
        else:
            self.setWindowTitle('No planning units selected')

    def keyPressEvent(self, e):
        widget_name = 'identifySelectedTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)


class RichnessDialog(QDialog, Ui_richnessDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        final_count_field_name = return_initial_field_name(setup_object, 'F_COUNT')
        final_range_field_name = return_initial_field_name(setup_object, "RES_RANGE")
        self.countLineEdit.setText(final_count_field_name)
        self.rangeLineEdit.setText(final_range_field_name)
        type_list = produce_type_text_list(setup_object)
        self.typeListWidget.addItems(type_list)

        self.okButton.clicked.connect(lambda: self.create_richness_results(setup_object))

    def create_richness_results(self, setup_object):
        selected_feat_id_set = make_selected_feat_id_set(self, setup_object)
        pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
        field_name_list = [field.name() for field in pu_layer.fields()]

        progress_bool = check_richness_type_codes_selected_options_selected(self, selected_feat_id_set)
        add_layer_fudge = 0  # Added because QGIS doesn't recognise new layers that have been added when counting position of puLayer

        if self.countBox.isChecked() and progress_bool:
            return_richness_count_results(self, setup_object, field_name_list, selected_feat_id_set)
            add_layer_fudge += 1

        if self.rangeBox.isChecked() and progress_bool:
            return_richness_restricted_range_results(self, setup_object, field_name_list, selected_feat_id_set)
            add_layer_fudge += 1

        if progress_bool:
            success_message('Richness results', 'The fields have been successfully added to the planning unit layer attribute table.')
            remove_then_add_pu_layer(setup_object, add_layer_fudge)
            self.close()


class PortfolioDialog(QDialog, Ui_portfolioDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.sfComboBox.addItems(make_sf_field_list(setup_object))
        self.sfComboBox.setEnabled(False)
        self.sfFieldLabel.setEnabled(False)
        self.sfRunsLabel.setVisible(False)
        self.sfRunsLineEdit.setVisible(False)
        self.equalityCheckBox.setVisible(False)

        self.okButton.clicked.connect(lambda: self.run_return_portfolio_details(setup_object))

    def run_return_portfolio_details(self, setup_object):
        portfolio_pu_details_dict = make_portfolio_pu_details_dict()
        sf_runs_value_is_ok_bool = check_if_sf_runs_value_is_ok(self)
        if sf_runs_value_is_ok_bool:
            if self.puDetailsCheckBox.isChecked():
                portfolio_pu_details_dict = add_status_details_to_portfolio_dict(setup_object, portfolio_pu_details_dict)
            if self.spatialCheckBox.isChecked():
                portfolio_pu_details_dict = add_spatial_details_to_portfolio_dict(setup_object, portfolio_pu_details_dict)
            if self.patchTargetCheckBox.isChecked():
                portfolio_pu_details_dict = add_patch_feat_details_to_portfolio_dict(setup_object, portfolio_pu_details_dict)
            if self.sfCheckBox.isChecked():
                portfolio_pu_details_dict = add_sf_details_to_portfolio_dict(self, setup_object, portfolio_pu_details_dict)

        if sf_runs_value_is_ok_bool:
            self.close()

            if len(portfolio_pu_details_dict) > 0:
                self.portfolioResultsDialog = PortfolioResultsDialog(self, portfolio_pu_details_dict, setup_object)
                self.portfolioResultsDialog.show()
                self.portfolioResultsDialog.exec_()


class PortfolioResultsDialog(QDialog, Ui_portfolioResultsDialog):
    def __init__(self, iface, portfolio_pu_details_dict, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        self.portfolio_pu_details_dict = portfolio_pu_details_dict
        remove_superfluous_tabs(self, portfolio_pu_details_dict)
        if portfolio_pu_details_dict["status_details_bool"]:
            status_data_dict = portfolio_pu_details_dict["status_data_dict"]
            self.make_status_tab(setup_object, status_data_dict)
        if portfolio_pu_details_dict["spatial_details_bool"]:
            spatial_data_dict = portfolio_pu_details_dict["spatial_data_dict"]
            self.make_spatial_tab(setup_object, spatial_data_dict)
        if portfolio_pu_details_dict["sf_details_bool"]:
            sf_data_dict = portfolio_pu_details_dict["sf_data_dict"]
            self.make_sf_tab(sf_data_dict)
        if portfolio_pu_details_dict["patch_feat_details_bool"]:
            patch_feat_data_dict = portfolio_pu_details_dict["patch_feat_data_dict"]
            self.make_patch_feat_tab(setup_object, patch_feat_data_dict)
        if portfolio_pu_details_dict["pe_details_bool"]:
            pe_data_dict = portfolio_pu_details_dict["pe_data_dict"]
            self.makePETab(pe_data_dict)

    def make_status_tab(self, setup_object, status_data_dict):
        add_details_to_status_tab(self, setup_object, status_data_dict)

    def make_spatial_tab(self, setup_object, spatial_data_dict):
        add_details_to_spatial_tab(self, setup_object, spatial_data_dict)

    def make_sf_tab(self, sf_data_dict):
        add_details_to_sf_tab(self, sf_data_dict)

    def make_patch_feat_tab(self, setup_object, patch_feat_data_dict):
        add_details_to_patch_feat_tab(self, setup_object, patch_feat_data_dict)

    def keyPressEvent(self, e):
        widget_tab_index = self.portfolioTabWidget.currentIndex()
        if widget_tab_index == 0:
            widget_name = 'statusTabTableWidget'
        elif widget_tab_index == 1:
            widget_name = 'spatialTabTableWidget'
        elif widget_tab_index == 2 and self.portfolio_pu_details_dict["sf_details_bool"]:
            widget_name = 'sfTabTableWidget'
        elif widget_tab_index == 2 and self.portfolio_pu_details_dict["sf_details_bool"] is False:
            widget_name = 'patchFeatTabTableWidget'
        elif widget_tab_index == 3:
            widget_name = 'patchFeatTabTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)
