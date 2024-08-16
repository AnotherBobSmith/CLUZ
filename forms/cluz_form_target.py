# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_target.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_targetDialog(object):
    def setupUi(self, targetDialog):
        targetDialog.setObjectName("targetDialog")
        targetDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        targetDialog.setMinimumSize(QtCore.QSize(900, 500))
        self.gridLayout = QtWidgets.QGridLayout(targetDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.targetTableWidget = QtWidgets.QTableWidget(targetDialog)
        self.targetTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.targetTableWidget.setAlternatingRowColors(True)
        self.targetTableWidget.setObjectName("targetTableWidget")
        self.targetTableWidget.setColumnCount(0)
        self.targetTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.targetTableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtWidgets.QPushButton(targetDialog)
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

        self.retranslateUi(targetDialog)
        self.cancelButton.clicked.connect(targetDialog.close)
        QtCore.QMetaObject.connectSlotsByName(targetDialog)

    def retranslateUi(self, targetDialog):
        _translate = QtCore.QCoreApplication.translate
        targetDialog.setWindowTitle(_translate("targetDialog", "Target table"))
        self.targetTableWidget.setSortingEnabled(True)
        self.cancelButton.setText(_translate("targetDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    targetDialog = QtWidgets.QDialog()
    ui = Ui_targetDialog()
    ui.setupUi(targetDialog)
    targetDialog.show()
    sys.exit(app.exec_())

