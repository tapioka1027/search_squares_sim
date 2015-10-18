import random, queue

from enum import Enum

class SearchList(Enum):
    random = 0
    UDLR = 1 #up down left right
    LRUD = 2
    RLDU = 3

class UniformCostAgent():
    def __init__(self, mode=SearchList.random):
        qu = Queue()
