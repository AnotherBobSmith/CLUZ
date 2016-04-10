# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_inputs.ui'
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

class Ui_inputsDialog(object):
    def setupUi(self, inputsDialog):
        inputsDialog.setObjectName(_fromUtf8("inputsDialog"))
        inputsDialog.resize(620, 390)
        inputsDialog.setMinimumSize(QtCore.QSize(620, 390))
        self.sponsorLabel = QtGui.QLabel(inputsDialog)
        self.sponsorLabel.setGeometry(QtCore.QRect(20, 10, 151, 351))
        self.sponsorLabel.setText(_fromUtf8(""))
        self.sponsorLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo.png")))
        self.sponsorLabel.setObjectName(_fromUtf8("sponsorLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(inputsDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(280, 300, 201, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.inputsLabel = QtGui.QLabel(inputsDialog)
        self.inputsLabel.setGeometry(QtCore.QRect(190, 30, 421, 16))
        self.inputsLabel.setObjectName(_fromUtf8("inputsLabel"))
        self.verticalLayoutWidget = QtGui.QWidget(inputsDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(190, 60, 371, 151))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.targetBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.targetBox.setObjectName(_fromUtf8("targetBox"))
        self.verticalLayout.addWidget(self.targetBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.puBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.puBox.setObjectName(_fromUtf8("puBox"))
        self.verticalLayout.addWidget(self.puBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.boundBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.boundBox.setObjectName(_fromUtf8("boundBox"))
        self.verticalLayout.addWidget(self.boundBox)
        self.boundextBox = QtGui.QCheckBox(inputsDialog)
        self.boundextBox.setGeometry(QtCore.QRect(230, 220, 351, 24))
        self.boundextBox.setMinimumSize(QtCore.QSize(0, 24))
        self.boundextBox.setObjectName(_fromUtf8("boundextBox"))

        self.retranslateUi(inputsDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), inputsDialog.close)
        QtCore.QObject.connect(self.boundBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.boundextBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(inputsDialog)

    def retranslateUi(self, inputsDialog):
        inputsDialog.setWindowTitle(_translate("inputsDialog", "Create Marxan files", None))
        self.okButton.setText(_translate("inputsDialog", "OK", None))
        self.cancelButton.setText(_translate("inputsDialog", "Cancel", None))
        self.inputsLabel.setText(_translate("inputsDialog", "Create the following Marxan files from the CLUZ files:", None))
        self.targetBox.setText(_translate("inputsDialog", "Target file (spec.dat)", None))
        self.puBox.setText(_translate("inputsDialog", "Planning unit file (pu.dat)", None))
        self.boundBox.setText(_translate("inputsDialog", "Boundary file (bound.dat)", None))
        self.boundextBox.setText(_translate("inputsDialog", "Include planning region boundaries", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    inputsDialog = QtGui.QDialog()
    ui = Ui_inputsDialog()
    ui.setupUi(inputsDialog)
    inputsDialog.show()
    sys.exit(app.exec_())

