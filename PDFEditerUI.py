# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\WORK\python\untitled.ui'
#
# Created: Thu Feb 14 01:33:22 2013
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(639, 529)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setFrameShape(QtGui.QFrame.WinPanel)
        self.textEdit.setFrameShadow(QtGui.QFrame.Sunken)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 639, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTearOffEnabled(False)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuDocument = QtGui.QMenu(self.menubar)
        self.menuDocument.setObjectName(_fromUtf8("menuDocument"))
        self.menuPage = QtGui.QMenu(self.menubar)
        self.menuPage.setObjectName(_fromUtf8("menuPage"))
        self.menuObject = QtGui.QMenu(self.menubar)
        self.menuObject.setObjectName(_fromUtf8("menuObject"))
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setCheckable(False)
        self.actionOpen.setSoftKeyRole(QtGui.QAction.SelectSoftKey)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionInfo_Doc = QtGui.QAction(MainWindow)
        self.actionInfo_Doc.setObjectName(_fromUtf8("actionInfo_Doc"))
        self.actionOutLines = QtGui.QAction(MainWindow)
        self.actionOutLines.setObjectName(_fromUtf8("actionOutLines"))
        self.actionNamedDestination = QtGui.QAction(MainWindow)
        self.actionNamedDestination.setObjectName(_fromUtf8("actionNamedDestination"))
        self.actionTest = QtGui.QAction(MainWindow)
        self.actionTest.setObjectName(_fromUtf8("actionTest"))
        self.actionInfo_Page = QtGui.QAction(MainWindow)
        self.actionInfo_Page.setObjectName(_fromUtf8("actionInfo_Page"))
        self.actionObjGet = QtGui.QAction(MainWindow)
        self.actionObjGet.setObjectName(_fromUtf8("actionObjGet"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionFinder = QtGui.QAction(MainWindow)
        self.actionFinder.setObjectName(_fromUtf8("actionFinder"))
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFinder)
        self.menuFile.addAction(self.actionTest)
        self.menuDocument.addAction(self.actionInfo_Doc)
        self.menuDocument.addSeparator()
        self.menuDocument.addAction(self.actionOutLines)
        self.menuDocument.addAction(self.actionNamedDestination)
        self.menuPage.addAction(self.actionInfo_Page)
        self.menuObject.addAction(self.actionObjGet)
        self.menuObject.addAction(self.actionExport)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDocument.menuAction())
        self.menubar.addAction(self.menuPage.menuAction())
        self.menubar.addAction(self.menuObject.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "PDFEditViewer", None))
        self.menuFile.setToolTip(_translate("MainWindow", "PDFEditer", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuDocument.setTitle(_translate("MainWindow", "Document", None))
        self.menuPage.setTitle(_translate("MainWindow", "Page", None))
        self.menuObject.setTitle(_translate("MainWindow", "Object", None))
        self.actionOpen.setText(_translate("MainWindow", "Open...", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionInfo_Doc.setText(_translate("MainWindow", "Info", None))
        self.actionOutLines.setText(_translate("MainWindow", "OutLines", None))
        self.actionNamedDestination.setText(_translate("MainWindow", "NamedDestination", None))
        self.actionTest.setText(_translate("MainWindow", "test", None))
        self.actionInfo_Page.setText(_translate("MainWindow", "Info", None))
        self.actionObjGet.setText(_translate("MainWindow", "Get...", None))
        self.actionObjGet.setShortcut(_translate("MainWindow", "Ctrl+G", None))
        self.actionSave.setText(_translate("MainWindow", "Save...", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionFinder.setText(_translate("MainWindow", "Finder...", None))
        self.actionFinder.setShortcut(_translate("MainWindow", "Ctrl+F", None))
        self.actionExport.setText(_translate("MainWindow", "Export...", None))

