# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_start.ui'
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

class Ui_startDialog(object):
    def setupUi(self, startDialog):
        startDialog.setObjectName(_fromUtf8("startDialog"))
        startDialog.resize(500, 300)
        startDialog.setMinimumSize(QtCore.QSize(500, 300))
        self.horizontalLayoutWidget = QtGui.QWidget(startDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(180, 230, 181, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.graphicLabel = QtGui.QLabel(startDialog)
        self.graphicLabel.setGeometry(QtCore.QRect(20, 30, 51, 51))
        self.graphicLabel.setText(_fromUtf8(""))
        self.graphicLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Cluz/icons/icons/marxan_logo_small.png")))
        self.graphicLabel.setObjectName(_fromUtf8("graphicLabel"))
        self.verticalLayoutWidget = QtGui.QWidget(startDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 20, 232, 181))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(230, 0))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.openRadioButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.openRadioButton.setMinimumSize(QtCore.QSize(211, 20))
        self.openRadioButton.setChecked(True)
        self.openRadioButton.setObjectName(_fromUtf8("openRadioButton"))
        self.verticalLayout.addWidget(self.openRadioButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.createButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.createButton.setMinimumSize(QtCore.QSize(211, 20))
        self.createButton.setCheckable(True)
        self.createButton.setObjectName(_fromUtf8("createButton"))
        self.verticalLayout.addWidget(self.createButton)

        self.retranslateUi(startDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), startDialog.close)
        QtCore.QMetaObject.connectSlotsByName(startDialog)

    def retranslateUi(self, startDialog):
        startDialog.setWindowTitle(_translate("startDialog", "Select or create CLUZ setup file", None))
        self.okButton.setText(_translate("startDialog", "OK", None))
        self.cancelButton.setText(_translate("startDialog", "Cancel", None))
        self.label.setText(_translate("startDialog", "The selected action cannot continue because a CLUZ setup file has not been specified.\n"
"\n"
"Please open an existing setup file or create a new one.", None))
        self.openRadioButton.setText(_translate("startDialog", "Open existing setup file", None))
        self.createButton.setText(_translate("startDialog", "Create new setup file", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    startDialog = QtGui.QDialog()
    ui = Ui_startDialog()
    ui.setupUi(startDialog)
    startDialog.show()
    sys.exit(app.exec_())

