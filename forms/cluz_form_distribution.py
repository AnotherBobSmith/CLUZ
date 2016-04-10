# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_distribution.ui'
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

class Ui_distributionDialog(object):
    def setupUi(self, distributionDialog):
        distributionDialog.setObjectName(_fromUtf8("distributionDialog"))
        distributionDialog.resize(728, 540)
        self.logoLabel = QtGui.QLabel(distributionDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, 30, 131, 351))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(distributionDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(290, 480, 221, 51))
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
        self.featLabel = QtGui.QLabel(distributionDialog)
        self.featLabel.setGeometry(QtCore.QRect(140, 20, 561, 24))
        self.featLabel.setMinimumSize(QtCore.QSize(421, 24))
        self.featLabel.setObjectName(_fromUtf8("featLabel"))
        self.featListWidget = QtGui.QListWidget(distributionDialog)
        self.featListWidget.setGeometry(QtCore.QRect(140, 50, 561, 171))
        self.featListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.featListWidget.setObjectName(_fromUtf8("featListWidget"))
        self.filePathlabel = QtGui.QLabel(distributionDialog)
        self.filePathlabel.setGeometry(QtCore.QRect(140, 390, 541, 16))
        self.filePathlabel.setMinimumSize(QtCore.QSize(351, 16))
        self.filePathlabel.setObjectName(_fromUtf8("filePathlabel"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(distributionDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(140, 410, 561, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.filePathlineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.filePathlineEdit.setMinimumSize(QtCore.QSize(0, 26))
        self.filePathlineEdit.setObjectName(_fromUtf8("filePathlineEdit"))
        self.horizontalLayout_2.addWidget(self.filePathlineEdit)
        self.filePathButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.filePathButton.setMinimumSize(QtCore.QSize(0, 26))
        self.filePathButton.setObjectName(_fromUtf8("filePathButton"))
        self.horizontalLayout_2.addWidget(self.filePathButton)
        self.verticalLayoutWidget = QtGui.QWidget(distributionDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(150, 230, 423, 138))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.catFeatLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.catFeatLabel.setMinimumSize(QtCore.QSize(421, 24))
        self.catFeatLabel.setObjectName(_fromUtf8("catFeatLabel"))
        self.verticalLayout.addWidget(self.catFeatLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.intervalRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.intervalRadioButton.setMinimumSize(QtCore.QSize(0, 24))
        self.intervalRadioButton.setChecked(True)
        self.intervalRadioButton.setObjectName(_fromUtf8("intervalRadioButton"))
        self.verticalLayout.addWidget(self.intervalRadioButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.areaRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.areaRadioButton.setMinimumSize(QtCore.QSize(0, 24))
        self.areaRadioButton.setObjectName(_fromUtf8("areaRadioButton"))
        self.verticalLayout.addWidget(self.areaRadioButton)
        self.groupBox = QtGui.QGroupBox(distributionDialog)
        self.groupBox.setGeometry(QtCore.QRect(140, 230, 351, 141))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox.raise_()
        self.logoLabel.raise_()
        self.horizontalLayoutWidget.raise_()
        self.featLabel.raise_()
        self.featListWidget.raise_()
        self.filePathlabel.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.verticalLayoutWidget.raise_()

        self.retranslateUi(distributionDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), distributionDialog.close)
        QtCore.QMetaObject.connectSlotsByName(distributionDialog)

    def retranslateUi(self, distributionDialog):
        distributionDialog.setWindowTitle(_translate("distributionDialog", "Show distribution of features", None))
        self.okButton.setText(_translate("distributionDialog", "OK", None))
        self.cancelButton.setText(_translate("distributionDialog", "Cancel", None))
        self.featLabel.setText(_translate("distributionDialog", "Select conservation features to display", None))
        self.filePathlabel.setText(_translate("distributionDialog", "Name of shapefile that will be produced:", None))
        self.filePathButton.setText(_translate("distributionDialog", "Browse", None))
        self.catFeatLabel.setText(_translate("distributionDialog", "Choose legend categories", None))
        self.intervalRadioButton.setText(_translate("distributionDialog", "Equal  interval", None))
        self.areaRadioButton.setText(_translate("distributionDialog", "Equal area", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    distributionDialog = QtGui.QDialog()
    ui = Ui_distributionDialog()
    ui.setupUi(distributionDialog)
    distributionDialog.show()
    sys.exit(app.exec_())

