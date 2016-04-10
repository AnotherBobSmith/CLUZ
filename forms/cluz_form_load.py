# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_load.ui'
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

class Ui_loadDialog(object):
    def setupUi(self, loadDialog):
        loadDialog.setObjectName(_fromUtf8("loadDialog"))
        loadDialog.resize(764, 432)
        loadDialog.setMinimumSize(QtCore.QSize(460, 430))
        self.logoLabel = QtGui.QLabel(loadDialog)
        self.logoLabel.setGeometry(QtCore.QRect(-10, 0, 121, 371))
        self.logoLabel.setText(_fromUtf8(""))
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/setup_logo.png")))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        self.horizontalLayoutWidget = QtGui.QWidget(loadDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(309, 350, 191, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.bestCheckBox = QtGui.QCheckBox(loadDialog)
        self.bestCheckBox.setGeometry(QtCore.QRect(150, 20, 591, 17))
        self.bestCheckBox.setObjectName(_fromUtf8("bestCheckBox"))
        self.bestLabel = QtGui.QLabel(loadDialog)
        self.bestLabel.setGeometry(QtCore.QRect(170, 90, 571, 16))
        self.bestLabel.setObjectName(_fromUtf8("bestLabel"))
        self.bestNameLineEdit = QtGui.QLineEdit(loadDialog)
        self.bestNameLineEdit.setGeometry(QtCore.QRect(170, 110, 241, 20))
        self.bestNameLineEdit.setObjectName(_fromUtf8("bestNameLineEdit"))
        self.summedCheckBox = QtGui.QCheckBox(loadDialog)
        self.summedCheckBox.setGeometry(QtCore.QRect(150, 180, 441, 17))
        self.summedCheckBox.setObjectName(_fromUtf8("summedCheckBox"))
        self.summedLabel = QtGui.QLabel(loadDialog)
        self.summedLabel.setGeometry(QtCore.QRect(170, 260, 571, 16))
        self.summedLabel.setObjectName(_fromUtf8("summedLabel"))
        self.summedNameLineEdit = QtGui.QLineEdit(loadDialog)
        self.summedNameLineEdit.setGeometry(QtCore.QRect(170, 280, 241, 20))
        self.summedNameLineEdit.setObjectName(_fromUtf8("summedNameLineEdit"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(loadDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(150, 40, 591, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.bestLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.bestLineEdit.setMaxLength(32766)
        self.bestLineEdit.setObjectName(_fromUtf8("bestLineEdit"))
        self.horizontalLayout_2.addWidget(self.bestLineEdit)
        self.bestButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.bestButton.setObjectName(_fromUtf8("bestButton"))
        self.horizontalLayout_2.addWidget(self.bestButton)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(loadDialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(150, 210, 591, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.summedLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget_3)
        self.summedLineEdit.setObjectName(_fromUtf8("summedLineEdit"))
        self.horizontalLayout_3.addWidget(self.summedLineEdit)
        self.summedButton = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.summedButton.setObjectName(_fromUtf8("summedButton"))
        self.horizontalLayout_3.addWidget(self.summedButton)

        self.retranslateUi(loadDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), loadDialog.close)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.bestLabel.setVisible)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.bestNameLineEdit.setVisible)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.summedLabel.setVisible)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.summedNameLineEdit.setVisible)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.bestLineEdit.setVisible)
        QtCore.QObject.connect(self.bestCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.bestButton.setVisible)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.summedLineEdit.setVisible)
        QtCore.QObject.connect(self.summedCheckBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.summedButton.setVisible)
        QtCore.QMetaObject.connectSlotsByName(loadDialog)

    def retranslateUi(self, loadDialog):
        loadDialog.setWindowTitle(_translate("loadDialog", "Load previous Marxan results", None))
        self.okButton.setText(_translate("loadDialog", "OK", None))
        self.cancelButton.setText(_translate("loadDialog", "Cancel", None))
        self.bestCheckBox.setText(_translate("loadDialog", "Load best solution results (default name is *_best.txt)", None))
        self.bestLabel.setText(_translate("loadDialog", "New best field name", None))
        self.summedCheckBox.setText(_translate("loadDialog", "Load summed solution results (default name is *_ssoln.txt)", None))
        self.summedLabel.setText(_translate("loadDialog", "New summed solution field name", None))
        self.bestButton.setText(_translate("loadDialog", "Browse", None))
        self.summedButton.setText(_translate("loadDialog", "Browse", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    loadDialog = QtGui.QDialog()
    ui = Ui_loadDialog()
    ui.setupUi(loadDialog)
    loadDialog.show()
    sys.exit(app.exec_())

