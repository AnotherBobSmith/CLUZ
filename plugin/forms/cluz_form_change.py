# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_change.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChangeStatusDialog(object):
    def setupUi(self, ChangeStatusDialog):
        ChangeStatusDialog.setObjectName("ChangeStatusDialog")
        ChangeStatusDialog.setMinimumSize(QtCore.QSize(300, 400))
        self.gridLayout = QtWidgets.QGridLayout(ChangeStatusDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logoLabel = QtWidgets.QLabel(ChangeStatusDialog)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap(":/logos/images/marxan_logo.png"))
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.logoLabel.setObjectName("logoLabel")
        self.horizontalLayout_2.addWidget(self.logoLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(ChangeStatusDialog)
        self.frame.setMinimumSize(QtCore.QSize(100, 300))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 271, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.availableButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.availableButton.setChecked(True)
        self.availableButton.setObjectName("availableButton")
        self.verticalLayout.addWidget(self.availableButton)
        self.earmarkedButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.earmarkedButton.setObjectName("earmarkedButton")
        self.verticalLayout.addWidget(self.earmarkedButton)
        self.changeCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.changeCheckBox.setObjectName("changeCheckBox")
        self.verticalLayout.addWidget(self.changeCheckBox)
        self.conservedButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.conservedButton.setEnabled(False)
        self.conservedButton.setObjectName("conservedButton")
        self.verticalLayout.addWidget(self.conservedButton)
        self.excludedButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.excludedButton.setEnabled(False)
        self.excludedButton.setObjectName("excludedButton")
        self.verticalLayout.addWidget(self.excludedButton)
        self.verticalLayout_2.addWidget(self.frame)
        self.targetsMetLabel = QtWidgets.QLabel(ChangeStatusDialog)
        self.targetsMetLabel.setObjectName("targetsMetLabel")
        self.verticalLayout_2.addWidget(self.targetsMetLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.changeButton = QtWidgets.QPushButton(ChangeStatusDialog)
        self.changeButton.setObjectName("changeButton")
        self.horizontalLayout.addWidget(self.changeButton)
        self.undoButton = QtWidgets.QPushButton(ChangeStatusDialog)
        self.undoButton.setObjectName("undoButton")
        self.horizontalLayout.addWidget(self.undoButton)
        self.closeButton = QtWidgets.QPushButton(ChangeStatusDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(ChangeStatusDialog)
        self.closeButton.clicked.connect(ChangeStatusDialog.close)
        self.changeCheckBox.clicked['bool'].connect(self.conservedButton.setEnabled)
        self.changeCheckBox.clicked['bool'].connect(self.excludedButton.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ChangeStatusDialog)

    def retranslateUi(self, ChangeStatusDialog):
        _translate = QtCore.QCoreApplication.translate
        ChangeStatusDialog.setWindowTitle(_translate("ChangeStatusDialog", "Change Status panel"))
        self.availableButton.setText(_translate("ChangeStatusDialog", "Set as Available"))
        self.earmarkedButton.setText(_translate("ChangeStatusDialog", "Set as Earmarked"))
        self.changeCheckBox.setText(_translate("ChangeStatusDialog", "Allow changes\n"
"to Conserved and\n"
"Excluded status"))
        self.conservedButton.setText(_translate("ChangeStatusDialog", "Set as Conserved"))
        self.excludedButton.setText(_translate("ChangeStatusDialog", "Set as Excluded"))
        self.targetsMetLabel.setText(_translate("ChangeStatusDialog", "Targets met: X of Y"))
        self.changeButton.setText(_translate("ChangeStatusDialog", "Change"))
        self.undoButton.setText(_translate("ChangeStatusDialog", "Undo"))
        self.closeButton.setText(_translate("ChangeStatusDialog", "Close"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChangeStatusDialog = QtWidgets.QDialog()
    ui = Ui_ChangeStatusDialog()
    ui.setupUi(ChangeStatusDialog)
    ChangeStatusDialog.show()
    sys.exit(app.exec_())

