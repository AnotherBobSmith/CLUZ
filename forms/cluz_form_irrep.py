# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_irrep.ui'
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

class Ui_irrepDialog(object):
    def setupUi(self, irrepDialog):
        irrepDialog.setObjectName(_fromUtf8("irrepDialog"))
        irrepDialog.resize(570, 540)
        irrepDialog.setMinimumSize(QtCore.QSize(570, 540))
        self.logoLabel = QtGui.QLabel(irrepDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, 0, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(irrepDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 480, 271, 41))
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
        self.typeLabel = QtGui.QLabel(irrepDialog)
        self.typeLabel.setGeometry(QtCore.QRect(120, 210, 419, 13))
        self.typeLabel.setObjectName(_fromUtf8("typeLabel"))
        self.typeListWidget = QtGui.QListWidget(irrepDialog)
        self.typeListWidget.setGeometry(QtCore.QRect(120, 229, 419, 110))
        self.typeListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.typeListWidget.setObjectName(_fromUtf8("typeListWidget"))
        self.outputCheckBox = QtGui.QCheckBox(irrepDialog)
        self.outputCheckBox.setGeometry(QtCore.QRect(120, 350, 401, 21))
        self.outputCheckBox.setObjectName(_fromUtf8("outputCheckBox"))
        self.verticalLayoutWidget = QtGui.QWidget(irrepDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(120, 30, 421, 74))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.allRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.allRadioButton.setMinimumSize(QtCore.QSize(211, 20))
        self.allRadioButton.setChecked(True)
        self.allRadioButton.setObjectName(_fromUtf8("allRadioButton"))
        self.verticalLayout.addWidget(self.allRadioButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.availableRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.availableRadioButton.setMinimumSize(QtCore.QSize(211, 20))
        self.availableRadioButton.setCheckable(True)
        self.availableRadioButton.setObjectName(_fromUtf8("availableRadioButton"))
        self.verticalLayout.addWidget(self.availableRadioButton)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(irrepDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(120, 110, 421, 31))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.irrepLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.irrepLabel.setObjectName(_fromUtf8("irrepLabel"))
        self.horizontalLayout_2.addWidget(self.irrepLabel)
        self.irrepLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.irrepLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.irrepLineEdit.setObjectName(_fromUtf8("irrepLineEdit"))
        self.horizontalLayout_2.addWidget(self.irrepLineEdit)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(irrepDialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(120, 380, 421, 31))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.outputLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
        self.outputLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.horizontalLayout_3.addWidget(self.outputLineEdit)
        self.browseButton = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.browseButton.setMinimumSize(QtCore.QSize(0, 20))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout_3.addWidget(self.browseButton)

        self.retranslateUi(irrepDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), irrepDialog.close)
        QtCore.QObject.connect(self.outputCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.outputLineEdit.setVisible)
        QtCore.QObject.connect(self.outputCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.browseButton.setVisible)
        QtCore.QMetaObject.connectSlotsByName(irrepDialog)

    def retranslateUi(self, irrepDialog):
        irrepDialog.setWindowTitle(_translate("irrepDialog", "Calculate irreplaceability values", None))
        self.okButton.setText(_translate("irrepDialog", "OK", None))
        self.cancelButton.setText(_translate("irrepDialog", "Cancel", None))
        self.typeLabel.setText(_translate("irrepDialog", "Use features with type codes from the target file:", None))
        self.outputCheckBox.setText(_translate("irrepDialog", "Save irreplaceability scores for each feature as a text file", None))
        self.allRadioButton.setText(_translate("irrepDialog", "Calculate values for all planning units", None))
        self.availableRadioButton.setText(_translate("irrepDialog", "Calculate values for Available planning units only", None))
        self.irrepLabel.setText(_translate("irrepDialog", "Field name", None))
        self.browseButton.setText(_translate("irrepDialog", "Browse", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    irrepDialog = QtGui.QDialog()
    ui = Ui_irrepDialog()
    ui.setupUi(irrepDialog)
    irrepDialog.show()
    sys.exit(app.exec_())

