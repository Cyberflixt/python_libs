
import networkx as nx
import matplotlib.pyplot as plt
import pylab as P

from networkVis import Window

sommets_g1 = [['A', 9], ['B', 34], ['C',  18], ['E', 86], ['F', 20]]

sommets_dict = {'A': 9, 'B': 34, 'C': 18, 'E': 86, 'F': 20}

aretes_g1 =[[0 , 8 , 3 , 0 , 0],
            [0 , 0 , 7 , 0 , 0], 
            [0 , 0 , 0 , 6 , 9],
            [0 , 0 , 0 , 0 , 0],
            [5 , 0 , 0 , 0 , 0]]

G = { 'A' : [ { 'B' : 3 , 'E' : 8 } , 13 ] ,

      'B' : [ { 'A' : 7 , 'C' : 5 , 'E' : 2 } , 28 ]  ,

      'C' : [ { 'D' : 3 } , 17 ] ,

      'D' : [ { 'D' : 1 } , 16 ] ,

      'E' : [ { 'B' : 6 } , 14 ] }

class Network:
    def __init__(self, nodes, matrix = None):
        """Creates a new network with a given structure"""
        
        self.nodes = nodes
        self.matrix = matrix

        if isinstance(nodes, dict):
            if matrix == None:
                self.nodes_and_matrix_by_dict(nodes)
            else:
                self.nodes_by_dict_weight(nodes)
                
    def nodes_by_dict_weight(self, d):
        """Nodes by structure {name:weight} --> eg: nodes = {'A': 5, 'B': 2}"""
        res = []
        
        for name in d:
            weight = d[name]
            res.append([name, weight])

        self.nodes = res
        return res

    def node_links_by_dict(self, di, names, node_i):
        """Matrix links by dict {name: weight} --> eg: links = {'B': 3}"""
        for name in di:
            weight = di[name]

            
            if not(name in names):
                raise ValueError(f'Tried linking node "{names[node_i]}" towards unexisting node "{name}" (current nodes: {names})')
            
            node_b = names.index(name)
            self.matrix[node_i][node_b] = weight
            
    
    def nodes_and_matrix_by_dict(self, di):
        """Nodes and matrix by structure {name: [{link_tar: link_weight}, weight]} --> eg: net = {'A': [{'B': 3}, 5]}"""
        
        res = []
        size = len(di)

        self.matrix = [[0 for x in range(size)] for y in range(size)]
        names = [name for name in di]

        for i in range(size):
            name = names[i]
            v = di[name]
            weight = 0
            if isinstance(v, dict):
                # only links, no weight
                self.node_links_by_dict(elem, names, i)
            else:
                # list
                for elem in v:
                    if isinstance(elem, dict):
                        self.node_links_by_dict(elem, names, i)
                    else:
                        weight = elem
            res.append([name, weight])
                
        self.nodes = res
        return res

        
    def size(self):
        """Size of the network"""
        return len(self.nodes)

    def node_name(self, node_i: int):
        """The name of the node of a given index"""
        return self.nodes[node_i][0]

    def node_index(self, name):
        """The index of the node of a given name"""
        for i,li in enumerate(self.nodes):
            if li[0] == name:
                return i

    def is_neighbor(self, ia: int, ib: int):
        """Can a node of given index go to another node of given index"""
        return self.matrix[ia][ib] != 0

    def is_neighbor_by_name(self, a, b):
        """Can a node of given name go to another node of given name"""
        ia = self.node_index(a)
        ib = self.node_index(b)
        return self.is_neighbor(ia, ib)

    def neighbors_int(self, node_i: int) -> int:
        """Number of neighbors of node of given index"""
        r = 0
        for b in range(self.size()):
            if self.is_neighbor(node_i, b):
                r += 1
        return r

    def neighbors_int_by_name(self, name) -> int:
        """Number of neighbors of node of given name"""
        i = self.node_index(name)
        return self.neighbors_int(i)

    def neighbors(self, node_i: int):
        """Neighbors indices list of a given node's index"""
        r = []
        line = self.matrix[node_i]
        for x in range(len(self.nodes)):
            if line[x] != 0: # weight is not 0
                r.append(x)
        return r

    def neighbors_by_name(self, name):
        """Neighbors indices list of a given node's name"""
        y = self.node_index(name)
        r = []
        line = self.matrix[y]
        for x in range(len(self.nodes)):
            if line[x] != 0:
                r.append(x)
        return r

    def neighbors_names_by_name(self, name):
        """Neighbors names list of a given node's name"""
        i = self.node_index(name)
        li = self.neighbors(i)
        return [self.node_name(i) for i in li]

    def nodes_edges(self, node_i: int):
        """List of pairs of a edges between a given node's index and its neighbors indices"""
        li = self.neighbors(node_i)
        r = [(node_i, i) for i in li]
        return r

    def nodes_edges_by_name(self, name):
        """List of pairs of a edges between a given node's name and its neighbors indices"""
        return self.nodes_edges(self.node_index(name))

    def nodes_edges_name_by_name(self, name):
        """List of pairs of a edges between a given node's index and its neighbors names"""
        li = self.neighbors_by_name(name)
        r = [(name, self.node_name(i)) for i in li]
        return r

    def node_names(self):
        """Returns a tuple of all node names"""
        return [v[0] for v in self.nodes]

    def edges(self):
        """Returns all edges as pairs of nodes indices"""
        size = self.size()
        names = self.node_names()
        res = []
        for y in range(size):
            for x in range(size):
                if self.matrix[y][x] != 0:
                    res.append((y,x))
        return res
    
    def edges_names(self):
        """Returns all edges as pairs of nodes names"""
        size = self.size()
        names = self.node_names()
        res = []
        for y in range(size):
            for x in range(size):
                if self.matrix[y][x] != 0:
                    res.append((names[y], names[x]))
        return res

    def path_depth(self, node_i, li = None):
        """Returns the indices of nodes in the depth path started from a given node's index"""
        if li == None:
            li = []
        
        li.append(node_i)
        for b in self.neighbors(node_i):
            if not(b in li):
                self.path_depth(b, li)
        return li

    def path_depth_by_name(self, name):
        """Returns the names of nodes in the depth path started from a given node's name"""
        i = self.node_index(name)
        li = self.path_depth(i)
        return [self.node_name(i) for i in li]


    def remove_node(self, i: int):
        """Removes a node by index"""

        # supprimer sommet
        del self.nodes[i]
        # supprimer arrete ligne
        del self.matrix[i]
        # supprimer arrete colonne
        for line in self.matrix:
            del line[i]
        

    def remove_node_name(self, name):
        """Removes a node by name"""
        return self.remove_node(self.node_index(name))

    def add_node(self, name, weight=0):
        """Adds a node with a given name and weight"""
        
        size = self.size()
        self.nodes.append([name, weight])
        self.matrix.append([0 for i in range(size)])

        for line in self.matrix:
            line.append(0)
        return size

    def edit_edge(self, a, b, poids = 0):
        """Edit the weight of the edge between 2 nodes"""
        self.matrix[a][b] = poids

    def edit_edge_by_name(self, a, b, poids = 0):
        """Edit the weight of the edge between 2 node names"""
        a = self.node_index(a)
        b = self.node_index(b)
        return self.edit_edge(a, b, poids)

    def remove_edge(self, a,b):
        """Removes an edge between 2 nodes"""
        self.matrix[a][b] = 0

    def remove_edge_by_name(self, a, b):
        """Removes an edge between 2 node names"""
        
        a = self.node_index(a)
        b = self.node_index(b)
        return self.remove_edge(a,b)
        
    def show(self):
        #old
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







