
from cyutils.networkVis import Window

class Network:
    def __init__(self, nodes = None, matrix = None):
        """Creates a new network with a given structure"""
        
        self.nodes = nodes
        self.matrix = matrix
        self.win = None

        if nodes == None:
            self.clear()
        elif isinstance(nodes, dict):
            if matrix == None:
                self.nodes_and_matrix_by_dict(nodes)
            else:
                self.nodes_by_dict_weight(nodes)
        elif isinstance(nodes, str):
            self.graph_quick_string(nodes)

        if matrix:
            if isinstance(self.matrix[0], list):
                # matrix is multi-line
                self.matrix_multi = True
            else:
                self.matrix_multi = False

    def from_quick_links(self, s, sep=';'):
        s = s.replace('\n','').replace(' ',sep)
        arr = s.split(sep)
        size = len(arr)//3
        names = []
        nodes = []
        matrix = [[0 for x in range(size)] for y in range(size)]

        # nodes
        for i in range(size):
            a = arr[i*3]
            b = arr[i*3+2]
            if not(a in names):
                names.append(a)
                nodes.append([a, 0])
            if not(b in names):
                names.append(b)
                nodes.append([b, 0])
        
        for i in range(size):
            a = arr[i*3]
            cost = int(arr[i*3+1])
            b = arr[i*3+2]

            ia = names.index(a)
            ib = names.index(b)
            matrix[ia][ib] = cost
            matrix[ib][ia] = cost

        self.nodes = nodes
        self.matrix = matrix

            
        

    def graph_quick_string(self, s, sep=';'):
        s = s.replace('\n','').replace(' ',sep)
        arr = s.split(sep)
        nodes = []
        names = []

        # nodes
        for elem in arr:
            a = elem[0]
            names.append(a)
            nodes.append([a, 0])
        size = len(nodes)
        matrix = [[0 for x in range(size)] for y in range(size)]

        # links
        for elem in arr:
            if len(elem)>1:
                a = elem[0]
                ia = names.index(a)
                for b in elem[1:]:
                    ib = names.index(b)
                    matrix[ia][ib] = 1
                    matrix[ib][ia] = 1
                    
        self.matrix = matrix
        self.nodes = nodes
                

    def undirected(self):
        """Transforms the given graph data to an undirected one"""
        size = self.size()
        for y in range(size):
            for x in range(y):
                v = self.matrix[x][y]
                if v!=0:
                    self.matrix[y][x] = v
                else:
                    self.matrix[x][y] = self.matrix[y][x]
        return self

    def clear(self):
        """Clear out all nodes and links"""
        self.nodes = []
        self.matrix = []
        
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
                self.node_links_by_dict(v, names, i)
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

    def get_links_dictionary(self):
        """Get a dictionary containing nodes names, weight and connetions.
        structure: {name: [{link_tar: link_weight}, weight]} --> eg: net = {'A': [{'B': 3}, 5]}"""
        
        di = {}
        size = len(self.nodes)
        names = self.node_names()
        for y in range(size):
            node, weight = self.nodes[y]
            
            # get links
            links = {}
            for x in range(size):
                w = self.matrix[y][x]
                if w != 0:
                    links[names[x]] = w

            # get free name
            name = node
            name_i = 0
            while name in di:
                name = str(node)+'_'+name_i
                name_i += 1
            di[name] = [links, weight]

        return di

        
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
        raise ValueError(f'The network node named "{name}" does not exist!')

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
        if li == None: # no funky default arg problems
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

    def path_exists(self, node_i, tar_i, li = None):
        """Does a path exist between two nodes of given index"""
        if li == None:
            li = []
        
        for b in self.neighbors(node_i):
            if b == tar_i:
                return True
            if not(b in li):
                found = self.path_exists(b, tar_i, li)
                if found:
                    return True
        return False

    def path_exists_by_name(self, start_name, tar_name):
        """Does a path exist between two nodes of given name"""
        a = self.node_index(start_name)
        b = self.node_index(tar_name)
        return self.path_exists(a,b)


    def remove_node(self, i: int):
        """Removes a node by index"""

        # supprimer sommet
        del self.nodes[i]
        # supprimer arrete ligne
        del self.matrix[i]
        # supprimer arrete colonne
        for line in self.matrix:
            del line[i]
        

    def remove_node_by_name(self, name):
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

    def edit_edge(self, a, b, weight = 0):
        """Edit the weight of the edge between 2 nodes"""
        self.matrix[a][b] = weight

    def edit_edge_by_name(self, a, b, weight = 0):
        """Edit the weight of the edge between 2 node names"""
        a = self.node_index(a)
        b = self.node_index(b)
        return self.edit_edge(a, b, weight)

    def remove_edge(self, a,b):
        """Removes an edge between 2 nodes"""
        self.matrix[a][b] = 0

    def remove_edge_by_name(self, a, b):
        """Removes an edge between 2 node names"""
        
        a = self.node_index(a)
        b = self.node_index(b)
        return self.remove_edge(a,b)
    """
    def path_cycle(self, node_i):
        found = []
        free = [node_i]
        size = self.size()
        while len(found) < size:
            cur = free.pop()
            for neigh in self.neighbors(cur):
                if not(neigh in found):
                    free.append(neigh)
            if cur in found:
                return True

            found.append(cur)
        return False
    """

    def path_cycle(self, node_i):
        found = []
        free = [node_i]
        size = self.size()
        while len(found) < size:
            cur = free.pop(0)
            
            for neigh in self.neighbors(cur):
                if neigh in found:
                    return True
                else:
                    free.append(neigh)
            
            found.append(cur)
        return False

    def path_width(self, node_i):
        search = [node_i]
        found = []
        size = self.size()
        while len(search) > 0:
            cur = search.pop(0)
            found.append(cur)

            for neigh in self.neighbors(cur):
                if not(neigh in found) and not(neigh in search):
                    search.append(neigh)
        return found
    
    def path_width_by_name(self, name):
        i = self.node_index(name)
        return self.path_width(i)
    
    def path_width_names_by_name(self, name):
        return [self.node_name(i) for i in self.path_width_by_name(name)]

    def dijkstra(self, node_i):
        cost = {node_i}
        

    """VISUAL"""
    

    def get_window(self):
        """Gets or creates a window object"""
        if not self.win:
            self.win = Window(self)
        return self.win

    def show(self, *args, **kwargs):
        """Show and gets a window object"""
        win = self.get_window()
        win.show(*args, **kwargs)
        return win

    def set_layout(self, *args, **kwargs):
        win = self.get_window()
        win.set_layout(*args, **kwargs)
        return win

