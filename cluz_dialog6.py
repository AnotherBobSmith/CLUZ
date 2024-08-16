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
from cluz_form_minpatch import Ui_minpatchDialog

from .cluz_setup import MinPatchObject

from .cluz_mpmain import run_min_patch
from .cluz_mpsetup import make_minpatch_data_dict
from .cluz_messages import warning_message
from .cluz_dialog6_code import make_marxan_file_list, check_min_patch_file, check_min_patch_blm_value, check_minpatch_selected_items_list


class MinpatchDialog(QDialog, Ui_minpatchDialog):
    def __init__(self, iface, setup_object):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        input_text = 'Marxan input folder: ' + setup_object.input_path
        self.inputLabel.setText(input_text)
        output_text = 'Marxan output folder: ' + setup_object.output_path
        self.outputLabel.setText(output_text)

        self.blmLineEdit.setText('0')

        marxan_file_list = make_marxan_file_list(setup_object)
        if len(marxan_file_list) > 0:
            self.fileListWidget.addItems(marxan_file_list)
        else:
            self.startButton.setEnabled(False)
            warning_message('No files found', 'The specified Marxan output folder does not contain any individual portfolio files that can be analysed in MinPatch.')

        self.browseButton.clicked.connect(self.set_minpatch_detail_file)
        self.startButton.clicked.connect(lambda: self.start_minpatch(setup_object))

    def set_minpatch_detail_file(self):
        (minpatch_detail_path_name_text, file_type_details_text) = QFileDialog.getOpenFileName(self, 'Select MinPatch details file', '*.dat')
        self.detailsLineEdit.setText(minpatch_detail_path_name_text)

    def start_minpatch(self, setup_object):
        minpatch_object = MinPatchObject()
        run_min_patch_bool, minpatch_object = check_min_patch_file(self, minpatch_object)
        run_min_patch_bool, minpatch_object = check_min_patch_blm_value(self, minpatch_object, run_min_patch_bool)
        run_min_patch_bool, minpatch_object = check_minpatch_selected_items_list(self, minpatch_object, run_min_patch_bool)

        minpatch_object.removeBool = self.removeCheckBox.isChecked()
        minpatch_object.addBool = self.addCheckBox.isChecked()
        minpatch_object.whittleBool = self.whittleCheckBox.isChecked()

        if run_min_patch_bool:
            minpatch_data_dict, setup_ok_bool = make_minpatch_data_dict(setup_object, minpatch_object)
            self.close()
            if setup_ok_bool:
                run_min_patch(setup_object, minpatch_object, minpatch_data_dict)
