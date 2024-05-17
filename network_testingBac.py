
import random
from libs.network import Network

graphe = {
'A': {'B': 4, 'E': 4},
'B': {'A': 4, 'F': 7, 'G': 5},
'C': {'E': 8, 'D': 4},
'D': {'C': 4, 'E': 6, 'F': 8},
'E': {'A': 4, 'C': 8, 'D': 6},
'F': {'B': 7, 'D': 8, 'G': 3},
'G': {'B': 5, 'F': 3},
}
graphe = {
'A': {'E': 1, 'D': 1},
'B': {'C': 1},
'C': {'G': 1},
'D': {'E': 1},
'E': {'B': 1, 'G': 1, 'F': 1},
'F': {'G': 1},
'G': {},
}

a = Network(graphe)
a.undirected()


w = a.get_window()
w.set_layout(1)
w.bake()
a.show()

