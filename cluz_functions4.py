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

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFields, QgsVectorLayer, QgsVectorLayer, QgsVectorFileWriter, QgsWkbTypes, QgsFeature, QgsField, QgsSpatialIndex

from os import path, sep
from statistics import median

from .cluz_functions5 import create_bound_dat_file
from .cluz_mpsetup import make_bound_matrix_dict
from .cluz_make_file_dicts import make_abundance_pu_key_dict
from .cluz_mpfunctions import make_mp_patch_dict
from .cluz_messages import clear_progress_bar, make_progress_bar, info_message, set_progress_bar_value_complicated, set_progress_bar_value
from .cluz_mpoutputs import make_patch_area_lists


# Display distributions of conservation features #################################################
def create_distribution_map_shapefile(setup_object, dist_shape_file_path_name, selected_feat_id_list):
    dist_file_name = path.basename(dist_shape_file_path_name)
    make_base_distribution_map_shapefile(setup_object, dist_shape_file_path_name)

    distr_layer = QgsVectorLayer(dist_shape_file_path_name, dist_file_name, "ogr")
    add_pu_id_values_to_base_distribution_map_shapefile(distr_layer, selected_feat_id_list)
    abund_values_dict = dict()
    for a_value in selected_feat_id_list:
        abund_values_dict[a_value] = list()

    distr_features = distr_layer.getFeatures()
    distr_id_field_index = distr_layer.fields().indexFromName('Unit_ID')
    distr_layer.startEditing()

    progress_bar = make_progress_bar('Displaying conservation feature data')
    poly_total_count = distr_layer.featureCount()
    poly_count = 1
    for distr_feature in distr_features:
        distr_pu_row = distr_feature.id()
        distr_geom = distr_feature.geometry()
        distr_area = distr_geom.area()
        distr_attributes = distr_feature.attributes()
        distr_id = distr_attributes[distr_id_field_index]

        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        for feat_id in selected_feat_id_list:
            feat_field_index = distr_layer.fields().indexFromName('F_' + str(feat_id))
            try:
                pu_abund_dict = setup_object.abund_pu_key_dict[distr_id]
                abund_value = pu_abund_dict[feat_id]
            except KeyError:
                abund_value = 0
            a_feat_abund_value_tuple_list = abund_values_dict[feat_id]
            a_feat_abund_value_tuple_list.append((abund_value, distr_area))
            abund_values_dict[feat_id] = a_feat_abund_value_tuple_list

            distr_layer.changeAttributeValue(distr_pu_row, feat_field_index, abund_value)

    distr_layer.commitChanges()
    clear_progress_bar()
    return abund_values_dict


def make_base_distribution_map_shapefile(setup_object, dist_shape_file_path_name):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_id_field = pu_layer.fields().indexFromName('Unit_ID')
    new_fields = QgsFields()
    new_fields.append(QgsField('Unit_ID', QVariant.Int))
    dist_writer = QgsVectorFileWriter(dist_shape_file_path_name, "System", new_fields, QgsWkbTypes.MultiPolygon, pu_layer.dataProvider().crs(), "ESRI Shapefile")

    pu_features = pu_layer.getFeatures()
    # Make distribution shapefile copying PU polygons and ID field
    for puFeature in pu_features:
        pu_geom = puFeature.geometry()
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[pu_id_field]
        feat_attrib_list = [pu_id]

        dist_feat = QgsFeature()
        dist_feat.setGeometry(pu_geom)
        dist_feat.setAttributes(feat_attrib_list)
        dist_writer.addFeature(dist_feat)

    del dist_writer


def add_pu_id_values_to_base_distribution_map_shapefile(distr_layer, selected_feat_id_list):
    distr_provider = distr_layer.dataProvider()
    for aFeatID in selected_feat_id_list:
        distr_provider.addAttributes([QgsField('F_' + str(aFeatID), QVariant.Double, "double", 12, 3)])
        distr_layer.updateFields()


# Identify features in selected units #################################

def return_string_amount_per_status(setup_object, selected_pu_details_dict, status_value, feat_id):
    decimal_places = setup_object.decimal_places
    try:
        feat_amount = selected_pu_details_dict[status_value][feat_id]
        feat_amount_round = round(float(feat_amount), decimal_places)
        feat_amount_string = format(feat_amount_round, '.' + str(decimal_places) + 'f')

    except KeyError:
        feat_amount_string = '0'

    return feat_amount_string


