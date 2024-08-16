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

from qgis.core import QgsVectorLayer, NULL

from csv import reader

from .cluz_messages import clear_progress_bar, make_progress_bar, set_progress_bar_value


def check_zones_fields_target_csv_file(setup_object):
    target_csv_file_path = setup_object.target_path

    with open(target_csv_file_path, 'rt') as f:
        count_reader = reader(f)
        row_total_count = len(list(count_reader))

    progress_bar = make_progress_bar('Processing target file')
    row_count = 1

    with open(target_csv_file_path, 'rt') as f:
        target_reader = reader(f)
        orig_header_list = next(target_reader)
        header_list = list()  # convert to lowercase so it doesn't matter whether the headers or lowercase, uppercase or a mix
        for aHeader in orig_header_list:
            header_list.append(aHeader.lower())

        target_error_set = set()
        for aRow in target_reader:
            set_progress_bar_value(progress_bar, row_count, row_total_count)
            row_count += 1
            for zoneID in setup_object.zones_dict:
                prop_zone_name_string = 'z' + str(zoneID) + '_prop'
                target_zone_name_string = 'z' + str(zoneID) + '_target'
                earlock_zone_name_string = 'z' + str(zoneID) + '_ear+lock'

                prop_zone_string = aRow[header_list.index(prop_zone_name_string)]
                target_zone_string = aRow[header_list.index(target_zone_name_string)]
                earlock_zone_string = aRow[header_list.index(earlock_zone_name_string)]

                target_error_set = check_zone_prop_string(prop_zone_string, target_error_set)
                target_error_set = check_zone_feat_target_string(target_zone_string, target_error_set)
                target_error_set = check_zone_feat_ear_lock_string(earlock_zone_string, target_error_set)

    clear_progress_bar()

    return target_error_set


def check_zone_prop_string(prop_zone_string, error_set):
    if prop_zone_string == '':
        error_set.add('featZonePropBlank')
    else:
        try:
            float(prop_zone_string)
            if float(prop_zone_string) < 0:
                error_set.add('featZonePropNotFloat')
        except ValueError:
            error_set.add('featZonePropNotFloat')

    return error_set


def check_zone_feat_target_string(target_zone_string, error_set):
    if target_zone_string == '':
        error_set.add('featZoneTargetBlank')
    else:
        try:
            float(target_zone_string)
            if float(target_zone_string) < 0:
                error_set.add('featZoneTargetNotFloat')
        except ValueError:
            error_set.add('featZoneTargetNotFloat')

    return error_set


def check_zone_feat_ear_lock_string(earlock_zone_string, error_set):
    if earlock_zone_string == '':
        error_set.add('featZoneEarLockBlank')
    else:
        try:
            float(earlock_zone_string)
            if float(earlock_zone_string) < 0:
                error_set.add('featZoneEarLockNotFloat')
        except ValueError:
            error_set.add('featZoneEarLockNotFloat')

    return error_set


def zones_check_pu_shape_file_pu_status_value(shape_error_set, pu_attributes, unit_status_field):
    pu_status = pu_attributes[unit_status_field]
    if pu_status not in ['Unassigned', 'Earmarked', 'Excluded', 'Locked']:
        shape_error_set.add('puZonesStatusWrong')

    return shape_error_set


def check_zones_field_status_list_for_conflicts(shape_error_set, zones_field_status_list):
    if zones_field_status_list.count('Locked') > 1:
        shape_error_set.add('puZonesStatusConflict')

    return shape_error_set
