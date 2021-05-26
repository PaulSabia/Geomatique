import numpy as np
import pandas as pd
from lieu import Lieu

class Graph:
    def __init__(self, nb_lieux, largeur, hauteur, path_file='graph.csv', generate=False, save=True):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        self.NB_LIEUX = nb_lieux
        self.save = save
        if generate:
            self.df_lieux = self.create_df(self.NB_LIEUX, path_file)
        else:
            self.df_lieux = self.load_df(path_file)
            self.NB_LIEUX = self.df_lieux.shape[0]
        self.matrice_od = self.calcul_matrice_cout_od(self.df_lieux)


    def load_df(self, path_file):
        df = pd.read_csv(path_file)
        return df

    def save_df(self, df, path_file):
        df.to_csv(path_file, index=False)

    def generate_graph(self, nb_lieux):
        liste_lieux = []
        np.random.seed(1)
        for _ in range(nb_lieux):
            x = np.random.randint(0, self.LARGEUR)
            y = np.random.randint(0, self.HAUTEUR)
            liste_lieux.append([x, y])       
        return liste_lieux

    def create_df(self, nb_lieux, path_file):
        liste_lieux = self.generate_graph(nb_lieux)
        liste_x, liste_y = [], []
        for lieux in liste_lieux:
            liste_x.append(lieux[0])
            liste_y.append(lieux[1])    
        data = {'x': liste_x, 'y': liste_y}
        df = pd.DataFrame(data)
        if self.save: self.save_df(df, path_file)
        return df

    def add_data_to_csv(self, name, x, y):
        new_row = {'x': x, 'y': y}
        self.df_lieux = self.df_lieux.append(new_row, ignore_index=True)
        return 'Elements insérés et enregistrés'


    def calcul_matrice_cout_od(self, df):
        self.liste_x, self.liste_y = df['x'].values, df['y'].values
        liste_lieux = [[x, y] for x, y in zip(self.liste_x, self.liste_y)]
        matrix = np.zeros((self.NB_LIEUX, self.NB_LIEUX), dtype='float64')
        for i, elem in enumerate(matrix):
            point_ref = liste_lieux[i]
            for y in range(len(elem)):
                point_distant = liste_lieux[y]
                matrix[i][y] = Lieu.calcul_distance(point_ref, point_distant)
        #df = pd.DataFrame(data, columns=[i for i in range(self.NB_LIEUX)], index=[i for i in range(self.NB_LIEUX)])
        return matrix

    def plus_proche_voisin(self, indice:int, indices_precedents:list):
        lieu = self.matrice_od[indice]
        distance_voisin = max(lieu)
        index_voisin = None
        for i, l in enumerate(lieu):
            if i in indices_precedents:
                pass
            elif len(indices_precedents) == len(lieu)-1 and i not in indices_precedents:
                distance_voisin = l
                index_voisin = i
            else:
                if l < distance_voisin and l != 0:
                    distance_voisin = l
                    index_voisin = i
        return index_voisin, distance_voisin


    def get_liste_lieux(self):
        liste_lieux = [Lieu(i, x, y) for i, (x, y) in enumerate(zip(self.liste_x, self.liste_y))]
        return liste_lieux


