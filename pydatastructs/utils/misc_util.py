__all__ = [
    'TreeNode',
    'MAryTreeNode',
    'LinkedListNode',
    'BinomialTreeNode',
    'AdjacencyListGraphNode',
    'AdjacencyMatrixGraphNode',
    'GraphEdge',
    'Set'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class Node(object):
    """
    Abstract class representing a node.
    """
    pass

class TreeNode(Node):
    """
    Represents node in trees.

    Parameters
    ==========

    data
        Any valid data to be stored in the node.
    key
        Required for comparison operations.
    left: int
        Optional, index of the left child node.
    right: int
        Optional, index of the right child node.
    """

    __slots__ = ['key', 'data', 'left', 'right', 'is_root',
                 'height', 'parent', 'size']

    def __new__(cls, key, data=None):
        obj = Node.__new__(cls)
        obj.data, obj.key = data, key
        obj.left, obj.right, obj.parent, obj.height, obj.size = \
            None, None, None, 0, 1
        obj.is_root = False
        return obj

    def __str__(self):
        """
        Used for printing.
        """
        return str((self.left, self.key, self.data, self.right))

class BinomialTreeNode(TreeNode):
    """
    Represents node in binomial trees.

    Parameters
    ==========

    data
        Any valid data to be stored in the node.
    key
        Required for comparison operations.

    Note
    ====

    The following are the data members of the class:

    parent: BinomialTreeNode
        A reference to the BinomialTreeNode object
        which is a prent of this.
    children: DynamicOneDimensionalArray
        An array of references to BinomialTreeNode objects
        which are children this node.
    is_root: bool, by default, False
        If the current node is a root of the tree then
        set it to True otherwise False.
    """
    __slots__ = ['parent', 'key', 'children', 'data', 'is_root']

    def __new__(cls, key, data=None):
        from pydatastructs.linear_data_structures.arrays import DynamicOneDimensionalArray
        obj = Node.__new__(cls)
        obj.data, obj.key = data, key
        obj.children, obj.parent, obj.is_root = (
        DynamicOneDimensionalArray(BinomialTreeNode, 0),
        None,
        False
        )
        return obj

    def add_children(self, *children):
        """
        Adds children of current node.
        """
        for child in children:
            self.children.append(child)
            child.parent = self

    def __str__(self):
        """
        For printing the key and data.
        """
        return str((self.key, self.data))

class MAryTreeNode(TreeNode):
    """
    Represents node in an M-ary trees.

    Parameters
    ==========

    data
        Any valid data to be stored in the node.
    key
        Required for comparison operations.

    Note
    ====

    The following are the data members of the class:

    children: DynamicOneDimensionalArray
        An array of indices which stores the children of
        this node in the M-ary tree array
    is_root: bool, by default, False
        If the current node is a root of the tree then
        set it to True otherwise False.
    """
    __slots__ = ['key', 'children', 'data', 'is_root']

    def __new__(cls, key, data=None):
        from pydatastructs.linear_data_structures.arrays import DynamicOneDimensionalArray
        obj = Node.__new__(cls)
        obj.data = data
        obj.key = key
        obj.is_root = False
        obj.children = DynamicOneDimensionalArray(int, 0)
        return obj

    def add_children(self, *children):
        """
        Adds children of current node.
        """
        for child in children:
            self.children.append(child)


class LinkedListNode(Node):
    """
    Represents node in linked lists.

    Parameters
    ==========

    key
        Any valid identifier to uniquely
        identify the node in the linked list.
    data
        Any valid data to be stored in the node.
    links
        List of names of attributes which should be used as links to other nodes.
    addrs
        List of address of nodes to be assigned to each of the attributes in links.
    """
    def __new__(cls, key, data=None, links=['next'], addrs=[None]):
        obj = Node.__new__(cls)
        obj.key = key
        obj.data = data
        for link, addr in zip(links, addrs):
            obj.__setattr__(link, addr)
        obj.__slots__ = ['key', 'data'] + links
        return obj

    def __str__(self):
        return str(self.key)

class GraphNode(Node):
    """
    Abastract class for graph nodes/vertices.
    """
    def __str__(self):
        return str((self.name, self.data))

class AdjacencyListGraphNode(GraphNode):
    """
    Represents nodes for adjacency list implementation
    of graphs.

    Parameters
    ==========

    name: str
        The name of the node by which it is identified
        in the graph. Must be unique.
    data
        The data to be stored at each graph node.
    adjacency_list: iterator
        Any valid iterator to initialize the adjacent
        nodes of the current node.
        Optional, by default, None
    """
    def __new__(cls, name, data=None, adjacency_list=None):
        obj = GraphNode.__new__(cls)
        obj.name, obj.data = str(name), data
        obj._impl = 'adjacency_list'
        if adjacency_list is not None:
            for node in adjacency_list:
                obj.__setattr__(node.name, node)
        obj.adjacent = set(adjacency_list) if adjacency_list is not None \
                       else set()
        return obj

    def add_adjacent_node(self, name, data):
        """
        Adds adjacent node to the current node's
        adjacency list with given name and data.
        """
        if hasattr(self, name):
            getattr(self, name).data = data
        else:
            new_node = AdjacencyListGraphNode(name, data)
            self.__setattr__(new_node.name, new_node)
            self.adjacent.add(new_node.name)

    def remove_adjacent_node(self, name):
        """
        Removes node with given name from
        adjacency list.
        """
        if not hasattr(self, name):
            raise ValueError("%s is not adjacent to %s"%(name, self.name))
        self.adjacent.remove(name)
        delattr(self, name)

class AdjacencyMatrixGraphNode(GraphNode):
    """
    Represents nodes for adjacency matrix implementation
    of graphs.

    Parameters
    ==========

    name: int
        The index of the node in the AdjacencyMatrix.
    data
        The data to be stored at each graph node.
    """
    __slots__ = ['name', 'data']

    def __new__(cls, name, data=None):
        obj = GraphNode.__new__(cls)
        obj.name, obj.data, obj.is_connected = \
            int(name), data, None
        obj._impl = 'adjacency_matrix'
        return obj

class GraphEdge(object):
    """
    Represents the concept of edges in graphs.

    Parameters
    ==========

    node1: GraphNode or it's child classes
        The source node of the edge.
    node2: GraphNode or it's child classes
        The target node of the edge.
    """
    def __new__(cls, node1, node2, value=None):
        obj = object.__new__(cls)
        obj.source, obj.target = node1, node2
        obj.value = value
        return obj

    def __str__(self):
        return str((self.source.name, self.target.name))

class Set(object):
    """
    Represents a set in a forest of disjoint sets.

    Parameters
    ==========

    key: Hashable python object
        The key which uniquely identifies
        the set.
    data: Python object
        The data to be stored in the set.
    """

    __slots__ = ['parent', 'size', 'key', 'data']

    def __new__(cls, key, data=None):
        obj = object.__new__(cls)
        obj.key = key
        obj.data = data
        obj.parent, obj.size = [None]*2
        return obj
