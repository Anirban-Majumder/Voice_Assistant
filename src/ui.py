from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QWidget
from PyQt5.QtGui import QIcon, QFont, QFontDatabase



class Ui_Assistant(object):

    def setupUi(self, Assistant):
        Assistant.setObjectName("Assistant")
        Assistant.resize(450, 400)
        Assistant.setFixedWidth(450)
        Assistant.setFixedHeight(400)
        Assistant.setWindowIcon(QIcon('iicon.png'))
        self.centralwidget = QWidget(Assistant)
        self.centralwidget.setObjectName("centralwidget")
        Assistant.setCentralWidget(self.centralwidget)

        # load font
        fontId = QFontDatabase.addApplicationFont("fonts/Rajdhani.ttf")
        families = QFontDatabase.applicationFontFamilies(fontId)
        self.font = QFont(families[0])

        # init button
        self.activate_button = QPushButton(self.centralwidget)
        self.activate_button.setGeometry(QRect(125, 50, 200, 200))
        font = self.font
        font.setPointSize(35)
        self.activate_button.setFont(font)
        self.default="""
        QPushButton {
            color: #333;
            border: 2px solid #555;
            border-radius: 100px;
            border-style: outset;
            background: qradialgradient(
                cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                radius: 1.35, stop: 0 #fff, stop: 1 #888
                );
            padding: 5px;
            }
        QPushButton:hover {
            background: qradialgradient(
                cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                radius: 1.35, stop: 0 #fff, stop: 1 #bbb
                );
            }
        """
        self.activate_button.setStyleSheet(self.default)
        self.activate_button.setObjectName("activate_button")

        # text label
        self.output = QLabel(self.centralwidget)
        self.output.setGeometry(QRect(25, 260, 400, 150))
        font = self.font
        font.setPointSize(20)
        font.setKerning(True)
        self.output.setFont(font)
        self.output.setAutoFillBackground(False)
        self.output.setScaledContents(False)
        self.output.setAlignment(Qt.AlignCenter)
        self.output.setObjectName("output")

        # upper text
        self.direct = QLabel(self.centralwidget)
        self.direct.setGeometry(QRect(25, 10, 400, 30))
        font = self.font
        font.setPointSize(20)
        font.setKerning(True)
        self.direct.setFont(font)
        self.direct.setAutoFillBackground(False)
        self.direct.setScaledContents(False)
        self.direct.setAlignment(Qt.AlignCenter)
        self.direct.setObjectName("direct")

        self.retranslateUi(Assistant)
        QMetaObject.connectSlotsByName(Assistant)


    def retranslateUi(self, Assistant):
        _translate = QCoreApplication.translate
        Assistant.setWindowTitle(_translate("Assistant", "Voice Assistant"))
        self.activate_button.setText(_translate("Assistant", "Activate"))
        self.output.setText(_translate("Assistant", " "))
        self.direct.setText(_translate("Assistant", "Activate to Start listening"))
