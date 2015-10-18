import random

from search_robot import *

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 400, 400)
        self.graphicsView.setScene(scene)
        self.celluarAutomaton = CelllarAutomaton(400,400)
        scene.addItem(self.celluarAutomaton)

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

        self.resetButton = QPushButton("&Reset")
        self.randomInitButton = QPushButton("&Random init")
        self.nextButton = QPushButton("&Next")
        self.prevButton = QPushButton("&Prev")
        self.autoButton = QPushButton("&Auto")
        self.stopButton = QPushButton("&Stop")
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.resetButton)
        buttonLayout.addWidget(self.randomInitButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.prevButton)
        buttonLayout.addWidget(self.autoButton)
        buttonLayout.addWidget(self.stopButton)

        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(ruleLayout)
        propertyLayout.addLayout(buttonLayout)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Cellular Automaton")
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

    def update_rule10(self):
        n = self.rule10Edit.text()
        if n == "": return
        rule = int(n)
        self.updating_rule = True
        for i in range(7,-1,-1):
            self.ruleEdits[i].setText(str(rule & 0b1))
            rule >>= 1
        self.updating_rule = False

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

    #def keyPressEvent(self, event):
    #    key = event.key()
    #    super(MainWindow, self).keyPressEvent(event)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
