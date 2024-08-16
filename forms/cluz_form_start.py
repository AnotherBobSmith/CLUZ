# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_start.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_startDialog(object):
    def setupUi(self, startDialog):
        startDialog.setObjectName("startDialog")
        startDialog.setMinimumSize(QtCore.QSize(400, 200))
        self.gridLayout = QtWidgets.QGridLayout(startDialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(startDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.openRadioButton = QtWidgets.QRadioButton(startDialog)
        self.openRadioButton.setMinimumSize(QtCore.QSize(211, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.openRadioButton.setFont(font)
        self.openRadioButton.setChecked(True)
        self.openRadioButton.setObjectName("openRadioButton")
        self.verticalLayout.addWidget(self.openRadioButton)
        self.createButton = QtWidgets.QRadioButton(startDialog)
        self.createButton.setMinimumSize(QtCore.QSize(211, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.createButton.setFont(font)
        self.createButton.setCheckable(True)
        self.createButton.setObjectName("createButton")
        self.verticalLayout.addWidget(self.createButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem4)
        self.okButton = QtWidgets.QPushButton(startDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(startDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.cluzLogoLabel = QtWidgets.QLabel(startDialog)
        self.cluzLogoLabel.setText("")
        self.cluzLogoLabel.setPixmap(QtGui.QPixmap(":/logos/images/marxan_logo.png"))
        self.cluzLogoLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.cluzLogoLabel.setObjectName("cluzLogoLabel")
        self.gridLayout.addWidget(self.cluzLogoLabel, 0, 0, 1, 1)

        self.retranslateUi(startDialog)
        self.cancelButton.clicked.connect(startDialog.close)
        QtCore.QMetaObject.connectSlotsByName(startDialog)

    def retranslateUi(self, startDialog):
        _translate = QtCore.QCoreApplication.translate
        startDialog.setWindowTitle(_translate("startDialog", "Select or create CLUZ setup file"))
        self.label.setText(_translate("startDialog", "The selected action cannot continue because a CLUZ setup file has not been specified. Please open an existing setup file or create a new one."))
        self.openRadioButton.setText(_translate("startDialog", "Open existing setup file"))
        self.createButton.setText(_translate("startDialog", "Create new setup file"))
        self.okButton.setText(_translate("startDialog", "OK"))
        self.cancelButton.setText(_translate("startDialog", "Cancel"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    startDialog = QtWidgets.QDialog()
    ui = Ui_startDialog()
    ui.setupUi(startDialog)
    startDialog.show()
    sys.exit(app.exec_())