def return_string_shortfall(setup_object, feat_id):
    decimal_places = setup_object.decimal_places
    target_amount = setup_object.target_dict[feat_id][3]
    con_amount = setup_object.target_dict[feat_id][4]
    if con_amount >= target_amount:
        string_shortfall = 'Target met'
    else:
        short_value = target_amount - con_amount
        short_value_round = round(float(short_value), decimal_places)
        string_shortfall = format(short_value_round, '.' + str(decimal_places) + 'f')

    return string_shortfall


# Calculate richness scores #########################################################

def make_feat_id_set_from_feat_type_set(setup_object, selected_type_set):
    selected_feat_id_set = set()
    for feat_id in setup_object.target_dict:
        feat_type = setup_object.target_dict[feat_id][1]
        if feat_type in selected_type_set:
            selected_feat_id_set.add(feat_id)

    return selected_feat_id_set


def produce_count_field(setup_object, count_field_name, selected_feat_id_set):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    provider = pu_layer.dataProvider()
    id_field_order = pu_layer.fields().indexFromName('Unit_ID')

    provider.addAttributes([QgsField(count_field_name, QVariant.Int)])
    pu_layer.updateFields()
    count_field_order = pu_layer.fields().indexFromName(count_field_name)

    progress_bar = make_progress_bar('Producing the feature count field')
    poly_total_count = pu_layer.featureCount()
    poly_count = 1

    count_dict = dict()
    for pu_id in setup_object.abund_pu_key_dict:
        set_progress_bar_value_complicated(progress_bar, poly_count, poly_total_count, 50, 0)
        poly_count += 1
        feat_count = 0
        pu_feat_dict = setup_object.abund_pu_key_dict[pu_id]
        for featID in pu_feat_dict:
            feat_amount = pu_feat_dict[featID]
            if feat_amount > 0 and featID in selected_feat_id_set:
                feat_count += 1
        count_dict[pu_id] = feat_count

    poly_count = 1
    pu_features = pu_layer.getFeatures()
    pu_layer.startEditing()
    for puFeature in pu_features:
        set_progress_bar_value_complicated(progress_bar, poly_count, poly_total_count, 50, 50)
        poly_count += 1

        pu_row = puFeature.id()
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[id_field_order]
        try:
            count_value = count_dict[pu_id]
        except KeyError:
            count_value = 0
        pu_layer.changeAttributeValue(pu_row, count_field_order, count_value, True)

    clear_progress_bar()
    pu_layer.commitChanges()


def produce_restricted_range_field(setup_object, range_field_name, selected_feat_id_set):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    provider = pu_layer.dataProvider()
    id_field_order = pu_layer.fields().indexFromName('Unit_ID')

    pu_id_set = set()
    pu_features = pu_layer.getFeatures()
    for puFeature in pu_features:
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[id_field_order]
        pu_id_set.add(pu_id)

    score_dict, high_score_pu_id = make_restricted_range_dict(setup_object, selected_feat_id_set, pu_id_set)

    pu_layer.startEditing()
    provider.addAttributes([QgsField(range_field_name, QVariant.Double)])
    pu_layer.updateFields()
    range_field_order = pu_layer.fields().indexFromName(range_field_name)

    progress_bar = make_progress_bar('Producing restricted range richness field')
    poly_count = 1
    poly_total_count = pu_layer.featureCount()

    pu_features = pu_layer.getFeatures()
    pu_layer.startEditing()
    for puFeature in pu_features:
        set_progress_bar_value(progress_bar, poly_count, poly_total_count)
        poly_count += 1

        pu_row = puFeature.id()
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[id_field_order]
        try:
            range_value = score_dict[pu_id]
        except KeyError:
            range_value = 0
        pu_layer.changeAttributeValue(pu_row, range_field_order, range_value, True)

    clear_progress_bar()
    pu_layer.commitChanges()


def make_restricted_range_dict(setup_object, selected_feat_id_set, pu_id_set):
    score_dict = dict()
    high_score_value = -1
    high_score_pu_id = -1

    for pu_id in pu_id_set:
        range_score = 0
        try:
            pu_feat_dict = setup_object.abund_pu_key_dict[pu_id]
        except KeyError:
            pu_feat_dict = dict()
        pu_feat_list = pu_feat_dict.keys()
        for featID in pu_feat_list:
            if featID in selected_feat_id_set:
                feat_amount = pu_feat_dict[featID]
                feat_total = setup_object.target_dict[featID][5]
                feat_score = feat_amount / feat_total
                range_score += feat_score
        score_dict[pu_id] = range_score
        if range_score > high_score_value:
            high_score_value = range_score
            high_score_pu_id = pu_id

    return score_dict, high_score_pu_id


# Make portfolio details ##########################################################################################


