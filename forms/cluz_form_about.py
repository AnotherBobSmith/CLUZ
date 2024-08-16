# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\rjsmi\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cluz\forms\cluz_form_about.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.setMinimumSize(QtCore.QSize(630, 260))
        self.gridLayout = QtWidgets.QGridLayout(aboutDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.iconLogo = QtWidgets.QLabel(aboutDialog)
        self.iconLogo.setText("")
        self.iconLogo.setPixmap(QtGui.QPixmap(":/logos/images/marxan_logo.png"))
        self.iconLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.iconLogo.setObjectName("iconLogo")
        self.horizontalLayout.addWidget(self.iconLogo)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.authorLabel = QtWidgets.QLabel(aboutDialog)
        self.authorLabel.setOpenExternalLinks(True)
        self.authorLabel.setObjectName("authorLabel")
        self.verticalLayout.addWidget(self.authorLabel)
        self.fundedLabel = QtWidgets.QLabel(aboutDialog)
        self.fundedLabel.setOpenExternalLinks(True)
        self.fundedLabel.setObjectName("fundedLabel")
        self.verticalLayout.addWidget(self.fundedLabel)
        self.codeLabel = QtWidgets.QLabel(aboutDialog)
        self.codeLabel.setOpenExternalLinks(True)
        self.codeLabel.setObjectName("codeLabel")
        self.verticalLayout.addWidget(self.codeLabel)
        self.websiteLLabel = QtWidgets.QLabel(aboutDialog)
        self.websiteLLabel.setOpenExternalLinks(True)
        self.websiteLLabel.setObjectName("websiteLLabel")
        self.verticalLayout.addWidget(self.websiteLLabel)
        self.mailingLabel = QtWidgets.QLabel(aboutDialog)
        self.mailingLabel.setOpenExternalLinks(True)
        self.mailingLabel.setObjectName("mailingLabel")
        self.verticalLayout.addWidget(self.mailingLabel)
        self.citationLabel = QtWidgets.QLabel(aboutDialog)
        self.citationLabel.setWordWrap(True)
        self.citationLabel.setOpenExternalLinks(True)
        self.citationLabel.setObjectName("citationLabel")
        self.verticalLayout.addWidget(self.citationLabel)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(aboutDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(aboutDialog)
        self.pushButton.clicked.connect(aboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        _translate = QtCore.QCoreApplication.translate
        aboutDialog.setWindowTitle(_translate("aboutDialog", "About CLUZ"))
        self.authorLabel.setText(_translate("aboutDialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Written by</span><span style=\" font-size:10pt;\">: Bob Smith, </span><a href=\"https://www.kent.ac.uk/dice\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">Durrell Institute of Conservation and Ecology</span></a></p></body></html>"))
        self.fundedLabel.setText(_translate("aboutDialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Funded by</span><span style=\" font-size:10pt;\">: </span><a href=\"http://www.darwininitiative.org.uk/\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">UK Government\'s Darwin Initiative</span></a></p></body></html>"))
        self.codeLabel.setText(_translate("aboutDialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Code</span><span style=\" font-size:10pt;\">: </span><a href=\"https://github.com/AnotherBobSmith/CLUZ_QGIS3\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">https://github.com/AnotherBobSmith/CLUZ_QGIS3</span></a></p></body></html>"))
        self.websiteLLabel.setText(_translate("aboutDialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Website</span><span style=\" font-size:10pt;\">: </span><a href=\"https://anotherbobsmith.github.io/cluz\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">https://anotherbobsmith.github.io/cluz</span></a></p></body></html>"))
        self.mailingLabel.setText(_translate("aboutDialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Mailing list</span><span style=\" font-size:10pt;\">: </span><a href=\"http://eepurl.com/geIHtf\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">http://eepurl.com/geIHtf</span></a></p></body></html>"))
        self.citationLabel.setText(_translate("aboutDialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Citation</span><span style=\" font-size:10pt;\">: Smith, RJ (2019). The CLUZ plugin for QGIS: designing conservation area systems and other ecological networks.</span><span style=\" font-size:10pt; font-style:italic;\"> Research Ideas and Outcome</span><span style=\" font-size:10pt;\">s, </span><span style=\" font-size:10pt; font-weight:600;\">5</span><span style=\" font-size:10pt;\">, </span><a href=\"https://riojournal.com/article/33510/\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">e33510</span></a><span style=\" font-size:10pt;\">.</span></p></body></html>"))
        self.pushButton.setText(_translate("aboutDialog", "Close"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    aboutDialog = QtWidgets.QDialog()
    ui = Ui_aboutDialog()
    ui.setupUi(aboutDialog)
    aboutDialog.show()
    sys.exit(app.exec_())

