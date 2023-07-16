import random
import networkx as nx
from typing import Dict, List, Tuple


def random_graph(n: int, e: int) -> nx.Graph:
    """
    Return a random graph with [n] nodes and [e] edges.
    """
    if e + 1 < n:
        raise ValueError("Need enough edges to connect all nodes")
    if e > n * (n - 1) / 2:
        raise ValueError("Too many edges for too few nodes")

    return nx.gnm_random_graph(n, e)


def non_isomorphic_graph(first: nx.Graph) -> nx.Graph:
    """
    Return a random graph that is not isomorphic to the [first] graph.

    The returned graph has the same number of nodes and edges.
    """
    n = len(first.nodes)
    e = len(first.edges)
    if e == n * (n - 1) / 2:
        raise ValueError("Graph is complete: There are only isomorphic graphs with the same number of nodes and edges")

    while True:
        second = nx.gnm_random_graph(n, e)
        if not nx.is_isomorphic(first, second):
            return second


def three_colorable_graph(n: int) -> Tuple[nx.Graph, Dict[int, int]]:
    """
    Return a random graph with at least [n] nodes that is three-colorable.
    Also return the coloring
    """
    graph = nx.cycle_graph(n)
    coloring = nx.coloring.greedy_color(graph, strategy="largest_first")
    coloring = {node: color % 3 for node, color in coloring.items()}

    return graph, coloring


def not_three_colorable_graph(n: int) -> Tuple[nx.Graph, Dict[int, int]]:
    """
    Return a random graph with at least [n] nodes that is not three-colorable.
    Also return a fake coloring.
    """
    n = max(4, n)

    graph = nx.circulant_graph(n, offsets=[1, 2, 3])
    coloring = nx.coloring.greedy_color(graph, strategy="largest_first")
    coloring = {node: color % 3 for node, color in coloring.items()}

    return graph, coloring


class Mapping:
    """
    Mapping of values: Values are mapped onto other values.
    """

    def __init__(self, inner: Dict):
        self.inner = inner

    def __repr__(self) -> str:
        return str(self.inner)

    def __iter__(self):
        for key, value in self.inner.items():
            yield key, value

    def __getitem__(self, index):
        return self.inner[index]

    def __len__(self):
        return len(self.inner)

    @classmethod
    def shuffle_graph(cls, graph: nx.Graph) -> "Mapping":
        """
        Create a mapping of node labels by random shuffling nodes.
        """
        original = list(graph.nodes())
        shuffled = original.copy()
        random.shuffle(shuffled)
        inner = {original[i]: shuffled[i] for i in range(len(original))}

        return Mapping(inner)

    @classmethod
    def shuffle_list(cls, lst: List) -> "Mapping":
        """
        Create a mapping by randomly shuffling list elements.

        The original list remains unchanged.
        """
        shuffled = lst.copy()
        random.shuffle(shuffled)
        inner = {lst[i]: shuffled[i] for i in range(len(lst))}

        return Mapping(inner)

    def apply_graph(self, graph: nx.Graph) -> nx.Graph:
        """
        Apply the mapping of node labels to a graph.

        The original graph remains unchanged and a new graph is crated.
        """
        return nx.relabel_nodes(graph, self.inner, copy=True)

    def apply_list(self, lst: List) -> List:
        """
        Apply the mapping to a list.

        The original list remains unchanged and a new list is created.
        """
        return [self.inner[x] for x in lst]

    def invert(self) -> "Mapping":
        """
        Inverts the mapping.

        If A is mapped to B in this mapping, then B is mapped to A in the inverse.
        """
        inner = {v: k for k, v in self.inner.items()}
        return Mapping(inner)

    def and_then(self, second: "Mapping") -> "Mapping":
        """
        Compose this mapping with a second mapping.

        If A is mapped to B in this mapping and B is mapped to C in the second mapping,
        then A is mapped to C in their composition.
        """
        inner = {k: second.inner[self.inner[k]] for k in self.inner}
        return Mapping(inner)
