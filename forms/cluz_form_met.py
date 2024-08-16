# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_met.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_metDialog(object):
    def setupUi(self, metDialog):
        metDialog.setObjectName("metDialog")
        metDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        metDialog.setMinimumSize(QtCore.QSize(500, 300))
        self.gridLayout = QtWidgets.QGridLayout(metDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.metTableWidget = QtWidgets.QTableWidget(metDialog)
        self.metTableWidget.setAlternatingRowColors(True)
        self.metTableWidget.setObjectName("metTableWidget")
        self.metTableWidget.setColumnCount(0)
        self.metTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.metTableWidget, 0, 0, 1, 1)

        self.retranslateUi(metDialog)
        QtCore.QMetaObject.connectSlotsByName(metDialog)

    def retranslateUi(self, metDialog):
        _translate = QtCore.QCoreApplication.translate
        metDialog.setWindowTitle(_translate("metDialog", "Marxan Targets Met table"))
        self.metTableWidget.setSortingEnabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    metDialog = QtWidgets.QDialog()
    ui = Ui_metDialog()
    ui.setupUi(metDialog)
    metDialog.show()
    sys.exit(app.exec_())

