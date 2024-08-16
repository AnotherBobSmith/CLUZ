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

from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog, QTableWidgetItem
from qgis.gui import QgsMapTool
from qgis.core import *

from os import path
import sys

from .cluz_dialog7_code import load_marxan_results_met_dialog, load_abund_select_feature_list, set_identify_dialog_window_title, add_target_table_data
from .cluz_dialog7_code import add_identify_data_to_table_widget, undo_status_of_pu_layer_update_target_table, return_point_pu_id_list, change_status_of_pu_layer_update_target_table
from .cluz_dialog7_code import load_abund_dict_data, make_identify_data, make_zones_target_table_title_text
from .cluz_display import update_pu_layer_to_show_changes_by_shifting_extent, make_pu_layer_active
from .cluz_functions7 import return_targets_met_tuple
from .cluz_make_file_dicts import make_target_dict, make_target_dialog_row_list
from .cluz_shared import copy_table_contents_to_clipboard

from .zcluz_make_file_dicts import make_zones_target_dict


sys.path.append(path.dirname(path.abspath(__file__)) + "/forms")
from cluz_form_target import Ui_targetDialog
from cluz_form_abund_select import Ui_abundSelectDialog
from cluz_form_abund import Ui_abundDialog
from cluz_form_met import Ui_metDialog
from cluz_form_change import Ui_ChangeStatusDialog
from cluz_form_identify import Ui_identifyDialog


# Target table #################################################


class TargetDialog(QDialog, Ui_targetDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        if setup_object.analysis_type != 'MarxanWithZones':
            target_dict = make_target_dict(setup_object)
            target_dialog_row_list, numeric_cols_list = make_target_dialog_row_list(setup_object)
            if target_dict != 'blank':
                setup_object.target_dict = target_dict
                setup_object.target_dialog_row_list = target_dialog_row_list
                setup_object.numeric_cols_list = numeric_cols_list
                self.load_target_dict_data(setup_object)
        else:
            zones_target_table_title_text = make_zones_target_table_title_text(setup_object)
            self.setWindowTitle(zones_target_table_title_text)

            target_dict = make_zones_target_dict(setup_object)
            target_dialog_row_list, numeric_cols_list = make_target_dialog_row_list(setup_object)
            if target_dict != 'blank':
                setup_object.target_dict = target_dict
                setup_object.target_dialog_row_list = target_dialog_row_list
                setup_object.numeric_cols_list = numeric_cols_list
                self.load_target_dict_data(setup_object)

    def load_target_dict_data(self, setup_object):
        add_target_table_data(self, setup_object)

    def keyPressEvent(self, e):
        widget_name = 'targetTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)


# Abund table ###########################################################


class AbundSelectDialog(QDialog, Ui_abundSelectDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        feat_string_dict = load_abund_select_feature_list(self, setup_object)
        self.okButton.clicked.connect(lambda: self.display_abund_values(setup_object, feat_string_dict))

    def display_abund_values(self, setup_object, feat_string_dict):
        selected_feat_id_list = [feat_string_dict[item.text()] for item in self.featListWidget.selectedItems()]
        if len(selected_feat_id_list) == 0:
            selected_feat_id_list = setup_object.target_dict.keys()
        self.close()

        self.abundDialog = AbundDialog(self, setup_object, selected_feat_id_list)
        self.abundDialog.show()
        self.abundDialog.exec_()


class AbundDialog(QDialog, Ui_abundDialog):
    def __init__(self, iface, setup_object, selected_feat_id_list):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        load_abund_dict_data(self, setup_object, selected_feat_id_list)

    def keyPressEvent(self, e):
        widget_name = 'abundTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)


class IdentifyTool(QgsMapTool):
    def __init__(self, canvas, setup_object):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.setup_object = setup_object

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def canvasReleaseEvent(self, event):
        # Get the click
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

        self.identifyDialog = IdentifyDialog(self, self.setup_object, point)
        # show the dialog
        self.identifyDialog.show()
        # Run the dialog event loop
        self.identifyDialog.exec_()

    def activate(self):
        self.canvas.setCursor(Qt.CrossCursor)

    def deactivate(self):
        self.canvas.setCursor(Qt.ArrowCursor)

        # Close the identify dialog if it's open
        if self.identifyDialog is not None:
            self.identifyDialog.close()

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


class MetDialog(QDialog, Ui_metDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()
        load_marxan_results_met_dialog(self, setup_object)
        self.setWindowTitle('Marxan Targets Met table for analysis ' + setup_object.output_name)


    def keyPressEvent(self, e):
        widget_name = 'metTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)


class ChangeStatusDialog(QDialog, Ui_ChangeStatusDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.iface = iface
        self.setupUi(self)

        make_pu_layer_active()
        targets_met_count, target_count = return_targets_met_tuple(setup_object)
        self.targetsMetLabel.setText("Targets met: " + str(targets_met_count) + " of " + str(target_count))
        self.undoButton.setEnabled(False)
        self.changeButton.clicked.connect(lambda: self.change_status(setup_object))
        self.undoButton.clicked.connect(lambda: self.undo_status_change(setup_object))

    def change_status(self, setup_object):
        change_status_of_pu_layer_update_target_table(self, setup_object)

    def undo_status_change(self, setup_object):
        undo_status_of_pu_layer_update_target_table(self, setup_object)
        update_pu_layer_to_show_changes_by_shifting_extent()


class IdentifyDialog(QDialog, Ui_identifyDialog):
    def __init__(self, iface, setup_object, point):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.clip = QApplication.clipboard()

        selected_pu_id_list = return_point_pu_id_list(setup_object, point)
        ident_dict, target_met_dict = make_identify_data(setup_object, selected_pu_id_list)
        title_string = set_identify_dialog_window_title(selected_pu_id_list, ident_dict)

        if len(ident_dict.keys()) > 0:
            self.identDict = ident_dict
            self.targetMetDict = target_met_dict
            self.show_identify_data(setup_object)
            self.setWindowTitle(title_string)

        self.setWindowTitle(title_string)

    def show_identify_data(self, setup_object):
        self.identifyTableWidget.clear()
        self.identifyTableWidget.setColumnCount(7)
        add_identify_data_to_table_widget(self.identifyTableWidget, setup_object, self.targetMetDict, self.identDict)

        header_list = ['ID ', 'Name ', 'Amount ', 'As % of total ', 'Target ', 'As % of target ', '% of target currently met ']
        self.identifyTableWidget.setHorizontalHeaderLabels(header_list)
        for aColValue in range(len(header_list)):
            self.identifyTableWidget.resizeColumnToContents(aColValue)

    def keyPressEvent(self, e):
        widget_name = 'identifyTableWidget'
        copy_table_contents_to_clipboard(self, widget_name, e)
