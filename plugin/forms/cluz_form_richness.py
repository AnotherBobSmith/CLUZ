# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_richness.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_richnessDialog(object):
    def setupUi(self, richnessDialog):
        richnessDialog.setObjectName("richnessDialog")
        richnessDialog.setMinimumSize(QtCore.QSize(600, 450))
        self.gridLayout_2 = QtWidgets.QGridLayout(richnessDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logoLabel = QtWidgets.QLabel(richnessDialog)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap(":/logos/images/setup_logo_panel.png"))
        self.logoLabel.setObjectName("logoLabel")
        self.horizontalLayout_2.addWidget(self.logoLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.inputsLabel = QtWidgets.QLabel(richnessDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputsLabel.sizePolicy().hasHeightForWidth())
        self.inputsLabel.setSizePolicy(sizePolicy)
        self.inputsLabel.setMinimumSize(QtCore.QSize(24, 24))
        self.inputsLabel.setObjectName("inputsLabel")
        self.gridLayout.addWidget(self.inputsLabel, 0, 0, 1, 1)
        self.rangeLabel = QtWidgets.QLabel(richnessDialog)
        self.rangeLabel.setEnabled(False)
        self.rangeLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.rangeLabel.setObjectName("rangeLabel")
        self.gridLayout.addWidget(self.rangeLabel, 5, 0, 1, 1)
        self.rangeLineEdit = QtWidgets.QLineEdit(richnessDialog)
        self.rangeLineEdit.setEnabled(False)
        self.rangeLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.rangeLineEdit.setObjectName("rangeLineEdit")
        self.gridLayout.addWidget(self.rangeLineEdit, 5, 1, 1, 1)
        self.countLabel = QtWidgets.QLabel(richnessDialog)
        self.countLabel.setEnabled(False)
        self.countLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.countLabel.setObjectName("countLabel")
        self.gridLayout.addWidget(self.countLabel, 2, 0, 1, 1)
        self.rangeBox = QtWidgets.QCheckBox(richnessDialog)
        self.rangeBox.setMinimumSize(QtCore.QSize(0, 24))
        self.rangeBox.setObjectName("rangeBox")
        self.gridLayout.addWidget(self.rangeBox, 4, 0, 1, 1)
        self.countBox = QtWidgets.QCheckBox(richnessDialog)
        self.countBox.setMinimumSize(QtCore.QSize(0, 24))
        self.countBox.setObjectName("countBox")
        self.gridLayout.addWidget(self.countBox, 1, 0, 1, 1)
        self.countLineEdit = QtWidgets.QLineEdit(richnessDialog)
        self.countLineEdit.setEnabled(False)
        self.countLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.countLineEdit.setObjectName("countLineEdit")
        self.gridLayout.addWidget(self.countLineEdit, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.typeLabel = QtWidgets.QLabel(richnessDialog)
        self.typeLabel.setObjectName("typeLabel")
        self.verticalLayout.addWidget(self.typeLabel)
        self.typeListWidget = QtWidgets.QListWidget(richnessDialog)
        self.typeListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.typeListWidget.setObjectName("typeListWidget")
        self.verticalLayout.addWidget(self.typeListWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem3)
        self.okButton = QtWidgets.QPushButton(richnessDialog)
        self.okButton.setMinimumSize(QtCore.QSize(0, 24))
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem4)
        self.cancelButton = QtWidgets.QPushButton(richnessDialog)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 24))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem5)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_3.setStretch(0, 2)
        self.verticalLayout_3.setStretch(1, 2)
        self.verticalLayout_3.setStretch(2, 4)
        self.verticalLayout_3.setStretch(3, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(richnessDialog)
        self.cancelButton.clicked.connect(richnessDialog.close)
        self.countBox.clicked['bool'].connect(self.countLabel.setEnabled)
        self.countBox.clicked['bool'].connect(self.countLineEdit.setEnabled)
        self.rangeBox.clicked['bool'].connect(self.rangeLabel.setEnabled)
        self.rangeBox.clicked['bool'].connect(self.rangeLineEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(richnessDialog)

    def retranslateUi(self, richnessDialog):
        _translate = QtCore.QCoreApplication.translate
        richnessDialog.setWindowTitle(_translate("richnessDialog", "Calculate richness scores"))
        self.inputsLabel.setText(_translate("richnessDialog", "Calculate the following for each planning unit:"))
        self.rangeLabel.setText(_translate("richnessDialog", "Field name"))
        self.countLabel.setText(_translate("richnessDialog", "Field name"))
        self.rangeBox.setText(_translate("richnessDialog", "Restricted Range Richness"))
        self.countBox.setText(_translate("richnessDialog", "Feature Count"))
        self.typeLabel.setText(_translate("richnessDialog", "Use features with type codes from the target file:"))
        self.okButton.setText(_translate("richnessDialog", "OK"))
        self.cancelButton.setText(_translate("richnessDialog", "Cancel"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    richnessDialog = QtWidgets.QDialog()
    ui = Ui_richnessDialog()
    ui.setupUi(richnessDialog)
    richnessDialog.show()
    sys.exit(app.exec_())

