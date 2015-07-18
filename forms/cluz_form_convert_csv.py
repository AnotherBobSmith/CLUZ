# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_convert_csv.ui'
#
# Created: Thu Apr 23 09:37:47 2015
#      by: PyQt4 UI code generator 4.10.3
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
        convertCsvDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        convertCsvDialog.resize(622, 371)
        self.csvLabel = QtGui.QLabel(convertCsvDialog)
        self.csvLabel.setGeometry(QtCore.QRect(150, 20, 301, 16))
        self.csvLabel.setObjectName(_fromUtf8("csvLabel"))
        self.okButton = QtGui.QPushButton(convertCsvDialog)
        self.okButton.setGeometry(QtCore.QRect(260, 320, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(convertCsvDialog)
        self.cancelButton.setGeometry(QtCore.QRect(380, 320, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.idfieldLabel = QtGui.QLabel(convertCsvDialog)
        self.idfieldLabel.setGeometry(QtCore.QRect(150, 90, 111, 16))
        self.idfieldLabel.setObjectName(_fromUtf8("idfieldLabel"))
        self.convLineEdit = QtGui.QLineEdit(convertCsvDialog)
        self.convLineEdit.setGeometry(QtCore.QRect(300, 210, 100, 20))
        self.convLineEdit.setObjectName(_fromUtf8("convLineEdit"))
        self.convLabel = QtGui.QLabel(convertCsvDialog)
        self.convLabel.setGeometry(QtCore.QRect(180, 210, 111, 16))
        self.convLabel.setObjectName(_fromUtf8("convLabel"))
        self.noneRadioButton = QtGui.QRadioButton(convertCsvDialog)
        self.noneRadioButton.setGeometry(QtCore.QRect(160, 140, 300, 17))
        self.noneRadioButton.setObjectName(_fromUtf8("noneRadioButton"))
        self.userRadioButton = QtGui.QRadioButton(convertCsvDialog)
        self.userRadioButton.setGeometry(QtCore.QRect(160, 180, 201, 17))
        self.userRadioButton.setObjectName(_fromUtf8("userRadioButton"))
        self.logoLabel = QtGui.QLabel(convertCsvDialog)
        self.logoLabel.setGeometry(QtCore.QRect(0, -10, 131, 401))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.csvFileLineEdit = QtGui.QLineEdit(convertCsvDialog)
        self.csvFileLineEdit.setGeometry(QtCore.QRect(150, 50, 371, 20))
        self.csvFileLineEdit.setObjectName(_fromUtf8("csvFileLineEdit"))
        self.browseButton = QtGui.QPushButton(convertCsvDialog)
        self.browseButton.setGeometry(QtCore.QRect(530, 50, 75, 23))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.idfieldComboBox = QtGui.QComboBox(convertCsvDialog)
        self.idfieldComboBox.setGeometry(QtCore.QRect(250, 90, 271, 22))
        self.idfieldComboBox.setObjectName(_fromUtf8("idfieldComboBox"))

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
        self.idfieldLabel.setText(_translate("convertCsvDialog", "Layer ID field name", None))
        self.convLabel.setText(_translate("convertCsvDialog", "Area conversion value", None))
        self.noneRadioButton.setText(_translate("convertCsvDialog", "No conversion (results will be in layer measurement units)", None))
        self.userRadioButton.setText(_translate("convertCsvDialog", "User defined conversion", None))
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

