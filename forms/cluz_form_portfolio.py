# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_portfolio.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_portfolioDialog(object):
    def setupUi(self, portfolioDialog):
        portfolioDialog.setObjectName(_fromUtf8("portfolioDialog"))
        portfolioDialog.resize(750, 400)
        portfolioDialog.setMinimumSize(QtCore.QSize(750, 400))
        self.logoLabel = QtGui.QLabel(portfolioDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, 0, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(portfolioDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(280, 350, 271, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setMinimumSize(QtCore.QSize(0, 24))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 24))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.tabWidget = QtGui.QTabWidget(portfolioDialog)
        self.tabWidget.setGeometry(QtCore.QRect(120, 20, 611, 331))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.standardTab = QtGui.QWidget()
        self.standardTab.setObjectName(_fromUtf8("standardTab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.standardTab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.portfolioLabel = QtGui.QLabel(self.standardTab)
        self.portfolioLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.portfolioLabel.setObjectName(_fromUtf8("portfolioLabel"))
        self.verticalLayout.addWidget(self.portfolioLabel)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.puDetailsCheckBox = QtGui.QCheckBox(self.standardTab)
        self.puDetailsCheckBox.setChecked(True)
        self.puDetailsCheckBox.setObjectName(_fromUtf8("puDetailsCheckBox"))
        self.verticalLayout_2.addWidget(self.puDetailsCheckBox)
        self.spatialCheckBox = QtGui.QCheckBox(self.standardTab)
        self.spatialCheckBox.setChecked(True)
        self.spatialCheckBox.setObjectName(_fromUtf8("spatialCheckBox"))
        self.verticalLayout_2.addWidget(self.spatialCheckBox)
        spacerItem = QtGui.QSpacerItem(40, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.sfCheckBox = QtGui.QCheckBox(self.standardTab)
        self.sfCheckBox.setObjectName(_fromUtf8("sfCheckBox"))
        self.verticalLayout_2.addWidget(self.sfCheckBox)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.sfFieldLabel = QtGui.QLabel(self.standardTab)
        self.sfFieldLabel.setObjectName(_fromUtf8("sfFieldLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.sfFieldLabel)
        self.sfComboBox = QtGui.QComboBox(self.standardTab)
        self.sfComboBox.setMinimumSize(QtCore.QSize(0, 24))
        self.sfComboBox.setObjectName(_fromUtf8("sfComboBox"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.sfComboBox)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.sfRunsLabel = QtGui.QLabel(self.standardTab)
        self.sfRunsLabel.setTextFormat(QtCore.Qt.PlainText)
        self.sfRunsLabel.setWordWrap(True)
        self.sfRunsLabel.setObjectName(_fromUtf8("sfRunsLabel"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.sfRunsLabel)
        self.sfRunsLineEdit = QtGui.QLineEdit(self.standardTab)
        self.sfRunsLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.sfRunsLineEdit.setObjectName(_fromUtf8("sfRunsLineEdit"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.sfRunsLineEdit)
        self.verticalLayout.addLayout(self.formLayout_6)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.standardTab, _fromUtf8(""))
        self.advancedTab = QtGui.QWidget()
        self.advancedTab.setObjectName(_fromUtf8("advancedTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.advancedTab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.patchTargetCheckBox = QtGui.QCheckBox(self.advancedTab)
        self.patchTargetCheckBox.setObjectName(_fromUtf8("patchTargetCheckBox"))
        self.verticalLayout_3.addWidget(self.patchTargetCheckBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem1)
        self.equalityCheckBox = QtGui.QCheckBox(self.advancedTab)
        self.equalityCheckBox.setObjectName(_fromUtf8("equalityCheckBox"))
        self.verticalLayout_3.addWidget(self.equalityCheckBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem3)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem4)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.advancedTab, _fromUtf8(""))

        self.retranslateUi(portfolioDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), portfolioDialog.close)
        QtCore.QObject.connect(self.sfCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.sfFieldLabel.setEnabled)
        QtCore.QObject.connect(self.sfCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.sfComboBox.setEnabled)
        QtCore.QObject.connect(self.sfCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.sfRunsLabel.setVisible)
        QtCore.QObject.connect(self.sfCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.sfRunsLineEdit.setVisible)
        QtCore.QMetaObject.connectSlotsByName(portfolioDialog)

    def retranslateUi(self, portfolioDialog):
        portfolioDialog.setWindowTitle(_translate("portfolioDialog", "Create Marxan files", None))
        self.okButton.setText(_translate("portfolioDialog", "OK", None))
        self.cancelButton.setText(_translate("portfolioDialog", "Cancel", None))
        self.portfolioLabel.setText(_translate("portfolioDialog", "Calculate the following details about the current portfolio of planning units:", None))
        self.puDetailsCheckBox.setText(_translate("portfolioDialog", "Planning unit details", None))
        self.spatialCheckBox.setText(_translate("portfolioDialog", "Spatial details (patch sizes and boundary length)", None))
        self.sfCheckBox.setText(_translate("portfolioDialog", "Selection frequency details of Available and Earmarked planning units", None))
        self.sfFieldLabel.setText(_translate("portfolioDialog", "Field containing values", None))
        self.sfRunsLabel.setText(_translate("portfolioDialog", "Number of runs used in analysis (ie maximum potential selection frequency)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.standardTab), _translate("portfolioDialog", "Standard", None))
        self.patchTargetCheckBox.setText(_translate("portfolioDialog", "Number of patches containing each conservation feature", None))
        self.equalityCheckBox.setText(_translate("portfolioDialog", "Protection equality", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.advancedTab), _translate("portfolioDialog", "Advanced", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    portfolioDialog = QtGui.QDialog()
    ui = Ui_portfolioDialog()
    ui.setupUi(portfolioDialog)
    portfolioDialog.show()
    sys.exit(app.exec_())

