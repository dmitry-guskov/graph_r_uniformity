import numpy as np
import networkx as nx
from itertools import combinations


def _adjacency(adj_mat):
    """Validate a simple undirected graph, without modifying the caller's data."""
    a = np.asarray(adj_mat)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("Adjacency matrix must be square.")
    if not np.isin(a, [0, 1]).all() or np.any(np.diag(a)) or not np.array_equal(a, a.T):
        raise ValueError("Expected a symmetric binary adjacency matrix with zero diagonal.")
    return a.astype(np.uint8, copy=True)


def binary_rank(matrix):
    """Matrix rank over GF(2), not floating-point or real-valued rank."""
    a = np.asarray(matrix)
    if a.ndim != 2 or not np.isin(a, [0, 1]).all():
        raise ValueError("Expected a binary matrix.")
    a = a.astype(np.uint8, copy=True)
    rank = 0
    for col in range(a.shape[1]):
        pivots = np.flatnonzero(a[rank:, col])
        if not len(pivots):
            continue
        pivot = rank + pivots[0]
        a[[rank, pivot]] = a[[pivot, rank]]
        for row in range(rank + 1, len(a)):
            if a[row, col]:
                a[row] ^= a[rank]
        rank += 1
        if rank == len(a):
            break
    return rank


def cut_rank(adj_mat, retained):
    """Log2 Schmidt rank of the graph state across retained and its complement."""
    a = _adjacency(adj_mat)
    retained = list(retained)
    if (any(not isinstance(i, (int, np.integer)) or not 0 <= i < len(a) for i in retained)
            or len(set(retained)) != len(retained)):
        raise ValueError("Retained vertices must be distinct valid integer indices.")
    complement = [i for i in range(len(a)) if i not in retained]
    return binary_rank(a[np.ix_(retained, complement)])


def is_maximally_mixed(adj_mat, retained):
    """Exact graph-state marginal test; unlike peeling, failure is conclusive."""
    retained = list(retained)
    return cut_rank(adj_mat, retained) == len(retained)


def uniformity_certificate(adj_mat, k):
    """Check every k-subset; return a failing cut and rank when one exists.

    Complexity is combinatorial in k. A failed randomized search over graphs is
    never a certificate that k-uniform graph states do not exist.
    """
    a = _adjacency(adj_mat)
    if not isinstance(k, (int, np.integer)) or not 0 <= k <= len(a):
        raise ValueError("k must be an integer between zero and the graph order.")
    for retained in combinations(range(len(a)), k):
        rank = cut_rank(a, retained)
        if rank != k:
            return {"is_uniform": False, "k": int(k), "retained": list(retained), "rank": rank}
    return {"is_uniform": True, "k": int(k), "retained": None, "rank": None}


def is_k_uniform(adj_mat, k):
    """Whether every k-qubit marginal of this graph state is maximally mixed."""
    return uniformity_certificate(adj_mat, k)["is_uniform"]

class Node:
    def __init__(self,node_type=0, neighbours = [],name=''):
        '''
        type: int; 0 = qubit, 1 = traced, 2 = open wire
        neighbours: list[*Node]
        '''
        self.name = str(name)
        self.node_type = node_type
        if len(neighbours)==0:
            self.neighbours = [] 
        else:
            self.neighbours = neighbours
    def __str__(self):
        """prints name, node_type, lists neighbours

        Returns:
            str: self.name,self.node_type, [neighbours]
        """        
        s = f"{self.name}({self.node_type}), neighbours:"
        for i in self.neighbours:
            s+= i.name + ", "
        return s
    
    def connect(self, *another_nodes):
        """connects node to nodes in argument of the function
        """        
        for n in another_nodes:
            if n != self and n not in self.neighbours:
                self.neighbours.append(n)
                n.neighbours.append(self)
    def disconnect(self, *another_nodes):
        """disconnects node and nodes in argument of the function
        """        
        for n in another_nodes:
            if n != self and n in self.neighbours:
                self.neighbours.remove(n)
                n.neighbours.remove(self)

    def change_type(self, new_type):
        self.node_type = new_type


