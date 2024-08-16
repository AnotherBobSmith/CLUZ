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

from qgis.PyQt.QtCore import Qt, QVariant
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtGui import QColor

from qgis.core import QgsVectorLayer, QgsField
from qgis.utils import iface

from csv import writer
from os import path, sep

from .cluz_make_file_dicts import return_rounded_value, return_lowest_unused_file_name_number
from .cluz_functions4 import return_string_amount_per_status, make_patch_feat_data_dict, produce_count_field, produce_restricted_range_field, make_sf_details_to_portfolio_dict, return_string_shortfall
from .cluz_functions4 import create_distribution_map_shapefile, make_feat_id_set_from_feat_type_set, make_full_sf_value_list, make_patch_dict_based_on_dummy_zone_file
from .cluz_messages import clear_progress_bar, make_progress_bar, warning_message, set_progress_bar_value
from .cluz_display import display_graduated_layer, display_distribution_maps

# Display distributions of conservation features ##########################


def load_distribution_feature_list(distribution_dialog, setup_object):
    feat_list = list(setup_object.target_dict.keys())
    feat_list.sort()
    feat_string_list = list()
    for aFeat in feat_list:
        a_string = str(aFeat) + ' - ' + setup_object.target_dict[aFeat][0]
        feat_string_list.append(a_string)
    distribution_dialog.featListWidget.addItems(feat_string_list)


def set_initial_distribution_shapefile_path(distribution_dialog, setup_object):
    dir_path_text = path.dirname(setup_object.pu_path)
    dist_shape_file_name_number = return_lowest_unused_file_name_number(dir_path_text, 'cluz_dist', '.shp')
    dist_shape_file_full_path = str(dir_path_text) + sep + 'cluz_dist' + str(dist_shape_file_name_number) + '.shp'
    distribution_dialog.filePathlineEdit.setText(dist_shape_file_full_path)
    
    
def create_display_distribution_maps(distribution_dialog, setup_object):
    if distribution_dialog.intervalRadioButton.isChecked():
        legend_type = 'equal_interval'
    else:
        legend_type = 'equal_area'
    dist_shape_file_path_name = distribution_dialog.filePathlineEdit.text()
    selected_feat_list = [item.text() for item in distribution_dialog.featListWidget.selectedItems()]
    selected_feat_id_list = [int(item.split(' - ')[0]) for item in selected_feat_list]

    abund_values_dict = create_distribution_map_shapefile(setup_object, dist_shape_file_path_name, selected_feat_id_list)
    display_distribution_maps(setup_object, dist_shape_file_path_name, abund_values_dict, legend_type, selected_feat_id_list)

    distribution_dialog.close()


# Identify features in selected units #####################################################

def return_selected_pu_id_dict(setup_object):
    selected_pu_id_dict = dict()

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    iface.setActiveLayer(pu_layer)
    pu_layer = iface.activeLayer()
    provider = pu_layer.dataProvider()
    id_field_index = provider.fieldNameIndex('Unit_ID')
    status_field_index = provider.fieldNameIndex('Status')

    selected_p_us = pu_layer.selectedFeatures()
    for a_pu in selected_p_us:
        pu_id = int(a_pu.attributes()[id_field_index])
        pu_status = str(a_pu.attributes()[status_field_index])
        selected_pu_id_dict[pu_id] = pu_status

    return selected_pu_id_dict


def return_selected_pu_id_details_dict(setup_object, selected_pu_id_dict):
    selected_pu_details_dict = dict()
    for pu_id in selected_pu_id_dict:
        pu_status = selected_pu_id_dict[pu_id]
        try:
            pu_abund_dict = setup_object.abund_pu_key_dict[pu_id]
        except KeyError:
            pu_abund_dict = dict()
        try:
            status_details_dict = selected_pu_details_dict[pu_status]
        except KeyError:
            status_details_dict = dict()

        for featID in pu_abund_dict:
            try:
                feat_amount = pu_abund_dict[featID]
            except KeyError:
                feat_amount = 0
            try:
                feat_running_amount = status_details_dict[featID]
            except KeyError:
                feat_running_amount = 0
            feat_running_amount += feat_amount
            status_details_dict[featID] = feat_running_amount

        selected_pu_details_dict[pu_status] = status_details_dict

    return selected_pu_details_dict


