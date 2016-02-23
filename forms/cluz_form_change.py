# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_change.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ChangeStatusDialog(object):
    def setupUi(self, ChangeStatusDialog):
        ChangeStatusDialog.setObjectName(_fromUtf8("ChangeStatusDialog"))
        ChangeStatusDialog.setWindowModality(QtCore.Qt.WindowModal)
        ChangeStatusDialog.resize(320, 340)
        ChangeStatusDialog.setMinimumSize(QtCore.QSize(320, 340))
        self.changeButton = QtGui.QPushButton(ChangeStatusDialog)
        self.changeButton.setGeometry(QtCore.QRect(70, 300, 75, 23))
        self.changeButton.setObjectName(_fromUtf8("changeButton"))
        self.undoButton = QtGui.QPushButton(ChangeStatusDialog)
        self.undoButton.setGeometry(QtCore.QRect(150, 300, 75, 23))
        self.undoButton.setObjectName(_fromUtf8("undoButton"))
        self.statusGroupBox = QtGui.QGroupBox(ChangeStatusDialog)
        self.statusGroupBox.setGeometry(QtCore.QRect(80, 10, 191, 221))
        self.statusGroupBox.setTitle(_fromUtf8(""))
        self.statusGroupBox.setObjectName(_fromUtf8("statusGroupBox"))
        self.availableButton = QtGui.QRadioButton(self.statusGroupBox)
        self.availableButton.setGeometry(QtCore.QRect(20, 20, 161, 17))
        self.availableButton.setChecked(True)
        self.availableButton.setObjectName(_fromUtf8("availableButton"))
        self.statusButtonGroup = QtGui.QButtonGroup(ChangeStatusDialog)
        self.statusButtonGroup.setObjectName(_fromUtf8("statusButtonGroup"))
        self.statusButtonGroup.addButton(self.availableButton)
        self.earmarkedButton = QtGui.QRadioButton(self.statusGroupBox)
        self.earmarkedButton.setGeometry(QtCore.QRect(20, 50, 161, 17))
        self.earmarkedButton.setObjectName(_fromUtf8("earmarkedButton"))
        self.statusButtonGroup.addButton(self.earmarkedButton)
        self.conservedButton = QtGui.QRadioButton(self.statusGroupBox)
        self.conservedButton.setEnabled(False)
        self.conservedButton.setGeometry(QtCore.QRect(20, 160, 161, 17))
        self.conservedButton.setObjectName(_fromUtf8("conservedButton"))
        self.statusButtonGroup.addButton(self.conservedButton)
        self.excludedButton = QtGui.QRadioButton(self.statusGroupBox)
        self.excludedButton.setEnabled(False)
        self.excludedButton.setGeometry(QtCore.QRect(20, 190, 161, 17))
        self.excludedButton.setObjectName(_fromUtf8("excludedButton"))
        self.statusButtonGroup.addButton(self.excludedButton)
        self.changeCheckBox = QtGui.QCheckBox(self.statusGroupBox)
        self.changeCheckBox.setGeometry(QtCore.QRect(20, 80, 101, 31))
        self.changeCheckBox.setText(_fromUtf8(""))
        self.changeCheckBox.setObjectName(_fromUtf8("changeCheckBox"))
        self.checkLabel = QtGui.QLabel(self.statusGroupBox)
        self.checkLabel.setGeometry(QtCore.QRect(40, 80, 131, 61))
        self.checkLabel.setLineWidth(1)
        self.checkLabel.setObjectName(_fromUtf8("checkLabel"))
        self.closeButton = QtGui.QPushButton(ChangeStatusDialog)
        self.closeButton.setGeometry(QtCore.QRect(230, 300, 75, 23))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.targetsMetLabel = QtGui.QLabel(ChangeStatusDialog)
        self.targetsMetLabel.setGeometry(QtCore.QRect(80, 250, 191, 16))
        self.targetsMetLabel.setObjectName(_fromUtf8("targetsMetLabel"))
        self.logoLabel = QtGui.QLabel(ChangeStatusDialog)
        self.logoLabel.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo_small.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))

        self.retranslateUi(ChangeStatusDialog)
        QtCore.QObject.connect(self.changeCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.conservedButton.setEnabled)
        QtCore.QObject.connect(self.changeCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.excludedButton.setEnabled)
        QtCore.QObject.connect(self.changeCheckBox, QtCore.SIGNAL(_fromUtf8("clicked()")), self.availableButton.toggle)
        QtCore.QMetaObject.connectSlotsByName(ChangeStatusDialog)

    def retranslateUi(self, ChangeStatusDialog):
        ChangeStatusDialog.setWindowTitle(_translate("ChangeStatusDialog", "Change Status panel", None))
        self.changeButton.setText(_translate("ChangeStatusDialog", "Change", None))
        self.undoButton.setText(_translate("ChangeStatusDialog", "Undo", None))
        self.availableButton.setText(_translate("ChangeStatusDialog", "Set as Available", None))
        self.earmarkedButton.setText(_translate("ChangeStatusDialog", "Set as Earmarked", None))
        self.conservedButton.setText(_translate("ChangeStatusDialog", "Set as Conserved", None))
        self.excludedButton.setText(_translate("ChangeStatusDialog", "Set as Excluded", None))
        self.checkLabel.setText(_translate("ChangeStatusDialog", "Allow changes\n"
"to Conserved and\n"
"Excluded status", None))
        self.closeButton.setText(_translate("ChangeStatusDialog", "Close", None))
        self.targetsMetLabel.setText(_translate("ChangeStatusDialog", "Targets met: X of Y", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ChangeStatusDialog = QtGui.QDialog()
    ui = Ui_ChangeStatusDialog()
    ui.setupUi(ChangeStatusDialog)
    ChangeStatusDialog.show()
    sys.exit(app.exec_())

