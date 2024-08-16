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

from qgis.core import QgsProject, QgsVectorLayer, QgsCategorizedSymbolRenderer, QgsFillSymbol, QgsRendererCategory
from qgis.core import QgsRendererRange, QgsGraduatedSymbolRenderer, QgsCoordinateReferenceSystem, QgsRectangle
from qgis.core import QgsClassificationEqualInterval
from qgis.utils import iface

from os import path, sep


def make_pu_layer_active():
    try:
        pu_layer = QgsProject.instance().mapLayersByName('Planning units')[0]
        iface.setActiveLayer(pu_layer)
    except IndexError:
        pass


def return_lowest_unused_file_name_number(dir_path, file_name_base, ext_type_text):
    file_name_number = 1
    while path.exists(dir_path + sep + file_name_base + str(file_name_number) + ext_type_text):
        file_name_number += 1

    return file_name_number


def remove_then_add_pu_layer(setup_object, add_layer_fudge):  # This is a way of refreshing PU Layer, so it shows newly added fields; addLayerFudge copes with QGIS not counting newly added layers
    iface.mapCanvas().refreshAllLayers()
    all_layers = iface.mapCanvas().layers()
    pu_layer_position_in_toc = -1
    position_in_toc = 0
    for aLayer in all_layers:
        if aLayer.name() == 'Planning units':
            pu_layer = aLayer
            QgsProject.instance().removeMapLayers([pu_layer.id()])
            iface.mapCanvas().refresh()
            pu_layer_position_in_toc = position_in_toc
        position_in_toc += 1
    if pu_layer_position_in_toc > -1:
        pu_layer_position_in_toc += add_layer_fudge
        add_pu_layer(setup_object, pu_layer_position_in_toc)


def add_pu_layer(setup_object, legend_position):
    root = QgsProject.instance().layerTreeRoot()
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_layer_renderer = make_pu_layer_renderer(setup_object)
    pu_layer.setRenderer(pu_layer_renderer)

    QgsProject.instance().addMapLayer(pu_layer, False)
    root.insertLayer(legend_position, pu_layer)
    set_pu_layer_active_crs_zoom_refresh(pu_layer)


def make_pu_layer_renderer(setup_object):
    category_list = make_pu_layer_legend_category(setup_object)
    my_renderer = QgsCategorizedSymbolRenderer('', category_list)
    my_renderer.setClassAttribute('Status')

    return my_renderer


def set_pu_layer_active_crs_zoom_refresh(pu_layer):
    iface.setActiveLayer(pu_layer)
    layer_crs_text = pu_layer.crs().authid()
    layer_crs = QgsCoordinateReferenceSystem(layer_crs_text)
    iface.mapCanvas().setDestinationCrs(layer_crs)
    iface.mapCanvas().zoomToFeatureExtent(pu_layer.extent())
    iface.mapCanvas().refresh()


def update_pu_layer_to_show_changes_by_shifting_extent():  # This refreshes PU Layer, so it displays changes in values
    canvas_extent = iface.mapCanvas().extent()
    ext_min_x, ext_max_x = canvas_extent.xMinimum(), canvas_extent.xMaximum()
    ext_min_y, ext_max_y = canvas_extent.yMinimum(), canvas_extent.yMaximum()
    x_shift = (ext_max_x - ext_min_x) * 0.0001
    shift_min_x, shift_max_x = ext_min_x + x_shift, ext_max_x + x_shift
    iface.mapCanvas().setExtent(QgsRectangle(shift_min_x, ext_min_y, shift_max_x, ext_max_y))
    iface.mapCanvas().refresh()


