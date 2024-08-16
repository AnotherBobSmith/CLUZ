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

from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QApplication

from cluz_form_zones_identify_selected import Ui_zonesIdentifySelectedDialog

from .cluz_shared import copy_table_contents_to_clipboard


from .zcluz_dialog4_code import zones_make_selected_avail_ear_excl_lock_dict
from .zcluz_dialog4_code import zones_add_selected_identify_data_to_table_widget
from .zcluz_dialog4_code import zones_add_formatting_headings_to_table_widget
from .zcluz_dialog4_code import zones_return_selected_pu_details_dict


class ZonesIdentifySelectedDialog(QDialog, Ui_zonesIdentifySelectedDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()

        selected_total_ear_lock_dict = zones_make_selected_avail_ear_excl_lock_dict(setup_object)
        selected_pu_details_dict = zones_return_selected_pu_details_dict(selected_total_ear_lock_dict)
        selected_pu_count = len(selected_total_ear_lock_dict)

        self.zones_show_selected_identify_data(setup_object, selected_pu_details_dict, selected_pu_count)

    def zones_show_selected_identify_data(self, setup_object, zones_selected_pu_details_dict, selected_pu_count):
        if len(zones_selected_pu_details_dict) > 0:
            self.zonesIdentifySelectedTableWidget.clear()
            column_count_value = 5 + (2 * len(setup_object.zones_dict))
            self.zonesIdentifySelectedTableWidget.setColumnCount(column_count_value)
            zones_add_selected_identify_data_to_table_widget(self, setup_object, zones_selected_pu_details_dict)
            zones_add_formatting_headings_to_table_widget(self, setup_object)
            self.setWindowTitle('Details of ' + str(selected_pu_count) + ' planning units.')
        else:
            self.setWindowTitle('No planning units selected')

    def keyPressEvent(self, e):
        widget_name = 'zonesIdentifySelectedTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)
