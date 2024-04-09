
import networkx as nx
import matplotlib.pyplot as plt
import pylab as P

from networkVis import Window

sommets_g1 = [['A', 9], ['B', 34], ['C',  18], ['E', 86], ['F', 20]]

aretes_g1 =[[0 , 8 , 3 , 0 , 0],
            [0 , 0 , 7 , 0 , 0], 
            [0 , 0 , 0 , 6 , 9],
            [0 , 0 , 0 , 0 , 0],
            [5 , 0 , 0 , 0 , 0]]

class Graphe:
    def __init__(self, nodes, matrix):
        self.nodes = nodes
        self.matrix = matrix
        
    def size(self):
        return len(self.nodes)

    def index_node(self, name):
        for i,li in enumerate(self.nodes):
            if li[0] == name:
                return i

    def is_adjacent(self, a, b):
        ia = self.index_point(a)
        ib = self.index_point(b)
        return self.matrix[ia][ib] != 0

    def neighbors_int(self, node):
        r = 0
        for other in self.nodes:
            if self.is_adjacent(node, other):
                r += 1
        return r

    def neighbors(self, nom):
        y = self.index_point(nom)
        r = []
        if y != None:
            line = self.matrix[y]
            for x in range(len(self.nodes)):
                if line[x] != 0:
                    r.append(x)
        return r

    def neighbors_name(self, name):
        li = self.neighbors(name)
        names = self.node_names()
        return [names[i] for i in li]

    def nodes_edges(self, name):
        li = self.neighbors(name)
        r = [(name, self.nodes[i][0]) for i in li]
        return r

    def node_names(self):
        return [v[0] for v in self.nodes]

    def edges(self):
        """Pairs of nodes"""
        size = self.size()
        names = self.liste_noms()
        res = []
        for y in range(size):
            for x in range(size):
                if self.matrix[y][x] != 0:
                    res.append((names[y], names[x]))
        return res


    def remove_point(self, i):
        """Supprime un sommet par indice"""

        # supprimer sommet
        del self.nodes[i]
        # supprimer arrete ligne
        del self.matrix[i]
        # supprimer arrete colonne
        for line in self.matrix:
            del line[i]
        

    def remove_point_name(self, name):
        """Supprime un sommet par nom"""
        
        names = self.node_names()
        self.remove_point(names.index(name))

    def add_point(self, name, weight=0):
        """Ajoute un sommet d'un nom donné avec un poids"""
        
        size = self.size()
        self.nodes.append([name, weight])
        self.matrix.append([0 for i in range(size)])

        for line in self.matrix:
            line.append(0)
        return size

    def edit_edge(self, a, b, poids = 0):
        """Edit the weight of the edge between 2 nodes"""
        self.matrix[a][b] = poids

    def edit_edge_name(self, a, b, poids = 0):
        """Edit the weight of the edge between 2 node names"""

        a = self.index_node(a)
        b = self.index_node(b)
        return self.edit_edge(a, b, poids)

    def remove_edge(self, a,b):
        """Delete the edge between 2 nodes"""
        self.matrix[a][b] = 0

    def remove_edge_name(self, a, b):
        """Delete the edge between 2 node names"""
        
        a = self.index_node(a)
        b = self.index_node(b)
        return self.remove_edge(a,b)

    def parcours_profoundeur(self, sommet, li = []):
        li.append(sommet)
        for b in self.liste_voisins(sommet):
            pass
        
    def show(self):
        G = nx.DiGraph()
        sommets = self.nodes
        matrice = self.matrix
        n = len(sommets)
        for som in sommets:
            if len(som)>1:
                G.add_node(som[0],name=som[0],weight=som[1])
            else:
                G.add_node(som)
        la=[]

        for i in range(n):
            for j in range(n):
                if matrice[i][j]:
                    la.append([sommets[i],sommets[j],matrice[i][j]])

        for aa in la:
            G.add_edge(aa[0][0], aa[1][0],weight=aa[2])
            
        edge_lab = nx.get_edge_attributes(G,'weight')
        node_list= nx.get_node_attributes(G,'weight')
        node_lab = {nam:str(nam)+'\n'+str(wei) for nam,wei in node_list.items() }
        pos = nx.circular_layout(G)
        nx.draw(G, pos=pos,with_labels=False,node_size=1500,node_color='green')
        nx.draw_networkx_labels(G,pos,labels=node_lab, font_weight='bold')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab,label_pos=0.5)
        P.show()








if __name__ == '__main__':
    graphe = Graphe(sommets_g1, aretes_g1)
    win = Window(graphe)
    
    #win.show(graphe)
    #graphe.show()
    
    graphe.remove_point_name('F')
    #win.show(graphe,2)
    
    graphe.add_point('D', 27)
    #win.show(graphe,2)
    
    graphe.edit_edge_name('C','A', 5)
    graphe.edit_edge_name('E','A', 2)
    graphe.edit_edge_name('E','D', 1)
    #win.show(graphe,2)
    graphe.edit_edge_name('D','B', 12)
    graphe.edit_edge_name('D','D', 4)
    win.show(graphe)
    win.layout = 1
    win.show(graphe)
    graphe.show()
