# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_abund_select.ui'
#
# Created: Sun Mar 08 11:23:23 2015
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

class Ui_abundSelectDialog(object):
    def setupUi(self, abundSelectDialog):
        abundSelectDialog.setObjectName(_fromUtf8("abundSelectDialog"))
        abundSelectDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        abundSelectDialog.resize(622, 580)
        self.featLabel = QtGui.QLabel(abundSelectDialog)
        self.featLabel.setGeometry(QtCore.QRect(150, 20, 371, 16))
        self.featLabel.setObjectName(_fromUtf8("featLabel"))
        self.featListWidget = QtGui.QListWidget(abundSelectDialog)
        self.featListWidget.setGeometry(QtCore.QRect(150, 40, 450, 481))
        self.featListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.featListWidget.setObjectName(_fromUtf8("featListWidget"))
        self.okButton = QtGui.QPushButton(abundSelectDialog)
        self.okButton.setGeometry(QtCore.QRect(250, 540, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(abundSelectDialog)
        self.cancelButton.setGeometry(QtCore.QRect(370, 540, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.logoLabel = QtGui.QLabel(abundSelectDialog)
        self.logoLabel.setGeometry(QtCore.QRect(0, 20, 131, 351))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))

        self.retranslateUi(abundSelectDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), abundSelectDialog.close)
        QtCore.QMetaObject.connectSlotsByName(abundSelectDialog)

    def retranslateUi(self, abundSelectDialog):
        abundSelectDialog.setWindowTitle(_translate("abundSelectDialog", "Select features for Abundance table", None))
        self.featLabel.setText(_translate("abundSelectDialog", "Display all or select conservation features to display in abundance table", None))
        self.okButton.setText(_translate("abundSelectDialog", "OK", None))
        self.cancelButton.setText(_translate("abundSelectDialog", "Cancel", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    abundSelectDialog = QtGui.QDialog()
    ui = Ui_abundSelectDialog()
    ui.setupUi(abundSelectDialog)
    abundSelectDialog.show()
    sys.exit(app.exec_())

