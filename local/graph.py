import random
import networkx as nx
from typing import Dict, List, Tuple, TypeVar, Generic, Iterator


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


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class Mapping(Generic[A, B]):
    """
    Mapping of values:

    Values from the domain A are mapped onto values from the codomain B.

    Each input from A is mapped to exactly one output from B, or A is undefined (function).

    Each output from B is the result of mapping some input A onto it (surjective).

    There might be distinct inputs that map onto the same output (not injective),
    or each input maps onto a unique output (injective).

    If the mapping is injective, then (because it is always surjective) it is a bijection, aka a one-to-one mapping.
    """
    inner: Dict[A, B]

    def __init__(self, inner: Dict[A, B]):
        self.inner = inner

    def __repr__(self) -> str:
        return str(self.inner)

    def __iter__(self) -> A:
        for key in self.inner:
            yield key

    def __getitem__(self, index: A) -> B:
        return self.inner[index]

    def __len__(self) -> int:
        return len(self.inner)

    @classmethod
    def shuffle_graph(cls, graph: nx.Graph) -> "Mapping[int, int]":
        """
        Create a mapping of node labels by random shuffling nodes.

        :param graph: original graph
        :return: random shuffling of node labels
        """
        original = list(graph.nodes())
        shuffled = original.copy()
        random.shuffle(shuffled)
        inner = {original[i]: shuffled[i] for i in range(len(original))}

        return Mapping(inner)

    @classmethod
    def shuffle_list(cls, lst: List[A]) -> "Mapping[A, A]":
        """
        Create a mapping by randomly shuffling list elements.

        The original list remains unchanged.

        :param lst: original list
        :return: random shuffling of list elements
        """
        shuffled = lst.copy()
        random.shuffle(shuffled)
        inner = {lst[i]: shuffled[i] for i in range(len(lst))}

        return Mapping(inner)

    def apply_graph(self, graph: nx.Graph) -> nx.Graph:
        """
        Apply the mapping of node labels to a graph.

        The original graph remains unchanged and a new graph is crated.

        :param graph: original graph
        :return: graph with mapped node labels
        """
        return nx.relabel_nodes(graph, self.inner, copy=True)

    def apply_list(self, lst: List[A]) -> List[A]:
        """
        Apply the mapping to a list.

        The original list remains unchanged and a new list is created.

        :param lst: original list
        :return: list of mapped values
        """
        return [self.inner[x] if x in self.inner else x for x in lst]

    def is_bijection(self) -> bool:
        """
        Return whether the mapping is a bijection:

        Each input from A is mapped to a unique output from B.

        :return: mapping is a bijection
        """
        return len(self.inner) == len(set(self.inner.values()))

    def invert(self) -> "Mapping[B, A]":
        """
        Invert the mapping.

        If `a → b` in this mapping, then `b → a` in the inverse.

        **Only bijections are invertible!**

        :return: inverse mapping
        """
        if not self.is_bijection():
            raise ValueError("Can only invert bijective mappings")

        inner = {v: k for k, v in self.inner.items()}
        return Mapping(inner)

    def and_then(self, second: "Mapping[B, C]") -> "Mapping[A, C]":
        """
        Compose this mapping with a second mapping.

        If `a → b` in this mapping and `b → a` in the second mapping,
        then `a → c` in the composition.

        If `a → b` in this mapping and `b` is undefined for the second mapping,
        then `a` is undefined in the composition.

        :param second: second mapping
        :return: composed mapping
        """
        inner = {k: second.inner[self.inner[k]] for k in self.inner if self.inner[k] in second.inner}
        return Mapping(inner)
