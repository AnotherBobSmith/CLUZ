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

from qgis.core import QgsProject, QgsVectorLayer

from csv import reader
from os import access, path, W_OK

from .cluz_messages import warning_message, success_message, critical_message
from .cluz_make_file_dicts import make_puvspr2_dat_file, add_features_to_target_csv_file, make_target_dict
from .cluz_functions2 import add_abund_dict_to_abund_pu_key_dict, create_target_puvspr2_files, create_pu_layer, make_vec_add_abund_dict, make_raster_add_abund_dict
from .cluz_functions2 import update_abund_data

from .zcluz_make_file_dicts import zones_add_features_to_target_csv_file, make_zones_target_dict, make_zones_prop_dict, make_zones_target_zones_dict
from .zcluz_dialog3 import recalc_update_zones_target_table_details


# Make new CLUZ files ###########################################################################


def check_make_new_cluz_files(create_dialog):
    shapefile_ok_bool = check_shapefile(create_dialog)
    conversion_format_ok_bool = check_conversion_format(create_dialog)
    input_folder_ok_bool = check_input_folder_path(create_dialog)
    target_table_ok_bool = check_target_table(create_dialog)

    if shapefile_ok_bool and conversion_format_ok_bool and input_folder_ok_bool and target_table_ok_bool:
        create_pu_layer(create_dialog)
        create_target_puvspr2_files(create_dialog)
        success_message('Task completed', 'The CLUZ planning unit layer, blank abundance and target tables have been created. You can now use them when creating the CLUZ setup file.')
        create_dialog.close()


def check_shapefile(create_dialog):
    shapefile_ok_bool = True
    if create_dialog.puLineEdit.text() == '':
        warning_message('Shapefile error', 'No shapefile was specified.')
        shapefile_ok_bool = False

    if shapefile_ok_bool:
        pu_layer = QgsVectorLayer(create_dialog.puLineEdit.text(), 'Shapefile', 'ogr')
        layer_geom_type = pu_layer.geometryType()
        pu_provider = pu_layer.dataProvider()
        pu_id_field_order = pu_provider.fieldNameIndex('Unit_ID')
        pu_cost_field_order = pu_provider.fieldNameIndex('Area')
        pu_area_field_order = pu_provider.fieldNameIndex('Cost')
        pu_status_field_order = pu_provider.fieldNameIndex('Status')

        if layer_geom_type != 2:
            warning_message('Incorrect format', 'The specified shapefile is not a polygon layer.')
            shapefile_ok_bool = False

        if pu_id_field_order != -1 or pu_cost_field_order != -1 or pu_area_field_order != -1 or pu_status_field_order != -1:
            warning_message('Incorrect format', 'The specified shapefile cannot contain fields named Unit_ID, Area, Cost or Status as these will be created here. Please remove/rename these fields and try again.')
            shapefile_ok_bool = False

    return shapefile_ok_bool


def check_conversion_format(create_dialog):
    conversion_format_ok_bool = True
    try:
        conv_factor = float(create_dialog.convLineEdit.text())
        if conversion_format_ok_bool and conv_factor <= 0:
            warning_message('Incorrect format', 'The specified conversion format is in an incorrect format. It should be a number greater than 0.')
            conversion_format_ok_bool = False
    except ValueError:
        warning_message('Incorrect format', 'The specified conversion format is in an incorrect format. It should be a number greater than 0.')
        conversion_format_ok_bool = False

    return conversion_format_ok_bool


def check_input_folder_path(create_dialog):
    input_folder_ok_bool = True
    if create_dialog.inputLineEdit.text() == '':
        warning_message('No folder specified', 'You need to specify the input folder where the puvspr2.dat file will be saved.')
        input_folder_ok_bool = False
    else:
        if access(path.dirname(create_dialog.inputLineEdit.text()), W_OK):
            pass
        else:
            warning_message('Incorrect format', 'You do not have access to the specified input folder.')
            input_folder_ok_bool = False

    return input_folder_ok_bool


