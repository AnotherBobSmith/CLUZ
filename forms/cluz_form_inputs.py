# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_inputs.ui'
#
# Created: Sun Mar 08 10:57:36 2015
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

class Ui_inputsDialog(object):
    def setupUi(self, inputsDialog):
        inputsDialog.setObjectName(_fromUtf8("inputsDialog"))
        inputsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        inputsDialog.resize(498, 377)
        self.targetBox = QtGui.QCheckBox(inputsDialog)
        self.targetBox.setGeometry(QtCore.QRect(210, 60, 141, 17))
        self.targetBox.setObjectName(_fromUtf8("targetBox"))
        self.puBox = QtGui.QCheckBox(inputsDialog)
        self.puBox.setGeometry(QtCore.QRect(210, 110, 161, 17))
        self.puBox.setObjectName(_fromUtf8("puBox"))
        self.inputsLabel = QtGui.QLabel(inputsDialog)
        self.inputsLabel.setGeometry(QtCore.QRect(200, 30, 301, 16))
        self.inputsLabel.setObjectName(_fromUtf8("inputsLabel"))
        self.boundBox = QtGui.QCheckBox(inputsDialog)
        self.boundBox.setGeometry(QtCore.QRect(210, 160, 161, 17))
        self.boundBox.setObjectName(_fromUtf8("boundBox"))
        self.boundextBox = QtGui.QCheckBox(inputsDialog)
        self.boundextBox.setGeometry(QtCore.QRect(250, 190, 281, 17))
        self.boundextBox.setObjectName(_fromUtf8("boundextBox"))
        self.okButton = QtGui.QPushButton(inputsDialog)
        self.okButton.setGeometry(QtCore.QRect(260, 320, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(inputsDialog)
        self.cancelButton.setGeometry(QtCore.QRect(360, 320, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.sponsorLabel = QtGui.QLabel(inputsDialog)
        self.sponsorLabel.setGeometry(QtCore.QRect(20, 10, 151, 351))
        self.sponsorLabel.setText(_fromUtf8(""))
        self.sponsorLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo.png")))
        self.sponsorLabel.setObjectName(_fromUtf8("sponsorLabel"))

        self.retranslateUi(inputsDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), inputsDialog.close)
        QtCore.QObject.connect(self.boundBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.boundextBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(inputsDialog)

    def retranslateUi(self, inputsDialog):
        inputsDialog.setWindowTitle(_translate("inputsDialog", "Create Marxan files", None))
        self.targetBox.setText(_translate("inputsDialog", "Target file (spec.dat)", None))
        self.puBox.setText(_translate("inputsDialog", "Planning unit file (pu.dat)", None))
        self.inputsLabel.setText(_translate("inputsDialog", "Create the following Marxan files from the CLUZ files:", None))
        self.boundBox.setText(_translate("inputsDialog", "Boundary file (bound.dat)", None))
        self.boundextBox.setText(_translate("inputsDialog", "Include planning region boundaries", None))
        self.okButton.setText(_translate("inputsDialog", "OK", None))
        self.cancelButton.setText(_translate("inputsDialog", "Cancel", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    inputsDialog = QtGui.QDialog()
    ui = Ui_inputsDialog()
    ui.setupUi(inputsDialog)
    inputsDialog.show()
    sys.exit(app.exec_())

