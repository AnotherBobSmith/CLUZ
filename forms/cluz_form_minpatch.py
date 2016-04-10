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
        minpatchDialog.resize(750, 470)
        minpatchDialog.setMinimumSize(QtCore.QSize(750, 470))
        self.logoLabel = QtGui.QLabel(minpatchDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-20, 10, 131, 401))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.tabWidget = QtGui.QTabWidget(minpatchDialog)
        self.tabWidget.setGeometry(QtCore.QRect(130, 20, 591, 381))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.tab1)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 100, 551, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.minpatchFileLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.minpatchFileLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.minpatchFileLabel.setObjectName(_fromUtf8("minpatchFileLabel"))
        self.horizontalLayout_2.addWidget(self.minpatchFileLabel)
        self.detailsLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.detailsLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.detailsLineEdit.setObjectName(_fromUtf8("detailsLineEdit"))
        self.horizontalLayout_2.addWidget(self.detailsLineEdit)
        self.browseButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.browseButton.setMinimumSize(QtCore.QSize(0, 24))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout_2.addWidget(self.browseButton)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(self.tab1)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 150, 371, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.listLabel_2 = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.listLabel_2.setMinimumSize(QtCore.QSize(0, 24))
        self.listLabel_2.setObjectName(_fromUtf8("listLabel_2"))
        self.horizontalLayout_3.addWidget(self.listLabel_2)
        self.blmLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
        self.blmLineEdit.setMinimumSize(QtCore.QSize(0, 24))
        self.blmLineEdit.setObjectName(_fromUtf8("blmLineEdit"))
        self.horizontalLayout_3.addWidget(self.blmLineEdit)
        self.fileListWidget = QtGui.QListWidget(self.tab1)
        self.fileListWidget.setGeometry(QtCore.QRect(10, 230, 561, 121))
        self.fileListWidget.setObjectName(_fromUtf8("fileListWidget"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.tab1)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 551, 81))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.inputLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.inputLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.inputLabel.setObjectName(_fromUtf8("inputLabel"))
        self.verticalLayout_2.addWidget(self.inputLabel)
        self.outputLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.outputLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.verticalLayout_2.addWidget(self.outputLabel)
        self.horizontalLayoutWidget_4 = QtGui.QWidget(self.tab1)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 200, 561, 31))
        self.horizontalLayoutWidget_4.setObjectName(_fromUtf8("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.listLabel = QtGui.QLabel(self.horizontalLayoutWidget_4)
        self.listLabel.setMinimumSize(QtCore.QSize(0, 24))
        self.listLabel.setObjectName(_fromUtf8("listLabel"))
        self.horizontalLayout_4.addWidget(self.listLabel)
        self.tabWidget.addTab(self.tab1, _fromUtf8(""))
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName(_fromUtf8("tab2"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tab2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 561, 171))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.removeCheckBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.removeCheckBox.setChecked(True)
        self.removeCheckBox.setObjectName(_fromUtf8("removeCheckBox"))
        self.verticalLayout.addWidget(self.removeCheckBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.addCheckBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.addCheckBox.setChecked(True)
        self.addCheckBox.setObjectName(_fromUtf8("addCheckBox"))
        self.verticalLayout.addWidget(self.addCheckBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.whittleCheckBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.whittleCheckBox.setChecked(True)
        self.whittleCheckBox.setObjectName(_fromUtf8("whittleCheckBox"))
        self.verticalLayout.addWidget(self.whittleCheckBox)
        self.tabWidget.addTab(self.tab2, _fromUtf8(""))
        self.horizontalLayoutWidget = QtGui.QWidget(minpatchDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(280, 410, 311, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout.addWidget(self.startButton)
        self.closeButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)

        self.retranslateUi(minpatchDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), minpatchDialog.close)
        QtCore.QMetaObject.connectSlotsByName(minpatchDialog)

    def retranslateUi(self, minpatchDialog):
        minpatchDialog.setWindowTitle(_translate("minpatchDialog", "Launch MinPatch", None))
        self.minpatchFileLabel.setText(_translate("minpatchDialog", "MinPatch details file", None))
        self.browseButton.setText(_translate("minpatchDialog", "Browse", None))
        self.listLabel_2.setText(_translate("minpatchDialog", "Boundary Length Modifier Value", None))
        self.inputLabel.setText(_translate("minpatchDialog", "Marxan input folder:", None))
        self.outputLabel.setText(_translate("minpatchDialog", "Marxan output folder:", None))
        self.listLabel.setText(_translate("minpatchDialog", "Marxan files to analyse", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("minpatchDialog", "Standard options", None))
        self.removeCheckBox.setText(_translate("minpatchDialog", "Remove small patches", None))
        self.addCheckBox.setText(_translate("minpatchDialog", "Add patches", None))
        self.whittleCheckBox.setText(_translate("minpatchDialog", "Simulated whittling", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("minpatchDialog", "Advanced options", None))
        self.startButton.setText(_translate("minpatchDialog", "Start MinPatch", None))
        self.closeButton.setText(_translate("minpatchDialog", "Close", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    minpatchDialog = QtGui.QDialog()
    ui = Ui_minpatchDialog()
    ui.setupUi(minpatchDialog)
    minpatchDialog.show()
    sys.exit(app.exec_())

