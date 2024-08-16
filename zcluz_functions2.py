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

from os import sep
from csv import writer

from processing.core.Processing import Processing
Processing.initialize()


# Transform to Marxan with Zones ###################################################

def create_zones_pu_layer(setup_object, zones_transform_object):
    pu_layer = QgsVectorLayer(setup_object.pu_path, 'Planning units', 'ogr')
    pu_id_field = pu_layer.fields().indexFromName('Unit_ID')
    pu_area_field = pu_layer.fields().indexFromName('Area')

    zones_pu_layer_path_name = zones_transform_object.transformFolderPath + sep + zones_transform_object.puLayerName + '.shp'
    new_fields = QgsFields()
    new_fields.append(QgsField('Unit_ID', QVariant.Int))
    new_fields.append(QgsField('Area', QVariant.Double, 'double', 12, setup_object.decimal_places))
    for zoneID in range(1, zones_transform_object.zoneNum + 1):
        new_fields.append(QgsField('Z' + str(zoneID) + '_Cost', QVariant.Double, 'double', 12, setup_object.decimal_places))
        new_fields.append(QgsField('Z' + str(zoneID) + '_Status', QVariant.String))

    shapefile_writer = QgsVectorFileWriter(zones_pu_layer_path_name, 'System', new_fields, QgsWkbTypes.MultiPolygon, pu_layer.dataProvider().crs(), 'ESRI Shapefile')
    pu_features = pu_layer.getFeatures()
    # Make distribution shapefile copying PU polygons and ID field
    for puFeature in pu_features:
        pu_geom = puFeature.geometry()
        pu_attributes = puFeature.attributes()
        pu_id = pu_attributes[pu_id_field]
        pu_area = pu_attributes[pu_area_field]
        pu_zone_data_list = [0, 'Unassigned'] * zones_transform_object.zoneNum
        feat_attrib_list = [pu_id, pu_area] + pu_zone_data_list

        dist_feat = QgsFeature()
        dist_feat.setGeometry(pu_geom)
        dist_feat.setAttributes(feat_attrib_list)
        shapefile_writer.addFeature(dist_feat)

    del shapefile_writer


def convert_old_to_new_target_dict(setup_object, zone_num):
    zone_target_dict = dict()
    for feat_id in setup_object.target_dict:
        [old_feat_name, old_feat_type, old_feat_spf, old_feat_target, old_feat_earcon, old_feat_total, old_feat_pc_target] = setup_object.target_dict[feat_id]
        new_feat_list = [old_feat_name, old_feat_type] + ([1.0] * zone_num) + [old_feat_spf] + ([0.0] * zone_num) + [old_feat_target] + ([0.0] * zone_num) + [0] + [old_feat_total] + [0]
        zone_target_dict[feat_id] = new_feat_list

    return zone_target_dict


def create_zone_target_csv_file(zone_target_dict, zones_transform_object):
    transform_target_csv_file_path = zones_transform_object.transformFolderPath + sep + zones_transform_object.zonesTargetCSVFileName + '.csv'
    feat_id_list = list(zone_target_dict.keys())
    zone_target_csv_file_header_list = create_zone_target_csv_file_header_list(zones_transform_object.zoneNum)

    with open(transform_target_csv_file_path, 'w', newline='', encoding='utf-8') as out_file:
        target_writer = writer(out_file)
        target_writer.writerow(zone_target_csv_file_header_list)
        for featID in feat_id_list:
            text_list = [featID] + zone_target_dict[featID]
            target_writer.writerow(text_list)


def create_zone_target_csv_file_header_list(zone_num):
    zone_target_csv_file_header_list = ['Id', 'Name', 'Type']
    for zoneID in range(1, zone_num + 1):
        zone_target_csv_file_header_list.append('Z' + str(zoneID) + '_Prop')
    zone_target_csv_file_header_list = zone_target_csv_file_header_list + ['Spf']
    for zoneID in range(1, zone_num + 1):
        zone_target_csv_file_header_list.append('Z' + str(zoneID) + '_Target')
    zone_target_csv_file_header_list = zone_target_csv_file_header_list + ['Target']
    for zoneID in range(1, zone_num + 1):
        zone_target_csv_file_header_list.append('Z' + str(zoneID) + '_Ear+Lock')
    zone_target_csv_file_header_list = zone_target_csv_file_header_list + ['Ear+Lock', 'Total', 'PC_Target']

    return zone_target_csv_file_header_list


def create_zone_zones_csv_file(zones_transform_object):
    transform_zones_csv_file_path = zones_transform_object.transformFolderPath + sep + zones_transform_object.zonesZonesCSVFileName + '.csv'

    with open(transform_zones_csv_file_path, 'w', newline='', encoding='utf-8') as out_file:
        target_writer = writer(out_file)
        target_writer.writerow(['Id', 'Name'])
        for zone_id in range(1, zones_transform_object.zoneNum + 1):
            text_list = [str(zone_id), 'Blank']
            target_writer.writerow(text_list)


# Import Vec data #########################################################################

def update_zones_prop_dict_for_added_features(setup_object, add_feat_id_list):
    for featID in add_feat_id_list:
        for zoneID in setup_object.zones_dict:
            setup_object.zones_prop_dict[zoneID][featID] = 1

    return setup_object.zones_prop_dict
