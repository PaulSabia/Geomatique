import numpy as np
import random
from route import Route



class Fourmi:
    def __init__(self, liste_lieux, graph, nbr_fourmis=3):
        self.liste_lieux = liste_lieux
        self.graph = graph
        self.pheromone_matrix = self.create_pheromone_matrix()
        self.alpha = 2
        self.beta = 3
        self.rho = 0.7
        self.nbr_fourmis = nbr_fourmis
        self.NB_ITER = 200


    def create_pheromone_matrix(self):
        pheromone_matrix = np.ones((self.graph.NB_LIEUX, self.graph.NB_LIEUX))
        return pheromone_matrix

    
    def update_pheromone(self, order:list):
        pheromones_width = []
        distance = Route(self.liste_lieux, order).calcul_distance_route()
        for i, id in enumerate(order):
            if i != len(self.liste_lieux):
                self.pheromone_matrix[id][order[i+1]] += ((1 - self.rho) * self.alpha) + (1/distance)
                pheromones_width.append(self.pheromone_matrix[id][order[i+1]])
        return distance, pheromones_width
        

    def heuristique(self, index_depart):
        point_depart = self.liste_lieux[index_depart]
        order = [point_depart.id]
        for i in range(len(self.liste_lieux)):
            if i != len(self.liste_lieux)-1:
                next_point_index = self.graph.plus_proche_voisin(order[i], order)[0]
                next_point = self.liste_lieux[next_point_index].id
                order.append(next_point)
        order.append(point_depart.id)
        distance, _ = self.update_pheromone(order)
        return order, distance


    def path_choice(self, id_point, visited_list):
        unvisited_list = [elem for elem in self.liste_lieux if elem.id not in visited_list]
        pheromone_raw = self.pheromone_matrix[id_point]
        distance_raw = self.graph.matrice_od[id_point]
        dic = {}

        for city in unvisited_list:
            if city.id != id_point:
                denominator = 0
                numerator = (pow(pheromone_raw[city.id], self.alpha) * pow((1/distance_raw[city.id]), self.beta))
                for city_2 in unvisited_list:
                    if city_2.id == id_point:
                        pass
                    denominator += (pow(pheromone_raw[city_2.id], self.alpha) * pow((1/distance_raw[city_2.id]), self.beta))
                proba = numerator / float(denominator)
                dic[city.id] = proba

        next_point = random.choices(list(dic.keys()), weights = list(dic.values()), k=1)[0]
        return next_point


    def start_fourmis(self, point):
        for _ in range(self.nbr_fourmis):
            order = [point.id] 
            for y in range(len(self.liste_lieux)-1):
                path_choice = self.path_choice(order[y], order)
                order.append(path_choice)

            order.append(point.id)
            distance, pheromones_width = self.update_pheromone(order)
            yield order, distance, pheromones_width
 
