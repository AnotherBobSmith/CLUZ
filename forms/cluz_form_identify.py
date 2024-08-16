# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_identify.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_identifyDialog(object):
    def setupUi(self, identifyDialog):
        identifyDialog.setObjectName("identifyDialog")
        identifyDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(identifyDialog.sizePolicy().hasHeightForWidth())
        identifyDialog.setSizePolicy(sizePolicy)
        identifyDialog.setMinimumSize(QtCore.QSize(800, 500))
        self.gridLayout = QtWidgets.QGridLayout(identifyDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.identifyTableWidget = QtWidgets.QTableWidget(identifyDialog)
        self.identifyTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.identifyTableWidget.setObjectName("identifyTableWidget")
        self.identifyTableWidget.setColumnCount(0)
        self.identifyTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.identifyTableWidget)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.closeButton = QtWidgets.QPushButton(identifyDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem2)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 8)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(identifyDialog)
        self.closeButton.clicked.connect(identifyDialog.close)
        QtCore.QMetaObject.connectSlotsByName(identifyDialog)

    def retranslateUi(self, identifyDialog):
        _translate = QtCore.QCoreApplication.translate
        identifyDialog.setWindowTitle(_translate("identifyDialog", "Identify Tool"))
        self.closeButton.setText(_translate("identifyDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    identifyDialog = QtWidgets.QDialog()
    ui = Ui_identifyDialog()
    ui.setupUi(identifyDialog)
    identifyDialog.show()
    sys.exit(app.exec_())

