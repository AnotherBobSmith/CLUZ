# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_setup.ui'
#
# Created: Sun Mar 08 10:52:02 2015
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

class Ui_setupDialog(object):
    def setupUi(self, setupDialog):
        setupDialog.setObjectName(_fromUtf8("setupDialog"))
        setupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        setupDialog.resize(763, 395)
        self.saveasButton = QtGui.QPushButton(setupDialog)
        self.saveasButton.setGeometry(QtCore.QRect(470, 350, 75, 23))
        self.saveasButton.setObjectName(_fromUtf8("saveasButton"))
        self.cancelButton = QtGui.QPushButton(setupDialog)
        self.cancelButton.setGeometry(QtCore.QRect(590, 350, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.marxanButton = QtGui.QPushButton(setupDialog)
        self.marxanButton.setGeometry(QtCore.QRect(660, 30, 75, 23))
        self.marxanButton.setObjectName(_fromUtf8("marxanButton"))
        self.inputButton = QtGui.QPushButton(setupDialog)
        self.inputButton.setGeometry(QtCore.QRect(660, 70, 75, 23))
        self.inputButton.setObjectName(_fromUtf8("inputButton"))
        self.outputButton = QtGui.QPushButton(setupDialog)
        self.outputButton.setGeometry(QtCore.QRect(660, 110, 75, 23))
        self.outputButton.setObjectName(_fromUtf8("outputButton"))
        self.puButton = QtGui.QPushButton(setupDialog)
        self.puButton.setGeometry(QtCore.QRect(660, 150, 75, 23))
        self.puButton.setObjectName(_fromUtf8("puButton"))
        self.targButton = QtGui.QPushButton(setupDialog)
        self.targButton.setGeometry(QtCore.QRect(660, 190, 75, 23))
        self.targButton.setObjectName(_fromUtf8("targButton"))
        self.marxanLabel = QtGui.QLabel(setupDialog)
        self.marxanLabel.setGeometry(QtCore.QRect(180, 30, 110, 16))
        self.marxanLabel.setObjectName(_fromUtf8("marxanLabel"))
        self.inputLabel = QtGui.QLabel(setupDialog)
        self.inputLabel.setGeometry(QtCore.QRect(180, 70, 110, 16))
        self.inputLabel.setObjectName(_fromUtf8("inputLabel"))
        self.outputLabel = QtGui.QLabel(setupDialog)
        self.outputLabel.setGeometry(QtCore.QRect(180, 110, 110, 16))
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.puLabel = QtGui.QLabel(setupDialog)
        self.puLabel.setGeometry(QtCore.QRect(180, 150, 110, 16))
        self.puLabel.setObjectName(_fromUtf8("puLabel"))
        self.targetLabel = QtGui.QLabel(setupDialog)
        self.targetLabel.setGeometry(QtCore.QRect(180, 190, 110, 16))
        self.targetLabel.setObjectName(_fromUtf8("targetLabel"))
        self.marxanLineEdit = QtGui.QLineEdit(setupDialog)
        self.marxanLineEdit.setGeometry(QtCore.QRect(290, 30, 350, 20))
        self.marxanLineEdit.setObjectName(_fromUtf8("marxanLineEdit"))
        self.inputLineEdit = QtGui.QLineEdit(setupDialog)
        self.inputLineEdit.setGeometry(QtCore.QRect(290, 70, 350, 20))
        self.inputLineEdit.setObjectName(_fromUtf8("inputLineEdit"))
        self.outputLineEdit = QtGui.QLineEdit(setupDialog)
        self.outputLineEdit.setGeometry(QtCore.QRect(290, 110, 350, 20))
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.targLineEdit = QtGui.QLineEdit(setupDialog)
        self.targLineEdit.setGeometry(QtCore.QRect(290, 190, 350, 20))
        self.targLineEdit.setObjectName(_fromUtf8("targLineEdit"))
        self.puLineEdit = QtGui.QLineEdit(setupDialog)
        self.puLineEdit.setGeometry(QtCore.QRect(290, 150, 350, 20))
        self.puLineEdit.setObjectName(_fromUtf8("puLineEdit"))
        self.loadButton = QtGui.QPushButton(setupDialog)
        self.loadButton.setGeometry(QtCore.QRect(230, 350, 75, 23))
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.saveButton = QtGui.QPushButton(setupDialog)
        self.saveButton.setGeometry(QtCore.QRect(350, 350, 75, 23))
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.setupIconLabel = QtGui.QLabel(setupDialog)
        self.setupIconLabel.setGeometry(QtCore.QRect(10, 10, 141, 381))
        self.setupIconLabel.setText(_fromUtf8(""))
        self.setupIconLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.setupIconLabel.setObjectName(_fromUtf8("setupIconLabel"))
        self.setupPathLabel = QtGui.QLabel(setupDialog)
        self.setupPathLabel.setGeometry(QtCore.QRect(180, 280, 450, 16))
        self.setupPathLabel.setObjectName(_fromUtf8("setupPathLabel"))
        self.precLabel = QtGui.QLabel(setupDialog)
        self.precLabel.setGeometry(QtCore.QRect(180, 230, 321, 16))
        self.precLabel.setObjectName(_fromUtf8("precLabel"))
        self.precComboBox = QtGui.QComboBox(setupDialog)
        self.precComboBox.setGeometry(QtCore.QRect(520, 230, 121, 22))
        self.precComboBox.setObjectName(_fromUtf8("precComboBox"))

        self.retranslateUi(setupDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), setupDialog.close)
        QtCore.QMetaObject.connectSlotsByName(setupDialog)

    def retranslateUi(self, setupDialog):
        setupDialog.setWindowTitle(_translate("setupDialog", "Setup file settings", None))
        self.saveasButton.setText(_translate("setupDialog", "Save As...", None))
        self.cancelButton.setText(_translate("setupDialog", "Close", None))
        self.marxanButton.setText(_translate("setupDialog", "Browse...", None))
        self.inputButton.setText(_translate("setupDialog", "Browse...", None))
        self.outputButton.setText(_translate("setupDialog", "Browse...", None))
        self.puButton.setText(_translate("setupDialog", "Browse...", None))
        self.targButton.setText(_translate("setupDialog", "Browse...", None))
        self.marxanLabel.setText(_translate("setupDialog", "Marxan location", None))
        self.inputLabel.setText(_translate("setupDialog", "Input directory", None))
        self.outputLabel.setText(_translate("setupDialog", "Output directory", None))
        self.puLabel.setText(_translate("setupDialog", "Planning unit theme", None))
        self.targetLabel.setText(_translate("setupDialog", "Target table", None))
        self.marxanLineEdit.setText(_translate("setupDialog", "blank", None))
        self.inputLineEdit.setText(_translate("setupDialog", "blank", None))
        self.outputLineEdit.setText(_translate("setupDialog", "blank", None))
        self.targLineEdit.setText(_translate("setupDialog", "blank", None))
        self.puLineEdit.setText(_translate("setupDialog", "blank", None))
        self.loadButton.setText(_translate("setupDialog", "Load", None))
        self.saveButton.setText(_translate("setupDialog", "Save", None))
        self.setupPathLabel.setText(_translate("setupDialog", "Setup file location: blank", None))
        self.precLabel.setText(_translate("setupDialog", "Decimal places for numbers in Abundance and Target tables", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    setupDialog = QtGui.QDialog()
    ui = Ui_setupDialog()
    ui.setupUi(setupDialog)
    setupDialog.show()
    sys.exit(app.exec_())

