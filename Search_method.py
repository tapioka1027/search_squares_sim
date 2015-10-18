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

        self.qu = Queue()
        self.routemap = []
        for y in range(12):
            self.routemap.append([-1] * 17)
        self.routemap[starty][startx] = 0
        self.colormap = colormap

        self.do_next()
        #print(self.colormap)

    def do_next(self):
        searchlist = ()
        chooselist = [SearchList.UDLR, SearchList.LRUD, SearchList.RLDU]
        if self.searchmode == SearchList.rand:
            searchlist = random.choice(chooselist).value
        else:
            searchlist = self.searchmode.value
    
