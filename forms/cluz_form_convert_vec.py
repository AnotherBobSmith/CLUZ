# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_convert_vec.ui'
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

class Ui_convertVecDialog(object):
    def setupUi(self, convertVecDialog):
        convertVecDialog.setObjectName(_fromUtf8("convertVecDialog"))
        convertVecDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        convertVecDialog.resize(590, 460)
        convertVecDialog.setMinimumSize(QtCore.QSize(590, 460))
        self.selectLabel = QtGui.QLabel(convertVecDialog)
        self.selectLabel.setGeometry(QtCore.QRect(120, 20, 301, 16))
        self.selectLabel.setObjectName(_fromUtf8("selectLabel"))
        self.selectListWidget = QtGui.QListWidget(convertVecDialog)
        self.selectListWidget.setGeometry(QtCore.QRect(130, 50, 441, 171))
        self.selectListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.selectListWidget.setObjectName(_fromUtf8("selectListWidget"))
        self.okButton = QtGui.QPushButton(convertVecDialog)
        self.okButton.setGeometry(QtCore.QRect(230, 420, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(convertVecDialog)
        self.cancelButton.setGeometry(QtCore.QRect(350, 420, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.idfieldLineEdit = QtGui.QLineEdit(convertVecDialog)
        self.idfieldLineEdit.setGeometry(QtCore.QRect(300, 240, 100, 20))
        self.idfieldLineEdit.setObjectName(_fromUtf8("idfieldLineEdit"))
        self.idfieldLabel = QtGui.QLabel(convertVecDialog)
        self.idfieldLabel.setGeometry(QtCore.QRect(130, 240, 141, 16))
        self.idfieldLabel.setMinimumSize(QtCore.QSize(141, 16))
        self.idfieldLabel.setObjectName(_fromUtf8("idfieldLabel"))
        self.convLineEdit = QtGui.QLineEdit(convertVecDialog)
        self.convLineEdit.setGeometry(QtCore.QRect(300, 360, 100, 20))
        self.convLineEdit.setObjectName(_fromUtf8("convLineEdit"))
        self.convLabel = QtGui.QLabel(convertVecDialog)
        self.convLabel.setGeometry(QtCore.QRect(150, 360, 141, 16))
        self.convLabel.setMinimumSize(QtCore.QSize(141, 16))
        self.convLabel.setObjectName(_fromUtf8("convLabel"))
        self.noneRadioButton = QtGui.QRadioButton(convertVecDialog)
        self.noneRadioButton.setGeometry(QtCore.QRect(130, 290, 431, 17))
        self.noneRadioButton.setMinimumSize(QtCore.QSize(431, 17))
        self.noneRadioButton.setObjectName(_fromUtf8("noneRadioButton"))
        self.userRadioButton = QtGui.QRadioButton(convertVecDialog)
        self.userRadioButton.setGeometry(QtCore.QRect(130, 330, 201, 17))
        self.userRadioButton.setObjectName(_fromUtf8("userRadioButton"))
        self.logoLabel = QtGui.QLabel(convertVecDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-20, 10, 131, 401))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))

        self.retranslateUi(convertVecDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), convertVecDialog.close)
        QtCore.QObject.connect(self.userRadioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.convLabel.setEnabled)
        QtCore.QObject.connect(self.userRadioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.convLineEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(convertVecDialog)

    def retranslateUi(self, convertVecDialog):
        convertVecDialog.setWindowTitle(_translate("convertVecDialog", "Convert polylines or polygons to abundance data", None))
        self.selectLabel.setText(_translate("convertVecDialog", "Select themes to import data into Marxan", None))
        self.okButton.setText(_translate("convertVecDialog", "OK", None))
        self.cancelButton.setText(_translate("convertVecDialog", "Cancel", None))
        self.idfieldLabel.setText(_translate("convertVecDialog", "Layer ID field name", None))
        self.convLabel.setText(_translate("convertVecDialog", "Area conversion value", None))
        self.noneRadioButton.setText(_translate("convertVecDialog", "No conversion (results will be in layer measurement units)", None))
        self.userRadioButton.setText(_translate("convertVecDialog", "User defined conversion", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    convertVecDialog = QtGui.QDialog()
    ui = Ui_convertVecDialog()
    ui.setupUi(convertVecDialog)
    convertVecDialog.show()
    sys.exit(app.exec_())

