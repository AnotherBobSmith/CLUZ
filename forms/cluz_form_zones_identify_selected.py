# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_zones_identify_selected.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_zonesIdentifySelectedDialog(object):
    def setupUi(self, zonesIdentifySelectedDialog):
        zonesIdentifySelectedDialog.setObjectName("zonesIdentifySelectedDialog")
        zonesIdentifySelectedDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(zonesIdentifySelectedDialog.sizePolicy().hasHeightForWidth())
        zonesIdentifySelectedDialog.setSizePolicy(sizePolicy)
        zonesIdentifySelectedDialog.setMinimumSize(QtCore.QSize(750, 500))
        self.gridLayout = QtWidgets.QGridLayout(zonesIdentifySelectedDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.zonesIdentifySelectedTableWidget = QtWidgets.QTableWidget(zonesIdentifySelectedDialog)
        self.zonesIdentifySelectedTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.zonesIdentifySelectedTableWidget.setObjectName("zonesIdentifySelectedTableWidget")
        self.zonesIdentifySelectedTableWidget.setColumnCount(0)
        self.zonesIdentifySelectedTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.zonesIdentifySelectedTableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(zonesIdentifySelectedDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(zonesIdentifySelectedDialog)
        self.closeButton.clicked.connect(zonesIdentifySelectedDialog.close)
        QtCore.QMetaObject.connectSlotsByName(zonesIdentifySelectedDialog)

    def retranslateUi(self, zonesIdentifySelectedDialog):
        _translate = QtCore.QCoreApplication.translate
        zonesIdentifySelectedDialog.setWindowTitle(_translate("zonesIdentifySelectedDialog", "Zones Identify Tool"))
        self.closeButton.setText(_translate("zonesIdentifySelectedDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    zonesIdentifySelectedDialog = QtWidgets.QDialog()
    ui = Ui_zonesIdentifySelectedDialog()
    ui.setupUi(zonesIdentifySelectedDialog)
    zonesIdentifySelectedDialog.show()
    sys.exit(app.exec_())

