# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_create.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_createDialog(object):
    def setupUi(self, createDialog):
        createDialog.setObjectName("createDialog")
        createDialog.setMinimumSize(QtCore.QSize(760, 450))
        self.gridLayout = QtWidgets.QGridLayout(createDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.logoLabel = QtWidgets.QLabel(createDialog)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap(":/logos/images/setup_logo_panel.png"))
        self.logoLabel.setObjectName("logoLabel")
        self.horizontalLayout_6.addWidget(self.logoLabel)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.puLabel = QtWidgets.QLabel(createDialog)
        self.puLabel.setObjectName("puLabel")
        self.verticalLayout.addWidget(self.puLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.puLineEdit = QtWidgets.QLineEdit(createDialog)
        self.puLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.puLineEdit.setMaxLength(32766)
        self.puLineEdit.setObjectName("puLineEdit")
        self.horizontalLayout_2.addWidget(self.puLineEdit)
        self.puButton = QtWidgets.QPushButton(createDialog)
        self.puButton.setMinimumSize(QtCore.QSize(0, 24))
        self.puButton.setObjectName("puButton")
        self.horizontalLayout_2.addWidget(self.puButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.convLabel = QtWidgets.QLabel(createDialog)
        self.convLabel.setMinimumSize(QtCore.QSize(111, 16))
        self.convLabel.setObjectName("convLabel")
        self.horizontalLayout_3.addWidget(self.convLabel)
        self.convLineEdit = QtWidgets.QLineEdit(createDialog)
        self.convLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.convLineEdit.setObjectName("convLineEdit")
        self.horizontalLayout_3.addWidget(self.convLineEdit)
        self.convHintLabel2 = QtWidgets.QLabel(createDialog)
        self.convHintLabel2.setMinimumSize(QtCore.QSize(171, 16))
        self.convHintLabel2.setTextFormat(QtCore.Qt.RichText)
        self.convHintLabel2.setObjectName("convHintLabel2")
        self.horizontalLayout_3.addWidget(self.convHintLabel2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.equalCheckBox = QtWidgets.QCheckBox(createDialog)
        self.equalCheckBox.setMinimumSize(QtCore.QSize(401, 24))
        self.equalCheckBox.setObjectName("equalCheckBox")
        self.verticalLayout.addWidget(self.equalCheckBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.inputLabel = QtWidgets.QLabel(createDialog)
        self.inputLabel.setObjectName("inputLabel")
        self.verticalLayout.addWidget(self.inputLabel)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.inputLineEdit = QtWidgets.QLineEdit(createDialog)
        self.inputLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.inputLineEdit.setObjectName("inputLineEdit")
        self.horizontalLayout_4.addWidget(self.inputLineEdit)
        self.inputButton = QtWidgets.QPushButton(createDialog)
        self.inputButton.setMinimumSize(QtCore.QSize(0, 24))
        self.inputButton.setObjectName("inputButton")
        self.horizontalLayout_4.addWidget(self.inputButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.targetLabel = QtWidgets.QLabel(createDialog)
        self.targetLabel.setObjectName("targetLabel")
        self.verticalLayout.addWidget(self.targetLabel)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.targetLineEdit = QtWidgets.QLineEdit(createDialog)
        self.targetLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.targetLineEdit.setObjectName("targetLineEdit")
        self.horizontalLayout_5.addWidget(self.targetLineEdit)
        self.targetButton = QtWidgets.QPushButton(createDialog)
        self.targetButton.setMinimumSize(QtCore.QSize(0, 24))
        self.targetButton.setObjectName("targetButton")
        self.horizontalLayout_5.addWidget(self.targetButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem5)
        self.okButton = QtWidgets.QPushButton(createDialog)
        self.okButton.setMinimumSize(QtCore.QSize(0, 24))
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem6)
        self.cancelButton = QtWidgets.QPushButton(createDialog)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 24))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_6.addItem(spacerItem8)
        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)

        self.retranslateUi(createDialog)
        self.cancelButton.clicked.connect(createDialog.close)
        QtCore.QMetaObject.connectSlotsByName(createDialog)

    def retranslateUi(self, createDialog):
        _translate = QtCore.QCoreApplication.translate
        createDialog.setWindowTitle(_translate("createDialog", "Create CLUZ files for Marxan"))
        self.puLabel.setText(_translate("createDialog", "Select shapefile that will be used to produce the planning unit layer"))
        self.puButton.setText(_translate("createDialog", "Browse"))
        self.convLabel.setText(_translate("createDialog", "Area conversion factor"))
        self.convHintLabel2.setText(_translate("createDialog", "<html><head/><body><p>10000 to convert m2 to ha</p><p>1000000 to convert m2 to km2</p></body></html>"))
        self.equalCheckBox.setText(_translate("createDialog", "Set cost layer as equal to planning unit area"))
        self.inputLabel.setText(_translate("createDialog", "Specify input folder where puvspr2.dat file will be created"))
        self.inputButton.setText(_translate("createDialog", "Browse"))
        self.targetLabel.setText(_translate("createDialog", "Name of target table to be created"))
        self.targetButton.setText(_translate("createDialog", "Save As"))
        self.okButton.setText(_translate("createDialog", "OK"))
        self.cancelButton.setText(_translate("createDialog", "Cancel"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    createDialog = QtWidgets.QDialog()
    ui = Ui_createDialog()
    ui.setupUi(createDialog)
    createDialog.show()
    sys.exit(app.exec_())

