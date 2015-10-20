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
        self.is_finish = False

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
        pen = painter.pen()
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setPen(QColor(220,220,220))
        for y in range(self.NH + 1):
            painter.drawLine(0, y*self.size, self.width, y*self.size)
        for x in range(self.NW + 1):
            painter.drawLine(x*self.size, 0, x*self.size, self.height)

        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(15)
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
                    printnum = self.agent.routemap[y][x]
                    if printnum < 10:
                        painter.drawText(self.size*x+16, self.size*y+10, self.size, self.size, self.size, str(printnum))
                    elif printnum < 100:
                        painter.drawText(self.size*x+10, self.size*y+10, self.size, self.size, self.size, str(printnum))
                    else:
                        painter.drawText(self.size*x+6, self.size*y+10, self.size, self.size, self.size, str(printnum))

        if self.is_finish:
            pen.setWidth(5)
            pen.setColor(QColor(255, 165, 0))
            painter.setPen(pen)
            points = []
            for point in self.agent.tracelist:
                print(point)
                points.append(QPointF(self.size*(point[0]+0.5), self.size*(point[1]+0.5)))
            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i+1])

    def reset(self, str="UniformCost"):
        self.agent = None
        if str == "UniformCost":
            print(str)
            self.agent = UniformCostAgent(colormap=copy.deepcopy(self.colormap))
        elif str == "A*":
            print(str)
            self.agent = AstarAgent(colormap=copy.deepcopy(self.colormap))
        elif str == "LRTA*":
            print(str)
            self.agent = UniformCostAgent(colormap=copy.deepcopy(self.colormap))
        self.update()

    def update_map(self):
        r = self.agent.do_next()
        while r == 0:
            r = self.agent.do_next()
        else:
            if r == 1:
                self.update()
                return True
            else:
                self.is_finish = True
                self.update()
                return False

    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)
