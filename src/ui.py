from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt



class Ui_Assistant(object):

    def setupUi(self, Assistant):
        Assistant.setObjectName("Assistant")
        Assistant.resize(450, 400)
        Assistant.setFixedWidth(450)
        Assistant.setFixedHeight(400)
        Assistant.setWindowIcon(QtGui.QIcon('iicon.png'))
        self.centralwidget = QtWidgets.QWidget(Assistant)
        self.centralwidget.setObjectName("centralwidget")
      
        Assistant.setCentralWidget(self.centralwidget)

        #init button
        self.activate_button = QtWidgets.QPushButton(self.centralwidget)
        self.activate_button.setGeometry(QtCore.QRect(125, 50, 200, 200))
        font = QtGui.QFont()
        font.setFamily("Freestyle Script")
        font.setPointSize(35)
        self.activate_button.setFont(font)
        self.default="""QPushButton {\n
    color: #333;\n
    border: 2px solid #555;\n
    border-radius: 100px;\n
    border-style: outset;\n
    background: qradialgradient(\n
        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n
        radius: 1.35, stop: 0 #fff, stop: 1 #888\n
        );\n
    padding: 5px;\n
    }\n
\n
QPushButton:hover {\n
    background: qradialgradient(\n
        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n
        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n
        );\n
    }\n
\n
QPushButton:pressed {\n
    border-style: inset;\n
    background: qradialgradient(\n
        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n
        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n
        );\n
    }"""
        self.activate_button.setStyleSheet(self.default)
        self.activate_button.setObjectName("activate_button")

        #text label
        self.output = QtWidgets.QLabel(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(25, 260, 400, 150))
        font = QtGui.QFont()
        font.setFamily("Freestyle Script")
        font.setPointSize(20)
        font.setKerning(True)
        self.output.setFont(font)
        self.output.setAutoFillBackground(False)
        self.output.setScaledContents(False)
        self.output.setAlignment(QtCore.Qt.AlignCenter)
        self.output.setObjectName("output")


        #upper text
        self.direct = QtWidgets.QLabel(self.centralwidget)
        self.direct.setGeometry(QtCore.QRect(25, 10, 400, 30))
        font = QtGui.QFont()
        font.setFamily("Freestyle Script")
        font.setPointSize(20)
        font.setKerning(True)
        self.direct.setFont(font)
        self.direct.setAutoFillBackground(False)
        self.direct.setScaledContents(False)
        self.direct.setAlignment(QtCore.Qt.AlignCenter)
        self.direct.setObjectName("direct")


        self.retranslateUi(Assistant)
        QtCore.QMetaObject.connectSlotsByName(Assistant)

        
        

    def retranslateUi(self, Assistant):
        _translate = QtCore.QCoreApplication.translate
        Assistant.setWindowTitle(_translate("Assistant", "Assistant"))
        self.activate_button.setText(_translate("Assistant", "Activate"))
        self.output.setText(_translate("Assistant", " "))
        self.direct.setText(_translate("Assistant", "Activate to Start listening"))
