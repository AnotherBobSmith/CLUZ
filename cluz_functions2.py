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
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsApplication, QgsProcessingFeedback, QgsProcessingException

from os import sep
from csv import DictReader, reader, writer

import processing
from processing.core.Processing import Processing
Processing.initialize()

from .cluz_messages import info_message, warning_message, make_progress_bar, clear_progress_bar, set_progress_bar_value
from .cluz_make_file_dicts import remove_prefix_make_id_value, make_puvspr2_dat_file
from .cluz_make_file_dicts import add_features_to_target_csv_file, make_target_dict, make_abundance_pu_key_dict


def check_conv_factor(convert_dialog):
    conv_factor_check = True
    if convert_dialog.userRadioButton.isChecked():
        try:
            conv_factor = float(convert_dialog.convLineEdit.text())
            if conv_factor <= 0:
                convert_dialog.close()
                warning_message('Incorrect conversion value', 'The conversion value must be a number greater than 0.')
                conv_factor_check = False

        except ValueError:
            convert_dialog.close()
            warning_message('Incorrect conversion value type', 'The conversion value must be a number greater than 0.')
            conv_factor_check = False

    return conv_factor_check


def update_abund_data(setup_object, add_abund_dict, add_feat_id_list):
    if setup_object.abund_pu_key_dict == 'blank':
        setup_object.abund_pu_key_dict = make_abundance_pu_key_dict(setup_object)
    add_features_from_add_abund_dict_to_puvspr2_file(setup_object, add_abund_dict)
    setup_object.abund_pu_key_dict = make_abundance_pu_key_dict(setup_object)

    add_features_to_target_csv_file(setup_object, add_abund_dict, add_feat_id_list)
    setup_object.target_dict = make_target_dict(setup_object)


def make_vec_add_abund_dict(setup_object, layer_list, id_field_name, conv_factor):
    add_abund_dict = dict()
    add_feat_id_set = set()
    error_layer_list = list()

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')

    for aLayer in layer_list:
        layer_geom_type = aLayer.geometryType()
        layer_name = aLayer.name()
        info_message('Processing files:', 'intersecting layer ' + layer_name + '...')
        try:
            output_layer = make_intersection_output_layer(pu_layer, aLayer)

            if layer_geom_type == 1:
                add_abund_dict, add_feat_id_set = make_add_abund_dict_from_line_vec_file(setup_object, aLayer, output_layer, id_field_name, conv_factor, add_abund_dict, add_feat_id_set)
            elif layer_geom_type == 2:
                add_abund_dict, add_feat_id_set = make_add_abund_dict_from_poly_vec_file(setup_object, aLayer, output_layer, id_field_name, conv_factor, add_abund_dict, add_feat_id_set)
        except QgsProcessingException:
            error_layer_list.append(layer_name)

    add_feat_id_list = list(add_feat_id_set)
    add_feat_id_list.sort()

    return add_abund_dict, add_feat_id_list, error_layer_list


def make_intersection_output_layer(pu_layer, a_layer):
    feedback = QgsProcessingFeedback()
    intersect_params_dict = {'INPUT': a_layer, 'INPUT_FIELDS': [], 'OUTPUT': 'memory:', 'OVERLAY': pu_layer, 'OVERLAY_FIELDS': []}
    intersect_results = processing.run('native:intersection', intersect_params_dict, feedback=feedback)
    output_layer = intersect_results['OUTPUT']

    return output_layer


def make_add_abund_dict_from_line_vec_file(setup_object, a_layer, output_layer, id_field_name, conv_factor, add_abund_dict, add_feat_id_set):
    decimal_places = setup_object.decimal_places

    output_id_field = output_layer.fields().indexFromName('Unit_ID')
    output_feat_id_field = output_layer.fields().indexFromName(id_field_name)
    output_features = output_layer.getFeatures()

    attribute_feature_error = False
    for outputFeature in output_features:
        output_attributes = outputFeature.attributes()
        pu_id = output_attributes[output_id_field]
        feat_id = output_attributes[output_feat_id_field]
        add_feat_id_set.add(feat_id)

        try:
            final_shape_amount = calc_feat_line_length_in_pu(outputFeature, conv_factor, decimal_places)
        except AttributeError:
            final_shape_amount = -1

        if final_shape_amount > 0:
            pu_add_abund_dict, add_amount = check_add_dict_amount_values(add_abund_dict, pu_id, feat_id)
            add_amount += final_shape_amount
            pu_add_abund_dict[feat_id] = add_amount
            add_abund_dict[pu_id] = pu_add_abund_dict
        else:
            attribute_feature_error = True

    if attribute_feature_error:
        warning_message('Layer warning: ', 'layer ' + str(a_layer.name()) + ' contains at least one feature that produces fragments with no spatial characteristics when intersected with the planning units.')

    return add_abund_dict, add_feat_id_set