class Graph:
    def __init__(self, nodes=[], rules=[],name=""):
        """class of Graph, stores information about list of nodes in the Graph, list of rules that can be applied
            , and as additional stores information about starred nodes and if the Graph has been changed during the last simplification step

        Args:
            nodes (list, optional): list of Nodes of type Node. Defaults to [].
            rules (list, optional): list of rules (no special class). Defaults to [].
            name (str, optional): name for Graph. Defaults to "".
        """        
        self.name = name
        if len(nodes)!=0:
            self.nodes = nodes
        else:
            self.nodes = []
        if len(rules)!=0:
            self.rules = rules
        else:
            self.rules = []
        self.wires = []
        starred = []
        for i in range(len(self.nodes)):
            if self.nodes[i].node_type==1:
                starred.append(self.nodes[i])
        self.starred = starred
        self.changed  = True
        self.can_simplify = False
        
    def add_wires(self, *wires):
        """adds wires, i.e. open indices that are nodes
        """        
        for w in wires:
            self.wires.append(w)

    def __str__(self):
        """prints {self.name}: nodes({len(self.nodes)}, starred({len(self.starred)}); was changed? {self.changed}; Simplified? {len(self.nodes)==len(self.starred)}

        Returns:
            str: _description_
        """        
        return f"{self.name}: nodes({len(self.nodes)}, starred({len(self.starred)}); was changed? {self.changed}; Simplified? {len(self.nodes)==len(self.starred)}"
    
    def simplify_step(self):
        """ Iterate over starred nodes and tries to implement a rule

        Returns:
            bool: returns False if there were no changes
        """        
        any_change = False
        for n in list(self.starred):
            for r in self.rules:
                if r(n,self):
                    any_change = True
        if any_change:
            self.changed = True
        else:
            self.changed = False
        return self.changed
    
    def simplify(self):
        """Apply the graphical peeling rules until no rule applies.

        This is an incomplete certificate, not an exact uniformity test.
        Use is_maximally_mixed or is_k_uniform on the original adjacency matrix.

        Returns:
            bool: returns True if Graph is simplified, i.e. all nodes are starred.
        """        
        while self.changed:
            self.simplify_step()
            # print(self)
        if len(self.starred) == len(self.nodes):
            self.can_simplify = True
            # print("Simplified!")
    
        else:
            self.can_simplify = False
            # print("Cannot be simplified!")
        return self.can_simplify
        
    def set_rules(self, *rules):
        """adds rules to the Graph
        """        
        for r in rules:
            self.rules.append(r)
    def print_nodes(self,):
        """Prints all nodes of the graph
        """        
        for i in self.nodes:
            print(i)
    def plot_graph(self,):
        """Makes a plot of the Graph with the nx-library 

        Returns:
            nx.Graph: instance of nx library graph 
        """        
        G = nx.Graph()
        for i in range(len(self.nodes)):
            G.add_node(self.nodes[i].name)

        for i in range(len(self.nodes)):
            for j in range(i+1,len(self.nodes)):
                if self.nodes[i] in self.nodes[j].neighbours:
                    G.add_edge(self.nodes[i].name,self.nodes[j].name)


        color_map = []
        for node in self.nodes:
            if node.node_type == 0:
                color_map.append('pink')
            elif node.node_type == 1: 
                color_map.append('blue') 
                
        if len(self.wires) != 0:
            for w in self.wires:
                G.add_node(w.name)
                G.add_edge(w.name, w.neighbours[0].name)
                color_map.append('gray')


        nx.draw(G, node_color=color_map,with_labels=True, font_weight='bold')
        return G