def make_portfolio_pu_details_dict():
    portfolio_pu_details_dict = dict()
    portfolio_pu_details_dict['status_details_bool'] = False
    portfolio_pu_details_dict['spatial_details_bool'] = False
    portfolio_pu_details_dict['sf_details_bool'] = False
    portfolio_pu_details_dict['patch_feat_details_bool'] = False
    portfolio_pu_details_dict['pe_details_bool'] = False

    return portfolio_pu_details_dict


def add_status_details_to_portfolio_dict(setup_object, portfolio_pu_details_dict):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_features = pu_layer.getFeatures()
    id_field_index = pu_layer.fields().indexFromName('Unit_ID')
    status_field_index = pu_layer.fields().indexFromName('Status')
    pu_dict, area_dict = make_pu_dict_from_cluz_portfolio(setup_object)

    running_status_dict = {'Available': [0, 0, 0], 'Conserved': [0, 0, 0], 'Earmarked': [0, 0, 0], 'Excluded': [0, 0, 0]}  # status, area, cost, PU count
    for puFeature in pu_features:
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[id_field_index]
        pu_status_text = str(pu_attributes[status_field_index])
        running_status_dict = update_portfolio_status_dict(running_status_dict, pu_dict, area_dict, pu_id, pu_status_text)

    portfolio_pu_details_dict['status_details_bool'] = True
    portfolio_pu_details_dict['status_data_dict'] = make_status_data_dict(running_status_dict)

    return portfolio_pu_details_dict


def make_pu_dict_from_cluz_portfolio(setup_object):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_features = pu_layer.getFeatures()
    id_field_index = pu_layer.fields().indexFromName('Unit_ID')
    area_field_index = pu_layer.fields().indexFromName('Area')
    cost_field_index = pu_layer.fields().indexFromName('Cost')
    status_field_index = pu_layer.fields().indexFromName('Status')

    pu_dict = dict()
    pu_status_dict = {'Available': 0, 'Conserved': 2, 'Earmarked': 2, 'Excluded': 3}

    area_dict = dict()

    for pu_feature in pu_features:
        pu_attributes = pu_feature.attributes()
        pu_id = pu_attributes[id_field_index]
        pu_area = pu_attributes[area_field_index]
        pu_cost = pu_attributes[cost_field_index]
        pu_status_text = str(pu_attributes[status_field_index])
        pu_status = pu_status_dict[pu_status_text]

        pu_dict[pu_id] = [pu_cost, pu_status]
        area_dict[pu_id] = pu_area

    return pu_dict, area_dict


def update_portfolio_status_dict(portfolio_status_dict, pu_dict, area_dict, pu_id, pu_status_text):
    pu_area = area_dict[pu_id]
    pu_cost = pu_dict[pu_id][0]
    pu_list = portfolio_status_dict[pu_status_text]
    [running_area, running_cost, running_pu_count] = pu_list
    pu_list = [running_area + pu_area, running_cost + pu_cost, running_pu_count + 1]
    portfolio_status_dict[pu_status_text] = pu_list

    return portfolio_status_dict


def make_status_data_dict(running_status_dict):
    status_data_dict = dict()
    [available_area, available_cost, available_pu_count] = running_status_dict['Available']
    [conserved_area, conserved_cost, conserved_pu_count] = running_status_dict['Conserved']
    [earmarked_area, earmarked_cost, earmarked_pu_count] = running_status_dict['Earmarked']
    [excluded_area, excluded_cost, excluded_pu_count] = running_status_dict['Excluded']

    region_area = available_area + conserved_area + earmarked_area + excluded_area
    region_cost = available_cost + conserved_cost + earmarked_cost + excluded_cost
    region_pu_count = available_pu_count + conserved_pu_count + earmarked_pu_count + excluded_pu_count

    portfolio_area = conserved_area + earmarked_area
    portfolio_cost = conserved_cost + earmarked_cost
    portfolio_pu_count = conserved_pu_count + earmarked_pu_count

    status_data_dict['Region'] = [region_area, region_cost, region_pu_count]
    status_data_dict['Portfolio'] = [portfolio_area, portfolio_cost, portfolio_pu_count]
    status_data_dict['Available'] = running_status_dict['Available']
    status_data_dict['Conserved'] = running_status_dict['Conserved']
    status_data_dict['Earmarked'] = running_status_dict['Earmarked']
    status_data_dict['Excluded'] = running_status_dict['Excluded']

    return status_data_dict


