# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_zones.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_zonesDialog(object):
    def setupUi(self, zonesDialog):
        zonesDialog.setObjectName("zonesDialog")
        zonesDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        zonesDialog.resize(530, 374)
        self.gridLayout = QtWidgets.QGridLayout(zonesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.zonesTableWidget = QtWidgets.QTableWidget(zonesDialog)
        self.zonesTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.zonesTableWidget.setAlternatingRowColors(True)
        self.zonesTableWidget.setObjectName("zonesTableWidget")
        self.zonesTableWidget.setColumnCount(0)
        self.zonesTableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.zonesTableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtWidgets.QPushButton(zonesDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 6)
        self.verticalLayout_2.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(zonesDialog)
        self.cancelButton.clicked.connect(zonesDialog.close)
        QtCore.QMetaObject.connectSlotsByName(zonesDialog)

    def retranslateUi(self, zonesDialog):
        _translate = QtCore.QCoreApplication.translate
        zonesDialog.setWindowTitle(_translate("zonesDialog", "Zones table"))
        self.zonesTableWidget.setSortingEnabled(True)
        self.cancelButton.setText(_translate("zonesDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    zonesDialog = QtWidgets.QDialog()
    ui = Ui_zonesDialog()
    ui.setupUi(zonesDialog)
    zonesDialog.show()
    sys.exit(app.exec_())