def generate_graph( N, adj_mat):
    """Makes a graph according to the adjacency matrix 

    Args:
        N (int): Number of nodes
        adj_mat (_type_): 2d array

    Returns:
        Graph: returns instance of the Graph
    """    
    adj_mat = _adjacency(adj_mat)
    if N != len(adj_mat):
        raise ValueError("N must match the adjacency matrix size.")
    nodes = []
    for i in range(N):
        nodes.append(Node(1,name=i))
    for i in range(N):
        for j in range(i+1,N):
            # print( adj_mat[i][j],end=' ')
            if adj_mat[i][j]==1:
                nodes[i].connect(nodes[j])
        # print()
    G = Graph(nodes)
    return G
    
def genereate_given_state(G,qubits):
    """ Makes a coloring of the Graph. qubits array corresponds to the regular (non-starred) nodes

    Args:
        G (Graph): A graph on which the coloring casts
        qubits (list): Marks which nodes should stay as non-starred
    """    
    counter = 0
    for i in qubits:
        if G.nodes[i].node_type != 0:
            G.nodes[i].change_type(0)
            wire = Node(2,name='wire{}'.format(counter))
            G.nodes[i].connect(wire)
            G.starred.remove(G.nodes[i])
            G.add_wires(wire)   
            counter+=1
    

def generate_random_state(G,r):
    """Generates random state with r non-starred nodes

    Args:
        G (Graph): A graph instance
        r (int): number of non-colored nodes

    Returns:
        list: list of chosen nodes 
    """    
    qubits = np.random.choice(len(G.nodes),r,replace=False)
    
    counter = 0
    for i in qubits:
        if G.nodes[i].node_type != 0:
            G.nodes[i].change_type(0)
            wire = Node(2,name='wire{}'.format(counter))
            G.nodes[i].connect(wire)
            G.starred.remove(G.nodes[i])
            G.add_wires(wire)  
            counter+=1
    return qubits

def spread(node, G):
    """One of the basic rules that correspondes to the situation where one starred node has only one connection to a non-starred node.

    Args:
        node (Node): node that the rule applied to 
        G (Graph): Graph

    Returns:
        bool: returns True if the rule was applied 
    """    
    if node.node_type == 1 and len(node.neighbours)==1 and node.neighbours[0].node_type == 0:
        node.neighbours[0].change_type(1)
        G.starred.append(node.neighbours[0])
        
        node.neighbours[0].disconnect(node)
        G.starred.remove(node)
        G.nodes.remove(node)
        return True
    else:
        return False
        
def disconnect(node, G):
    """One of the basic rules that correspondes to the situation where two starred nodes has connection between them.

    Args:
        node (Node): node that the rule applied to 
        G (Graph): Graph

    Returns:
        bool: returns True if the rule was applied 
    """      
    buf = False
    if node.node_type == 1:
        for n in list(node.neighbours):
            if n.node_type == 1:
                node.disconnect(n)
                buf = True
    return buf

def adjacency_matrix_binomial(N,prob=0.5, seed=None):
    """Makes a random adjacency matrix according to np.random.binomial function

    Args:
        N (int): number of nodes
        prob (float, optional): _description_. Defaults to 0.5.

    Returns:
        _type_: _description_
    """    
    if not isinstance(N, (int, np.integer)) or N < 0 or not 0 <= prob <= 1:
        raise ValueError("N must be nonnegative and prob must be in [0, 1].")
    rng = np.random if seed is None else np.random.default_rng(seed)
    upper = np.triu(rng.binomial(1, prob, size=(N, N)), 1)
    return upper + upper.T

def adjacency_matrix_regular(N,d=3, seed=None):
    """Makes adjacency matrix for a regular graph 

    Args:
        N (int): Number of nodes
        d (int, optional): Nodes' degrees. Defaults to 3.

    Returns:
        ndarray: returns 2d array
    """    
    G = nx.random_regular_graph(d,N, seed=seed)
    return nx.to_numpy_array(G)
