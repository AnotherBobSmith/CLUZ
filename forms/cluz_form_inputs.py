# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_inputs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_inputsDialog(object):
    def setupUi(self, inputsDialog):
        inputsDialog.setObjectName("inputsDialog")
        inputsDialog.setMinimumSize(QtCore.QSize(620, 390))
        self.gridLayout = QtWidgets.QGridLayout(inputsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(inputsDialog)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/images/marxan_logo_panel.png"))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.inputsLabel = QtWidgets.QLabel(inputsDialog)
        self.inputsLabel.setMinimumSize(QtCore.QSize(0, 20))
        self.inputsLabel.setObjectName("inputsLabel")
        self.verticalLayout_2.addWidget(self.inputsLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.targetBox = QtWidgets.QCheckBox(inputsDialog)
        self.targetBox.setMinimumSize(QtCore.QSize(0, 30))
        self.targetBox.setObjectName("targetBox")
        self.verticalLayout.addWidget(self.targetBox)
        self.puBox = QtWidgets.QCheckBox(inputsDialog)
        self.puBox.setMinimumSize(QtCore.QSize(0, 30))
        self.puBox.setObjectName("puBox")
        self.verticalLayout.addWidget(self.puBox)
        self.boundBox = QtWidgets.QCheckBox(inputsDialog)
        self.boundBox.setMinimumSize(QtCore.QSize(0, 30))
        self.boundBox.setObjectName("boundBox")
        self.verticalLayout.addWidget(self.boundBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.boundextBox = QtWidgets.QCheckBox(inputsDialog)
        self.boundextBox.setMinimumSize(QtCore.QSize(0, 24))
        self.boundextBox.setObjectName("boundextBox")
        self.horizontalLayout_2.addWidget(self.boundextBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem5)
        self.okButton = QtWidgets.QPushButton(inputsDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem6)
        self.cancelButton = QtWidgets.QPushButton(inputsDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(5, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(inputsDialog)
        self.cancelButton.clicked.connect(inputsDialog.close)
        self.boundBox.clicked['bool'].connect(self.boundextBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(inputsDialog)

    def retranslateUi(self, inputsDialog):
        _translate = QtCore.QCoreApplication.translate
        inputsDialog.setWindowTitle(_translate("inputsDialog", "Create Marxan files"))
        self.inputsLabel.setText(_translate("inputsDialog", "Create the following Marxan files from the CLUZ files:"))
        self.targetBox.setText(_translate("inputsDialog", "Target file (spec.dat)"))
        self.puBox.setText(_translate("inputsDialog", "Planning unit file (pu.dat)"))
        self.boundBox.setText(_translate("inputsDialog", "Boundary file (bound.dat)"))
        self.boundextBox.setText(_translate("inputsDialog", "Include planning region boundaries"))
        self.okButton.setText(_translate("inputsDialog", "OK"))
        self.cancelButton.setText(_translate("inputsDialog", "Cancel"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    inputsDialog = QtWidgets.QDialog()
    ui = Ui_inputsDialog()
    ui.setupUi(inputsDialog)
    inputsDialog.show()
    sys.exit(app.exec_())

