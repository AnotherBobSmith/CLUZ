# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_abund.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_abundDialog(object):
    def setupUi(self, abundDialog):
        abundDialog.setObjectName("abundDialog")
        abundDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        abundDialog.setMinimumSize(QtCore.QSize(800, 500))
        self.gridLayout = QtWidgets.QGridLayout(abundDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.abundTableWidget = QtWidgets.QTableWidget(abundDialog)
        self.abundTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.abundTableWidget.setAlternatingRowColors(True)
        self.abundTableWidget.setObjectName("abundTableWidget")
        self.abundTableWidget.setColumnCount(0)
        self.abundTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.abundTableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtWidgets.QPushButton(abundDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(abundDialog)
        self.cancelButton.clicked.connect(abundDialog.close)
        QtCore.QMetaObject.connectSlotsByName(abundDialog)

    def retranslateUi(self, abundDialog):
        _translate = QtCore.QCoreApplication.translate
        abundDialog.setWindowTitle(_translate("abundDialog", "Abundance table"))
        self.abundTableWidget.setSortingEnabled(True)
        self.cancelButton.setText(_translate("abundDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    abundDialog = QtWidgets.QDialog()
    ui = Ui_abundDialog()
    ui.setupUi(abundDialog)
    abundDialog.show()
    sys.exit(app.exec_())

