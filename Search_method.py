import random, math

from queue import PriorityQueue
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
        self.startpos = (startx, starty)
        self.destpos = (goalx, goaly)
        self.searchmode = mode

        self.now_cost = 0
        self.now_num = 0
        self.qu = PriorityQueue()
        self.qu.put((0, (startx, starty), 0)) #(cost, (nowx, nowy))
        self.mapsize_x = len(colormap[0])
        self.mapsize_y = len(colormap)

        #to store search number
        self.routemap = []
        for y in range(12):
            self.routemap.append([-1] * 17)
        self.routemap[starty][startx] = 0

        #to trace seach route
        self.tracelist = []

        self.costmap = colormap
        for y in range(len(self.costmap)):
            for x in range(len(self.costmap[0])):
                if self.costmap[y][x] == 0:
                    self.costmap[y][x] = 1
                elif self.costmap[y][x] == 0.5:
                    self.costmap[y][x] = 3
                elif self.costmap[y][x] == 1:
                    self.costmap[y][x] = -1
        self.costmap[starty][startx] = -1

        self.do_next()

    def do_next(self):
        #state memo 1:next 0:none -1:finish
        searchlist = ()
        chooselist = [SearchList.UDLR, SearchList.LRUD, SearchList.RLDU]
        templist = []
        tempqu = self.qu.get()
        routecost = tempqu[2]
        now_x = tempqu[1][0]
        now_y = tempqu[1][1]

        if routecost > 0:
            if self.costmap[now_y][now_x] == -1:
                return 0
            else:
                self.costmap[now_y][now_x] = -1
            self.now_num += 1
            self.routemap[now_y][now_x] = self.now_num

        if tempqu[1] == self.destpos:
            self.traceroute()
            return -1

        if self.searchmode == SearchList.rand:
            searchlist = random.choice(chooselist).value
        else:
            searchlist = self.searchmode.value
        for i in searchlist:
            if i == 0:
                templist.append((now_x, now_y - 1))
            elif i == 1:
                templist.append((now_x, now_y + 1))
            elif i == 2:
                templist.append((now_x - 1, now_y))
            elif i == 3:
                templist.append((now_x + 1, now_y))
        for temppos in templist:
            if temppos[0] >= 0 and temppos[1] >= 0 and temppos[0] < self.mapsize_x and temppos[1] < self.mapsize_y and self.costmap[temppos[1]][temppos[0]] != -1:
                self.qu.put((self.calccost(routecost, temppos), temppos, routecost + self.costmap[temppos[1]][temppos[0]]))
        return 1

    def calccost(self, routecost, nextpos):
        r = routecost + self.costmap[nextpos[1]][nextpos[0]]
        print(r)
        return r

    def traceroute(self):
        self.tracelist.append(self.destpos)
        nowpos = self.destpos
        minnum = 0
        minpos = nowpos
        while nowpos != self.startpos:
            self.tracelist.append(nowpos)
            if nowpos[1] - 1 >= 0:
                num = self.routemap[nowpos[1] - 1][nowpos[0]]
                if num != -1:
                    minnum = num
                minpos = (nowpos[0], nowpos[1] - 1)
            if nowpos[1] + 1 < self.mapsize_y:
                num = self.routemap[nowpos[1] + 1][nowpos[0]]
                if num != -1:
                    if minnum == 0:
                        minnum = num
                    elif minnum > num:
                        minnum = num
                        minpos = (nowpos[0], nowpos[1] + 1)
            if nowpos[0] - 1 >= 0:
                num = self.routemap[nowpos[1]][nowpos[0] - 1]
                if num != -1:
                    if minnum == 0:
                        minnum = num
                    elif minnum > num:
                        minnum = num
                        minpos = (nowpos[0] - 1, nowpos[1])
            if nowpos[0] + 1 < self.mapsize_x:
                num = self.routemap[nowpos[1]][nowpos[0] + 1]
                if num != -1:
                    if minnum == 0:
                        minnum = num
                        minpos = (nowpos[0] + 1, nowpos[1])
                    elif minnum > num:
                        minnum = num
                        minpos = (nowpos[0] + 1, nowpos[1])
            nowpos = minpos

class AstarAgent(UniformCostAgent):
    def calccost(self, routecost, nextpos):
        r = routecost + self.costmap[nextpos[1]][nextpos[0]] + self.Heuristicfunc(nextpos)
        print(r)
        return r

    def Heuristicfunc(self, pos):
        return math.fabs(self.destpos[0] - pos[0]) + math.fabs(self.destpos[1] - pos[1])