def add_selected_identify_data_to_table_widget(identify_selected_dialog, setup_object, selected_pu_details_dict):
    feat_id_list = list(setup_object.target_dict.keys())
    feat_id_list.sort()
    for rowNumber in range(0, len(feat_id_list)):
        feat_id = feat_id_list[rowNumber]
        identify_selected_dialog.identifySelectedTableWidget.insertRow(rowNumber)
        feat_id_table_item = QTableWidgetItem(str(feat_id))
        feat_name_table_item = QTableWidgetItem(str(setup_object.target_dict[feat_id][0]))
        ava_id_table_item = QTableWidgetItem(str(return_string_amount_per_status(setup_object, selected_pu_details_dict, 'Available', feat_id)))
        con_id_table_item = QTableWidgetItem(str(return_string_amount_per_status(setup_object, selected_pu_details_dict, 'Conserved', feat_id)))
        ear_id_table_item = QTableWidgetItem(str(return_string_amount_per_status(setup_object, selected_pu_details_dict, 'Earmarked', feat_id)))
        exl_id_table_item = QTableWidgetItem(str(return_string_amount_per_status(setup_object, selected_pu_details_dict, 'Excluded', feat_id)))
        feat_target = return_rounded_value(setup_object, setup_object.target_dict[feat_id][3])
        feat_target_table_item = QTableWidgetItem(feat_target)
        feat_shortfall_table_item = QTableWidgetItem(return_string_shortfall(setup_object, feat_id))

        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 0, feat_id_table_item)
        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 1, feat_name_table_item)
        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 2, ava_id_table_item)
        con_id_table_item.setForeground(QColor.fromRgb(0, 153, 51))
        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 3, con_id_table_item)
        ear_id_table_item.setForeground(QColor.fromRgb(51, 204, 51))
        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 4, ear_id_table_item)
        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 5, exl_id_table_item)
        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 6, feat_target_table_item)
        if return_string_shortfall(setup_object, feat_id) == 'Target met':
            feat_shortfall_table_item.setForeground(QColor.fromRgb(128, 128, 128))
        identify_selected_dialog.identifySelectedTableWidget.setItem(rowNumber, 7, feat_shortfall_table_item)


def add_formatting_headings_to_table_widget(identify_selected_dialog, setup_object):
    header_list = ['ID  ', 'Name  ', 'Available  ', 'Conserved  ', 'Earmarked  ', 'Excluded  ', 'Target  ', 'Target shortfall  ']
    identify_selected_dialog.identifySelectedTableWidget.setHorizontalHeaderLabels(header_list)
    identify_selected_dialog.identifySelectedTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
    identify_selected_dialog.identifySelectedTableWidget.verticalHeader().hide()
    for aColValue in range(len(header_list)):
        identify_selected_dialog.identifySelectedTableWidget.resizeColumnToContents(aColValue)


# Calculate richness scores #################################################

def return_initial_field_name(setup_object, field_name):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    field_name_list = [field.name() for field in pu_layer.fields()]

    count_suffix = ''
    if field_name in field_name_list:
        count_suffix = 1
        while (field_name + str(count_suffix)) in field_name_list:
            count_suffix += 1
    final_field_name = field_name + str(count_suffix)

    return final_field_name


def produce_type_text_list(setup_object):
    type_text_list = list()
    type_dict = dict()
    for feat_id in setup_object.target_dict:
        feat_type = setup_object.target_dict[feat_id][1]
        try:
            feat_count = type_dict[feat_type]
            feat_count += 1
        except KeyError:
            feat_count = 1
        type_dict[feat_type] = feat_count

    type_list = list(type_dict.keys())
    type_list.sort()
    for a_type in type_list:
        type_text = 'Type ' + str(a_type) + ' (' + str(type_dict[a_type]) + ' features)'
        type_text_list.append(type_text)

    return type_text_list


def make_selected_feat_id_set(a_dialog, setup_object):
    selected_type_text_list = [item.text() for item in a_dialog.typeListWidget.selectedItems()]
    selected_type_set = set([int(item.split(" ")[1]) for item in selected_type_text_list])
    selected_feat_id_set = make_feat_id_set_from_feat_type_set(setup_object, selected_type_set)

    return selected_feat_id_set


