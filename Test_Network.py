
import random
from cyutils.matrix import Matrix
from cyutils.network import Network

nodes_a = [['A', 9], ['B', 34], ['C',  18], ['E', 86], ['F', 20]]

nodes_b = {'A': 9, 'B': 34, 'C': 18, 'E': 86, 'F': 20}

matrix_a = [[0 , 8 , 3 , 0 , 0],
            [0 , 0 , 7 , 0 , 0], 
            [0 , 0 , 0 , 6 , 9],
            [0 , 0 , 0 , 0 , 0],
            [5 , 0 , 0 , 0 , 0]]

matrix_b = Matrix(0 , 8 , 3 , 0 , 0,
                  0 , 0 , 7 , 0 , 0,
                  0 , 0 , 0 , 6 , 9,
                  0 , 0 , 0 , 0 , 0,
                  5 , 0 , 0 , 0 , 0)[5]

def testing():
    net = Network(nodes_a, matrix_a)
    
    print(net.size())
    print(net.is_neighbor(1,2))
    print(net.is_neighbor_by_name('B','C'))
    print(net.neighbors_int(1))
    print(net.neighbors_int_by_name('B'))
    print(net.neighbors(1))
    print(net.neighbors_by_name('B'))
    print(net.neighbors_names_by_name('B'))
    print(net.nodes_edges(1))
    print(net.nodes_edges_by_name('B'))
    print(net.nodes_edges_name_by_name('B'))
    print(net.node_names())
    print(net.edges())
    print(net.edges_names())
    print(net.path_depth(1))
    print(net.path_depth_by_name('B'))
    print(net.get_links_dictionary())

    print('Cycle:', net.path_cycle(0))

    win = net.get_window()
    win.set_layout('tension')
    win.bake()
    win.show()

    print(net.remove_node(3))
    win.show(time=.1)
    print(net.remove_node_by_name('C'))
    win.show(time=.1)
    print(i:=net.add_node('Z', 16))
    win.show(time=.1)
    print(net.edit_edge(i, 0, 8))
    win.show(time=.1)
    print(net.edit_edge_by_name('Z', 'B', 9))
    win.show(time=.1)
    print(net.remove_edge(0,1))
    win.show(time=.1)
    print(net.remove_edge_by_name('Z','A'))
    win.show()

def random_network():
    net = Network()
    names = 'azertyuiop'
    for name in names:
        net.add_node(name, random.randint(1, 100))
    
    for i in range(len(names)):
        for _ in range(random.randint(1,2)):
            b = random.randint(0, len(names)-1)
            net.edit_edge(i, b, random.randint(1,9))

    win = net.set_layout('tension')
    win.bake()
    win.show()

if __name__ == '__main__':
    testing()

    while True:
        random_network()
