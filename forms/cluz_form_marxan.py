# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_marxan.ui'
#
# Created: Sat Jul 11 16:58:58 2015
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

class Ui_marxanDialog(object):
    def setupUi(self, marxanDialog):
        marxanDialog.setObjectName(_fromUtf8("marxanDialog"))
        marxanDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        marxanDialog.resize(631, 402)
        self.tabWidget = QtGui.QTabWidget(marxanDialog)
        self.tabWidget.setGeometry(QtCore.QRect(190, 50, 411, 251))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.extraCheckBox = QtGui.QCheckBox(self.tab1)
        self.extraCheckBox.setGeometry(QtCore.QRect(10, 180, 181, 17))
        self.extraCheckBox.setObjectName(_fromUtf8("extraCheckBox"))
        self.outputLineEdit = QtGui.QLineEdit(self.tab1)
        self.outputLineEdit.setGeometry(QtCore.QRect(190, 80, 200, 20))
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.runLineEdit = QtGui.QLineEdit(self.tab1)
        self.runLineEdit.setGeometry(QtCore.QRect(190, 50, 200, 20))
        self.runLineEdit.setObjectName(_fromUtf8("runLineEdit"))
        self.iterLineEdit = QtGui.QLineEdit(self.tab1)
        self.iterLineEdit.setGeometry(QtCore.QRect(190, 20, 200, 20))
        self.iterLineEdit.setObjectName(_fromUtf8("iterLineEdit"))
        self.boundCheckBox = QtGui.QCheckBox(self.tab1)
        self.boundCheckBox.setGeometry(QtCore.QRect(10, 130, 161, 17))
        self.boundCheckBox.setObjectName(_fromUtf8("boundCheckBox"))
        self.iterLabel = QtGui.QLabel(self.tab1)
        self.iterLabel.setGeometry(QtCore.QRect(20, 20, 111, 16))
        self.iterLabel.setObjectName(_fromUtf8("iterLabel"))
        self.outputLabel = QtGui.QLabel(self.tab1)
        self.outputLabel.setGeometry(QtCore.QRect(20, 80, 121, 16))
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.runLabel = QtGui.QLabel(self.tab1)
        self.runLabel.setGeometry(QtCore.QRect(20, 50, 121, 16))
        self.runLabel.setObjectName(_fromUtf8("runLabel"))
        self.boundLineEdit = QtGui.QLineEdit(self.tab1)
        self.boundLineEdit.setGeometry(QtCore.QRect(190, 130, 200, 20))
        self.boundLineEdit.setObjectName(_fromUtf8("boundLineEdit"))
        self.tabWidget.addTab(self.tab1, _fromUtf8(""))
        self.extraTab = QtGui.QWidget()
        self.extraTab.setObjectName(_fromUtf8("extraTab"))
        self.missingLineEdit = QtGui.QLineEdit(self.extraTab)
        self.missingLineEdit.setGeometry(QtCore.QRect(180, 50, 200, 20))
        self.missingLineEdit.setObjectName(_fromUtf8("missingLineEdit"))
        self.missingLabel = QtGui.QLabel(self.extraTab)
        self.missingLabel.setGeometry(QtCore.QRect(20, 50, 131, 16))
        self.missingLabel.setObjectName(_fromUtf8("missingLabel"))
        self.propLineEdit = QtGui.QLineEdit(self.extraTab)
        self.propLineEdit.setGeometry(QtCore.QRect(180, 20, 200, 20))
        self.propLineEdit.setObjectName(_fromUtf8("propLineEdit"))
        self.propLabel = QtGui.QLabel(self.extraTab)
        self.propLabel.setGeometry(QtCore.QRect(20, 20, 91, 13))
        self.propLabel.setObjectName(_fromUtf8("propLabel"))
        self.missingLabel_2 = QtGui.QLabel(self.extraTab)
        self.missingLabel_2.setGeometry(QtCore.QRect(20, 50, 131, 51))
        self.missingLabel_2.setObjectName(_fromUtf8("missingLabel_2"))
        self.parallelCheckBox = QtGui.QCheckBox(self.extraTab)
        self.parallelCheckBox.setGeometry(QtCore.QRect(20, 110, 351, 17))
        self.parallelCheckBox.setObjectName(_fromUtf8("parallelCheckBox"))
        self.parallelListWidget = QtGui.QListWidget(self.extraTab)
        self.parallelListWidget.setEnabled(False)
        self.parallelListWidget.setGeometry(QtCore.QRect(180, 140, 31, 71))
        self.parallelListWidget.setObjectName(_fromUtf8("parallelListWidget"))
        self.parallelLabel = QtGui.QLabel(self.extraTab)
        self.parallelLabel.setEnabled(False)
        self.parallelLabel.setGeometry(QtCore.QRect(40, 140, 161, 16))
        self.parallelLabel.setObjectName(_fromUtf8("parallelLabel"))
        self.tabWidget.addTab(self.extraTab, _fromUtf8(""))
        self.label = QtGui.QLabel(marxanDialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 151, 351))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.layoutWidget = QtGui.QWidget(marxanDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(330, 350, 158, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.runButton = QtGui.QPushButton(self.layoutWidget)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.horizontalLayout.addWidget(self.runButton)
        self.closeButton = QtGui.QPushButton(self.layoutWidget)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)

        self.retranslateUi(marxanDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), marxanDialog.close)
        QtCore.QObject.connect(self.boundCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.boundLineEdit.setVisible)
        QtCore.QObject.connect(self.parallelCheckBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.parallelLabel.setEnabled)
        QtCore.QObject.connect(self.parallelCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.parallelListWidget.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(marxanDialog)

    def retranslateUi(self, marxanDialog):
        marxanDialog.setWindowTitle(_translate("marxanDialog", "Run Marxan", None))
        self.extraCheckBox.setText(_translate("marxanDialog", "Produce extra Marxan outputs", None))
        self.boundCheckBox.setText(_translate("marxanDialog", "Set boundary length modifier", None))
        self.iterLabel.setText(_translate("marxanDialog", "Number of iterations", None))
        self.outputLabel.setText(_translate("marxanDialog", "Output file name", None))
        self.runLabel.setText(_translate("marxanDialog", "Number of runs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("marxanDialog", "Standard options", None))
        self.missingLabel.setText(_translate("marxanDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Species missing if target</p></body></html>", None))
        self.propLabel.setText(_translate("marxanDialog", "Starting proportion", None))
        self.missingLabel_2.setText(_translate("marxanDialog", "<html><head/><body><p>proportion is lower than</p></body></html>", None))
        self.parallelCheckBox.setText(_translate("marxanDialog", "Run parallel Marxan analyses", None))
        self.parallelLabel.setText(_translate("marxanDialog", "Number of parallel analyses", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.extraTab), _translate("marxanDialog", "Advanced options", None))
        self.runButton.setText(_translate("marxanDialog", "Run Marxan", None))
        self.closeButton.setText(_translate("marxanDialog", "Close", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    marxanDialog = QtGui.QDialog()
    ui = Ui_marxanDialog()
    ui.setupUi(marxanDialog)
    marxanDialog.show()
    sys.exit(app.exec_())

