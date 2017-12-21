# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
'''
Design of the gui
Participants:
    Gustaf Soderholm
    Alexander Zeijlon
Last changed:
    20/12-2017
'''




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
        MainWindow.resize(1047, 864)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.sendparam = QtGui.QPushButton(self.centralwidget)
        self.sendparam.setGeometry(QtCore.QRect(390, 770, 111, 31))
        self.sendparam.setObjectName(_fromUtf8("sendparam"))
        self.W = QtGui.QPushButton(self.centralwidget)
        self.W.setGeometry(QtCore.QRect(140, 650, 81, 51))
#        self.W.setCheckable(True)
        self.W.setChecked(False)
        self.W.setAutoRepeat(False)
        self.W.setAutoDefault(False)
        self.W.setDefault(False)
        self.W.setFlat(False)
        self.W.setObjectName(_fromUtf8("W"))
        self.pid_p = QtGui.QLineEdit(self.centralwidget)
        self.pid_p.setGeometry(QtCore.QRect(390, 690, 113, 31))
        self.pid_p.setObjectName(_fromUtf8("pid_p"))
        self.pid_p.setValidator(validator)
        self.pid_d = QtGui.QLineEdit(self.centralwidget)
        self.pid_d.setGeometry(QtCore.QRect(390, 730, 113, 33))
        self.pid_d.setObjectName(_fromUtf8("pid_d"))
        self.pid_d.setValidator(validator)
        self.A = QtGui.QPushButton(self.centralwidget)
        self.A.setGeometry(QtCore.QRect(50, 710, 81, 51))
#        self.A.setCheckable(True)
        self.A.setObjectName(_fromUtf8("A"))
        self.S = QtGui.QPushButton(self.centralwidget)
        self.S.setGeometry(QtCore.QRect(140, 710, 81, 51))
#        self.S.setCheckable(True)
        self.S.setObjectName(_fromUtf8("S"))
        self.D = QtGui.QPushButton(self.centralwidget)
        self.D.setGeometry(QtCore.QRect(230, 710, 81, 51))
#        self.D.setCheckable(True)
        self.D.setObjectName(_fromUtf8("D"))
        self.stop = QtGui.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(70, 770, 221, 51))
        self.stop.setObjectName(_fromUtf8("stop"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 690, 41, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 730, 41, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 1021, 611))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 630, 1041, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(890, 660, 131, 41))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.lcdNumber_2 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(890, 730, 131, 41))
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(850, 730, 41, 41))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(850, 660, 41, 41))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(590, 710, 221, 101))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(660, 650, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1047, 19))
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
        self.stop.setText(_translate("MainWindow", "Run", None))
        self.label.setText(_translate("MainWindow", "pid-P", None))
        self.label_2.setText(_translate("MainWindow", "pid-D", None))
        self.label_3.setText(_translate("MainWindow", "Rpm", None))
        self.label_4.setText(_translate("MainWindow", "Lap", None))
        self.pushButton.setText(_translate("MainWindow", "Mode", None))
        self.label_5.setText(_translate("MainWindow", "Manual", None))
        self.menu.setTitle(_translate("MainWindow", "Menu", None))
        self.quit.setText(_translate("MainWindow", "Quit", None))