def add_spatial_details_to_portfolio_dict(setup_object, portfolio_pu_details_dict):
    pu_dict, patch_dict, dummy_zone_dict = make_patch_dict_based_on_dummy_zone_file(setup_object)
    spatial_data_dict = make_spatial_data_dict(setup_object, pu_dict, patch_dict, dummy_zone_dict)
    portfolio_pu_details_dict['spatial_details_bool'] = True
    portfolio_pu_details_dict['spatial_data_dict'] = spatial_data_dict

    return portfolio_pu_details_dict


def make_patch_dict_based_on_dummy_zone_file(setup_object):
    pu_dict, area_dict = make_pu_dict_from_cluz_portfolio(setup_object)
    minpatch_data_dict = {'area_dict': area_dict}
    bound_matrix_dict = check_make_bound_dat_file(setup_object, pu_dict)
    minpatch_data_dict['boundary_matrix_dict'] = bound_matrix_dict
    dummy_zone_dict = make_dummy_zone_dict(pu_dict)
    minpatch_data_dict['zone_dict'] = dummy_zone_dict
    patch_dict = make_mp_patch_dict(pu_dict, minpatch_data_dict)

    return pu_dict, patch_dict, dummy_zone_dict


def make_dummy_zone_dict(pu_dict):
    dummy_zone_dict = dict()
    for pu_id in pu_dict:
        dummy_zone_dict[pu_id] = [1, 0, 0]

    return dummy_zone_dict


def make_spatial_data_dict(setup_object, pu_dict, patch_dict, dummy_zone_dict):
    spatial_data_dict = dict()
    all_area_list, valid_area_list = make_patch_area_lists(patch_dict, dummy_zone_dict)  # valid_area_list is irrelevant
    all_area_list.sort()
    if len(all_area_list) > 0:
        spatial_data_dict['patchCount'] = len(all_area_list)
        spatial_data_dict['patchMedian'] = median(all_area_list)
        spatial_data_dict['patchSmallest'] = all_area_list[0]
        spatial_data_dict['patchLargest'] = all_area_list[-1]
    else:
        spatial_data_dict['patchCount'] = 0
        spatial_data_dict['patchMedian'] = 0
        spatial_data_dict['patchSmallest'] = 0
        spatial_data_dict['patchLargest'] = 0

    bound_matrix_dict = check_make_bound_dat_file(setup_object, pu_dict)
    spatial_data_dict['totalBoundLength'] = calc_total_bound_length(bound_matrix_dict, pu_dict)

    return spatial_data_dict


def check_make_bound_dat_file(setup_object, pu_dict):
    bound_dat_file_path = setup_object.input_path + sep + 'bound.dat'
    if path.exists(bound_dat_file_path):
        bound_matrix_dict = make_bound_matrix_dict(bound_dat_file_path, pu_dict)
    else:
        info_message('Creating Bound.dat file', 'CLUZ uses the Marxan bound.dat file to calculate the patch statistics. This did not exist and so has been created.')
        ext_edge_bool = False
        create_bound_dat_file(setup_object, ext_edge_bool)
        bound_matrix_dict = make_bound_matrix_dict(bound_dat_file_path, pu_dict)

    return bound_matrix_dict


def make_spatial_index_spatial_dicts(pu_layer):
    unit_id_field_index = pu_layer.dataProvider().indexFromName('Unit_ID')
    pu_polygon_dict = dict()
    pu_id_geom_dict = dict()
    spatial_index = QgsSpatialIndex()
    for aPolygon in pu_layer.getFeatures():
        pu_polygon_dict[aPolygon.id()] = aPolygon
        pu_id_geom_dict[aPolygon.attributes()[unit_id_field_index]] = aPolygon.geometry()
        spatial_index.insertFeature(aPolygon)

    return spatial_index, pu_polygon_dict, pu_id_geom_dict


def calc_total_bound_length(boundary_matrix_dict, pu_dict):
    total_bound_length = 0

    for id1Value in boundary_matrix_dict:
        pu_bound_dict = boundary_matrix_dict[id1Value]
        for id2Value in pu_bound_dict:
            if id2Value >= id1Value:
                bound_value = pu_bound_dict[id2Value]
                con_count = 0
                id1_status_value = pu_dict[id1Value][1]
                id2_status_value = pu_dict[id2Value][1]

                if id1_status_value == 1 or id1_status_value == 2:
                    con_count += 1
                if id2_status_value == 1 or id2_status_value == 2:
                    con_count += 1
                if con_count == 1:
                    total_bound_length += bound_value
                # Allow for external edges
                if con_count == 2 and id1Value == id2Value:
                    total_bound_length += bound_value

    return total_bound_length


