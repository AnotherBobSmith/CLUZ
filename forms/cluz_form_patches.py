# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_patches.ui'
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

class Ui_patchesDialog(object):
    def setupUi(self, patchesDialog):
        patchesDialog.setObjectName(_fromUtf8("patchesDialog"))
        patchesDialog.resize(728, 394)
        self.logoLabel = QtGui.QLabel(patchesDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, 30, 131, 351))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(patchesDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(290, 160, 221, 51))
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
        self.filePathlabel = QtGui.QLabel(patchesDialog)
        self.filePathlabel.setGeometry(QtCore.QRect(140, 70, 541, 16))
        self.filePathlabel.setMinimumSize(QtCore.QSize(351, 16))
        self.filePathlabel.setObjectName(_fromUtf8("filePathlabel"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(patchesDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(140, 90, 561, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.filePathlineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.filePathlineEdit.setMinimumSize(QtCore.QSize(0, 26))
        self.filePathlineEdit.setObjectName(_fromUtf8("filePathlineEdit"))
        self.horizontalLayout_2.addWidget(self.filePathlineEdit)
        self.browseButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.browseButton.setMinimumSize(QtCore.QSize(0, 26))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout_2.addWidget(self.browseButton)

        self.retranslateUi(patchesDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), patchesDialog.close)
        QtCore.QMetaObject.connectSlotsByName(patchesDialog)

    def retranslateUi(self, patchesDialog):
        patchesDialog.setWindowTitle(_translate("patchesDialog", "Show distribution of features", None))
        self.okButton.setText(_translate("patchesDialog", "OK", None))
        self.cancelButton.setText(_translate("patchesDialog", "Cancel", None))
        self.filePathlabel.setText(_translate("patchesDialog", "Select Marxan or MinPatch portfolio file", None))
        self.browseButton.setText(_translate("patchesDialog", "Browse", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    patchesDialog = QtGui.QDialog()
    ui = Ui_patchesDialog()
    ui.setupUi(patchesDialog)
    patchesDialog.show()
    sys.exit(app.exec_())

