import random

from queue import Queue
from enum import Enum

class SearchList(Enum):
    rand = (0, 0, 0, 0)
    UDLR = (0, 1, 2, 3) #up down left right
    LRUD = (2, 3, 0, 1)
    RLDU = (3, 2, 1, 0)
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

class UniformCostAgent():
    def __init__(self, mode=SearchList.rand, colormap=[], startx=3, starty=0, goalx=13, goaly=0):
        self.now_x = startx
        self.now_y = starty
        self.dest_x = goalx
        self.dest_y = goaly
        self.searchmode = mode

        self.now_cost = 0
        self.qu = Queue()
        self.routemap = []
        for y in range(12):
            self.routemap.append([-1] * 17)
        self.routemap[starty][startx] = 0
        self.costmap = colormap
        for y in range(self.costmap):
            for x in range(self.costmap[0]):
                if self.costmap[y][x] == 0:
                    self.costmap[y][x] == 1
                elif self.costmap[y][x] == 0.5:
                    self.costmap[y][x] == 3
                elif self.costmap[y][x] == 1:
                    self.costmap[y][x] == -1
        self.costmap[starty][startx] = -1

        self.do_next()
        #print(self.colormap)

    def update_qu(self):
        searchlist = ()
        chooselist = [SearchList.UDLR, SearchList.LRUD, SearchList.RLDU]
        if self.searchmode == SearchList.rand:
            searchlist = random.choice(chooselist).value
        else:
            searchlist = self.searchmode.value
        for i in range(searchlist):
            if i == 0:
                if self.now_y > 1 and self.costmap[now_y - 1][now_x] != -1:
                    self.qu.put([now_x, now_y - 1, now_cost])

    def do_next():
        qufront = self.qu.get()
        self.now_x = qufront_x
        