def make_add_abund_dict_from_poly_vec_file(setup_object, a_layer, output_layer, id_field_name, conv_factor, add_abund_dict, add_feat_id_set):
    decimal_places = setup_object.decimal_places

    output_id_field = output_layer.fields().indexFromName('Unit_ID')
    output_feat_id_field = output_layer.fields().indexFromName(id_field_name)
    output_features = output_layer.getFeatures()

    attribute_feature_error = False
    for outputFeature in output_features:
        output_attributes = outputFeature.attributes()
        pu_id = output_attributes[output_id_field]
        feat_id = output_attributes[output_feat_id_field]
        add_feat_id_set.add(feat_id)

        try:
            final_shape_amount = calc_feat_polygon_area_in_pu(outputFeature, conv_factor, decimal_places)
        except AttributeError:
            final_shape_amount = -1
      
        if final_shape_amount > 0:
            pu_add_abund_dict, add_amount = check_add_dict_amount_values(add_abund_dict, pu_id, feat_id)
            add_amount += final_shape_amount
            pu_add_abund_dict[feat_id] = add_amount
            add_abund_dict[pu_id] = pu_add_abund_dict
        else:
            attribute_feature_error = True

    if attribute_feature_error:
        warning_message('Layer warning: ', 'layer ' + str(a_layer.name()) + ' contains at least one feature that produces fragments with no spatial characteristics when intersected with the planning units.')

    return add_abund_dict, add_feat_id_set


def check_add_dict_amount_values(add_abund_dict, pu_id, feat_id):
    try:
        pu_add_abund_dict = add_abund_dict[pu_id]
    except KeyError:
        pu_add_abund_dict = dict()
    try:
        add_amount = pu_add_abund_dict[feat_id]
    except KeyError:
        add_amount = 0

    return pu_add_abund_dict, add_amount


def calc_feat_line_length_in_pu(output_feature, conv_factor, decimal_places):
    output_geom = output_feature.geometry()
    intersect_shape_amount = output_geom.length()
    shape_amount = intersect_shape_amount / conv_factor
    final_shape_amount = round(shape_amount, decimal_places)

    return final_shape_amount


def calc_feat_polygon_area_in_pu(output_feature, conv_factor, decimal_places):
    output_geom = output_feature.geometry()
    intersect_shape_amount = output_geom.area()
    shape_amount = intersect_shape_amount / conv_factor
    final_shape_amount = round(shape_amount, decimal_places)

    return final_shape_amount

# Import raster file ########################################################################################


def make_raster_add_abund_dict(setup_object, layer_list, conv_factor):
    add_abund_dict = dict()
    add_feat_id_set = set()
    error_layer_list = list()
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')

    for aLayer in layer_list:
        layer_name = aLayer.name()
        layer_pixel_width = aLayer.rasterUnitsPerPixelX()
        layer_pixel_height = aLayer.rasterUnitsPerPixelY()
        layer_pixel_area = layer_pixel_width * layer_pixel_height
        info_message('Processing files:', 'calculating Zonal Histogram with ' + layer_name + '...')
        try:
            output_layer = make_zonal_histogram_output_layer(pu_layer, aLayer)
            output_zonal_histogram_feat_id_field_list = make_zonal_histogram_output_feat_id_field_list(output_layer)
            raster_values_are_valid_bool = check_raster_values_are_valid_bool(output_zonal_histogram_feat_id_field_list)
            if raster_values_are_valid_bool:
                add_abund_dict, add_feat_id_set = make_add_abund_dict_from_raster_file(setup_object, output_layer, add_abund_dict, add_feat_id_set, conv_factor, layer_pixel_area, output_zonal_histogram_feat_id_field_list)
            else:
                error_layer_list.append(layer_name)
        except QgsProcessingException:
            error_layer_list.append('ZonalHistogram failed')

    add_feat_id_list = list(add_feat_id_set)
    add_feat_id_list.sort()

    return add_abund_dict, add_feat_id_list, error_layer_list


def make_zonal_histogram_output_layer(pu_layer, a_layer):
    feedback = QgsProcessingFeedback()
    zonal_histogram_params_dict = {'INPUT_RASTER': a_layer,
                                'RASTER_BAND': 1,
                                'INPUT_VECTOR': pu_layer,
                                'COLUMN_PREFIX': 'ClZHi_',
                                'OUTPUT': 'TEMPORARY_OUTPUT'}
    zonal_histogram_results = processing.run('native:zonalhistogram', zonal_histogram_params_dict, feedback=feedback)
    output_layer = zonal_histogram_results['OUTPUT']

    return output_layer


