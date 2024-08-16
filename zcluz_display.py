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
from qgis.utils import iface

from .cluz_display import make_graduated_layer_range_list, make_my_sf_renderer, make_pu_layer_legend_category
from .cluz_display import set_pu_layer_active_crs_zoom_refresh


def add_zones_pu_layers(setup_object, legend_position):
    all_layers = iface.mapCanvas().layers()
    layer_name_list = list()
    for aLayer in all_layers:
        layer_name_list.append(aLayer.name)

    root = QgsProject.instance().layerTreeRoot()
    for zoneID in list(setup_object.zones_dict)[::-1]:
        zone_pu_layer_name = 'Z' + str(zoneID) + ' ' + setup_object.zones_dict[zoneID] + ' Planning units'
        status_field = 'Z' + str(zoneID) + '_Status'

        if not QgsProject.instance().mapLayersByName(zone_pu_layer_name):
            pu_layer = QgsVectorLayer(setup_object.pu_path, zone_pu_layer_name, 'ogr')
            category_list = make_pu_layer_legend_category(setup_object)
            my_renderer = QgsCategorizedSymbolRenderer('', category_list)
            my_renderer.setClassAttribute(status_field)
            pu_layer.setRenderer(my_renderer)

            QgsProject.instance().addMapLayer(pu_layer, False)
            root.insertLayer(legend_position, pu_layer)
            set_pu_layer_active_crs_zoom_refresh(pu_layer)

            # iface.setActiveLayer(pu_layer)
            #
            # layer_crs_text = pu_layer.crs().authid()
            # layer_crs = QgsCoordinateReferenceSystem(layer_crs_text)
            # iface.mapCanvas().setDestinationCrs(layer_crs)
            # iface.mapCanvas().zoomToFeatureExtent(pu_layer.extent())
            # iface.mapCanvas().refresh()


def check_zones_pu_layer_present(setup_object):
    all_layers = iface.mapCanvas().layers()
    pu_layer_present_bool = True
    zone_pu_name_list = list()
    for zoneID in setup_object.zones_dict:
        zone_pu_layer_name = 'Z' + str(zoneID) + ' ' + setup_object.zones_dict[zoneID] + ' Planning units'
        zone_pu_name_list.append(zone_pu_layer_name)

    zones_layer_count = 0
    for aLayer in all_layers:
        if aLayer.name() in zone_pu_name_list:
            zones_layer_count += 1
            zone_pu_name_list.remove(aLayer.name())

    if zones_layer_count != 3:
        pu_layer_present_bool = False

    return pu_layer_present_bool


# def make_zones_pu_layer_legend_category():
#     category_list = []
#     # Set category 1
#     cat1_value = 'Locked'
#     cat1_label = 'Locked'
#     cat1_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#006633', 'color_border': '#006633'})
#     my_cat1 = QgsRendererCategory(cat1_value, cat1_symbol, cat1_label)
#     category_list.append(my_cat1)
#
#     # Set category 2
#     cat2_value = 'Excluded'
#     cat2_label = 'Excluded'
#     cat2_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#730083', 'color_border': '#730083'})
#     my_cat2 = QgsRendererCategory(cat2_value, cat2_symbol, cat2_label)
#     category_list.append(my_cat2)
#
#     # Set category 3
#     cat3_value = 'Unassigned'
#     cat3_label = 'Unassigned'
#     cat3_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#d9ffd9', 'color_border': '#d9ffd9'})
#     my_cat3 = QgsRendererCategory(cat3_value, cat3_symbol, cat3_label)
#     category_list.append(my_cat3)
#
#     # Set category 4
#     cat4_value = 'Earmarked'
#     cat4_label = 'Earmarked'
#     cat4_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': '#33cc33', 'color_border': '#33cc33'})
#     my_cat4 = QgsRendererCategory(cat4_value, cat4_symbol, cat4_label)
#     category_list.append(my_cat4)

    return category_list


def display_zones_best_output(setup_object, best_layer_name, zones_best_field_name):
    best_zones_layer = QgsVectorLayer(setup_object.pu_path, best_layer_name, 'ogr')

    category_list = list()
    zone_id_list = list(setup_object.zones_dict)
    zone_id_list.sort()

    for zone_id in setup_object.zones_dict:
        cat_label = 'Zone ' + str(zone_id) + ' ' + setup_object.zones_dict[zone_id]
        cat_symbol = return_zone_cat_symbol(list(setup_object.zones_dict).index(zone_id))
        my_cat = QgsRendererCategory(zone_id, cat_symbol, cat_label)
        category_list.append(my_cat)

    my_renderer = QgsCategorizedSymbolRenderer('', category_list)

    my_renderer.setClassAttribute(zones_best_field_name)
    best_zones_layer.setRenderer(my_renderer)
    QgsProject.instance().addMapLayer(best_zones_layer)

    iface.mapCanvas().refresh()


def return_zone_cat_symbol(zone_id):
    colour_dict = {0: '#c05000', 1: '#ffb070', 2: '#d0e0ff', 3: '#33a02c', 4: '#fb9a99', 5: '#e31a1c'}
    if zone_id < 6:
        cat_colour = colour_dict[zone_id]
    else:
        cat_colour = '#e6e6e6'
    cat_symbol = QgsFillSymbol.createSimple({'style': 'solid', 'color': cat_colour, 'color_border': cat_colour})

    return cat_symbol


def reload_zones_pu_layer(setup_object):
    root = QgsProject.instance().layerTreeRoot()

    layers = QgsProject.instance().mapLayers()
    name_list = list()
    for QGISFullname, layer in layers.items():
        layer_name = str(layer.name())
        name_list.insert(0, layer_name)
        if layer_name.endswith('Planning units'):
            QgsProject.instance().removeMapLayer(layer.id())

    for zoneID in list(setup_object.zones_dict):
        pu_layer_position = name_list.index('Z' + str(zoneID) + ' ' + setup_object.zones_dict[zoneID] + ' Planning units')
        pu_layer = QgsVectorLayer(setup_object.pu_path, 'Z' + str(zoneID) + ' ' + setup_object.zones_dict[zoneID] + ' Planning units', 'ogr')
        category_list = make_pu_layer_legend_category(setup_object)
        my_renderer = QgsCategorizedSymbolRenderer('', category_list)
        my_renderer.setClassAttribute('Z' + str(zoneID) + '_Status')
        pu_layer.setRenderer(my_renderer)

        QgsProject.instance().addMapLayer(pu_layer, False)
        root.insertLayer(pu_layer_position, pu_layer)


def display_zones_sf_layer(setup_object, run_number, output_name, field_name_prefix, field_name_suffix):
    colour_list = ['#C5C2C5', '#CDCEB4', '#DEDEA3', '#EEE894', '#FFFA8B', '#FFE273', '#FFAA52', '#FF8541', '#FF6D31', '#FF0000']

    for zoneID in list(setup_object.zones_dict)[::-1]:
        zone_layer_name = str(zoneID) + ' ' + setup_object.zones_dict[zoneID] + ' SF' + ' (' + output_name + ')'
        graduated_layer = QgsVectorLayer(setup_object.pu_path, zone_layer_name, 'ogr')
        field_name = field_name_prefix + str(zoneID) + field_name_suffix

        range_list = make_graduated_layer_range_list(setup_object, colour_list, run_number)
        my_sf_renderer = make_my_sf_renderer(range_list, field_name)
        graduated_layer.setRenderer(my_sf_renderer)
        QgsProject.instance().addMapLayer(graduated_layer)

    iface.mapCanvas().refresh()
