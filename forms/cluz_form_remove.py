# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_remove.ui'
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

class Ui_removeDialog(object):
    def setupUi(self, removeDialog):
        removeDialog.setObjectName(_fromUtf8("removeDialog"))
        removeDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        removeDialog.resize(800, 400)
        removeDialog.setMinimumSize(QtCore.QSize(800, 400))
        self.featLabel = QtGui.QLabel(removeDialog)
        self.featLabel.setGeometry(QtCore.QRect(120, 20, 661, 16))
        self.featLabel.setMinimumSize(QtCore.QSize(461, 16))
        self.featLabel.setObjectName(_fromUtf8("featLabel"))
        self.featListWidget = QtGui.QListWidget(removeDialog)
        self.featListWidget.setGeometry(QtCore.QRect(120, 40, 661, 290))
        self.featListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.featListWidget.setObjectName(_fromUtf8("featListWidget"))
        self.logoLabel = QtGui.QLabel(removeDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-20, 20, 131, 351))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(removeDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(350, 340, 211, 51))
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

        self.retranslateUi(removeDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), removeDialog.close)
        QtCore.QMetaObject.connectSlotsByName(removeDialog)

    def retranslateUi(self, removeDialog):
        removeDialog.setWindowTitle(_translate("removeDialog", "Choose features to remove", None))
        self.featLabel.setText(_translate("removeDialog", "Select conservation features to remove from the abundance and target tables", None))
        self.okButton.setText(_translate("removeDialog", "OK", None))
        self.cancelButton.setText(_translate("removeDialog", "Cancel", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    removeDialog = QtGui.QDialog()
    ui = Ui_removeDialog()
    ui.setupUi(removeDialog)
    removeDialog.show()
    sys.exit(app.exec_())