def make_pu_layer_legend_category(setup_object):
    category_list = list()
    if setup_object.analysis_type == 'Marxan':
        cat1_value_label = 'Available'
        cat1_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#99ff99', 'color_border': '#99ff99'})
        cat2_value_label = 'Earmarked'
        cat2_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#33cc33', 'color_border': '#33cc33'})
        cat3_value_label = 'Conserved'
        cat3_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#006633', 'color_border': '#006633'})
        cat4_value_label = 'Excluded'
        cat4_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#730083', 'color_border': '#730083'})
    else:
        cat1_value_label = 'Locked'
        cat1_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#006633', 'color_border': '#006633'})
        cat2_value_label = 'Excluded'
        cat2_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#730083', 'color_border': '#730083'})
        cat3_value_label = 'Unassigned'
        cat3_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#d9ffd9', 'color_border': '#d9ffd9'})
        cat4_value_label = 'Earmarked'
        cat4_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#33cc33', 'color_border': '#33cc33'})

    my_cat1 = QgsRendererCategory(cat1_value_label, cat1_symbol, cat1_value_label)
    category_list.append(my_cat1)
    my_cat2 = QgsRendererCategory(cat2_value_label, cat2_symbol, cat2_value_label)
    category_list.append(my_cat2)
    my_cat3 = QgsRendererCategory(cat3_value_label, cat3_symbol, cat3_value_label)
    category_list.append(my_cat3)
    my_cat4 = QgsRendererCategory(cat4_value_label, cat4_symbol, cat4_value_label)
    category_list.append(my_cat4)

    return category_list


def display_distribution_maps(setup_object, dist_shape_file_path_name, abund_values_dict, legend_type, selected_feat_id_list):
    colour_dict = make_colour_dict()
    colour_key = 1

    for featID in selected_feat_id_list:
        range_list = list()
        colour_list = colour_dict[colour_key]
        colour_key += 1
        if colour_key > len(list(colour_dict.keys())):
            colour_key = 1

        a_dist_layer_name = setup_object.target_dict[int(featID)][0]
        a_dist_layer = QgsVectorLayer(dist_shape_file_path_name, a_dist_layer_name, 'ogr')
        a_dist_layer_field_name = 'F_' + str(featID)
        a_feat_abund_value_tuple_list = abund_values_dict[featID]
        if legend_type == 'equal_interval':
            legend_val_cat_list = calc_equal_interval_legend_classes(setup_object, a_feat_abund_value_tuple_list)
        else:
            legend_val_cat_list = calc_equal_area_legend_classes(setup_object, a_feat_abund_value_tuple_list)
        for aValue in range(0, 5):
            min_value = legend_val_cat_list[aValue]
            max_value = legend_val_cat_list[aValue + 1]
            my_colour = colour_list[aValue]
            my_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': my_colour, 'color_border': my_colour})
            the_range = QgsRendererRange(min_value, max_value, my_symbol, str(min_value) + ' - ' + str(max_value))
            range_list.insert(0, the_range)

        my_renderer = QgsGraduatedSymbolRenderer('', range_list)
        my_renderer.setClassificationMethod(QgsClassificationEqualInterval())
        my_renderer.setClassAttribute(a_dist_layer_field_name)
        a_dist_layer.setRenderer(my_renderer)
        a_dist_layer.setOpacity(0.6)
        QgsProject.instance().addMapLayer(a_dist_layer)

    iface.mapCanvas().refresh()


def make_colour_dict():
    colour_dict = dict()
    colour_dict[1] = ['#FEE1E1', '#FE8787', '#FF0000', '#AE0000', '#630000']
    colour_dict[2] = ['#FEEEE1', '#FEBC87', '#FE8828', '#D15D00', '#863C00']
    colour_dict[3] = ['#FEFAE1', '#FEEC87', '#FEDD28', '#D1B100', '#867100']
    colour_dict[4] = ['#F6FEE1', '#DCFE87', '#C1FE28', '#95D100', '#608600']
    colour_dict[5] = ['#E1FEFE', '#87FEFE', '#28FEFE', '#00D6D6', '#009A9A']
    colour_dict[6] = ['#E6FEE6', '#88FE87', '#00FF00', '#02A900', '#015400']
    colour_dict[7] = ['#E1FEF5', '#87FEDA', '#28FEBD', '#00D192', '#00865D']
    colour_dict[8] = ['#E1E1FE', '#8789FE', '#282CFE', '#0004D1', '#000286']
    colour_dict[9] = ['#FAD7FE', '#F587FE', '#DD00EF', '#A500B3', '#5C0063']
    colour_dict[10] = ['#FEE1F6', '#FE87DE', '#FE28C4', '#D10098', '#860062']
    colour_dict[11] = ['#F5F5F5', '#B9B9B9', '#7D7D7D', '#414141', '#000000']
    colour_dict[12] = ['#FFEABE', '#E0B986', '#BC865D', '#8B5445', '#5A2D2D']

    return colour_dict