def check_target_table(create_dialog):
    target_table_ok_bool = True
    if create_dialog.targetLineEdit.text() == '':
        warning_message('No file specified', 'You need to specify the name and path for the new target file.')
        target_table_ok_bool = False
    else:
        if access(path.dirname(create_dialog.targetLineEdit.text()), W_OK):
            pass
        else:
            warning_message('Incorrect format', 'You cannot save the target table into the specified folder because you do not have access.')
            target_table_ok_bool = False

        if create_dialog.targetLineEdit.text()[-4:] != '.csv':
            warning_message('Incorrect format', 'Your target table must be a .csv file.')
            target_table_ok_bool = False

    return target_table_ok_bool


# Import vec data #########################################################################

def check_add_layer_list_convert_vec_dialog(convert_vec_dialog):
    layer_name_list = load_vec_themes_list()
    if len(layer_name_list) == 0:
        warning_message('No suitable layers', 'Please add to the project the polyline or polygon shapefiles that you want to import.')
        convert_vec_dialog.okButton.setEnabled(False)
    convert_vec_dialog.selectListWidget.addItems(layer_name_list)


def load_vec_themes_list():
    list_map_items = QgsProject.instance().mapLayers()
    layer_name_list = list()
    for nameCode, layer in list_map_items.items():
        layer_name = layer.name()
        try:
            layer_geom_type = layer.geometryType()
            if layer_name != "Planning units" and layer_geom_type != 0:
                layer_name_list.append(str(layer_name))
        except AttributeError:
            pass

    return layer_name_list


def check_return_layer_list(convert_vec_dialog):
    layer_check = True
    layer_list = list()
    selected_layer_name_list = [item.text() for item in convert_vec_dialog.selectListWidget.selectedItems()]
    layer_check = check_at_least_one_layer_selected(convert_vec_dialog, selected_layer_name_list, layer_check)
    if layer_check:
        layer_list = make_layer_list(selected_layer_name_list)

    return layer_list, layer_check


def check_at_least_one_layer_selected(convert_vec_dialog, selected_layer_name_list, layer_factor_check):
    if len(selected_layer_name_list) == 0:
        convert_vec_dialog.close()
        warning_message('No layers selected', 'No layers were selected.')
        layer_factor_check = False

    return layer_factor_check


def make_layer_list(selected_layer_name_list):
    layer_list = list()
    list_map_items = QgsProject.instance().mapLayers()
    for nameCode, layer in list_map_items.items():
        layer_name = layer.name()
        if layer_name in selected_layer_name_list:
            layer_list.append(layer)

    return layer_list


def check_layer_list_for_incorrect_fields(convert_vec_dialog, layer_list, layer_factor_check):
    for aLayer in layer_list:
        provider = aLayer.dataProvider()
        a_layer_name = aLayer.name()
        incorrect_field_order = provider.fieldNameIndex('Unit_ID')
        if incorrect_field_order != -1:
            convert_vec_dialog.close()
            critical_message('Layer format error', 'Only the planning unit layer should contain a field named Unit_ID. Please remove this field from the layer: ' + a_layer_name)
            layer_factor_check = False

    return layer_factor_check

def check_layer_factor_convert_vec(convert_vec_dialog, layer_list, layer_factor_check):
    id_field_name = convert_vec_dialog.idfieldLineEdit.text()
    if layer_factor_check:
        for aLayer in layer_list:
            provider = aLayer.dataProvider()
            a_layer_name = aLayer.name()
            id_field_order = provider.fieldNameIndex(id_field_name)
            if id_field_order == -1:
                convert_vec_dialog.close()
                warning_message('Layer format error with ' + a_layer_name, 'The specified ID field ' + id_field_name + ' is not in the layer ' + a_layer_name + '.')
                layer_factor_check = False
            else:
                id_field = provider.fields().field(id_field_order)
                id_field_type = id_field.typeName()
                if id_field_type != 'Integer' and id_field_type != 'Integer64' and id_field_type != 'integer':
                    convert_vec_dialog.close()
                    warning_message('Layer format error' + a_layer_name, 'The specified ID field ' + id_field_name + ' does not contain integer values.')
                    layer_factor_check = False

    return layer_factor_check


