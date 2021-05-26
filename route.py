import math
import pandas as pd
import numpy as np
from lieu import Lieu

class Route:
    def __init__(self, liste_lieux, order):
        self.liste_lieux = liste_lieux
        self.order = order

    def calcul_distance_route(self):
        distance_total = 0
        for i in range(len(self.order)):
            if i == len(self.order)-1:
                distance_total += Lieu.calcul_distance(self.liste_lieux[self.order[i]].coords, self.liste_lieux[self.order[0]].coords)
            else:
                distance_total += Lieu.calcul_distance(self.liste_lieux[self.order[i]].coords, self.liste_lieux[self.order[i+1]].coords)

        return distance_total



