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
        ChangeStatusDialog.resize(390, 432)
        ChangeStatusDialog.setMinimumSize(QtCore.QSize(390, 430))
        self.logoLabel = QtGui.QLabel(ChangeStatusDialog)
        self.logoLabel.setGeometry(QtCore.QRect(10, 20, 51, 51))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo_small.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(ChangeStatusDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80, 370, 281, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.changeButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.changeButton.setObjectName(_fromUtf8("changeButton"))
        self.horizontalLayout.addWidget(self.changeButton)
        self.undoButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.undoButton.setObjectName(_fromUtf8("undoButton"))
        self.horizontalLayout.addWidget(self.undoButton)
        self.closeButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.statusGroupBox = QtGui.QGroupBox(ChangeStatusDialog)
        self.statusGroupBox.setGeometry(QtCore.QRect(80, 20, 281, 271))
        self.statusGroupBox.setTitle(_fromUtf8(""))
        self.statusGroupBox.setObjectName(_fromUtf8("statusGroupBox"))
        self.verticalLayoutWidget = QtGui.QWidget(ChangeStatusDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(90, 20, 271, 271))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.availableButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.availableButton.setChecked(True)
        self.availableButton.setObjectName(_fromUtf8("availableButton"))
        self.verticalLayout.addWidget(self.availableButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.earmarkedButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.earmarkedButton.setObjectName(_fromUtf8("earmarkedButton"))
        self.verticalLayout.addWidget(self.earmarkedButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.changeCheckBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.changeCheckBox.setObjectName(_fromUtf8("changeCheckBox"))
        self.verticalLayout.addWidget(self.changeCheckBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.conservedButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.conservedButton.setEnabled(False)
        self.conservedButton.setObjectName(_fromUtf8("conservedButton"))
        self.verticalLayout.addWidget(self.conservedButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.excludedButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.excludedButton.setEnabled(False)
        self.excludedButton.setObjectName(_fromUtf8("excludedButton"))
        self.verticalLayout.addWidget(self.excludedButton)
        self.targetsMetLabel = QtGui.QLabel(ChangeStatusDialog)
        self.targetsMetLabel.setGeometry(QtCore.QRect(90, 310, 191, 16))
        self.targetsMetLabel.setObjectName(_fromUtf8("targetsMetLabel"))

        self.retranslateUi(ChangeStatusDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ChangeStatusDialog.close)
        QtCore.QObject.connect(self.changeCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.conservedButton.setEnabled)
        QtCore.QObject.connect(self.changeCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.excludedButton.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ChangeStatusDialog)

    def retranslateUi(self, ChangeStatusDialog):
        ChangeStatusDialog.setWindowTitle(_translate("ChangeStatusDialog", "Change Status panel", None))
        self.changeButton.setText(_translate("ChangeStatusDialog", "Change", None))
        self.undoButton.setText(_translate("ChangeStatusDialog", "Undo", None))
        self.closeButton.setText(_translate("ChangeStatusDialog", "Close", None))
        self.availableButton.setText(_translate("ChangeStatusDialog", "Set as Available", None))
        self.earmarkedButton.setText(_translate("ChangeStatusDialog", "Set as Earmarked", None))
        self.changeCheckBox.setText(_translate("ChangeStatusDialog", "Allow changes\n"
"to Conserved and\n"
"Excluded status", None))
        self.conservedButton.setText(_translate("ChangeStatusDialog", "Set as Conserved", None))
        self.excludedButton.setText(_translate("ChangeStatusDialog", "Set as Excluded", None))
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

