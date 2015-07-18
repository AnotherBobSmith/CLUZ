# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_met.ui'
#
# Created: Sun Mar 08 10:59:09 2015
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

class Ui_metDialog(object):
    def setupUi(self, metDialog):
        metDialog.setObjectName(_fromUtf8("metDialog"))
        metDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        metDialog.resize(711, 381)
        self.verticalLayout = QtGui.QVBoxLayout(metDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.metTableWidget = QtGui.QTableWidget(metDialog)
        self.metTableWidget.setAlternatingRowColors(True)
        self.metTableWidget.setObjectName(_fromUtf8("metTableWidget"))
        self.metTableWidget.setColumnCount(0)
        self.metTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.metTableWidget)

        self.retranslateUi(metDialog)
        QtCore.QMetaObject.connectSlotsByName(metDialog)

    def retranslateUi(self, metDialog):
        metDialog.setWindowTitle(_translate("metDialog", "Marxan Targets Met table", None))
        self.metTableWidget.setSortingEnabled(True)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    metDialog = QtGui.QDialog()
    ui = Ui_metDialog()
    ui.setupUi(metDialog)
    metDialog.show()
    sys.exit(app.exec_())

