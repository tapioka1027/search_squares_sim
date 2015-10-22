import random

from search_robot import *

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QTextBrowser,
                             QLabel, QLineEdit, QPushButton, QComboBox)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(-10, 0, 700, 480)
        self.graphicsView.setScene(scene)
        self.searchrobot = search_robot(680,480, 40)
        scene.addItem(self.searchrobot)

        self.graphicsView2 = QGraphicsView()
        gscene = QGraphicsScene(self.graphicsView2)
        gscene.setSceneRect(0, 0, 300, 300)
        self.graphicsView2.setScene(gscene)
        #gscene.addItem(self.searchrobot)

        self.intervalcombo = QComboBox(self)
        self.agentcombo = QComboBox(self)
        self.searchmodecombo = QComboBox(self)
        self.resetButton = QPushButton("&Reset")
        self.resetButton.clicked.connect(self.reset)
        self.nextButton = QPushButton("&Next")
        self.nextButton.clicked.connect(self.do_next)
        self.autoButton = QPushButton("&Auto")
        self.autoButton.clicked.connect(self.auto)
        self.loopButton = QPushButton("&Loop")
        self.loopButton.clicked.connect(self.loop)
        self.stopButton = QPushButton("&Stop")
        self.stopButton.clicked.connect(self.stop)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.intervalcombo)
        buttonLayout.addWidget(self.agentcombo)
        buttonLayout.addWidget(self.searchmodecombo)
        buttonLayout.addWidget(self.resetButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.autoButton)
        buttonLayout.addWidget(self.loopButton)
        buttonLayout.addWidget(self.stopButton)

        self.interval = 5
        for i in ("5", "10", "30", "50", "100"):
            self.intervalcombo.addItem(i)
        self.intervalcombo.activated.connect(self.set_interval)

        for i in ("UniformCost", "A*", "LRTA*"):
            self.agentcombo.addItem(i)
        self.agentcombo.activated.connect(self.reset)

        for i in ("random", "UpDownLeftRight", "LeftRightUpDown", "RightLeftDownUp"):
            self.searchmodecombo.addItem(i)
        self.searchmodecombo.activated.connect(self.reset)

        self.costtext = QLabel("0")
        showcostLayout = QHBoxLayout()
        showcostLayout.addWidget(QLabel("Last cost:"))
        showcostLayout.addWidget(self.costtext)

        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(buttonLayout)
        propertyLayout.addLayout(showcostLayout)
        propertyLayout.addWidget(self.graphicsView2)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        #self.resize(1000,600)
        self.setWindowTitle("Seach Squares Simulation")
        self.updating_rule = False
        self.timer = None
        self.loopflag = False

    def update_rule(self):
        if self.updating_rule: return
        rule = 0
        for i in range(8):
            n = self.ruleEdits[i].text()
            if n == "": return
            rule = (rule << 1) + int(n)
        self.updating_rule = True
        self.updating_rule = False

    def set_interval(self):
        self.stop()
        self.interval = int(self.intervalcombo.currentText())

    def reset(self):
        if not self.loopflag:
            self.stop()
        self.searchrobot.reset(self.agentcombo.currentText(), self.searchmodecombo.currentText())

    def do_next(self):
        return self.searchrobot.update_map()

    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def loop(self):
        self.loopflag = True
        self.auto()

    def timeout(self):
        r = self.do_next()
        self.costtext.setText(str(self.searchrobot.lastcount))
        if not r:
            if self.loopflag:
                self.reset()
            else:
                self.stop()

    def stop(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
            self.loopflag = False

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