def check_richness_type_codes_selected_options_selected(richness_dialog, selected_feat_id_set):
    progress_bool = True
    if len(selected_feat_id_set) == 0:
        warning_message('Calculating richness', 'No type codes have been selected.')
        progress_bool = False
    if richness_dialog.countBox.isChecked() is False and richness_dialog.rangeBox.isChecked() is False:
        warning_message('Calculating richness', 'No options have been selected.')
        progress_bool = False

    return progress_bool


def return_richness_count_results(richness_dialog, setup_object, field_name_list, selected_feat_id_set):
    count_field_name = richness_dialog.countLineEdit.text()
    if count_field_name in field_name_list:
        warning_message('Feature Count field name duplication', 'The planning unit layer already contains a field named ' + count_field_name + '. Please choose another name.')
    elif count_field_name == '':
        warning_message('Feature Count field name blank', 'The Feature Count name field is blank. Please choose a name.')
    elif len(count_field_name) > 10:
        warning_message('Invalid field name', 'The Feature Count field name cannot be more than 10 characters long.')
    else:
        produce_count_field(setup_object, count_field_name, selected_feat_id_set)
        display_graduated_layer(setup_object, count_field_name, 'Feature count', 2)  # 2 is yellow to green QGIS legend code


def return_richness_restricted_range_results(richness_dialog, setup_object, field_name_list, selected_feat_id_set):
    range_field_name = richness_dialog.rangeLineEdit.text()
    if range_field_name in field_name_list:
        warning_message('Restricted Range Richness field name duplication', 'The planning unit layer already contains a field named ' + range_field_name + '. Please choose another name.')
    elif range_field_name == '':
        warning_message('Restricted Range Richness field name blank', 'The Restricted Range Richness name field is blank. Please choose a name.')
    elif len(range_field_name) > 10:
        warning_message('Invalid field name', 'The Restricted Range Richness field name cannot be more than 10 characters long.')
    else:
        produce_restricted_range_field(setup_object, range_field_name, selected_feat_id_set)
        display_graduated_layer(setup_object, range_field_name, 'Restricted Range score', 2)  # 2 is yellow to green QGIS legend code


# Calculate irreplaceability details #####################################

def add_irrep_results(setup_object, irrep_dict, irrep_field_name, status_set):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    provider = pu_layer.dataProvider()
    id_field_index = pu_layer.fields().indexFromName("Unit_ID")
    status_field_index = pu_layer.fields().indexFromName("Status")

    provider.addAttributes([QgsField(irrep_field_name, QVariant.Double)])
    pu_layer.updateFields()
    irrep_field_order = provider.fieldNameIndex(irrep_field_name)

    progress_bar = make_progress_bar('Adding summed irreplaceability values to planning unit shapefile')
    poly_count = 1
    poly_total_count = pu_layer.featureCount()

    pu_features = pu_layer.getFeatures()
    pu_layer.startEditing()
    for puFeature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_row = puFeature.id()
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[id_field_index]
        pu_status = pu_attributes[status_field_index]
        if pu_status in status_set:
            summed_irrep_value = 0
            try:
                pu_irrep_dict = irrep_dict[pu_id]
                for feat_id in pu_irrep_dict:
                    summed_irrep_value += pu_irrep_dict[feat_id]
            except KeyError:
                pass
        else:
            summed_irrep_value = -99
        pu_layer.changeAttributeValue(pu_row, irrep_field_order, summed_irrep_value, True)
    pu_layer.commitChanges()
    clear_progress_bar()


def make_irrep_dict_output_file(setup_object, irrep_dict, irrep_output_file_path, pu_set):
    pu_id_list = list(setup_object.abund_pu_key_dict.keys())
    pu_id_list.sort()
    feat_id_list = list(setup_object.target_dict.keys())
    feat_id_list.sort()

    header_row = ['PU_ID']
    for feat_id in feat_id_list:
        header_row.append('FT_' + str(feat_id))
    na_list = ['NA'] * len(feat_id_list)

    with open(irrep_output_file_path, 'w', newline='', encoding='utf-8') as irrep_output_file_path:
        irrep_writer = writer(irrep_output_file_path)
        irrep_writer.writerow(header_row)

        for pu_id in pu_id_list:
            if pu_id in pu_set:
                row = [str(pu_id)]
                try:
                    pu_irrep_dict = irrep_dict[pu_id]
                except KeyError:
                    pu_irrep_dict = dict()
                for feat_id in feat_id_list:
                    try:
                        irrep_value = pu_irrep_dict[feat_id]
                    except KeyError:
                        irrep_value = 0
                    row.append(irrep_value)
                irrep_writer.writerow(row)
            else:
                na_row = [str(pu_id)] + na_list
                irrep_writer.writerow(na_row)


