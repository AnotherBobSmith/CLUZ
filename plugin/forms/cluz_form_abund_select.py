# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_abund_select.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_abundSelectDialog(object):
    def setupUi(self, abundSelectDialog):
        abundSelectDialog.setObjectName("abundSelectDialog")
        abundSelectDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(abundSelectDialog.sizePolicy().hasHeightForWidth())
        abundSelectDialog.setSizePolicy(sizePolicy)
        abundSelectDialog.setMinimumSize(QtCore.QSize(700, 580))
        self.gridLayout = QtWidgets.QGridLayout(abundSelectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logoLabel = QtWidgets.QLabel(abundSelectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logoLabel.sizePolicy().hasHeightForWidth())
        self.logoLabel.setSizePolicy(sizePolicy)
        self.logoLabel.setMinimumSize(QtCore.QSize(130, 200))
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap(":/logos/images/setup_logo_panel.png"))
        self.logoLabel.setObjectName("logoLabel")
        self.horizontalLayout_2.addWidget(self.logoLabel)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.featLabel = QtWidgets.QLabel(abundSelectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.featLabel.sizePolicy().hasHeightForWidth())
        self.featLabel.setSizePolicy(sizePolicy)
        self.featLabel.setMinimumSize(QtCore.QSize(350, 16))
        self.featLabel.setObjectName("featLabel")
        self.verticalLayout.addWidget(self.featLabel)
        self.featListWidget = QtWidgets.QListWidget(abundSelectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.featListWidget.sizePolicy().hasHeightForWidth())
        self.featListWidget.setSizePolicy(sizePolicy)
        self.featListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.featListWidget.setObjectName("featListWidget")
        self.verticalLayout.addWidget(self.featListWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(abundSelectDialog)
        self.okButton.setMinimumSize(QtCore.QSize(0, 16))
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancelButton = QtWidgets.QPushButton(abundSelectDialog)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 16))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem2)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 6)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(abundSelectDialog)
        self.cancelButton.clicked.connect(abundSelectDialog.close)
        QtCore.QMetaObject.connectSlotsByName(abundSelectDialog)

    def retranslateUi(self, abundSelectDialog):
        _translate = QtCore.QCoreApplication.translate
        abundSelectDialog.setWindowTitle(_translate("abundSelectDialog", "Select features for Abundance table"))
        self.featLabel.setText(_translate("abundSelectDialog", "Display all or select conservation features to display in abundance table"))
        self.okButton.setText(_translate("abundSelectDialog", "OK"))
        self.cancelButton.setText(_translate("abundSelectDialog", "Cancel"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    abundSelectDialog = QtWidgets.QDialog()
    ui = Ui_abundSelectDialog()
    ui.setupUi(abundSelectDialog)
    abundSelectDialog.show()
    sys.exit(app.exec_())

