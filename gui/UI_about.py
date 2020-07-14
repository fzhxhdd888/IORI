# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_about.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Window_about(object):
    def setupUi(self, Window_about):
        Window_about.setObjectName("Window_about")
        Window_about.resize(529, 211)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/11.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Window_about.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Window_about)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 481, 151))
        self.textBrowser.setObjectName("textBrowser")
        Window_about.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Window_about)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 529, 26))
        self.menubar.setObjectName("menubar")
        Window_about.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Window_about)
        self.statusbar.setObjectName("statusbar")
        Window_about.setStatusBar(self.statusbar)

        self.retranslateUi(Window_about)
        QtCore.QMetaObject.connectSlotsByName(Window_about)

    def retranslateUi(self, Window_about):
        _translate = QtCore.QCoreApplication.translate
        Window_about.setWindowTitle(_translate("Window_about", "About Me"))
        self.textBrowser.setHtml(_translate("Window_about", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">Automated Test program for RF </span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600; color:#000000;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Version: v1.0</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Author: Zhaohui Feng</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Email: feng.zhaohui@byd.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

