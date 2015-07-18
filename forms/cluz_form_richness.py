# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_richness.ui'
#
# Created: Sat Jul 11 16:31:59 2015
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

class Ui_richnessDialog(object):
    def setupUi(self, richnessDialog):
        richnessDialog.setObjectName(_fromUtf8("richnessDialog"))
        richnessDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        richnessDialog.resize(482, 585)
        self.countBox = QtGui.QCheckBox(richnessDialog)
        self.countBox.setGeometry(QtCore.QRect(180, 60, 241, 17))
        self.countBox.setObjectName(_fromUtf8("countBox"))
        self.rangeBox = QtGui.QCheckBox(richnessDialog)
        self.rangeBox.setGeometry(QtCore.QRect(180, 140, 161, 17))
        self.rangeBox.setObjectName(_fromUtf8("rangeBox"))
        self.inputsLabel = QtGui.QLabel(richnessDialog)
        self.inputsLabel.setGeometry(QtCore.QRect(170, 30, 301, 16))
        self.inputsLabel.setObjectName(_fromUtf8("inputsLabel"))
        self.okButton = QtGui.QPushButton(richnessDialog)
        self.okButton.setGeometry(QtCore.QRect(230, 510, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(richnessDialog)
        self.cancelButton.setGeometry(QtCore.QRect(330, 510, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.logoLabel = QtGui.QLabel(richnessDialog)
        self.logoLabel.setGeometry(QtCore.QRect(10, 30, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.typeLabel = QtGui.QLabel(richnessDialog)
        self.typeLabel.setGeometry(QtCore.QRect(170, 320, 301, 16))
        self.typeLabel.setObjectName(_fromUtf8("typeLabel"))
        self.typeListWidget = QtGui.QListWidget(richnessDialog)
        self.typeListWidget.setGeometry(QtCore.QRect(180, 350, 256, 131))
        self.typeListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.typeListWidget.setObjectName(_fromUtf8("typeListWidget"))
        self.countLabel = QtGui.QLabel(richnessDialog)
        self.countLabel.setEnabled(False)
        self.countLabel.setGeometry(QtCore.QRect(180, 90, 61, 16))
        self.countLabel.setObjectName(_fromUtf8("countLabel"))
        self.rangeLabel = QtGui.QLabel(richnessDialog)
        self.rangeLabel.setEnabled(False)
        self.rangeLabel.setGeometry(QtCore.QRect(180, 170, 61, 16))
        self.rangeLabel.setObjectName(_fromUtf8("rangeLabel"))
        self.countLineEdit = QtGui.QLineEdit(richnessDialog)
        self.countLineEdit.setEnabled(False)
        self.countLineEdit.setGeometry(QtCore.QRect(240, 90, 201, 20))
        self.countLineEdit.setObjectName(_fromUtf8("countLineEdit"))
        self.rangeLineEdit = QtGui.QLineEdit(richnessDialog)
        self.rangeLineEdit.setEnabled(False)
        self.rangeLineEdit.setGeometry(QtCore.QRect(240, 170, 201, 20))
        self.rangeLineEdit.setObjectName(_fromUtf8("rangeLineEdit"))

        self.retranslateUi(richnessDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), richnessDialog.close)
        QtCore.QObject.connect(self.countBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.countLabel.setEnabled)
        QtCore.QObject.connect(self.countBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.countLineEdit.setEnabled)
        QtCore.QObject.connect(self.rangeBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.rangeLabel.setEnabled)
        QtCore.QObject.connect(self.rangeBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.rangeLineEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(richnessDialog)

    def retranslateUi(self, richnessDialog):
        richnessDialog.setWindowTitle(_translate("richnessDialog", "Create Marxan files", None))
        self.countBox.setText(_translate("richnessDialog", "Feature Count", None))
        self.rangeBox.setText(_translate("richnessDialog", "Restricted Range Score", None))
        self.inputsLabel.setText(_translate("richnessDialog", "Calculate the following for each planning unit:", None))
        self.okButton.setText(_translate("richnessDialog", "OK", None))
        self.cancelButton.setText(_translate("richnessDialog", "Cancel", None))
        self.typeLabel.setText(_translate("richnessDialog", "Use features with type codes from the target file:", None))
        self.countLabel.setText(_translate("richnessDialog", "Field name", None))
        self.rangeLabel.setText(_translate("richnessDialog", "Field name", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    richnessDialog = QtGui.QDialog()
    ui = Ui_richnessDialog()
    ui.setupUi(richnessDialog)
    richnessDialog.show()
    sys.exit(app.exec_())

