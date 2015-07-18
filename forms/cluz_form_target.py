# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_target.ui'
#
# Created: Sat Mar 28 15:57:45 2015
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

class Ui_targetDialog(object):
    def setupUi(self, targetDialog):
        targetDialog.setObjectName(_fromUtf8("targetDialog"))
        targetDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        targetDialog.resize(753, 478)
        self.gridLayout = QtGui.QGridLayout(targetDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.targetTableWidget = QtGui.QTableWidget(targetDialog)
        self.targetTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.targetTableWidget.setAlternatingRowColors(True)
        self.targetTableWidget.setObjectName(_fromUtf8("targetTableWidget"))
        self.targetTableWidget.setColumnCount(0)
        self.targetTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.targetTableWidget, 0, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(targetDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout.addWidget(self.cancelButton, 1, 0, 1, 1)

        self.retranslateUi(targetDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), targetDialog.close)
        QtCore.QMetaObject.connectSlotsByName(targetDialog)

    def retranslateUi(self, targetDialog):
        targetDialog.setWindowTitle(_translate("targetDialog", "Target table", None))
        self.targetTableWidget.setSortingEnabled(True)
        self.cancelButton.setText(_translate("targetDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    targetDialog = QtGui.QDialog()
    ui = Ui_targetDialog()
    ui.setupUi(targetDialog)
    targetDialog.show()
    sys.exit(app.exec_())

