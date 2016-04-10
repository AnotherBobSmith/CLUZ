# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_convert_vec.ui'
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

class Ui_convertVecDialog(object):
    def setupUi(self, convertVecDialog):
        convertVecDialog.setObjectName(_fromUtf8("convertVecDialog"))
        convertVecDialog.resize(634, 525)
        convertVecDialog.setMinimumSize(QtCore.QSize(630, 520))
        self.logoLabel = QtGui.QLabel(convertVecDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, -10, 131, 401))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.selectLabel = QtGui.QLabel(convertVecDialog)
        self.selectLabel.setGeometry(QtCore.QRect(140, 20, 471, 16))
        self.selectLabel.setObjectName(_fromUtf8("selectLabel"))
        self.selectListWidget = QtGui.QListWidget(convertVecDialog)
        self.selectListWidget.setGeometry(QtCore.QRect(140, 50, 481, 171))
        self.selectListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.selectListWidget.setObjectName(_fromUtf8("selectListWidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(convertVecDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(210, 450, 311, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(convertVecDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(140, 230, 391, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.idfieldLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.idfieldLabel.setMinimumSize(QtCore.QSize(141, 22))
        self.idfieldLabel.setObjectName(_fromUtf8("idfieldLabel"))
        self.horizontalLayout_2.addWidget(self.idfieldLabel)
        self.idfieldLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.idfieldLineEdit.setObjectName(_fromUtf8("idfieldLineEdit"))
        self.horizontalLayout_2.addWidget(self.idfieldLineEdit)
        self.verticalLayoutWidget = QtGui.QWidget(convertVecDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(140, 290, 481, 78))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.noneRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.noneRadioButton.setMinimumSize(QtCore.QSize(431, 22))
        self.noneRadioButton.setChecked(True)
        self.noneRadioButton.setObjectName(_fromUtf8("noneRadioButton"))
        self.verticalLayout.addWidget(self.noneRadioButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.userRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.userRadioButton.setMinimumSize(QtCore.QSize(0, 22))
        self.userRadioButton.setObjectName(_fromUtf8("userRadioButton"))
        self.verticalLayout.addWidget(self.userRadioButton)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(convertVecDialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(160, 370, 331, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.convLabel = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.convLabel.setMinimumSize(QtCore.QSize(141, 22))
        self.convLabel.setObjectName(_fromUtf8("convLabel"))
        self.horizontalLayout_3.addWidget(self.convLabel)
        self.convLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
        self.convLineEdit.setObjectName(_fromUtf8("convLineEdit"))
        self.horizontalLayout_3.addWidget(self.convLineEdit)

        self.retranslateUi(convertVecDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), convertVecDialog.close)
        QtCore.QObject.connect(self.userRadioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.convLabel.setEnabled)
        QtCore.QObject.connect(self.userRadioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.convLineEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(convertVecDialog)

    def retranslateUi(self, convertVecDialog):
        convertVecDialog.setWindowTitle(_translate("convertVecDialog", "Convert polylines or polygons to abundance data", None))
        self.selectLabel.setText(_translate("convertVecDialog", "Select themes to import data into Marxan", None))
        self.okButton.setText(_translate("convertVecDialog", "OK", None))
        self.cancelButton.setText(_translate("convertVecDialog", "Cancel", None))
        self.idfieldLabel.setText(_translate("convertVecDialog", "Layer ID field name", None))
        self.noneRadioButton.setText(_translate("convertVecDialog", "No conversion (results will be in layer measurement units)", None))
        self.userRadioButton.setText(_translate("convertVecDialog", "User defined conversion", None))
        self.convLabel.setText(_translate("convertVecDialog", "Area conversion value", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    convertVecDialog = QtGui.QDialog()
    ui = Ui_convertVecDialog()
    ui.setupUi(convertVecDialog)
    convertVecDialog.show()
    sys.exit(app.exec_())