def make_patch_feat_data_dict(setup_object, patch_dict):
    if setup_object.setup_status == 'files_checked':
        if setup_object.abund_pu_key_dict == 'blank':
            setup_object.abund_pu_key_dict = make_abundance_pu_key_dict(setup_object)

    patch_feat_data_dict = dict()
    for patch_id in patch_dict:
        patch_feat_presence_set = set()
        patch_pu_id_list = patch_dict[patch_id][2]
        for pu_id in patch_pu_id_list:
            try:
                pu_id_feat_set = set(setup_object.abund_pu_key_dict[pu_id].keys())
                patch_feat_presence_set = patch_feat_presence_set.union(pu_id_feat_set)
            except KeyError:
                pass
        for featID in patch_feat_presence_set:
            try:
                feat_count = patch_feat_data_dict[featID]
            except KeyError:
                feat_count = 0
            feat_count += 1
            patch_feat_data_dict[featID] = feat_count

    return patch_feat_data_dict


def make_full_sf_value_list(setup_object, sf_field_name):
    sf_value_list = list()
    pu_layer = QgsVectorLayer(setup_object.pu_path, "Planning units", "ogr")
    pu_features = pu_layer.getFeatures()
    sf_field_index = pu_layer.fields().indexFromName(sf_field_name)
    status_field_index = pu_layer.fields().indexFromName('Status')

    for puFeature in pu_features:
        pu_attributes = puFeature.attributes()
        pu_sf_value = pu_attributes[sf_field_index]
        if pu_sf_value >= 0:
            pu_status_text = pu_attributes[status_field_index]
            if pu_status_text == 'Available' or pu_status_text == 'Earmarked':
                sf_value_list.append(pu_sf_value)

    return sf_value_list


def make_sf_details_to_portfolio_dict(portfolio_pu_details_dict, sf_value_list, sf_runs_value):
    sf_data_dict = dict()
    sf_value_list.sort()

    zero_sf_count, greater_than_zero_count = count_sf_values_zeroes_greater_than_zero(sf_value_list)

    sf_data_dict[0] = ['Equals 0', str(zero_sf_count)]
    sf_data_dict[1] = ['Greater than 0', str(greater_than_zero_count)]
    sf_data_dict[2] = ['---', '---']

    sf_data_dict_key = 3
    sf_quartile_tuple_list = make_sf_quartile_tuple_list(sf_runs_value)
    for (range_name, min_range_value, max_range_value) in sf_quartile_tuple_list:
        sf_range_value_list = make_sf_range_value_list(sf_value_list, min_range_value, max_range_value)
        final_range_name = range_name + ': ' + str(min_range_value) + " - " + str(max_range_value)
        sf_data_dict[sf_data_dict_key] = [final_range_name, str(len(sf_range_value_list))]
        sf_data_dict_key += 1
    sf_data_dict[7] = ['---', '---']

    top5pc_value = int(sf_runs_value * 0.95)
    top5pc_value_name = "Top 5% of SF values" + ': ' + str(top5pc_value) + " - " + str(sf_runs_value)
    sf_data_dict[8] = [top5pc_value_name, str(len(make_sf_range_value_list(sf_value_list, top5pc_value, sf_runs_value)))]
    sf_data_dict[9] = ['Max SF: ' + str(sf_runs_value), str(sf_value_list.count(sf_runs_value))]

    portfolio_pu_details_dict["sf_details_bool"] = True
    portfolio_pu_details_dict["sf_data_dict"] = sf_data_dict

    return portfolio_pu_details_dict


def count_sf_values_zeroes_greater_than_zero(full_sf_value_list):
    zero_sf_count, greater_than_zero_count = 0, 0
    for a_value in full_sf_value_list:
        if a_value == 0:
            zero_sf_count += 1
        elif a_value > 0:
            greater_than_zero_count += 1

    return zero_sf_count, greater_than_zero_count


def make_sf_range_value_list(full_sf_value_list, min_range, max_range):
    sf_value_list = list()
    for aValue in full_sf_value_list:
        if max_range >= aValue >= min_range:
            sf_value_list.append(aValue)

    return sf_value_list


def make_sf_quartile_tuple_list(sf_runs_value):
    sf_quartile_tuple_list = list()
    sf_quartile_tuple_list.append(("1st Quartile", 1, int(sf_runs_value * 0.25)))
    sf_quartile_tuple_list.append(("2nd Quartile", int(sf_runs_value * 0.25) + 1, int(sf_runs_value * 0.5)))
    sf_quartile_tuple_list.append(("3rd Quartile", int(sf_runs_value * 0.5) + 1, int(sf_runs_value * 0.75)))
    sf_quartile_tuple_list.append(("4th Quartile", int(sf_runs_value * 0.75) + 1, sf_runs_value))

    return sf_quartile_tuple_list