def calc_equal_interval_legend_classes(setup_object, a_feat_abund_value_tuple_list):
    decimal_places = setup_object.decimal_places
    abund_list = list()
    for aTuple in a_feat_abund_value_tuple_list:
        abund_value = aTuple[0]
        if abund_value > 0:
            abund_list.append(abund_value)

    if len(abund_list) > 0:
        min_value = min(abund_list)
        min_value = round(float(min_value), decimal_places)
        max_value = max(abund_list)
        max_value = round(float(max_value), decimal_places)
    else:
        min_value = 0
        max_value = 0

    inc_value = (max_value - min_value) / 5
    no2_value = round(min_value + (1 * inc_value), decimal_places)
    no3_value = round(min_value + (2 * inc_value), decimal_places)
    no4_value = round(min_value + (3 * inc_value), decimal_places)
    no5_value = round(min_value + (4 * inc_value), decimal_places)

    legend_val_cat_list = [min_value, no2_value, no3_value, no4_value, no5_value, max_value]

    return legend_val_cat_list


def calc_equal_area_legend_classes(setup_object, a_feat_abund_value_tuple_list):
    decimal_places = setup_object.decimal_places
    total_area, abund_list = make_abund_values_list(a_feat_abund_value_tuple_list)
    min_value, max_value = calc_equal_area_legend_classes_min_max(abund_list)
    min_value = round(float(min_value), decimal_places)
    max_value = round(float(max_value), decimal_places)

    abund_tuple_list = make_abund_tuple_list(a_feat_abund_value_tuple_list, abund_list)
    combined_area_dict = make_combined_area_dict(abund_tuple_list)

    abund_value_list = list(combined_area_dict.keys())
    abund_value_list.sort()
    running_total_area = 0
    legend_value1 = 'blank'
    legend_value2 = 'blank'
    legend_value3 = 'blank'
    legend_value4 = 'blank'
    for aValue in abund_value_list:
        area_amount = combined_area_dict[aValue]
        area_amount = round(float(area_amount), decimal_places)
        running_total_area += area_amount
        running_prop = running_total_area / total_area
        if legend_value1 == 'blank' and running_prop >= 0.2:
            legend_value1 = aValue
        if legend_value2 == 'blank' and running_prop >= 0.4:
            legend_value2 = aValue
        if legend_value3 == 'blank' and running_prop >= 0.6:
            legend_value3 = aValue
        if legend_value4 == 'blank' and running_prop >= 0.8:
            legend_value4 = aValue

    legend_val_cat_list = [min_value, legend_value1, legend_value2, legend_value3, legend_value4, max_value]

    return legend_val_cat_list


def calc_equal_area_legend_classes_min_max(abund_list):
    if len(abund_list) > 0:
        min_value = abund_list[0]
        max_value = abund_list[-1]
    else:
        min_value = 0
        max_value = 0

    return min_value, max_value


def make_abund_values_list(a_feat_abund_value_tuple_list):
    abund_list = list()
    total_area = 0
    for aTuple in a_feat_abund_value_tuple_list:
        abund_value = aTuple[0]
        if abund_value > 0:
            abund_list.append(aTuple[0])
            total_area += aTuple[1]
    abund_list.sort()

    return total_area, abund_list


def make_abund_tuple_list(a_feat_abund_value_tuple_list, abund_list):
    abund_tuple_list = list()
    while len(abund_list) > 0:
        abund_value = abund_list.pop(0)
        for aTuple in a_feat_abund_value_tuple_list:
            if aTuple[0] == abund_value:
                abund_tuple_list.append(aTuple)
                a_feat_abund_value_tuple_list.remove(aTuple)

    return abund_tuple_list


def make_combined_area_dict(abund_tuple_list):
    combined_area_dict = dict()
    for bTuple in abund_tuple_list:
        (bAmount, bArea) = bTuple
        try:
            running_area = combined_area_dict[bAmount]
        except KeyError:
            running_area = 0
        running_area += bArea
        combined_area_dict[bAmount] = running_area

    return combined_area_dict


