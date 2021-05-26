import random
import numpy as np
import tkinter as tk
from graph import Graph
from ACO import Fourmi


class Affichage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Groupe 4')
        self.LARGEUR, self.HAUTEUR = 800, 600
        self.geometry(f'{self.LARGEUR+20}x{self.HAUTEUR+40}')
        self.graph = Graph(100, self.LARGEUR, self.HAUTEUR, generate=True, save=False)
        # self.graph = Graph(50, self.LARGEUR, self.HAUTEUR, path_file='graph_10.csv')


    def draw_canvas(self, largeur, hauteur):
        self.canvas = tk.Canvas(self, bg="white", height=hauteur ,width=largeur)
        self.canvas.pack()


    def draw_evolution(self):
        self.evolution_text = tk.StringVar()
        self.evolution_text.set(f"")
        label = tk.Label(self, textvariable=self.evolution_text)
        label.pack()


    def draw_circle(self, lieu, id_order=None, init=False):
        r = 7
        x0 = lieu.x - r
        y0 = lieu.y - r
        x1 = lieu.x + r
        y1 = lieu.y + r

        if not init:
            if id_order == 0:
                self.canvas.create_oval(x0, y0, x1, y1, fill='red')
            else:
                self.canvas.create_oval(x0, y0, x1, y1, fill='#E8E5E4')
            self.canvas.create_text(lieu.x, lieu.y, text=f'{lieu.id}')
            self.canvas.create_text(lieu.x, lieu.y-20, text=f'{id_order}')
        else:
            self.canvas.create_oval(x0, y0, x1, y1, fill='#E8E5E4')
            self.canvas.create_text(lieu.x, lieu.y, text=f'{lieu.id}')
        self.update()


    def draw_lieux(self, liste_lieux, order=None, init=False):
        for lieu in liste_lieux:
            if not init:
                id_order = np.where(order == np.asarray(lieu.id))[0][0]
                self.draw_circle(lieu, id_order)
            else:
                self.draw_circle(lieu, init=True)
        self.update()


    def draw_line(self, lieu_1, lieu_2, fourmis=None, width=None):
        if fourmis:
            self.canvas.create_line(lieu_1.x, lieu_1.y, lieu_2.x, lieu_2.y, fill='#A9FF50', width=width, tags='fourmis')
        else:
            self.canvas.create_line(lieu_1.x, lieu_1.y, lieu_2.x, lieu_2.y, fill='blue', width=3) #dash=(5, 5),
        self.update()


    def draw_routes(self, liste_lieux, order, fourmis=False, pheromones_width_list:list=None, indice_algorithme:int=None):
        for i in range(len(order)):
            if i == len(order)-1:
                self.draw_line(liste_lieux[order[i]], liste_lieux[order[0]], fourmis)
            else:
                if fourmis:
                    # width = round(pheromones_width_list[i])
                    width = round((pheromones_width_list[i]-(0.3*indice_algorithme)), 0)
                    if width <= 0: 
                        width = 1
                    elif width >= 17: 
                        width = 17
                    # print(width)
                    self.draw_line(liste_lieux[order[i]], liste_lieux[order[i+1]], fourmis, width)
                else:
                    self.draw_line(liste_lieux[order[i]], liste_lieux[order[i+1]], fourmis)
            

    def process(self):
        self.canvas.delete('all')
        liste_lieux = self.graph.get_liste_lieux()

        #Classe Fourmi pour générer un ordre de visite heuristique sur le plus proche voisin
        ACO = Fourmi(liste_lieux, self.graph)
        order_heuristique, distance_heuristique = ACO.heuristique(0)

        #Classe route pour calculer la distance total d'un parcours
        print('Distance Initiale de la route heuristique: ', distance_heuristique)
        self.evolution_text.set(f"Meilleur itinéraire : {0}/{ACO.NB_ITER} itérations -- Distance : {distance_heuristique}")

        #Dessine la route heuristique et les lieux
        self.draw_routes(liste_lieux, order_heuristique)
        self.draw_lieux(liste_lieux, order_heuristique)

        #Boucle qui parcour chaque point du parcour et initialise des fourmis afin de chercher un parcours plus rapide
        self.best_distance = distance_heuristique
        self.best_order = order_heuristique
        for i in range(ACO.NB_ITER):
            self.canvas.delete('fourmis')
            # print(i)
            id_point = random.randint(0, self.graph.NB_LIEUX-1)
            point = liste_lieux[id_point]

            for order, distance, pheromones_width in ACO.start_fourmis(point):
                print(order, distance)
                # print(pheromones_width)
                self.draw_routes(liste_lieux, order, fourmis=True, pheromones_width_list=pheromones_width, indice_algorithme=i)
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_order = order
                    self.canvas.delete('all')
                    self.draw_routes(liste_lieux, order)
                    self.draw_lieux(liste_lieux, order)
                    print(f'Amelioration de l\'itinéraire : {self.best_distance}')
                    self.evolution_text.set(f"Meilleurs itinéraire : {i}/{ACO.NB_ITER} itérations -- Distance : {self.best_distance}") #Affichage du meilleurs parcours

        self.end(liste_lieux, self.best_distance, self.best_order)

    def end(self, liste_lieux, best_distance, best_order):
        self.draw_routes(liste_lieux, best_order)
        self.draw_lieux(liste_lieux, best_order)
        print(f'Meilleurs distance sur l\'itinéraire: {best_distance}')

    def end_press(self):
        self.destroy()
        print('--------- END ---------')
        print(self.best_distance)
        print(self.best_order)
        
    def play(self):
        self.draw_canvas(self.LARGEUR, self.HAUTEUR)
        self.draw_lieux(self.graph.get_liste_lieux(), init=True)
        self.draw_evolution()
        self.bind('<space>', lambda x: self.process())
        self.bind('<Escape>', lambda x: self.end_press())
        self.mainloop()
        

app = Affichage()
app.play()
