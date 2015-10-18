import random

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

class CelllarAutomaton(QGraphicsItem):
    def __init__(self, width=500, height=500, size=20):
        super(CelllarAutomaton, self).__init__()
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

    def randomInit(self):
        for y in range(self.NH):
            for x in range(self.NW):
                self.board[y][x] = 0
        for x in range(self.NW):
            self.board[0][x] = int(random.random() < 0.2)
        self.pos = 0
        self.update()

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

    def do_prev(self):
        if self.pos == 0:
            return
        for x in range(self.NW):
            self.board[self.pos][x] = 0
        self.pos -= 1
        self.update()

    def do_next(self, n):
        if self.pos+1 >= self.NH:
            return False
        p = []
        for i in range(8):
            p.append(n & 0b1)
            n >>= 1

        self.board[self.pos+1][0] = p[(self.board[self.pos][0]<<1) + self.board[self.pos][1]]
        self.board[self.pos+1][self.NW-1] = p[(self.board[self.pos][self.NW-2]<<1) + self.board[self.pos][self.NW-1]]
        for x in range(1,self.NW-1):
            self.board[self.pos+1][x] = p[(self.board[self.pos][x-1]<<2)
                                            + (self.board[self.pos][x]<<1)
                                            + (self.board[self.pos][x+1])]
        self.pos += 1
        self.update()
        return True

    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)
