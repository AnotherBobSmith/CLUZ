# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_load.ui'
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

class Ui_loadDialog(object):
    def setupUi(self, loadDialog):
        loadDialog.setObjectName(_fromUtf8("loadDialog"))
        loadDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        loadDialog.resize(620, 380)
        loadDialog.setMinimumSize(QtCore.QSize(620, 380))
        self.okButton = QtGui.QPushButton(loadDialog)
        self.okButton.setGeometry(QtCore.QRect(240, 330, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.summedLineEdit = QtGui.QLineEdit(loadDialog)
        self.summedLineEdit.setGeometry(QtCore.QRect(120, 210, 400, 20))
        self.summedLineEdit.setObjectName(_fromUtf8("summedLineEdit"))
        self.summedButton = QtGui.QPushButton(loadDialog)
        self.summedButton.setGeometry(QtCore.QRect(530, 210, 75, 23))
        self.summedButton.setObjectName(_fromUtf8("summedButton"))
        self.bestButton = QtGui.QPushButton(loadDialog)
        self.bestButton.setGeometry(QtCore.QRect(530, 60, 75, 23))
        self.bestButton.setObjectName(_fromUtf8("bestButton"))
        self.bestLineEdit = QtGui.QLineEdit(loadDialog)
        self.bestLineEdit.setGeometry(QtCore.QRect(120, 60, 400, 20))
        self.bestLineEdit.setMaxLength(32766)
        self.bestLineEdit.setObjectName(_fromUtf8("bestLineEdit"))
        self.bestCheckBox = QtGui.QCheckBox(loadDialog)
        self.bestCheckBox.setGeometry(QtCore.QRect(120, 30, 441, 17))
        self.bestCheckBox.setObjectName(_fromUtf8("bestCheckBox"))
        self.summedCheckBox = QtGui.QCheckBox(loadDialog)
        self.summedCheckBox.setGeometry(QtCore.QRect(120, 180, 441, 17))
        self.summedCheckBox.setObjectName(_fromUtf8("summedCheckBox"))
        self.bestLabel = QtGui.QLabel(loadDialog)
        self.bestLabel.setGeometry(QtCore.QRect(120, 90, 281, 16))
        self.bestLabel.setObjectName(_fromUtf8("bestLabel"))
        self.bestNameLineEdit = QtGui.QLineEdit(loadDialog)
        self.bestNameLineEdit.setGeometry(QtCore.QRect(120, 110, 200, 20))
        self.bestNameLineEdit.setObjectName(_fromUtf8("bestNameLineEdit"))
        self.summedNameLineEdit = QtGui.QLineEdit(loadDialog)
        self.summedNameLineEdit.setGeometry(QtCore.QRect(120, 260, 200, 20))
        self.summedNameLineEdit.setObjectName(_fromUtf8("summedNameLineEdit"))
        self.summedLabel = QtGui.QLabel(loadDialog)
        self.summedLabel.setGeometry(QtCore.QRect(120, 240, 301, 16))
        self.summedLabel.setObjectName(_fromUtf8("summedLabel"))
        self.logoLabel = QtGui.QLabel(loadDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-20, 0, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.cancelButton = QtGui.QPushButton(loadDialog)
        self.cancelButton.setGeometry(QtCore.QRect(370, 330, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))

        self.retranslateUi(loadDialog)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.summedLineEdit.setVisible)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), loadDialog.close)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.summedButton.setVisible)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.bestLineEdit.setVisible)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.bestButton.setVisible)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.bestLabel.setVisible)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.bestNameLineEdit.setVisible)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.summedLabel.setVisible)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.summedNameLineEdit.setVisible)
        QtCore.QMetaObject.connectSlotsByName(loadDialog)

    def retranslateUi(self, loadDialog):
        loadDialog.setWindowTitle(_translate("loadDialog", "Select or create CLUZ setup file", None))
        self.okButton.setText(_translate("loadDialog", "OK", None))
        self.summedButton.setText(_translate("loadDialog", "Browse", None))
        self.bestButton.setText(_translate("loadDialog", "Browse", None))
        self.bestCheckBox.setText(_translate("loadDialog", "Load best solution results (default name is *_best.txt)", None))
        self.summedCheckBox.setText(_translate("loadDialog", "Load summed solution results (default name is *_ssoln.txt)", None))
        self.bestLabel.setText(_translate("loadDialog", "New best field name", None))
        self.summedLabel.setText(_translate("loadDialog", "New summed solution field name", None))
        self.cancelButton.setText(_translate("loadDialog", "Cancel", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    loadDialog = QtGui.QDialog()
    ui = Ui_loadDialog()
    ui.setupUi(loadDialog)
    loadDialog.show()
    sys.exit(app.exec_())

