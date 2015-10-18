import random

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

class search_robot(QGraphicsItem):
    def __init__(self, width=500, height=500, size=20):
        super(search_robot, self).__init__()
        self.width = width
        self.height = height
        self.size = size
        self.NH = self.height//size
        self.NW = self.width//size
        self.board = []
        for y in range(self.NH):
            self.board.append([0] * self.NW)
        self.board[0][self.NW//2] = 1
        self.pos = 0

    def paint(self, painter, option, widget):
        painter.setPen(QColor(220,220,220))
        for y in range(self.NH):
            painter.drawLine(0, y*self.size, self.width, y*self.size)
        for x in range(self.NW):
            painter.drawLine(x*self.size, 0, x*self.size, self.height)

        painter.setBrush(Qt.blue)
        for y in range(self.NH):
            for x in range(self.NW):
                if self.board[y][x] == 1:
                    painter.drawRect(self.size*x, self.size*y, self.size, self.size)

    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)
