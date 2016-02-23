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
        distributionDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        distributionDialog.resize(580, 440)
        distributionDialog.setMinimumSize(QtCore.QSize(580, 440))
        self.legendGroupBox = QtGui.QGroupBox(distributionDialog)
        self.legendGroupBox.setGeometry(QtCore.QRect(120, 229, 251, 81))
        self.legendGroupBox.setTitle(_fromUtf8(""))
        self.legendGroupBox.setObjectName(_fromUtf8("legendGroupBox"))
        self.intervalRadioButton = QtGui.QRadioButton(self.legendGroupBox)
        self.intervalRadioButton.setGeometry(QtCore.QRect(10, 20, 171, 17))
        self.intervalRadioButton.setChecked(True)
        self.intervalRadioButton.setObjectName(_fromUtf8("intervalRadioButton"))
        self.areaRadioButton = QtGui.QRadioButton(self.legendGroupBox)
        self.areaRadioButton.setGeometry(QtCore.QRect(10, 50, 171, 17))
        self.areaRadioButton.setObjectName(_fromUtf8("areaRadioButton"))
        self.featLabel = QtGui.QLabel(distributionDialog)
        self.featLabel.setGeometry(QtCore.QRect(120, 20, 421, 16))
        self.featLabel.setMinimumSize(QtCore.QSize(421, 16))
        self.featLabel.setObjectName(_fromUtf8("featLabel"))
        self.featListWidget = QtGui.QListWidget(distributionDialog)
        self.featListWidget.setGeometry(QtCore.QRect(120, 40, 450, 171))
        self.featListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.featListWidget.setObjectName(_fromUtf8("featListWidget"))
        self.okButton = QtGui.QPushButton(distributionDialog)
        self.okButton.setGeometry(QtCore.QRect(220, 400, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(distributionDialog)
        self.cancelButton.setGeometry(QtCore.QRect(340, 400, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.filePathButton = QtGui.QPushButton(distributionDialog)
        self.filePathButton.setGeometry(QtCore.QRect(480, 350, 75, 23))
        self.filePathButton.setObjectName(_fromUtf8("filePathButton"))
        self.filePathlineEdit = QtGui.QLineEdit(distributionDialog)
        self.filePathlineEdit.setGeometry(QtCore.QRect(120, 350, 350, 20))
        self.filePathlineEdit.setObjectName(_fromUtf8("filePathlineEdit"))
        self.filePathlabel = QtGui.QLabel(distributionDialog)
        self.filePathlabel.setGeometry(QtCore.QRect(120, 330, 351, 16))
        self.filePathlabel.setMinimumSize(QtCore.QSize(351, 16))
        self.filePathlabel.setObjectName(_fromUtf8("filePathlabel"))
        self.logoLabel = QtGui.QLabel(distributionDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-20, 20, 131, 351))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.catFeatLabel = QtGui.QLabel(distributionDialog)
        self.catFeatLabel.setGeometry(QtCore.QRect(130, 230, 421, 16))
        self.catFeatLabel.setMinimumSize(QtCore.QSize(421, 16))
        self.catFeatLabel.setObjectName(_fromUtf8("catFeatLabel"))

        self.retranslateUi(distributionDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), distributionDialog.close)
        QtCore.QMetaObject.connectSlotsByName(distributionDialog)

    def retranslateUi(self, distributionDialog):
        distributionDialog.setWindowTitle(_translate("distributionDialog", "Show distribution of features", None))
        self.intervalRadioButton.setText(_translate("distributionDialog", "Equal  interval", None))
        self.areaRadioButton.setText(_translate("distributionDialog", "Equal area", None))
        self.featLabel.setText(_translate("distributionDialog", "Select conservation features to display", None))
        self.okButton.setText(_translate("distributionDialog", "OK", None))
        self.cancelButton.setText(_translate("distributionDialog", "Cancel", None))
        self.filePathButton.setText(_translate("distributionDialog", "Browse", None))
        self.filePathlabel.setText(_translate("distributionDialog", "Name of shapefile that will be produced:", None))
        self.catFeatLabel.setText(_translate("distributionDialog", "Choose legend categories", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    distributionDialog = QtGui.QDialog()
    ui = Ui_distributionDialog()
    ui.setupUi(distributionDialog)
    distributionDialog.show()
    sys.exit(app.exec_())