# Calculate irreplaceability details ###########################################

# Calculate portfolio details ##################################################
        
def make_sf_field_list(setup_object):
    sf_field_list = list()
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')

    for a_field in pu_layer.fields():
        if str(a_field.typeName()) == 'Integer' and str(a_field.name()) != 'Unit_ID':
            sf_field_list.append(a_field.name())

    if len(sf_field_list) == 0:
        sf_field_list.append('No suitable fields')

    return sf_field_list


def check_if_sf_runs_value_is_ok(self):
    sf_runs_value_is_ok = True
    if self.sfCheckBox.isChecked():
        try:
            sf_runs_value = int(self.sfRunsLineEdit.text())
            if sf_runs_value < 1:
                warning_message('Value error', 'The number of runs value must be an integer greater than 0.')
                sf_runs_value_is_ok = False
        except ValueError:
            warning_message('Value error', 'The number of runs value must be an integer greater than 0.')
            sf_runs_value_is_ok = False

    return sf_runs_value_is_ok


# portfolioResultsDialog ###########################################################

def remove_superfluous_tabs(portfolio_results_dialog, portfolio_pu_details_dict):
    tab_name_remove_list = list()
    if not portfolio_pu_details_dict['status_details_bool']:
        tab_name_remove_list.append('Status results')
    if not portfolio_pu_details_dict['spatial_details_bool']:
        tab_name_remove_list.append('Spatial results')
    if not portfolio_pu_details_dict['sf_details_bool']:
        tab_name_remove_list.append('Selection frequency results')
    if not portfolio_pu_details_dict['patch_feat_details_bool']:
        tab_name_remove_list.append('Patches per feature')
    if not portfolio_pu_details_dict['pe_details_bool']:
        tab_name_remove_list.append('Protection equality')

    for a_iter in range(0, len(tab_name_remove_list)):
        for tab_index in range(0, portfolio_results_dialog.portfolioTabWidget.count()):
            tab_name = portfolio_results_dialog.portfolioTabWidget.tabText(tab_index)
            if tab_name in tab_name_remove_list:
                portfolio_results_dialog.portfolioTabWidget.removeTab(tab_index)
                tab_name_remove_list.remove(tab_name)


def add_details_to_status_tab(portfolio_results_dialog, setup_object, status_data_dict):
    portfolio_results_dialog.statusTabTableWidget.clear()
    portfolio_results_dialog.statusTabTableWidget.setColumnCount(4)
    row_number = 0
    status_type_list = ['Available', 'Conserved', 'Earmarked', 'Excluded', 'Portfolio', 'Region']
    for statusType in status_type_list:
        portfolio_results_dialog.statusTabTableWidget.insertRow(row_number)
        status_table_item = QTableWidgetItem(statusType)
        cost_string, area_string, count_string = return_status_tab_string_values(setup_object, status_data_dict, statusType)
        cost_table_item = QTableWidgetItem(cost_string)
        area_table_item = QTableWidgetItem(area_string)
        count_table_item = QTableWidgetItem(count_string)
        portfolio_results_dialog.statusTabTableWidget.setItem(row_number, 0, status_table_item)
        portfolio_results_dialog.statusTabTableWidget.setItem(row_number, 1, cost_table_item)
        portfolio_results_dialog.statusTabTableWidget.setItem(row_number, 2, area_table_item)
        portfolio_results_dialog.statusTabTableWidget.setItem(row_number, 3, count_table_item)
        row_number += 1
    status_header_list = ['Status', 'Total cost', 'Total area', 'No. of planning units']
    portfolio_results_dialog.statusTabTableWidget.setHorizontalHeaderLabels(status_header_list)
    for aColValue in range(len(status_header_list)):
        portfolio_results_dialog.statusTabTableWidget.resizeColumnToContents(aColValue)
    portfolio_results_dialog.statusTabTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
    portfolio_results_dialog.statusTabTableWidget.verticalHeader().hide()
        
        
