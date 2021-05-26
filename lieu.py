import numpy as np
import random
import time
import pandas as pd
import math


class Lieu:
    def __init__(self, name, x, y):
        self.id = name
        self.x = x
        self.y = y
        self.coords = [x, y]

    @classmethod
    def calcul_distance(self, point_1:list, point_2:list):
        x1, y1 = point_1[0], point_1[1]
        x2, y2 = point_2[0], point_2[1]
        sq1 = (x1-x2)*(x1-x2)
        sq2 = (y1-y2)*(y1-y2)
        return math.sqrt(sq1 + sq2)
