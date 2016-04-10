# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_create.ui'
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

class Ui_createDialog(object):
    def setupUi(self, createDialog):
        createDialog.setObjectName(_fromUtf8("createDialog"))
        createDialog.resize(760, 454)
        createDialog.setMinimumSize(QtCore.QSize(760, 450))
        self.logoLabel = QtGui.QLabel(createDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, 0, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(createDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(310, 380, 201, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setMinimumSize(QtCore.QSize(0, 24))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setMinimumSize(QtCore.QSize(0, 24))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.puLabel = QtGui.QLabel(createDialog)
        self.puLabel.setGeometry(QtCore.QRect(140, 20, 571, 16))
        self.puLabel.setObjectName(_fromUtf8("puLabel"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(createDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(140, 50, 601, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.puLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.puLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.puLineEdit.setMaxLength(32766)
        self.puLineEdit.setObjectName(_fromUtf8("puLineEdit"))
        self.horizontalLayout_2.addWidget(self.puLineEdit)
        self.puButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.puButton.setMinimumSize(QtCore.QSize(0, 24))
        self.puButton.setObjectName(_fromUtf8("puButton"))
        self.horizontalLayout_2.addWidget(self.puButton)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(createDialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(140, 100, 351, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.convLabel = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.convLabel.setMinimumSize(QtCore.QSize(111, 16))
        self.convLabel.setObjectName(_fromUtf8("convLabel"))
        self.horizontalLayout_3.addWidget(self.convLabel)
        self.convLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
        self.convLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.convLineEdit.setObjectName(_fromUtf8("convLineEdit"))
        self.horizontalLayout_3.addWidget(self.convLineEdit)
        self.convHintLabel1 = QtGui.QLabel(createDialog)
        self.convHintLabel1.setGeometry(QtCore.QRect(500, 100, 241, 16))
        self.convHintLabel1.setMinimumSize(QtCore.QSize(171, 16))
        self.convHintLabel1.setObjectName(_fromUtf8("convHintLabel1"))
        self.convHintLabel2 = QtGui.QLabel(createDialog)
        self.convHintLabel2.setGeometry(QtCore.QRect(500, 120, 251, 16))
        self.convHintLabel2.setMinimumSize(QtCore.QSize(171, 16))
        self.convHintLabel2.setObjectName(_fromUtf8("convHintLabel2"))
        self.equalCheckBox = QtGui.QCheckBox(createDialog)
        self.equalCheckBox.setGeometry(QtCore.QRect(160, 150, 581, 24))
        self.equalCheckBox.setMinimumSize(QtCore.QSize(401, 24))
        self.equalCheckBox.setObjectName(_fromUtf8("equalCheckBox"))
        self.inputLabel = QtGui.QLabel(createDialog)
        self.inputLabel.setGeometry(QtCore.QRect(140, 210, 601, 16))
        self.inputLabel.setObjectName(_fromUtf8("inputLabel"))
        self.horizontalLayoutWidget_4 = QtGui.QWidget(createDialog)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(140, 230, 601, 41))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.inputLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_4)
        self.inputLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.inputLineEdit.setObjectName(_fromUtf8("inputLineEdit"))
        self.horizontalLayout_4.addWidget(self.inputLineEdit)
        self.inputButton = QtGui.QPushButton(self.horizontalLayoutWidget_4)
        self.inputButton.setMinimumSize(QtCore.QSize(0, 24))
        self.inputButton.setObjectName(_fromUtf8("inputButton"))
        self.horizontalLayout_4.addWidget(self.inputButton)
        self.targetLabel = QtGui.QLabel(createDialog)
        self.targetLabel.setGeometry(QtCore.QRect(140, 280, 601, 16))
        self.targetLabel.setObjectName(_fromUtf8("targetLabel"))
        self.horizontalLayoutWidget_5 = QtGui.QWidget(createDialog)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(140, 300, 601, 51))
        self.horizontalLayoutWidget_5.setObjectName(_fromUtf8("horizontalLayoutWidget_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.targetLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_5)
        self.targetLineEdit.setObjectName(_fromUtf8("targetLineEdit"))
        self.horizontalLayout_5.addWidget(self.targetLineEdit)
        self.targetButton = QtGui.QPushButton(self.horizontalLayoutWidget_5)
        self.targetButton.setMinimumSize(QtCore.QSize(0, 24))
        self.targetButton.setObjectName(_fromUtf8("targetButton"))
        self.horizontalLayout_5.addWidget(self.targetButton)

        self.retranslateUi(createDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), createDialog.close)
        QtCore.QMetaObject.connectSlotsByName(createDialog)

    def retranslateUi(self, createDialog):
        createDialog.setWindowTitle(_translate("createDialog", "Create CLUZ files", None))
        self.okButton.setText(_translate("createDialog", "OK", None))
        self.cancelButton.setText(_translate("createDialog", "Cancel", None))
        self.puLabel.setText(_translate("createDialog", "Select shapefile that will be used to produce the planning unit layer", None))
        self.puButton.setText(_translate("createDialog", "Browse", None))
        self.convLabel.setText(_translate("createDialog", "Area conversion factor", None))
        self.convHintLabel1.setText(_translate("createDialog", "10000 to convert m2 to ha", None))
        self.convHintLabel2.setText(_translate("createDialog", "1000000 to convert m2 to km2", None))
        self.equalCheckBox.setText(_translate("createDialog", "Set cost layer as equal to planning unit area", None))
        self.inputLabel.setText(_translate("createDialog", "Specify input folder where puvspr2.dat file will be created", None))
        self.inputButton.setText(_translate("createDialog", "Browse", None))
        self.targetLabel.setText(_translate("createDialog", "Name of target table to be created", None))
        self.targetButton.setText(_translate("createDialog", "Save As", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    createDialog = QtGui.QDialog()
    ui = Ui_createDialog()
    ui.setupUi(createDialog)
    createDialog.show()
    sys.exit(app.exec_())

