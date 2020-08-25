# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        # Form.resize(500, 468)
        Form.setFixedSize(500, 468)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 211, 41))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textEdit.setStyleSheet("")
        self.textEdit.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.textEdit.setOverwriteMode(True)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 20, 93, 41))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: #dbe3e5;\n"
"    border-radius: 15px;\n"
"    border: 1px blue solid;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setEnabled(False)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 70, 221, 181))
        self.textEdit_2.setStyleSheet("QTextEdit {\n"
"    background-color: white;\n"
"}")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(Form)
        self.textEdit_3.setEnabled(False)
        self.textEdit_3.setGeometry(QtCore.QRect(260, 70, 221, 181))
        self.textEdit_3.setStyleSheet("QTextEdit {\n"
"    background-color: white;\n"
"}")
        self.textEdit_3.setObjectName("textEdit_3")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(250, 30, 51, 20))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setEnabled(False)
        self.radioButton_2.setGeometry(QtCore.QRect(320, 30, 51, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 259, 461, 191))
        self.widget.setObjectName("widget")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(-11, -11, 481, 211))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "天气查询助手"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'3ds\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; vertical-align:middle;\">请输入城市名</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "查询"))
        self.radioButton.setText(_translate("Form", "1 天"))
        self.radioButton_2.setText(_translate("Form", "7 天"))
