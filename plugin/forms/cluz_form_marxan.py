# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_marxan.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_marxanDialog(object):
    def setupUi(self, marxanDialog):
        marxanDialog.setObjectName("marxanDialog")
        marxanDialog.setMinimumSize(QtCore.QSize(650, 400))
        self.gridLayout_2 = QtWidgets.QGridLayout(marxanDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.marxanPanelLabel = QtWidgets.QLabel(marxanDialog)
        self.marxanPanelLabel.setText("")
        self.marxanPanelLabel.setPixmap(QtGui.QPixmap(":/logos/images/marxan_logo_panel.png"))
        self.marxanPanelLabel.setObjectName("marxanPanelLabel")
        self.horizontalLayout_2.addWidget(self.marxanPanelLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(marxanDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.iterLineEdit = QtWidgets.QLineEdit(self.tab1)
        self.iterLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.iterLineEdit.setObjectName("iterLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.iterLineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.runLabel = QtWidgets.QLabel(self.tab1)
        self.runLabel.setMinimumSize(QtCore.QSize(150, 24))
        self.runLabel.setObjectName("runLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.runLabel)
        self.runLineEdit = QtWidgets.QLineEdit(self.tab1)
        self.runLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.runLineEdit.setObjectName("runLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.runLineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        self.outputLabel = QtWidgets.QLabel(self.tab1)
        self.outputLabel.setMinimumSize(QtCore.QSize(150, 24))
        self.outputLabel.setObjectName("outputLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.outputLabel)
        self.outputLineEdit = QtWidgets.QLineEdit(self.tab1)
        self.outputLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.outputLineEdit.setObjectName("outputLineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.outputLineEdit)
        self.iterLabel = QtWidgets.QLabel(self.tab1)
        self.iterLabel.setMinimumSize(QtCore.QSize(150, 24))
        self.iterLabel.setObjectName("iterLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.iterLabel)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.boundCheckBox = QtWidgets.QCheckBox(self.tab1)
        self.boundCheckBox.setMinimumSize(QtCore.QSize(180, 24))
        self.boundCheckBox.setObjectName("boundCheckBox")
        self.gridLayout.addWidget(self.boundCheckBox, 0, 0, 1, 1)
        self.boundLineEdit = QtWidgets.QLineEdit(self.tab1)
        self.boundLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.boundLineEdit.setText("")
        self.boundLineEdit.setObjectName("boundLineEdit")
        self.gridLayout.addWidget(self.boundLineEdit, 0, 1, 1, 1)
        self.extraCheckBox = QtWidgets.QCheckBox(self.tab1)
        self.extraCheckBox.setMinimumSize(QtCore.QSize(280, 24))
        self.extraCheckBox.setObjectName("extraCheckBox")
        self.gridLayout.addWidget(self.extraCheckBox, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab1, "")
        self.extraTab = QtWidgets.QWidget()
        self.extraTab.setObjectName("extraTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.extraTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.propLabel = QtWidgets.QLabel(self.extraTab)
        self.propLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.propLabel.setObjectName("propLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.propLabel)
        self.propLineEdit = QtWidgets.QLineEdit(self.extraTab)
        self.propLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.propLineEdit.setObjectName("propLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.propLineEdit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout_2.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem3)
        self.missingLabel = QtWidgets.QLabel(self.extraTab)
        self.missingLabel.setMinimumSize(QtCore.QSize(0, 40))
        self.missingLabel.setWordWrap(True)
        self.missingLabel.setObjectName("missingLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.missingLabel)
        self.missingLineEdit = QtWidgets.QLineEdit(self.extraTab)
        self.missingLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.missingLineEdit.setObjectName("missingLineEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.missingLineEdit)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout_2.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem4)
        self.gridLayout_4.addLayout(self.formLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.extraTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem6)
        self.startButton = QtWidgets.QPushButton(marxanDialog)
        self.startButton.setMinimumSize(QtCore.QSize(30, 16))
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem7)
        self.closeButton = QtWidgets.QPushButton(marxanDialog)
        self.closeButton.setMinimumSize(QtCore.QSize(0, 16))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(marxanDialog)
        self.tabWidget.setCurrentIndex(0)
        self.closeButton.clicked.connect(marxanDialog.close)
        self.boundCheckBox.clicked['bool'].connect(self.boundLineEdit.setVisible)
        QtCore.QMetaObject.connectSlotsByName(marxanDialog)

    def retranslateUi(self, marxanDialog):
        _translate = QtCore.QCoreApplication.translate
        marxanDialog.setWindowTitle(_translate("marxanDialog", "Launch Marxan"))
        self.runLabel.setText(_translate("marxanDialog", "Number of runs"))
        self.outputLabel.setText(_translate("marxanDialog", "Output file name"))
        self.iterLabel.setText(_translate("marxanDialog", "Number of iterations"))
        self.boundCheckBox.setText(_translate("marxanDialog", "Include boundary cost (BLM)"))
        self.extraCheckBox.setText(_translate("marxanDialog", "Produce extra Marxan outputs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("marxanDialog", "Standard options"))
        self.propLabel.setText(_translate("marxanDialog", "Starting proportion"))
        self.missingLabel.setText(_translate("marxanDialog", "Species missing if target proportion is lower than"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.extraTab), _translate("marxanDialog", "Advanced options"))
        self.startButton.setText(_translate("marxanDialog", "Start Marxan"))
        self.closeButton.setText(_translate("marxanDialog", "Close"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    marxanDialog = QtWidgets.QDialog()
    ui = Ui_marxanDialog()
    ui.setupUi(marxanDialog)
    marxanDialog.show()
    sys.exit(app.exec_())
