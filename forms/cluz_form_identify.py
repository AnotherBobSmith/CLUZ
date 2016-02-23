# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_identify.ui'
#
# Created: Fri May 08 12:03:13 2015
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

class Ui_identifyDialog(object):
    def setupUi(self, identifyDialog):
        identifyDialog.setObjectName(_fromUtf8("identifyDialog"))
        identifyDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        identifyDialog.resize(632, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(identifyDialog.sizePolicy().hasHeightForWidth())
        identifyDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(identifyDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.identifyTableWidget = QtGui.QTableWidget(identifyDialog)
        self.identifyTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.identifyTableWidget.setObjectName(_fromUtf8("identifyTableWidget"))
        self.identifyTableWidget.setColumnCount(0)
        self.identifyTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.identifyTableWidget, 0, 0, 1, 1)
        self.closeButton = QtGui.QPushButton(identifyDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 1, 0, 1, 1)

        self.retranslateUi(identifyDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), identifyDialog.close)
        QtCore.QMetaObject.connectSlotsByName(identifyDialog)

    def retranslateUi(self, identifyDialog):
        identifyDialog.setWindowTitle(_translate("identifyDialog", "Identify Tool", None))
        self.closeButton.setText(_translate("identifyDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    identifyDialog = QtGui.QDialog()
    ui = Ui_identifyDialog()
    ui.setupUi(identifyDialog)
    identifyDialog.show()
    sys.exit(app.exec_())

