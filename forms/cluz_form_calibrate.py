# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_calibrate.ui'
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

class Ui_calibrateDialog(object):
    def setupUi(self, calibrateDialog):
        calibrateDialog.setObjectName(_fromUtf8("calibrateDialog"))
        calibrateDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        calibrateDialog.resize(660, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(calibrateDialog.sizePolicy().hasHeightForWidth())
        calibrateDialog.setSizePolicy(sizePolicy)
        calibrateDialog.setMinimumSize(QtCore.QSize(660, 450))
        calibrateDialog.setMaximumSize(QtCore.QSize(660, 450))
        self.label = QtGui.QLabel(calibrateDialog)
        self.label.setGeometry(QtCore.QRect(10, 40, 150, 350))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(150, 350))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.numberLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.numberLineEdit.setGeometry(QtCore.QRect(340, 60, 113, 20))
        self.numberLineEdit.setObjectName(_fromUtf8("numberLineEdit"))
        self.outputLabel = QtGui.QLabel(calibrateDialog)
        self.outputLabel.setGeometry(QtCore.QRect(190, 300, 181, 16))
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.saveResultsButton = QtGui.QPushButton(calibrateDialog)
        self.saveResultsButton.setGeometry(QtCore.QRect(560, 360, 91, 23))
        self.saveResultsButton.setObjectName(_fromUtf8("saveResultsButton"))
        self.minLabel = QtGui.QLabel(calibrateDialog)
        self.minLabel.setGeometry(QtCore.QRect(190, 90, 141, 16))
        self.minLabel.setObjectName(_fromUtf8("minLabel"))
        self.minLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.minLineEdit.setGeometry(QtCore.QRect(340, 90, 113, 20))
        self.minLineEdit.setObjectName(_fromUtf8("minLineEdit"))
        self.maxLabel = QtGui.QLabel(calibrateDialog)
        self.maxLabel.setGeometry(QtCore.QRect(190, 120, 141, 16))
        self.maxLabel.setObjectName(_fromUtf8("maxLabel"))
        self.numberLabel = QtGui.QLabel(calibrateDialog)
        self.numberLabel.setGeometry(QtCore.QRect(190, 60, 141, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberLabel.sizePolicy().hasHeightForWidth())
        self.numberLabel.setSizePolicy(sizePolicy)
        self.numberLabel.setMinimumSize(QtCore.QSize(110, 16))
        self.numberLabel.setObjectName(_fromUtf8("numberLabel"))
        self.outputLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.outputLineEdit.setGeometry(QtCore.QRect(380, 300, 171, 20))
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.iterLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.iterLineEdit.setGeometry(QtCore.QRect(340, 190, 111, 20))
        self.iterLineEdit.setObjectName(_fromUtf8("iterLineEdit"))
        self.runLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.runLineEdit.setGeometry(QtCore.QRect(340, 220, 111, 20))
        self.runLineEdit.setObjectName(_fromUtf8("runLineEdit"))
        self.maxLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.maxLineEdit.setGeometry(QtCore.QRect(340, 120, 113, 20))
        self.maxLineEdit.setObjectName(_fromUtf8("maxLineEdit"))
        self.parameterLabel = QtGui.QLabel(calibrateDialog)
        self.parameterLabel.setGeometry(QtCore.QRect(190, 30, 141, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterLabel.sizePolicy().hasHeightForWidth())
        self.parameterLabel.setSizePolicy(sizePolicy)
        self.parameterLabel.setMinimumSize(QtCore.QSize(110, 16))
        self.parameterLabel.setObjectName(_fromUtf8("parameterLabel"))
        self.resultsLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.resultsLineEdit.setGeometry(QtCore.QRect(270, 360, 281, 20))
        self.resultsLineEdit.setObjectName(_fromUtf8("resultsLineEdit"))
        self.runLabel = QtGui.QLabel(calibrateDialog)
        self.runLabel.setGeometry(QtCore.QRect(190, 220, 141, 16))
        self.runLabel.setObjectName(_fromUtf8("runLabel"))
        self.iterLabel = QtGui.QLabel(calibrateDialog)
        self.iterLabel.setGeometry(QtCore.QRect(190, 190, 141, 16))
        self.iterLabel.setObjectName(_fromUtf8("iterLabel"))
        self.resultsLabel = QtGui.QLabel(calibrateDialog)
        self.resultsLabel.setGeometry(QtCore.QRect(190, 360, 81, 16))
        self.resultsLabel.setObjectName(_fromUtf8("resultsLabel"))
        self.boundLineEdit = QtGui.QLineEdit(calibrateDialog)
        self.boundLineEdit.setGeometry(QtCore.QRect(340, 250, 111, 20))
        self.boundLineEdit.setObjectName(_fromUtf8("boundLineEdit"))
        self.boundLabel = QtGui.QLabel(calibrateDialog)
        self.boundLabel.setGeometry(QtCore.QRect(190, 250, 141, 16))
        self.boundLabel.setObjectName(_fromUtf8("boundLabel"))
        self.paraComboBox = QtGui.QComboBox(calibrateDialog)
        self.paraComboBox.setGeometry(QtCore.QRect(340, 30, 211, 22))
        self.paraComboBox.setObjectName(_fromUtf8("paraComboBox"))
        self.runButton = QtGui.QPushButton(calibrateDialog)
        self.runButton.setGeometry(QtCore.QRect(290, 410, 111, 23))
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.expCheckBox = QtGui.QCheckBox(calibrateDialog)
        self.expCheckBox.setGeometry(QtCore.QRect(190, 150, 431, 17))
        self.expCheckBox.setObjectName(_fromUtf8("expCheckBox"))
        self.closeButton = QtGui.QPushButton(calibrateDialog)
        self.closeButton.setGeometry(QtCore.QRect(410, 410, 75, 23))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))

        self.retranslateUi(calibrateDialog)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), calibrateDialog.close)
        QtCore.QMetaObject.connectSlotsByName(calibrateDialog)
        calibrateDialog.setTabOrder(self.paraComboBox, self.numberLineEdit)
        calibrateDialog.setTabOrder(self.numberLineEdit, self.minLineEdit)
        calibrateDialog.setTabOrder(self.minLineEdit, self.maxLineEdit)
        calibrateDialog.setTabOrder(self.maxLineEdit, self.expCheckBox)
        calibrateDialog.setTabOrder(self.expCheckBox, self.iterLineEdit)
        calibrateDialog.setTabOrder(self.iterLineEdit, self.runLineEdit)
        calibrateDialog.setTabOrder(self.runLineEdit, self.boundLineEdit)
        calibrateDialog.setTabOrder(self.boundLineEdit, self.outputLineEdit)
        calibrateDialog.setTabOrder(self.outputLineEdit, self.resultsLineEdit)
        calibrateDialog.setTabOrder(self.resultsLineEdit, self.saveResultsButton)
        calibrateDialog.setTabOrder(self.saveResultsButton, self.runButton)
        calibrateDialog.setTabOrder(self.runButton, self.closeButton)

    def retranslateUi(self, calibrateDialog):
        calibrateDialog.setWindowTitle(_translate("calibrateDialog", "Calibrate Marxan parameters", None))
        self.outputLabel.setText(_translate("calibrateDialog", "Marxan output files base name", None))
        self.saveResultsButton.setText(_translate("calibrateDialog", "Save As...", None))
        self.minLabel.setText(_translate("calibrateDialog", "Minimum value", None))
        self.maxLabel.setText(_translate("calibrateDialog", "Maximum value", None))
        self.numberLabel.setText(_translate("calibrateDialog", "Number of analyses", None))
        self.parameterLabel.setText(_translate("calibrateDialog", "Parameter to calibrate", None))
        self.runLabel.setText(_translate("calibrateDialog", "Number of runs", None))
        self.iterLabel.setText(_translate("calibrateDialog", "Number of iterations", None))
        self.resultsLabel.setText(_translate("calibrateDialog", "Results file", None))
        self.boundLabel.setText(_translate("calibrateDialog", "BLM value", None))
        self.runButton.setText(_translate("calibrateDialog", "Run Analysis", None))
        self.expCheckBox.setText(_translate("calibrateDialog", "Use exponential steps between minimum and maximum values", None))
        self.closeButton.setText(_translate("calibrateDialog", "Close", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    calibrateDialog = QtGui.QDialog()
    ui = Ui_calibrateDialog()
    ui.setupUi(calibrateDialog)
    calibrateDialog.show()
    sys.exit(app.exec_())

