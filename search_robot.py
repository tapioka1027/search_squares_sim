import random
import copy

from Search_method import *

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

        #make map
        self.colormap = []
        self.colormap.append([0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0])
        self.colormap.append([0, 0.5, 0.5, 0.5, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0.5])
        self.colormap.append([0, 0.5, 0, 0.5, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0.5])
        self.colormap.append([0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0.5])
        self.colormap.append([0.5, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.colormap.append([0.5, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0])
        self.colormap.append([0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0])
        self.colormap.append([0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
        self.colormap.append([0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0])
        self.colormap.append([0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0])
        self.colormap.append([0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
        self.colormap.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0, 0, 0, 0])

        self.agent = UniformCostAgent(colormap=copy.deepcopy(self.colormap))

    def paint(self, painter, option, widget):
        painter.setPen(QColor(220,220,220))
        for y in range(self.NH + 1):
            painter.drawLine(0, y*self.size, self.width, y*self.size)
        for x in range(self.NW + 1):
            painter.drawLine(x*self.size, 0, x*self.size, self.height)

        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(20)
        font.setBold(True)
        painter.setFont(font)

        for y in range(self.NH):
            for x in range(self.NW):
                #if self.board[y][x] == 1:
                if self.colormap[y][x] == 1:
                    painter.setBrush(Qt.black)
                    painter.drawRect(self.size*x, self.size*y, self.size, self.size)
                elif self.colormap[y][x] == 0.5:
                    painter.setBrush(Qt.gray)
                    painter.drawRect(self.size*x, self.size*y, self.size, self.size)
                elif self.colormap[y][x] == 2:
                    painter.drawText(self.size*x+10, self.size*y+10, self.size, self.size, self.size, 'S')
                elif self.colormap[y][x] == 3:
                    painter.drawText(self.size*x+10, self.size*y+10, self.size, self.size, self.size, 'G')

                if self.agent.routemap[y][x] != -1:
                    painter.drawText(self.size*x+10, self.size*y+10, self.size, self.size, self.size, str(self.agent.routemap[y][x]))

    def update_map(self):
        self.agent.do_next()

    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)
