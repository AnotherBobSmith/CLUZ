# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_remove.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_removeDialog(object):
    def setupUi(self, removeDialog):
        removeDialog.setObjectName("removeDialog")
        removeDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        removeDialog.setMinimumSize(QtCore.QSize(800, 400))
        self.gridLayout = QtWidgets.QGridLayout(removeDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logoLabel = QtWidgets.QLabel(removeDialog)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap(":/logos/images/marxan_logo.png"))
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.logoLabel.setObjectName("logoLabel")
        self.horizontalLayout_2.addWidget(self.logoLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.featLabel = QtWidgets.QLabel(removeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.featLabel.sizePolicy().hasHeightForWidth())
        self.featLabel.setSizePolicy(sizePolicy)
        self.featLabel.setMinimumSize(QtCore.QSize(461, 20))
        self.featLabel.setObjectName("featLabel")
        self.verticalLayout.addWidget(self.featLabel)
        self.featListWidget = QtWidgets.QListWidget(removeDialog)
        self.featListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.featListWidget.setObjectName("featListWidget")
        self.verticalLayout.addWidget(self.featListWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.okButton = QtWidgets.QPushButton(removeDialog)
        self.okButton.setMinimumSize(QtCore.QSize(0, 24))
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem2)
        self.cancelButton = QtWidgets.QPushButton(removeDialog)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 24))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem3)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 6)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(removeDialog)
        self.cancelButton.clicked.connect(removeDialog.close)
        QtCore.QMetaObject.connectSlotsByName(removeDialog)

    def retranslateUi(self, removeDialog):
        _translate = QtCore.QCoreApplication.translate
        removeDialog.setWindowTitle(_translate("removeDialog", "Choose features to remove"))
        self.featLabel.setText(_translate("removeDialog", "Select conservation features to remove from the abundance and target tables"))
        self.okButton.setText(_translate("removeDialog", "OK"))
        self.cancelButton.setText(_translate("removeDialog", "Cancel"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    removeDialog = QtWidgets.QDialog()
    ui = Ui_removeDialog()
    ui.setupUi(removeDialog)
    removeDialog.show()
    sys.exit(app.exec_())