def ex3():
    graphe = Network(sommets_dict, aretes_g1)
    win = Window(graphe)
    
    graphe.show()
    win.open(graphe)
    
    graphe.remove_node_name('F')
    
    graphe.add_node('D', 27)
    
    graphe.edit_edge_name('C','A', 5)
    graphe.edit_edge_name('E','A', 2)
    graphe.edit_edge_name('E','D', 1)
    
    graphe.edit_edge_name('D','B', 12)
    graphe.edit_edge_name('D','D', 4)
    
    win.layout_tension_bake()
    win.show()



def testing():
    graphe = Network(G)
    win = Window(graphe)
    win.set_layout('tension')
    
    print(graphe.size())
    print(graphe.is_neighbor(1,2))
    print(graphe.is_neighbor_by_name('B','C'))
    print(graphe.neighbors_int(1))
    print(graphe.neighbors_int_by_name('B'))
    print(graphe.neighbors(1))
    print(graphe.neighbors_by_name('B'))
    print(graphe.neighbors_names_by_name('B'))
    print(graphe.nodes_edges(1))
    print(graphe.nodes_edges_by_name('B'))
    print(graphe.nodes_edges_name_by_name('B'))
    print(graphe.node_names())
    print(graphe.edges())
    print(graphe.edges_names())
    print(graphe.path_depth(1))
    print(graphe.path_depth_by_name('B'))

    win.open(graphe)
    print(graphe.remove_node(3))
    print(graphe.remove_node_name('C'))
    print(i:=graphe.add_node('Z', 16))
    print(graphe.edit_edge(i, 0, 8))
    print(graphe.edit_edge_by_name('Z', 'B', 9))
    print(graphe.remove_edge(0,1))
    print(graphe.remove_edge_by_name('Z','A'))
    win.open(graphe)



if __name__ == '__main__':
    testing()