def display_best_output(setup_object, best_field_name, best_shapefile_name):
    best_layer = QgsVectorLayer(setup_object.pu_path, best_shapefile_name, 'ogr')

    category_list = list()
    # Set category 1
    cat1_value = 'Selected'
    cat1_label = 'Selected'
    cat1_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#ff00ff', 'color_border': '#ff00ff'})
    my_cat1 = QgsRendererCategory(cat1_value, cat1_symbol, cat1_label)
    category_list.append(my_cat1)

    my_renderer = QgsCategorizedSymbolRenderer('', category_list)
    my_renderer.setClassAttribute(best_field_name)
    best_layer.setRenderer(my_renderer)
    QgsProject.instance().addMapLayer(best_layer)

    iface.mapCanvas().refresh()


def reload_pu_layer(setup_object):
    root = QgsProject.instance().layerTreeRoot()
    layers = QgsProject.instance().mapLayers()
    name_list = []
    for QGISFullname, layer in layers.items():
        layer_name = str(layer.name())
        name_list.insert(0, layer_name)
        if layer_name == 'Planning units':
            QgsProject.instance().removeMapLayer(layer.id())
    pu_layer_position = name_list.index('Planning units')

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_layer_renderer = make_pu_layer_renderer(setup_object)
    pu_layer.setRenderer(pu_layer_renderer)
    QgsProject.instance().addMapLayer(pu_layer, False)
    root.insertLayer(pu_layer_position, pu_layer)


def remove_previous_marxan_layers():
    layers = QgsProject.instance().mapLayers()
    for QGISFullname, layer in layers.items():
        layer_name = layer.name()
        if 'Best (' in layer_name or 'SF_Score (' in layer_name or ' SF (' in layer_name:
            QgsProject.instance().removeMapLayer(layer.id())


def remove_previous_min_patch_layers():
    layers = QgsProject.instance().mapLayers()
    for QGISFullname, layer in layers.items():
        layer_name = layer.name()
        if str(layer_name)[0:9] == 'MP Best (' or str(layer_name)[0:13] == 'MP SF_Score (':
            QgsProject.instance().removeMapLayer(layer.id())


def display_graduated_layer(setup_object, field_name, layer_name, legend_code):
    colour_dict = dict()
    colour_dict[1] = ['#C5C2C5', '#CDCEB4', '#DEDEA3', '#EEE894', '#FFFA8B', '#FFE273', '#FFAA52', '#FF8541', '#FF6D31', '#FF0000']
    colour_dict[2] = ['#FFFFCC', '#E3F3B5', '#C8E89E', '#A9DB8E', '#88CD80', '#68BE70', '#48AE60', '#2B9C50', '#158243', '#006837']

    colour_list = colour_dict[legend_code]

    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    graduated_layer = QgsVectorLayer(setup_object.pu_path, layer_name, 'ogr')
    provider = pu_layer.dataProvider()

    pu_features = pu_layer.getFeatures()
    graduated_field_order = provider.fieldNameIndex(field_name)

    max_count_score = 0  # This will be used to set highest value in legend
    for puFeature in pu_features:
        pu_attributes = puFeature.attributes()
        pu_count_score = pu_attributes[graduated_field_order]
        if pu_count_score > max_count_score:
            max_count_score = pu_count_score

    range_list = make_graduated_layer_range_list(setup_object, colour_list, max_count_score)
    my_sf_renderer = make_my_sf_renderer(range_list, field_name)
    graduated_layer.setRenderer(my_sf_renderer)
    QgsProject.instance().addMapLayer(graduated_layer)

    iface.mapCanvas().refresh()


def make_graduated_layer_range_list(setup_object, colour_list, max_count_score):
    range_list = list()
    min_value = 0
    inc_value = float(max_count_score) / 10

    for a_value in range(0, 10):
        max_value = min_value + inc_value
        if a_value == 9:
            max_value = max_count_score
        my_colour = colour_list[a_value]
        my_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': my_colour, 'color_border': my_colour})
        min_value_display = round(min_value, setup_object.decimal_places)
        max_value_display = round(min_value + inc_value, setup_object.decimal_places)
        the_range = QgsRendererRange(min_value_display, max_value_display, my_symbol, str(min_value_display) + ' - ' + str(max_value_display))
        min_value = max_value
        range_list.insert(0, the_range)

    return range_list


def make_my_sf_renderer(range_list, field_name):
    my_renderer = QgsGraduatedSymbolRenderer('', range_list)
    my_renderer.setClassificationMethod(QgsClassificationEqualInterval())
    my_renderer.setClassAttribute(field_name)

    return my_renderer
