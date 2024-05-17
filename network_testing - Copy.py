
import random
from libs.network import Network

graphe = {
'D': [{'O': 1, 'R': 1, 'C': 2, 'J': 1}, 0],
'C': [{'R': 1, 'L': 1, 'D': 2, 'J': 2}, 0],
'J': [{'C': 2, 'L': 2, 'D': 1}, 0],
'L': [{'O': 3, 'C': 1, 'J': 2}, 0],
'O': [{'D': 1, 'L': 3}, 0],
'R': [{'D': 1, 'C': 1}, 0],
}

a = Network(graphe)

print('Ordre',a.size())
print('D et O voisins')
print('Degre D',a.neighbors_int_by_name('D'))
print('Degre D',a.neighbors_by_name('D'))
print('Adjacence',a.matrix)

# C - R - D - O
# D - J - L





a.set_layout('tension')
a.show()