def check_layer_has_same_crs_as_pu_layer(convert_vec_dialog, setup_object):
    same_projection_check = True
    layer_list = list()
    pu_layer_crs = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr').crs().authid()

    selected_layer_name_list = [item.text() for item in convert_vec_dialog.selectListWidget.selectedItems()]
    list_map_items = QgsProject.instance().mapLayers()
    for nameCode, layer in list_map_items.items():
        layer_name = layer.name()
        if layer_name in selected_layer_name_list:
            layer_list.append(layer)

    for aLayer in layer_list:
        a_layer_name = aLayer.name()
        feature_layer_crs = aLayer.crs().authid()
        if feature_layer_crs != pu_layer_crs:
            convert_vec_dialog.close()
            warning_message('Layer format error with ' + a_layer_name, 'QGIS can only extract the data from this layer if it has the same projection system as the planning unit theme, so please reproject it.')
            same_projection_check = False

    return same_projection_check


def create_update_abund_data_from_vec_file(convert_vec_dialog, setup_object, layer_list):
    id_field_name = convert_vec_dialog.idfieldLineEdit.text()
    conv_factor = float(convert_vec_dialog.convLineEdit.text())
    add_abund_dict, add_feat_id_list, error_layer_list = make_vec_add_abund_dict(setup_object, layer_list, id_field_name, conv_factor)
    existing_id_set = set(add_feat_id_list).intersection(set(setup_object.target_dict.keys()))

    if len(existing_id_set) > 0:
        produce_warning_message_about_feats_already_in_abund_tab(convert_vec_dialog, existing_id_set)
    else:
        update_abund_data(setup_object, add_abund_dict, add_feat_id_list)
        convert_vec_dialog.close()

    return error_layer_list

        
def produce_warning_message_about_feats_already_in_abund_tab(convert_vec_dialog, existing_id_set):
    convert_vec_dialog.close()
    list_text = ''
    for aID in existing_id_set:
        list_text += str(aID) + ', '
    final_list_text = list_text[0: -2]
    warning_message('Existing features', 'The abundance table already contains features with ID values of ' + final_list_text + '. This process will terminate without adding the new values.')


def make_vector_error_layer_string(error_layer_list):
    raw_error_layer_string = 'please check your input data, as QGIS was unable to intersect the planning unit layer with the following data layers: '
    for aLayerName in error_layer_list:
        raw_error_layer_string += aLayerName + ' ,'

    error_layer_string = raw_error_layer_string[0:-2]

    return error_layer_string

# Import raster data ############################################################


def check_add_layer_list_convert_raster_dialog(convert_raster_dialog):
    layer_name_list = load_raster_themes_list()
    if len(layer_name_list) == 0:
        warning_message('No suitable layers ', 'Please add the raster layers that you want to import to the project. They must be single-band integer raster layers.')
        convert_raster_dialog.okButton.setEnabled(False)
    convert_raster_dialog.selectListWidget.addItems(layer_name_list)


def load_raster_themes_list():
    list_map_items = QgsProject.instance().mapLayers()
    layer_name_list = list()
    for nameCode, layer in list_map_items.items():
        layer_name = layer.name()
        try:
            layer_band_count = layer.bandCount()
            if layer_band_count == 1:
                layer_name_list.append(str(layer_name))
        except AttributeError:
            pass

    return layer_name_list


def check_layer_factor_convert_raster(convert_raster_dialog):
    layer_factor_check = True
    layer_list = list()

    selected_layer_name_list = [item.text() for item in convert_raster_dialog.selectListWidget.selectedItems()]
    if len(selected_layer_name_list) == 0:
        convert_raster_dialog.close()
        warning_message('No layers selected', 'No layers were selected.')
        layer_factor_check = False
    else:
        list_map_items = QgsProject.instance().mapLayers()
        for nameCode, layer in list_map_items.items():
            layer_name = layer.name()
            if layer_name in selected_layer_name_list:
                layer_list.append(layer)

    return layer_list, layer_factor_check


