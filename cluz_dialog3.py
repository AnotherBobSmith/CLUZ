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

from qgis.PyQt.QtWidgets import QDialog, QFileDialog

from cluz_form_remove import Ui_removeDialog

from .cluz_dialog3_code import remove_selected_features_from_target_abund_files, update_con_tot_fields_target_dict, return_con_tot_dict, create_feature_list_dict
from .cluz_make_file_dicts import update_target_csv_from_target_dict, make_abundance_pu_key_dict
from .cluz_messages import success_message


def recalc_update_target_table_details(setup_object):
    setup_object.abund_pu_key_dict = make_abundance_pu_key_dict(setup_object)
    new_con_tot_dict = return_con_tot_dict(setup_object)
    target_dict = update_con_tot_fields_target_dict(setup_object, new_con_tot_dict)

    setup_object.target_dict = target_dict
    update_target_csv_success_bool = update_target_csv_from_target_dict(setup_object, target_dict)
    if update_target_csv_success_bool:
        success_message('Target table updated: ', 'process completed.')


class RemoveDialog(QDialog, Ui_removeDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        feat_string_list, feat_string_dict = create_feature_list_dict(setup_object)
        self.featListWidget.addItems(feat_string_list)

        self.okButton.clicked.connect(lambda: self.remove_selected_features(setup_object, feat_string_dict))

    def remove_selected_features(self, setup_object, feat_string_dict):
        remove_selected_features_from_target_abund_files(self, setup_object, feat_string_dict)