def return_status_tab_string_values(setup_object, status_data_dict, status_type):
    decimal_places = setup_object.decimal_places
    cost_value = status_data_dict[status_type][0]
    limbo_cost_value = round(float(cost_value), decimal_places)
    cost_string = format(limbo_cost_value, '.' + str(decimal_places) + 'f')
    area_value = status_data_dict[status_type][1]
    limbo_area_value = round(float(area_value), decimal_places)
    area_string = format(limbo_area_value, '.' + str(decimal_places) + 'f')
    count_string = str(status_data_dict[status_type][2])

    return cost_string, area_string, count_string


def add_details_to_spatial_tab(portfolio_results_dialog, setup_object, spatial_data_dict):
    portfolio_results_dialog.spatialTabTableWidget.clear()
    portfolio_results_dialog.spatialTabTableWidget.setColumnCount(2)
    row_number = 0
    spatial_table_item_dict = make_spatial_table_item_dict(setup_object, spatial_data_dict)
    for spatial_row_order in range(0, 5):
        add_data_to_portfolio_results_table_widget(portfolio_results_dialog.spatialTabTableWidget, spatial_table_item_dict, spatial_row_order, row_number)
    spatial_header_list = ['Metric', 'Value']
    portfolio_results_dialog.spatialTabTableWidget.setHorizontalHeaderLabels(spatial_header_list)
    for aColValue in range(len(spatial_header_list)):
        portfolio_results_dialog.spatialTabTableWidget.resizeColumnToContents(aColValue)
    portfolio_results_dialog.spatialTabTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
    portfolio_results_dialog.spatialTabTableWidget.verticalHeader().hide()


def add_data_to_portfolio_results_table_widget(spatial_tab_table_widget, spatial_table_item_dict, spatial_row_order, row_number):
    spatial_tab_table_widget.insertRow(row_number)
    desc_table_item = QTableWidgetItem(spatial_table_item_dict[spatial_row_order][0])
    value_table_item = QTableWidgetItem(spatial_table_item_dict[spatial_row_order][1])
    spatial_tab_table_widget.setItem(row_number, 0, desc_table_item)
    spatial_tab_table_widget.setItem(row_number, 1, value_table_item)
    row_number += 1


def make_spatial_table_item_dict(setup_object, spatial_data_dict):
    decimal_places = setup_object.decimal_places
    spatial_table_item_dict = dict()
    spatial_table_item_dict[0] = ['Number of patches', str(spatial_data_dict['patchCount'])]

    small_patch_size = spatial_data_dict['patchSmallest']
    limbo_small_patch_size = round(float(small_patch_size), decimal_places)
    small_patch_size_string = format(limbo_small_patch_size, '.' + str(decimal_places) + 'f')
    spatial_table_item_dict[1] = ['Area of smallest patch', small_patch_size_string]

    median_patch_size = spatial_data_dict['patchMedian']
    limbo_median_patch_size = round(float(median_patch_size), decimal_places)
    median_patch_size_string = format(limbo_median_patch_size, '.' + str(decimal_places) + 'f')
    spatial_table_item_dict[2] = ['Median area of patches', median_patch_size_string]

    large_patch_size = spatial_data_dict['patchLargest']
    limbo_large_patch_size = round(float(large_patch_size), decimal_places)
    large_patch_size_string = format(limbo_large_patch_size, '.' + str(decimal_places) + 'f')
    spatial_table_item_dict[3] = ['Area of largest patch', large_patch_size_string]

    boundary_length = spatial_data_dict['totalBoundLength']
    limbo_boundary_length = round(float(boundary_length), decimal_places)
    boundary_string = format(limbo_boundary_length, '.' + str(decimal_places) + 'f')
    spatial_table_item_dict[4] = ['Portfolio boundary length', boundary_string]

    return spatial_table_item_dict


def add_patch_feat_details_to_portfolio_dict(setup_object, portfolio_pu_details_dict):
    pu_dict, patch_dict, dummy_zone_dict = make_patch_dict_based_on_dummy_zone_file(setup_object)  # Only need patch_dict
    patch_feat_data_dict = make_patch_feat_data_dict(setup_object, patch_dict)

    portfolio_pu_details_dict['patch_feat_details_bool'] = True
    portfolio_pu_details_dict['patch_feat_data_dict'] = patch_feat_data_dict

    return portfolio_pu_details_dict