def create_update_abund_data_from_raster_file(raster_vec_dialog, setup_object, layer_list):
    conv_factor = float(raster_vec_dialog.convLineEdit.text())
    add_abund_dict, add_feat_id_list, error_layer_list = make_raster_add_abund_dict(setup_object, layer_list, conv_factor)
    existing_id_set = set(add_feat_id_list).intersection(set(setup_object.target_dict.keys()))
    if len(existing_id_set) > 0:
        produce_warning_message_about_feats_already_in_abund_tab(raster_vec_dialog, existing_id_set)
    else:
        update_abund_data(setup_object, add_abund_dict, add_feat_id_list)
        raster_vec_dialog.close()

    return error_layer_list


def make_raster_error_layer_string(error_layer_list):
    raw_error_layer_string = 'the input raster data must only contain positive integer values (zeros are ignored), so the following layers are not valid: '
    for aLayerName in error_layer_list:
        raw_error_layer_string += aLayerName + ' ,'

    error_layer_string = raw_error_layer_string[0:-2]

    return error_layer_string

# Import csv data ##########################################################################################


def check_add_csv_file_path(convert_csv_dialog, csv_path_name_text):
    if csv_path_name_text != '':
        convert_csv_dialog.csvFileLineEdit.setText(csv_path_name_text)
        csv_file = open(csv_path_name_text, 'rt')
        try:
            csv_reader = reader(csv_file)
            file_header_list = next(csv_reader)
            convert_csv_dialog.idfieldComboBox.addItems(file_header_list)
            convert_csv_dialog.idfieldComboBox.setEnabled(True)
        except IOError:
            warning_message('Input file incorrectly formatted', 'CLUZ cannot read this file. Please check it is a csv file with commas between fields and each row representing a table line')


def check_layer_factor(convert_csv_dialog):
    layer_factor_check = True
    csv_file_path = convert_csv_dialog.csvFileLineEdit.text()
    if csv_file_path == '':
        convert_csv_dialog.close()
        warning_message('No file specified', 'Please specify a csv file to import.')
        layer_factor_check = False
    elif path.isfile(csv_file_path) is False:
        convert_csv_dialog.close()
        warning_message('Incorrect format', 'The specified csv file does not exist.')
        layer_factor_check = False
    else:
        pass

    return layer_factor_check


# def check_conv_factor(convert_csv_dialog, layer_factor_check):
#     conv_factor_check = True
#     if layer_factor_check:
#         if convert_csv_dialog.userRadioButton.isChecked():
#             try:
#                 conv_factor = float(convert_csv_dialog.convLineEdit.text())
#                 if conv_factor <= 0:
#                     convert_csv_dialog.close()
#                     warning_message('Incorrect conversion value', 'The conversion value must be a number greater than 0.')
#                     conv_factor_check = False
#
#             except ValueError:
#                 convert_csv_dialog.close()
#                 warning_message('Incorrect conversion value', 'The conversion value must be a number greater than 0.')
#                 conv_factor_check = False
#
#     return conv_factor_check


def add_csv_dict_to_abund_dict_update_puvspr2_target_files(setup_object, add_abund_dict, feat_id_list):
    setup_object.abund_pu_key_dict = add_abund_dict_to_abund_pu_key_dict(setup_object, add_abund_dict)
    make_puvspr2_dat_file(setup_object)

    if setup_object.analysis_type != 'MarxanWithZones':
        add_features_to_target_csv_file(setup_object, add_abund_dict, feat_id_list)
        setup_object.target_dict = make_target_dict(setup_object)
    else:
        zones_add_features_to_target_csv_file(setup_object, feat_id_list)
        setup_object.target_dict = make_zones_target_dict(setup_object)
        setup_object.zones_prop_dict = make_zones_prop_dict(setup_object)
        setup_object.zones_target_dict = make_zones_target_zones_dict(setup_object)
        recalc_update_zones_target_table_details(setup_object)
