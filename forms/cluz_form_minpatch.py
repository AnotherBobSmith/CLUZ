# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_minpatch.ui'
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

class Ui_minpatchDialog(object):
    def setupUi(self, minpatchDialog):
        minpatchDialog.setObjectName(_fromUtf8("minpatchDialog"))
        minpatchDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        minpatchDialog.resize(710, 410)
        minpatchDialog.setMinimumSize(QtCore.QSize(710, 410))
        self.logoLabel = QtGui.QLabel(minpatchDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, -20, 131, 401))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.tabWidget = QtGui.QTabWidget(minpatchDialog)
        self.tabWidget.setGeometry(QtCore.QRect(120, 10, 581, 391))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.minpatchFileLabel = QtGui.QLabel(self.tab1)
        self.minpatchFileLabel.setGeometry(QtCore.QRect(20, 100, 161, 16))
        self.minpatchFileLabel.setObjectName(_fromUtf8("minpatchFileLabel"))
        self.listLabel = QtGui.QLabel(self.tab1)
        self.listLabel.setGeometry(QtCore.QRect(20, 180, 351, 16))
        self.listLabel.setObjectName(_fromUtf8("listLabel"))
        self.outputLabel = QtGui.QLabel(self.tab1)
        self.outputLabel.setGeometry(QtCore.QRect(20, 60, 541, 16))
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.fileListWidget = QtGui.QListWidget(self.tab1)
        self.fileListWidget.setGeometry(QtCore.QRect(20, 200, 451, 101))
        self.fileListWidget.setObjectName(_fromUtf8("fileListWidget"))
        self.detailsLineEdit = QtGui.QLineEdit(self.tab1)
        self.detailsLineEdit.setGeometry(QtCore.QRect(190, 100, 281, 20))
        self.detailsLineEdit.setObjectName(_fromUtf8("detailsLineEdit"))
        self.listLabel_2 = QtGui.QLabel(self.tab1)
        self.listLabel_2.setGeometry(QtCore.QRect(20, 140, 321, 16))
        self.listLabel_2.setObjectName(_fromUtf8("listLabel_2"))
        self.browseButton = QtGui.QPushButton(self.tab1)
        self.browseButton.setGeometry(QtCore.QRect(490, 100, 75, 23))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.inputLabel = QtGui.QLabel(self.tab1)
        self.inputLabel.setGeometry(QtCore.QRect(20, 20, 521, 16))
        self.inputLabel.setObjectName(_fromUtf8("inputLabel"))
        self.blmLineEdit = QtGui.QLineEdit(self.tab1)
        self.blmLineEdit.setGeometry(QtCore.QRect(360, 140, 111, 20))
        self.blmLineEdit.setObjectName(_fromUtf8("blmLineEdit"))
        self.closeButton = QtGui.QPushButton(self.tab1)
        self.closeButton.setGeometry(QtCore.QRect(330, 330, 111, 23))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.startButton = QtGui.QPushButton(self.tab1)
        self.startButton.setGeometry(QtCore.QRect(150, 330, 111, 23))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.tabWidget.addTab(self.tab1, _fromUtf8(""))
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName(_fromUtf8("tab2"))
        self.removeCheckBox = QtGui.QCheckBox(self.tab2)
        self.removeCheckBox.setGeometry(QtCore.QRect(19, 30, 231, 20))
        self.removeCheckBox.setChecked(True)
        self.removeCheckBox.setObjectName(_fromUtf8("removeCheckBox"))
        self.addCheckBox = QtGui.QCheckBox(self.tab2)
        self.addCheckBox.setGeometry(QtCore.QRect(20, 90, 231, 20))
        self.addCheckBox.setChecked(True)
        self.addCheckBox.setObjectName(_fromUtf8("addCheckBox"))
        self.whittleCheckBox = QtGui.QCheckBox(self.tab2)
        self.whittleCheckBox.setGeometry(QtCore.QRect(20, 150, 231, 20))
        self.whittleCheckBox.setChecked(True)
        self.whittleCheckBox.setObjectName(_fromUtf8("whittleCheckBox"))
        self.tabWidget.addTab(self.tab2, _fromUtf8(""))

        self.retranslateUi(minpatchDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), minpatchDialog.close)
        QtCore.QMetaObject.connectSlotsByName(minpatchDialog)

    def retranslateUi(self, minpatchDialog):
        minpatchDialog.setWindowTitle(_translate("minpatchDialog", "Launch MinPatch", None))
        self.minpatchFileLabel.setText(_translate("minpatchDialog", "MinPatch details file", None))
        self.listLabel.setText(_translate("minpatchDialog", "Marxan files to analyse", None))
        self.outputLabel.setText(_translate("minpatchDialog", "Marxan output folder:", None))
        self.listLabel_2.setText(_translate("minpatchDialog", "Boundary Length Modifier Value", None))
        self.browseButton.setText(_translate("minpatchDialog", "Browse", None))
        self.inputLabel.setText(_translate("minpatchDialog", "Marxan input folder:", None))
        self.closeButton.setText(_translate("minpatchDialog", "Close", None))
        self.startButton.setText(_translate("minpatchDialog", "Start MinPatch", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("minpatchDialog", "Standard options", None))
        self.removeCheckBox.setText(_translate("minpatchDialog", "Remove small patches", None))
        self.addCheckBox.setText(_translate("minpatchDialog", "Add patches", None))
        self.whittleCheckBox.setText(_translate("minpatchDialog", "Simulated whittling", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("minpatchDialog", "Advanced options", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    minpatchDialog = QtGui.QDialog()
    ui = Ui_minpatchDialog()
    ui.setupUi(minpatchDialog)
    minpatchDialog.show()
    sys.exit(app.exec_())

