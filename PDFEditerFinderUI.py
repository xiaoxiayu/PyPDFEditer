# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\WORK\python\finder.ui'
#
# Created: Fri Feb 15 03:51:12 2013
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(525, 315)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(80, 20, 311, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.widget = QtGui.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(-50, 10, 351, 21))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.btn_fobj = QtGui.QPushButton(self.widget)
        self.btn_fobj.setGeometry(QtCore.QRect(320, 0, 31, 21))
        self.btn_fobj.setObjectName(_fromUtf8("btn_fobj"))
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 0, 201, 21))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(60, 0, 54, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(80, 150, 311, 101))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.textEdit = QtGui.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 221, 71))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.btn_findn = QtGui.QPushButton(self.groupBox_2)
        self.btn_findn.setGeometry(QtCore.QRect(250, 20, 51, 21))
        self.btn_findn.setObjectName(_fromUtf8("btn_findn"))
        self.btn_findp = QtGui.QPushButton(self.groupBox_2)
        self.btn_findp.setGeometry(QtCore.QRect(250, 60, 51, 23))
        self.btn_findp.setObjectName(_fromUtf8("btn_findp"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "PDF", None))
        self.btn_fobj.setText(_translate("Form", "Go", None))
        self.label.setText(_translate("Form", "Object:", None))
        self.groupBox_2.setTitle(_translate("Form", "Text", None))
        self.btn_findn.setText(_translate("Form", ">>", None))
        self.btn_findp.setText(_translate("Form", "<<", None))

