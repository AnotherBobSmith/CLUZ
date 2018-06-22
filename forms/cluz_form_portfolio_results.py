# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cluz_form_portfolio_results.ui'
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

class Ui_portfolioResultsDialog(object):
    def setupUi(self, portfolioResultsDialog):
        portfolioResultsDialog.setObjectName(_fromUtf8("portfolioResultsDialog"))
        portfolioResultsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        portfolioResultsDialog.resize(768, 547)
        self.gridLayout = QtGui.QGridLayout(portfolioResultsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(portfolioResultsDialog)
        self.tabWidget.setMinimumSize(QtCore.QSize(750, 500))
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.statusTab = QtGui.QWidget()
        self.statusTab.setObjectName(_fromUtf8("statusTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.statusTab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.statusTabTableWidget = QtGui.QTableWidget(self.statusTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusTabTableWidget.sizePolicy().hasHeightForWidth())
        self.statusTabTableWidget.setSizePolicy(sizePolicy)
        self.statusTabTableWidget.setMinimumSize(QtCore.QSize(500, 400))
        self.statusTabTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.statusTabTableWidget.setAlternatingRowColors(True)
        self.statusTabTableWidget.setObjectName(_fromUtf8("statusTabTableWidget"))
        self.statusTabTableWidget.setColumnCount(0)
        self.statusTabTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.statusTabTableWidget)
        self.tabWidget.addTab(self.statusTab, _fromUtf8(""))
        self.patchTab = QtGui.QWidget()
        self.patchTab.setObjectName(_fromUtf8("patchTab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.patchTab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spatialTabTableWidget = QtGui.QTableWidget(self.patchTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spatialTabTableWidget.sizePolicy().hasHeightForWidth())
        self.spatialTabTableWidget.setSizePolicy(sizePolicy)
        self.spatialTabTableWidget.setMinimumSize(QtCore.QSize(500, 400))
        self.spatialTabTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.spatialTabTableWidget.setAlternatingRowColors(True)
        self.spatialTabTableWidget.setObjectName(_fromUtf8("spatialTabTableWidget"))
        self.spatialTabTableWidget.setColumnCount(0)
        self.spatialTabTableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.spatialTabTableWidget)
        self.tabWidget.addTab(self.patchTab, _fromUtf8(""))
        self.sfTab = QtGui.QWidget()
        self.sfTab.setObjectName(_fromUtf8("sfTab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.sfTab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sfTabTableWidget = QtGui.QTableWidget(self.sfTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sfTabTableWidget.sizePolicy().hasHeightForWidth())
        self.sfTabTableWidget.setSizePolicy(sizePolicy)
        self.sfTabTableWidget.setMinimumSize(QtCore.QSize(500, 400))
        self.sfTabTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.sfTabTableWidget.setAlternatingRowColors(True)
        self.sfTabTableWidget.setObjectName(_fromUtf8("sfTabTableWidget"))
        self.sfTabTableWidget.setColumnCount(0)
        self.sfTabTableWidget.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.sfTabTableWidget)
        self.tabWidget.addTab(self.sfTab, _fromUtf8(""))
        self.patchFeatTab = QtGui.QWidget()
        self.patchFeatTab.setObjectName(_fromUtf8("patchFeatTab"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.patchFeatTab)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.patchFeatTabTableWidget = QtGui.QTableWidget(self.patchFeatTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.patchFeatTabTableWidget.sizePolicy().hasHeightForWidth())
        self.patchFeatTabTableWidget.setSizePolicy(sizePolicy)
        self.patchFeatTabTableWidget.setMinimumSize(QtCore.QSize(500, 400))
        self.patchFeatTabTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.patchFeatTabTableWidget.setAlternatingRowColors(True)
        self.patchFeatTabTableWidget.setObjectName(_fromUtf8("patchFeatTabTableWidget"))
        self.patchFeatTabTableWidget.setColumnCount(0)
        self.patchFeatTabTableWidget.setRowCount(0)
        self.horizontalLayout_3.addWidget(self.patchFeatTabTableWidget)
        self.tabWidget.addTab(self.patchFeatTab, _fromUtf8(""))
        self.peTab = QtGui.QWidget()
        self.peTab.setObjectName(_fromUtf8("peTab"))
        self.tabWidget.addTab(self.peTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.closeButton = QtGui.QPushButton(portfolioResultsDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 1, 0, 1, 1)

        self.retranslateUi(portfolioResultsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), portfolioResultsDialog.close)
        QtCore.QMetaObject.connectSlotsByName(portfolioResultsDialog)

    def retranslateUi(self, portfolioResultsDialog):
        portfolioResultsDialog.setWindowTitle(_translate("portfolioResultsDialog", "Portfolio details table", None))
        self.statusTabTableWidget.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.statusTab), _translate("portfolioResultsDialog", "Status results", None))
        self.spatialTabTableWidget.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.patchTab), _translate("portfolioResultsDialog", "Spatial results", None))
        self.sfTabTableWidget.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sfTab), _translate("portfolioResultsDialog", "Selection frequency results", None))
        self.patchFeatTabTableWidget.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.patchFeatTab), _translate("portfolioResultsDialog", "Patches per feature", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.peTab), _translate("portfolioResultsDialog", "Protection equality", None))
        self.closeButton.setText(_translate("portfolioResultsDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    portfolioResultsDialog = QtGui.QDialog()
    ui = Ui_portfolioResultsDialog()
    ui.setupUi(portfolioResultsDialog)
    portfolioResultsDialog.show()
    sys.exit(app.exec_())

