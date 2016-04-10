# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_convert_csv.ui'
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

class Ui_convertCsvDialog(object):
    def setupUi(self, convertCsvDialog):
        convertCsvDialog.setObjectName(_fromUtf8("convertCsvDialog"))
        convertCsvDialog.resize(730, 380)
        convertCsvDialog.setMinimumSize(QtCore.QSize(730, 380))
        self.logoLabel = QtGui.QLabel(convertCsvDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, -10, 131, 401))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.csvLabel = QtGui.QLabel(convertCsvDialog)
        self.csvLabel.setGeometry(QtCore.QRect(140, 20, 491, 16))
        self.csvLabel.setObjectName(_fromUtf8("csvLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(convertCsvDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(260, 320, 241, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setMinimumSize(QtCore.QSize(0, 22))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 22))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayoutWidget = QtGui.QWidget(convertCsvDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 170, 541, 74))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.noneRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.noneRadioButton.setMinimumSize(QtCore.QSize(441, 20))
        self.noneRadioButton.setObjectName(_fromUtf8("noneRadioButton"))
        self.verticalLayout.addWidget(self.noneRadioButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.userRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.userRadioButton.setMinimumSize(QtCore.QSize(0, 20))
        self.userRadioButton.setObjectName(_fromUtf8("userRadioButton"))
        self.verticalLayout.addWidget(self.userRadioButton)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(convertCsvDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(180, 250, 331, 31))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.convLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.convLabel.setMinimumSize(QtCore.QSize(151, 20))
        self.convLabel.setObjectName(_fromUtf8("convLabel"))
        self.horizontalLayout_2.addWidget(self.convLabel)
        self.convLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.convLineEdit.setMinimumSize(QtCore.QSize(0, 20))
        self.convLineEdit.setObjectName(_fromUtf8("convLineEdit"))
        self.horizontalLayout_2.addWidget(self.convLineEdit)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(convertCsvDialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(140, 100, 351, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.idfieldLabel = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.idfieldLabel.setMinimumSize(QtCore.QSize(151, 16))
        self.idfieldLabel.setObjectName(_fromUtf8("idfieldLabel"))
        self.horizontalLayout_3.addWidget(self.idfieldLabel)
        self.idfieldComboBox = QtGui.QComboBox(self.horizontalLayoutWidget_3)
        self.idfieldComboBox.setObjectName(_fromUtf8("idfieldComboBox"))
        self.horizontalLayout_3.addWidget(self.idfieldComboBox)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(convertCsvDialog)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(139, 40, 561, 41))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.csvFileLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_4)
        self.csvFileLineEdit.setObjectName(_fromUtf8("csvFileLineEdit"))
        self.horizontalLayout_4.addWidget(self.csvFileLineEdit)
        self.browseButton = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.browseButton.setMinimumSize(QtCore.QSize(0, 22))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout_4.addWidget(self.browseButton)
        self.logoLabel.raise_()
        self.csvLabel.raise_()
        self.horizontalLayoutWidget.raise_()
        self.verticalLayoutWidget.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.noneRadioButton.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.horizontalLayoutWidget_4.raise_()

        self.retranslateUi(convertCsvDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), convertCsvDialog.close)
        QtCore.QObject.connect(self.userRadioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.convLabel.setEnabled)
        QtCore.QObject.connect(self.userRadioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.convLineEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(convertCsvDialog)

    def retranslateUi(self, convertCsvDialog):
        convertCsvDialog.setWindowTitle(_translate("convertCsvDialog", "Convert themes to abundance data", None))
        self.csvLabel.setText(_translate("convertCsvDialog", "Select csv file to import data into Marxan", None))
        self.okButton.setText(_translate("convertCsvDialog", "OK", None))
        self.cancelButton.setText(_translate("convertCsvDialog", "Cancel", None))
        self.noneRadioButton.setText(_translate("convertCsvDialog", "No conversion (results will be in layer measurement units)", None))
        self.userRadioButton.setText(_translate("convertCsvDialog", "User defined conversion", None))
        self.convLabel.setText(_translate("convertCsvDialog", "Area conversion value", None))
        self.idfieldLabel.setText(_translate("convertCsvDialog", "Layer ID field name", None))
        self.browseButton.setText(_translate("convertCsvDialog", "Browse", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    convertCsvDialog = QtGui.QDialog()
    ui = Ui_convertCsvDialog()
    ui.setupUi(convertCsvDialog)
    convertCsvDialog.show()
    sys.exit(app.exec_())

