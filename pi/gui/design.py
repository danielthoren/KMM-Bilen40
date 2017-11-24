# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created: Thu Nov 23 10:36:18 2017
#      by: PyQt4 UI code generator 4.11.2
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
        validator = QtGui.QDoubleValidator()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(318, 362)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.sendparam = QtGui.QPushButton(self.centralwidget)
        self.sendparam.setGeometry(QtCore.QRect(10, 90, 111, 31))
        self.sendparam.setObjectName(_fromUtf8("sendparam"))
        self.W = QtGui.QPushButton(self.centralwidget)
        self.W.setGeometry(QtCore.QRect(120, 130, 81, 51))
#        self.W.setCheckable(True)
        self.W.setObjectName(_fromUtf8("W"))
        self.pid_p = QtGui.QLineEdit(self.centralwidget)
        self.pid_p.setGeometry(QtCore.QRect(50, 10, 113, 31))
        self.pid_p.setObjectName(_fromUtf8("pid_p"))
        self.pid_p.setValidator(validator)
        self.pid_d = QtGui.QLineEdit(self.centralwidget)
        self.pid_d.setGeometry(QtCore.QRect(50, 50, 113, 33))
        self.pid_d.setObjectName(_fromUtf8("pid_d"))
        self.pid_d.setValidator(validator)
        self.A = QtGui.QPushButton(self.centralwidget)
        self.A.setGeometry(QtCore.QRect(30, 190, 81, 51))
        self.A.setObjectName(_fromUtf8("A"))
        self.S = QtGui.QPushButton(self.centralwidget)
        self.S.setGeometry(QtCore.QRect(120, 190, 81, 51))
 #       self.S.setCheckable(True)
        self.S.setObjectName(_fromUtf8("S"))
        self.D = QtGui.QPushButton(self.centralwidget)
        self.D.setGeometry(QtCore.QRect(210, 190, 81, 51))
        self.D.setObjectName(_fromUtf8("D"))
        self.stop = QtGui.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(50, 250, 221, 51))
        self.stop.setObjectName(_fromUtf8("stop"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 41, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 41, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 318, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.quit = QtGui.QAction(MainWindow)
        self.quit.setObjectName(_fromUtf8("quit"))
        self.menu.addAction(self.quit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.sendparam.setText(_translate("MainWindow", "Send param.", None))
        self.W.setText(_translate("MainWindow", "W", None))
        self.A.setText(_translate("MainWindow", "A", None))
        self.S.setText(_translate("MainWindow", "S", None))
        self.D.setText(_translate("MainWindow", "D", None))
        self.stop.setText(_translate("MainWindow", "STOP!", None))
        self.label.setText(_translate("MainWindow", "pid-P", None))
        self.label_2.setText(_translate("MainWindow", "pid-D", None))
        self.menu.setTitle(_translate("MainWindow", "Menu", None))
        self.quit.setText(_translate("MainWindow", "Quit", None))

