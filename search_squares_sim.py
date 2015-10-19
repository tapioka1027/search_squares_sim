import random

from search_robot import *

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 680, 480)
        self.graphicsView.setScene(scene)
        self.searchrobot = search_robot(680,480, 40)
        scene.addItem(self.searchrobot)

        validator = QIntValidator(0,1)
        ruleLayout = QGridLayout()
        ruleLayout.setAlignment(Qt.AlignTop)
        self.ruleEdits = []
        for i in range(7,-1,-1):
            ruleEdit = QLineEdit()
            ruleEdit.setValidator(validator)
            ruleEdit.setText("0")
            ruleEdit.setFixedWidth(30)
            ruleEdit.textEdited.connect(self.update_rule)
            ruleLayout.addWidget(QLabel("{0:03b}".format(i)), 0, 7-i)
            ruleLayout.addWidget(ruleEdit, 1,7-i)
            self.ruleEdits.append(ruleEdit)

        self.agentcombo = QComboBox(self)
        self.resetButton = QPushButton("&Reset")
        self.nextButton = QPushButton("&Next")
        self.nextButton.clicked.connect(self.do_next)
        self.autoButton = QPushButton("&Auto")
        self.autoButton.clicked.connect(self.auto)
        self.stopButton = QPushButton("&Stop")
        self.stopButton.clicked.connect(self.stop)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.agentcombo)
        buttonLayout.addWidget(self.resetButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.autoButton)
        buttonLayout.addWidget(self.stopButton)

        for i in ("UniformCost", "A*", "LRTA*"):
            self.agentcombo.addItem(i)
        self.agentcombo.activated.connect(self.reset)

        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(ruleLayout)
        propertyLayout.addLayout(buttonLayout)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Seach Squares Simulation")
        self.updating_rule = False
        self.timer = None

    def update_rule(self):
        if self.updating_rule: return
        rule = 0
        for i in range(8):
            n = self.ruleEdits[i].text()
            if n == "": return
            rule = (rule << 1) + int(n)
        self.updating_rule = True
        self.updating_rule = False

    def reset(self):
        print(self.agentcombo.currentText())

    def do_next(self):
        return self.searchrobot.update_map()

    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def timeout(self):
        r = self.do_next()
        if not r:
            self.stop()

    def stop(self):
        if self.timer:
            self.timer.stop()
            self.timer = None

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
