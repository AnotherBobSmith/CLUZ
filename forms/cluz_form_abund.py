# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_abund.ui'
#
# Created: Sat Mar 28 16:02:34 2015
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

class Ui_abundDialog(object):
    def setupUi(self, abundDialog):
        abundDialog.setObjectName(_fromUtf8("abundDialog"))
        abundDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        abundDialog.resize(713, 432)
        self.gridLayout = QtGui.QGridLayout(abundDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.abundTableWidget = QtGui.QTableWidget(abundDialog)
        self.abundTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.abundTableWidget.setAlternatingRowColors(True)
        self.abundTableWidget.setObjectName(_fromUtf8("abundTableWidget"))
        self.abundTableWidget.setColumnCount(0)
        self.abundTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.abundTableWidget, 0, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(abundDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout.addWidget(self.cancelButton, 1, 0, 1, 1)

        self.retranslateUi(abundDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), abundDialog.close)
        QtCore.QMetaObject.connectSlotsByName(abundDialog)

    def retranslateUi(self, abundDialog):
        abundDialog.setWindowTitle(_translate("abundDialog", "Abundance table", None))
        self.abundTableWidget.setSortingEnabled(True)
        self.cancelButton.setText(_translate("abundDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    abundDialog = QtGui.QDialog()
    ui = Ui_abundDialog()
    ui.setupUi(abundDialog)
    abundDialog.show()
    sys.exit(app.exec_())