def make_zonal_histogram_output_feat_id_field_list(output_layer):
    output_zonal_histogram_feat_id_field_list = list()
    provider = output_layer.dataProvider()
    field_list = provider.fields()
    for aField in field_list:
        field_name = aField.name()
        if field_name[0:6] == 'ClZHi_':
            if field_name != 'ClZHi_0' and field_name != 'ClZHi_NODATA':
                output_zonal_histogram_feat_id_field_list.append(field_name)

    return output_zonal_histogram_feat_id_field_list


def check_raster_values_are_valid_bool(output_zonal_histogram_feat_id_field_list):
    raster_values_are_valid_bool = True

    for feat_id_field_name in output_zonal_histogram_feat_id_field_list:
        feat_id_string = feat_id_field_name.replace('ClZHi_', '')
        try:
            feat_id = int(feat_id_string)
            if feat_id < 0:
                raster_values_are_valid_bool = False
        except ValueError:
            raster_values_are_valid_bool = False
    if raster_values_are_valid_bool is False:
        warning_message('Invalid values in raster layer', 'The raster layer values must all be positive integers (Zero values are ignored) so data has been ignored.')

    return raster_values_are_valid_bool


def make_add_abund_dict_from_raster_file(setup_object, output_layer, add_abund_dict, add_feat_id_set, conv_factor, layer_pixel_area, output_zonal_histogram_feat_id_field_list):
    decimal_places = setup_object.decimal_places
    output_id_field = output_layer.fields().indexFromName('Unit_ID')
    output_features = output_layer.getFeatures()

    for outputFeature in output_features:
        output_attributes = outputFeature.attributes()
        unit_id = output_attributes[output_id_field]
        for featIDFieldName in output_zonal_histogram_feat_id_field_list:
            output_feat_field = output_layer.fields().indexFromName(featIDFieldName)
            feat_id = int(featIDFieldName.replace('ClZHi_', ''))
            add_feat_id_set.add(feat_id)
            raw_feat_amount = output_attributes[output_feat_field] * layer_pixel_area
            final_feat_amount = round(raw_feat_amount / conv_factor, decimal_places)
            if final_feat_amount > 0:
                try:
                    pu_add_abund_dict = add_abund_dict[unit_id]
                except KeyError:
                    pu_add_abund_dict = dict()
                pu_add_abund_dict[feat_id] = final_feat_amount
                add_abund_dict[unit_id] = pu_add_abund_dict

    return add_abund_dict, add_feat_id_set


# Import csv file ###################################################################################

def make_csv_add_abund_dict(convert_csv_dialog, setup_object):
    csv_file_path = convert_csv_dialog.csvFileLineEdit.text()
    conv_factor = float(convert_csv_dialog.convLineEdit.text())
    raw_unit_id_field_name = convert_csv_dialog.idfieldComboBox.currentText()
    add_abund_dict = dict()
    feat_id_list = list()
    continue_bool = True
    unit_id_field_name = str(raw_unit_id_field_name)  # Removes u from beginning of string

    csv_file = open(csv_file_path, 'rt')
    abund_data_reader = reader(csv_file)
    file_header_list = next(abund_data_reader)
    file_header_list.remove(unit_id_field_name)
    feat_header_dict = dict()
    for aFeatHeader in file_header_list:
        feat_id = remove_prefix_make_id_value(aFeatHeader)
        feat_header_dict[aFeatHeader] = feat_id
        feat_id_list.append(feat_id)

    if len(set(feat_id_list).intersection(set(setup_object.target_dict.keys()))) != 0:
        warning_message('Duplicate features', 'The feature ID values in the table duplicate some of those in the abundance table. This process will terminate.')
        continue_bool = False
    if feat_id_list.count('') != 0:
        warning_message('Missing ID code', 'One of the fields containing abundance data in the specified table does not contain any numerical characters and so does not specify the feature ID. This process will terminate.')
        continue_bool = False

    if continue_bool:
        add_abund_dict = make_add_abund_dict_from_csv_file(csv_file_path, feat_header_dict, file_header_list, unit_id_field_name, conv_factor)

    return add_abund_dict, feat_id_list, continue_bool


