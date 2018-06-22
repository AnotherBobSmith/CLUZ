# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_richness.ui'
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

class Ui_richnessDialog(object):
    def setupUi(self, richnessDialog):
        richnessDialog.setObjectName(_fromUtf8("richnessDialog"))
        richnessDialog.resize(570, 540)
        richnessDialog.setMinimumSize(QtCore.QSize(570, 540))
        self.logoLabel = QtGui.QLabel(richnessDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, 0, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(richnessDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 480, 271, 41))
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
        self.verticalLayoutWidget = QtGui.QWidget(richnessDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 330, 421, 131))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.typeLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.typeLabel.setObjectName(_fromUtf8("typeLabel"))
        self.verticalLayout.addWidget(self.typeLabel)
        self.typeListWidget = QtGui.QListWidget(self.verticalLayoutWidget)
        self.typeListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.typeListWidget.setObjectName(_fromUtf8("typeListWidget"))
        self.verticalLayout.addWidget(self.typeListWidget)
        self.gridLayoutWidget = QtGui.QWidget(richnessDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(130, 60, 421, 251))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.countLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.countLabel.setEnabled(False)
        self.countLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.countLabel.setObjectName(_fromUtf8("countLabel"))
        self.gridLayout.addWidget(self.countLabel, 1, 0, 1, 1)
        self.countLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.countLineEdit.setEnabled(False)
        self.countLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.countLineEdit.setObjectName(_fromUtf8("countLineEdit"))
        self.gridLayout.addWidget(self.countLineEdit, 1, 1, 1, 1)
        self.rangeBox = QtGui.QCheckBox(self.gridLayoutWidget)
        self.rangeBox.setMinimumSize(QtCore.QSize(0, 24))
        self.rangeBox.setObjectName(_fromUtf8("rangeBox"))
        self.gridLayout.addWidget(self.rangeBox, 2, 0, 1, 1)
        self.rangeLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.rangeLabel.setEnabled(False)
        self.rangeLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.rangeLabel.setObjectName(_fromUtf8("rangeLabel"))
        self.gridLayout.addWidget(self.rangeLabel, 3, 0, 1, 1)
        self.rangeLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.rangeLineEdit.setEnabled(False)
        self.rangeLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.rangeLineEdit.setObjectName(_fromUtf8("rangeLineEdit"))
        self.gridLayout.addWidget(self.rangeLineEdit, 3, 1, 1, 1)
        self.countBox = QtGui.QCheckBox(self.gridLayoutWidget)
        self.countBox.setMinimumSize(QtCore.QSize(0, 24))
        self.countBox.setObjectName(_fromUtf8("countBox"))
        self.gridLayout.addWidget(self.countBox, 0, 0, 1, 1)
        self.verticalLayoutWidget_2 = QtGui.QWidget(richnessDialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(130, 20, 421, 41))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.inputsLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.inputsLabel.setMinimumSize(QtCore.QSize(24, 0))
        self.inputsLabel.setObjectName(_fromUtf8("inputsLabel"))
        self.verticalLayout_2.addWidget(self.inputsLabel)

        self.retranslateUi(richnessDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), richnessDialog.close)
        QtCore.QObject.connect(self.countBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.countLabel.setEnabled)
        QtCore.QObject.connect(self.countBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.countLineEdit.setEnabled)
        QtCore.QObject.connect(self.rangeBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.rangeLabel.setEnabled)
        QtCore.QObject.connect(self.rangeBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.rangeLineEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(richnessDialog)

    def retranslateUi(self, richnessDialog):
        richnessDialog.setWindowTitle(_translate("richnessDialog", "Calculate richness scores", None))
        self.okButton.setText(_translate("richnessDialog", "OK", None))
        self.cancelButton.setText(_translate("richnessDialog", "Cancel", None))
        self.typeLabel.setText(_translate("richnessDialog", "Use features with type codes from the target file:", None))
        self.countLabel.setText(_translate("richnessDialog", "Field name", None))
        self.rangeBox.setText(_translate("richnessDialog", "Restricted Range Richness", None))
        self.rangeLabel.setText(_translate("richnessDialog", "Field name", None))
        self.countBox.setText(_translate("richnessDialog", "Feature Count", None))
        self.inputsLabel.setText(_translate("richnessDialog", "Calculate the following for each planning unit:", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    richnessDialog = QtGui.QDialog()
    ui = Ui_richnessDialog()
    ui.setupUi(richnessDialog)
    richnessDialog.show()
    sys.exit(app.exec_())