def add_sf_details_to_portfolio_dict(portfolio_dialog, setup_object, portfolio_pu_details_dict):
    sf_field_name = portfolio_dialog.sfComboBox.currentText()
    sf_runs_value = int(portfolio_dialog.sfRunsLineEdit.text())
    sf_value_list = make_full_sf_value_list(setup_object, sf_field_name)
    if check_sf_runs_value_not_lower_than_max_sf_value(sf_value_list, sf_runs_value):
        portfolio_pu_details_dict = make_sf_details_to_portfolio_dict(portfolio_pu_details_dict, sf_value_list, sf_runs_value)

    return portfolio_pu_details_dict


def check_sf_runs_value_not_lower_than_max_sf_value(sf_value_list, sf_runs_value):
    sf_runs_value_not_lower_than_max_sf_value = True

    if max(sf_value_list) > sf_runs_value:
        warning_message("Value error", "The specified number of runs value is less than the highest selection frequency value in the specified selection frequency field. Please check the number of runs used in the analysis and update this figure.")
        sf_runs_value_not_lower_than_max_sf_value = False

    return sf_runs_value_not_lower_than_max_sf_value


def add_details_to_sf_tab(portfolio_results_dialog, sf_data_dict):
    portfolio_results_dialog.sfTabTableWidget.clear()
    portfolio_results_dialog.sfTabTableWidget.setColumnCount(2)
    row_number = 0
    sf_dict_key_list = range(0, len(sf_data_dict))
    for sf_dict_key in sf_dict_key_list:
        add_data_to_portfolio_results_table_widget(portfolio_results_dialog.sfTabTableWidget, sf_data_dict, sf_dict_key, row_number)
        portfolio_results_dialog.sfTabTableWidget.insertRow(row_number)
        desc_table_item = QTableWidgetItem(sf_data_dict[sf_dict_key][0])
        value_table_item = QTableWidgetItem(sf_data_dict[sf_dict_key][1])
        portfolio_results_dialog.sfTabTableWidget.setItem(row_number, 0, desc_table_item)
        portfolio_results_dialog.sfTabTableWidget.setItem(row_number, 1, value_table_item)
        row_number += 1

    sf_header_list = ['Selection frequency value range', 'Number of planning units']
    portfolio_results_dialog.sfTabTableWidget.setHorizontalHeaderLabels(sf_header_list)
    for aColValue in range(len(sf_header_list)):
        portfolio_results_dialog.sfTabTableWidget.resizeColumnToContents(aColValue)


def add_details_to_patch_feat_tab(portfolio_results_dialog, setup_object, patch_feat_data_dict):
    portfolio_results_dialog.patchFeatTabTableWidget.clear()
    portfolio_results_dialog.patchFeatTabTableWidget.setColumnCount(3)
    row_number = 0
    feat_id_list = list(setup_object.target_dict.keys())
    feat_id_list.sort()
    for featID in feat_id_list:
        portfolio_results_dialog.patchFeatTabTableWidget.insertRow(row_number)
        feat_id_table_item = QTableWidgetItem(str(featID))
        feat_name_table_item = QTableWidgetItem(setup_object.target_dict[featID][0])
        try:
            count_table_item = QTableWidgetItem(str(patch_feat_data_dict[featID]))
        except KeyError:
            count_table_item = QTableWidgetItem(str(0))
        portfolio_results_dialog.patchFeatTabTableWidget.setItem(row_number, 0, feat_id_table_item)
        portfolio_results_dialog.patchFeatTabTableWidget.setItem(row_number, 1, feat_name_table_item)
        portfolio_results_dialog.patchFeatTabTableWidget.setItem(row_number, 2, count_table_item)
        row_number += 1

    sf_header_list = ['Feature ID', 'Feature name', "Number of patches"]
    portfolio_results_dialog.patchFeatTabTableWidget.setHorizontalHeaderLabels(sf_header_list)
    for aColValue in range(len(sf_header_list)):
        portfolio_results_dialog.patchFeatTabTableWidget.resizeColumnToContents(aColValue)
    portfolio_results_dialog.patchFeatTabTableWidget.horizontalHeader().setStyleSheet(setup_object.table_heading_style)
    portfolio_results_dialog.patchFeatTabTableWidget.verticalHeader().hide()
