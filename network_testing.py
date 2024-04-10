
import random
from libs.network import Network

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

def modif():
    graphe = Network(sommets_dict, aretes_g1)
    
    win = graphe.get_window()
    win.layout_tension_bake().show(time = 3)
    d = .2
    
    graphe.remove_node_by_name('F')
    win.show(time=d)
    graphe.add_node('D', 27)
    win.show(time=d)
    
    graphe.edit_edge_by_name('C','A', 5)
    win.show(time=d)
    graphe.edit_edge_by_name('E','A', 2)
    win.show(time=d)
    graphe.edit_edge_by_name('E','D', 1)
    win.show(time=d)
    graphe.edit_edge_by_name('D','B', 12)
    win.show(time=d)
    graphe.edit_edge_by_name('D','D', 4)
    win.show()
    



def testing():
    graphe = Network(G)
    win = graphe.get_window()
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
    print(graphe.get_links_dictionary())

    win.layout_tension_bake().show(time=3)

    print(graphe.remove_node(3))
    win.show(time=.1)
    print(graphe.remove_node_by_name('C'))
    win.show(time=.1)
    print(i:=graphe.add_node('Z', 16))
    win.show(time=.1)
    print(graphe.edit_edge(i, 0, 8))
    win.show(time=.1)
    print(graphe.edit_edge_by_name('Z', 'B', 9))
    win.show(time=.1)
    print(graphe.remove_edge(0,1))
    win.show(time=.1)
    print(graphe.remove_edge_by_name('B','E'))
    win.show()

def cloning():
    net = Network()
    names = 'azertyuiop'
    for name in names:
        net.add_node(name, random.randint(1, 100))
    
    for i in range(len(names)):
        for _ in range(random.randint(1,2)):
            b = random.randint(0, len(names)-1)
            net.edit_edge(i, b, random.randint(1,9))

    net.set_layout('tension')
    net.show()

if __name__ == '__main__':
    modif()
