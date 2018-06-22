# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_identify_selected.ui'
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

class Ui_identifySelectedDialog(object):
    def setupUi(self, identifySelectedDialog):
        identifySelectedDialog.setObjectName(_fromUtf8("identifySelectedDialog"))
        identifySelectedDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        identifySelectedDialog.resize(750, 500)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(identifySelectedDialog.sizePolicy().hasHeightForWidth())
        identifySelectedDialog.setSizePolicy(sizePolicy)
        identifySelectedDialog.setMinimumSize(QtCore.QSize(750, 500))
        self.gridLayout = QtGui.QGridLayout(identifySelectedDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.identifySelectedTableWidget = QtGui.QTableWidget(identifySelectedDialog)
        self.identifySelectedTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.identifySelectedTableWidget.setObjectName(_fromUtf8("identifySelectedTableWidget"))
        self.identifySelectedTableWidget.setColumnCount(0)
        self.identifySelectedTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.identifySelectedTableWidget, 0, 0, 1, 1)
        self.closeButton = QtGui.QPushButton(identifySelectedDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 1, 0, 1, 1)

        self.retranslateUi(identifySelectedDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), identifySelectedDialog.close)
        QtCore.QMetaObject.connectSlotsByName(identifySelectedDialog)

    def retranslateUi(self, identifySelectedDialog):
        identifySelectedDialog.setWindowTitle(_translate("identifySelectedDialog", "Identify Tool", None))
        self.closeButton.setText(_translate("identifySelectedDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    identifySelectedDialog = QtGui.QDialog()
    ui = Ui_identifySelectedDialog()
    ui.setupUi(identifySelectedDialog)
    identifySelectedDialog.show()
    sys.exit(app.exec_())

