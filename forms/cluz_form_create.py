# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_create.ui'
#
# Created: Sun Mar 08 11:02:31 2015
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

class Ui_createDialog(object):
    def setupUi(self, createDialog):
        createDialog.setObjectName(_fromUtf8("createDialog"))
        createDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        createDialog.resize(670, 376)
        self.okButton = QtGui.QPushButton(createDialog)
        self.okButton.setGeometry(QtCore.QRect(280, 320, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.inputLineEdit = QtGui.QLineEdit(createDialog)
        self.inputLineEdit.setGeometry(QtCore.QRect(160, 180, 400, 20))
        self.inputLineEdit.setObjectName(_fromUtf8("inputLineEdit"))
        self.inputButton = QtGui.QPushButton(createDialog)
        self.inputButton.setGeometry(QtCore.QRect(570, 180, 75, 20))
        self.inputButton.setObjectName(_fromUtf8("inputButton"))
        self.puButton = QtGui.QPushButton(createDialog)
        self.puButton.setGeometry(QtCore.QRect(570, 40, 75, 20))
        self.puButton.setObjectName(_fromUtf8("puButton"))
        self.puLineEdit = QtGui.QLineEdit(createDialog)
        self.puLineEdit.setGeometry(QtCore.QRect(160, 40, 400, 20))
        self.puLineEdit.setMaxLength(32766)
        self.puLineEdit.setObjectName(_fromUtf8("puLineEdit"))
        self.convLabel = QtGui.QLabel(createDialog)
        self.convLabel.setGeometry(QtCore.QRect(160, 70, 111, 16))
        self.convLabel.setObjectName(_fromUtf8("convLabel"))
        self.convLineEdit = QtGui.QLineEdit(createDialog)
        self.convLineEdit.setGeometry(QtCore.QRect(280, 70, 101, 20))
        self.convLineEdit.setObjectName(_fromUtf8("convLineEdit"))
        self.targetLineEdit = QtGui.QLineEdit(createDialog)
        self.targetLineEdit.setGeometry(QtCore.QRect(160, 260, 400, 20))
        self.targetLineEdit.setObjectName(_fromUtf8("targetLineEdit"))
        self.logoLabel = QtGui.QLabel(createDialog)
        self.logoLabel.setGeometry(QtCore.QRect(10, 0, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.cancelButton = QtGui.QPushButton(createDialog)
        self.cancelButton.setGeometry(QtCore.QRect(410, 320, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.equalCheckBox = QtGui.QCheckBox(createDialog)
        self.equalCheckBox.setGeometry(QtCore.QRect(160, 100, 251, 17))
        self.equalCheckBox.setObjectName(_fromUtf8("equalCheckBox"))
        self.targetButton = QtGui.QPushButton(createDialog)
        self.targetButton.setGeometry(QtCore.QRect(570, 260, 75, 20))
        self.targetButton.setObjectName(_fromUtf8("targetButton"))
        self.puLabel = QtGui.QLabel(createDialog)
        self.puLabel.setGeometry(QtCore.QRect(160, 20, 331, 16))
        self.puLabel.setObjectName(_fromUtf8("puLabel"))
        self.inputLabel = QtGui.QLabel(createDialog)
        self.inputLabel.setGeometry(QtCore.QRect(160, 160, 331, 16))
        self.inputLabel.setObjectName(_fromUtf8("inputLabel"))
        self.targetLabel = QtGui.QLabel(createDialog)
        self.targetLabel.setGeometry(QtCore.QRect(160, 240, 331, 16))
        self.targetLabel.setObjectName(_fromUtf8("targetLabel"))
        self.convHintLabel1 = QtGui.QLabel(createDialog)
        self.convHintLabel1.setGeometry(QtCore.QRect(390, 65, 141, 16))
        self.convHintLabel1.setObjectName(_fromUtf8("convHintLabel1"))
        self.convHintLabel2 = QtGui.QLabel(createDialog)
        self.convHintLabel2.setGeometry(QtCore.QRect(390, 80, 151, 16))
        self.convHintLabel2.setObjectName(_fromUtf8("convHintLabel2"))

        self.retranslateUi(createDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), createDialog.close)
        QtCore.QMetaObject.connectSlotsByName(createDialog)

    def retranslateUi(self, createDialog):
        createDialog.setWindowTitle(_translate("createDialog", "Create CLUZ files", None))
        self.okButton.setText(_translate("createDialog", "OK", None))
        self.inputButton.setText(_translate("createDialog", "Browse", None))
        self.puButton.setText(_translate("createDialog", "Browse", None))
        self.convLabel.setText(_translate("createDialog", "Area conversion factor", None))
        self.cancelButton.setText(_translate("createDialog", "Cancel", None))
        self.equalCheckBox.setText(_translate("createDialog", "Set cost layer as equal to planning unit area", None))
        self.targetButton.setText(_translate("createDialog", "Save As", None))
        self.puLabel.setText(_translate("createDialog", "Select shapefile that will be used to produce the planning unit layer", None))
        self.inputLabel.setText(_translate("createDialog", "Specify input folder where puvspr2.dat file will be created", None))
        self.targetLabel.setText(_translate("createDialog", "Name of target table to be created", None))
        self.convHintLabel1.setText(_translate("createDialog", "10000 to convert m2 to ha", None))
        self.convHintLabel2.setText(_translate("createDialog", "1000000 to convert m2 to km2", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    createDialog = QtGui.QDialog()
    ui = Ui_createDialog()
    ui.setupUi(createDialog)
    createDialog.show()
    sys.exit(app.exec_())