def make_add_abund_dict_from_csv_file(csv_file_path, feat_header_dict, file_header_list, unit_id_field_name, conv_factor):
    add_abund_dict = dict()
    with open(csv_file_path, 'rt') as f:
        data_dict = DictReader(f)
        for aDict in data_dict:
            pu_id = int(aDict[unit_id_field_name])
            for aHeader in file_header_list:
                orig_abund_value = float(aDict[aHeader])
                abund_value = orig_abund_value / conv_factor
                feat_id = feat_header_dict[aHeader]
                if abund_value > 0:
                    try:
                        pu_add_abund_dict = add_abund_dict[pu_id]
                    except KeyError:
                        pu_add_abund_dict = dict()
                    try:
                        add_amount = pu_add_abund_dict[feat_id]
                    except KeyError:
                        add_amount = 0
                    add_amount += abund_value
                    pu_add_abund_dict[feat_id] = add_amount
                    add_abund_dict[pu_id] = pu_add_abund_dict

    return add_abund_dict


def add_abund_dict_to_abund_pu_key_dict(setup_object, add_abund_dict):
    abund_pu_key_dict = setup_object.abund_pu_key_dict
    for pu_id in add_abund_dict:
        pu_add_abund_dict = add_abund_dict[pu_id]
        try:
            pu_abund_dict = setup_object.abund_pu_key_dict[pu_id]
        except KeyError:
            pu_abund_dict = dict()
        for a_feat in pu_add_abund_dict:
            a_amount = pu_add_abund_dict[a_feat]
            pu_abund_dict[a_feat] = a_amount

        abund_pu_key_dict[pu_id] = pu_abund_dict

    return abund_pu_key_dict


def add_features_from_add_abund_dict_to_puvspr2_file(setup_object, add_abund_dict):
    for pu_id in add_abund_dict:
        pu_add_abund_dict = add_abund_dict[pu_id]
        try:
            pu_abund_dict = setup_object.abund_pu_key_dict[pu_id]
        except KeyError:
            pu_abund_dict = dict()
        for feat_id in pu_add_abund_dict:
            pu_abund_dict[feat_id] = pu_add_abund_dict[feat_id]
        setup_object.abund_pu_key_dict[pu_id] = pu_abund_dict

    make_puvspr2_dat_file(setup_object)


def create_target_puvspr2_files(create_dialog):
    input_path = create_dialog.inputLineEdit.text()
    target_path = create_dialog.targetLineEdit.text()

    with open(target_path, 'w', newline='', encoding='utf-8') as targetFile:
        target_writer = writer(targetFile)
        target_writer.writerow(['Id', 'Name', 'Type', 'Target', 'Spf', 'Ear+Cons', 'Total', 'PC_target'])

    with open(input_path + sep + 'puvspr2.dat', 'w', newline='', encoding='utf-8') as puvspr2File:
        puvspr2_writer = writer(puvspr2File)
        puvspr2_writer.writerow(['species', 'pu', 'amount'])


def create_pu_layer(create_dialog):
    cost_as_area_bool = create_dialog.equalCheckBox.isChecked()
    conv_factor = float(create_dialog.convLineEdit.text())
    shape_path = create_dialog.puLineEdit.text()
    
    create_target_puvspr2_files(create_dialog)

    pu_layer = QgsVectorLayer(shape_path, 'Shapefile', 'ogr')
    pu_provider = pu_layer.dataProvider()
    pu_provider.addAttributes([QgsField('Unit_ID', QVariant.Int)])
    pu_provider.addAttributes([QgsField('Area', QVariant.Double, 'real', 10, 2)])
    pu_provider.addAttributes([QgsField('Cost', QVariant.Double, 'real', 10, 2)])
    pu_provider.addAttributes([QgsField('Status', QVariant.String)])
    pu_layer.updateFields()

    unit_id_field_index = pu_provider.fieldNameIndex('Unit_ID')
    pu_area_field_index = pu_provider.fieldNameIndex('Area')
    pu_cost_field_index = pu_provider.fieldNameIndex('Cost')
    status_field_index = pu_provider.fieldNameIndex('Status')

    progress_bar = make_progress_bar('Processing shapefile')
    poly_count = 1
    poly_total_count = pu_layer.featureCount()

    pu_layer.startEditing()
    pu_features = pu_layer.getFeatures()
    for puFeature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_row = puFeature.id()
        unit_id_value = pu_row + 1
        pu_geom = puFeature.geometry()
        pu_area = pu_geom.area()
        final_pu_area = pu_area / conv_factor
        if cost_as_area_bool:
            pu_cost = final_pu_area
        else:
            pu_cost = 0

        pu_layer.changeAttributeValue(pu_row, unit_id_field_index, unit_id_value, True)
        pu_layer.changeAttributeValue(pu_row, pu_cost_field_index, pu_cost, True)
        pu_layer.changeAttributeValue(pu_row, pu_area_field_index, final_pu_area, True)
        pu_layer.changeAttributeValue(pu_row, status_field_index, 'Available', True)

    clear_progress_bar()
    pu_layer.commitChanges()
