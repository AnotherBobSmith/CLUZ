# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_identify_selected.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_identifySelectedDialog(object):
    def setupUi(self, identifySelectedDialog):
        identifySelectedDialog.setObjectName("identifySelectedDialog")
        identifySelectedDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(identifySelectedDialog.sizePolicy().hasHeightForWidth())
        identifySelectedDialog.setSizePolicy(sizePolicy)
        identifySelectedDialog.setMinimumSize(QtCore.QSize(600, 500))
        self.gridLayout = QtWidgets.QGridLayout(identifySelectedDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.identifySelectedTableWidget = QtWidgets.QTableWidget(identifySelectedDialog)
        self.identifySelectedTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.identifySelectedTableWidget.setObjectName("identifySelectedTableWidget")
        self.identifySelectedTableWidget.setColumnCount(0)
        self.identifySelectedTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.identifySelectedTableWidget)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.closeButton = QtWidgets.QPushButton(identifySelectedDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 8)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(identifySelectedDialog)
        self.closeButton.clicked.connect(identifySelectedDialog.close)
        QtCore.QMetaObject.connectSlotsByName(identifySelectedDialog)

    def retranslateUi(self, identifySelectedDialog):
        _translate = QtCore.QCoreApplication.translate
        identifySelectedDialog.setWindowTitle(_translate("identifySelectedDialog", "Identify Tool"))
        self.closeButton.setText(_translate("identifySelectedDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    identifySelectedDialog = QtWidgets.QDialog()
    ui = Ui_identifySelectedDialog()
    ui.setupUi(identifySelectedDialog)
    identifySelectedDialog.show()
    sys.exit(app.exec_())

