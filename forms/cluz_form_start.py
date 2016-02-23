# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_start.ui'
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

class Ui_startDialog(object):
    def setupUi(self, startDialog):
        startDialog.setObjectName(_fromUtf8("startDialog"))
        startDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        startDialog.resize(320, 250)
        startDialog.setMinimumSize(QtCore.QSize(320, 250))
        self.okButton = QtGui.QPushButton(startDialog)
        self.okButton.setGeometry(QtCore.QRect(70, 210, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(startDialog)
        self.cancelButton.setGeometry(QtCore.QRect(200, 210, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.openRadioButton = QtGui.QRadioButton(startDialog)
        self.openRadioButton.setGeometry(QtCore.QRect(80, 120, 211, 17))
        self.openRadioButton.setMinimumSize(QtCore.QSize(211, 17))
        self.openRadioButton.setChecked(True)
        self.openRadioButton.setObjectName(_fromUtf8("openRadioButton"))
        self.startButtonGroup = QtGui.QButtonGroup(startDialog)
        self.startButtonGroup.setObjectName(_fromUtf8("startButtonGroup"))
        self.startButtonGroup.addButton(self.openRadioButton)
        self.createButton = QtGui.QRadioButton(startDialog)
        self.createButton.setGeometry(QtCore.QRect(80, 150, 211, 17))
        self.createButton.setMinimumSize(QtCore.QSize(211, 17))
        self.createButton.setCheckable(True)
        self.createButton.setObjectName(_fromUtf8("createButton"))
        self.startButtonGroup.addButton(self.createButton)
        self.instructionsLabel = QtGui.QLabel(startDialog)
        self.instructionsLabel.setGeometry(QtCore.QRect(80, 10, 230, 91))
        self.instructionsLabel.setMinimumSize(QtCore.QSize(230, 91))
        self.instructionsLabel.setObjectName(_fromUtf8("instructionsLabel"))
        self.graphicLabel = QtGui.QLabel(startDialog)
        self.graphicLabel.setGeometry(QtCore.QRect(10, 20, 51, 51))
        self.graphicLabel.setText(_fromUtf8(""))
        self.graphicLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo_small.png")))
        self.graphicLabel.setObjectName(_fromUtf8("graphicLabel"))

        self.retranslateUi(startDialog)
        QtCore.QMetaObject.connectSlotsByName(startDialog)

    def retranslateUi(self, startDialog):
        startDialog.setWindowTitle(_translate("startDialog", "Select or create CLUZ setup file", None))
        self.okButton.setText(_translate("startDialog", "OK", None))
        self.cancelButton.setText(_translate("startDialog", "Cancel", None))
        self.openRadioButton.setText(_translate("startDialog", "Open existing setup file", None))
        self.createButton.setText(_translate("startDialog", "Create new setup file", None))
        self.instructionsLabel.setText(_translate("startDialog", "The selected action cannot continue\n"
" because a CLUZ setup file has not\n"
" been specified.\n"
"\n"
"Please open an existing setup file or\n"
"create a new one.", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    startDialog = QtGui.QDialog()
    ui = Ui_startDialog()
    ui.setupUi(startDialog)
    startDialog.show()
    sys.exit(app.exec_())

