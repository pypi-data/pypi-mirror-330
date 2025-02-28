"""Graph backend implementation using the :py:mod:`networkx` library.

This module provides a concrete implementation of the :py:class:`GraphWrapper`
interface using py:class:`networkx.DiGraph`.
"""

from itertools import chain
from typing import TYPE_CHECKING, Any, Generic, Iterable, Mapping, Literal, cast
from logging import getLogger


try:
    import networkx as nx
except ImportError:  # pragma: no cover
    raise ImportError(
        "The networkx library is not available. "
        "Please install it through 'pip install networkx', "
        "or use the 'igraph' backend instead."
    )

from networkx import NetworkXError

from ..core.constant import V
from ..core.attribute import VertexAttributeName, VertexAttributes
from ..core.graphwrapper import (
    DEFAULT_EDGE_DIRECTION,
    EdgeDirection,
    GraphWrapper,
)
from ..core.funccall import CallMode

logger = getLogger(__name__)

# Handling Generic Type Support in NetworkX (with the types-networkx library)
if TYPE_CHECKING:  # pragma: no cover
    try:

        class _DiGraph(nx.DiGraph[V], Generic[V]):  # type: ignore[no-redef]
            pass

    except TypeError:

        class _DiGraph(nx.DiGraph, Generic[V]):  # type: ignore[no-redef]
            pass

else:

    class _DiGraph(nx.DiGraph, Generic[V]):
        pass


class NetworkXWrapper(GraphWrapper[_DiGraph[V], V]):
    """Graph backend for the networkx library using a directed graph (DiGraph)."""

    # Overridden methods =============================================================
    @classmethod
    def initialize_empty(cls) -> _DiGraph[V]:
        return _DiGraph()

    def get_graph_copy(self) -> _DiGraph:
        return cast(_DiGraph, self.graph.copy())

    # Construction ------------------------------------------------------------------
    def add_vertex(self, vertex: V, **attributes: Any) -> None:
        self.graph.add_node(vertex, **attributes)

    def add_edge(self, source: V, target: V) -> None:
        # Check the existence of the vertices
        # (so that the behaviour is consistent with the igraph backend).
        if not self.graph.has_node(source):
            self._raise_vertex_not_found(source)
        if not self.graph.has_node(target):
            self._raise_vertex_not_found(target)

        # Add the edge.
        self.graph.add_edge(source, target)

    # Destruction -------------------------------------------------------------------
    def delete_vertex(self, *vertices: V) -> None:
        for vertex in vertices:
            try:
                self.graph.remove_node(vertex)
            except NetworkXError as e:
                self._raise_vertex_not_found(vertex, e)

    def delete_edge(self, source: V, target: V) -> None:
        try:
            self.graph.remove_edge(source, target)
        except NetworkXError as e:
            self._raise_edge_not_found(source, target, e)

    # Vertex attributes -------------------------------------------------------------
    def get_vertex_attribute(self, vertex: V, key: VertexAttributeName) -> Any:
        vertex_attributes = self.get_vertex_attributes(vertex)
        return vertex_attributes[key]

    def get_vertex_attributes(self, vertex: V) -> VertexAttributes[V]:
        try:
            vertex_attributes = self.graph.nodes[vertex]
        except KeyError as e:
            self._raise_vertex_not_found(vertex, e)

        return cast(VertexAttributes[V], vertex_attributes)

    def set_vertex_attribute(
        self, vertex: V, key: VertexAttributeName, value: Any
    ) -> None:
        vertex_attributes = self.get_vertex_attributes(vertex)
        vertex_attributes[key] = value

    def update_vertex_attributes(
        self, vertex: V, attributes: Mapping[VertexAttributeName, Any]
    ) -> None:
        graph_attributes = self.get_vertex_attributes(vertex)

        for key, value in attributes.items():
            graph_attributes[key] = value

    # call_mode attribute -----------------------------------------------------------
    @property
    def call_mode(self) -> CallMode | None:
        return cast(CallMode | None, self.graph.graph.setdefault("call_mode", None))

    @call_mode.setter
    def call_mode(self, call_mode: CallMode | None) -> None:
        self._check_call_mode(call_mode)
        self.graph.graph["call_mode"] = call_mode

    # Nodes and edges ---------------------------------------------------------------
    @property
    def _vertices(self) -> Iterable[V]:
        return self.graph.nodes()

    @property
    def _edges(self) -> Iterable[tuple[V, V]]:
        return self.graph.edges()

    def get_neighbors(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> Iterable[V]:
        try:
            if direction == "out":
                return self.graph.successors(vertex)
            elif direction == "in":
                return self.graph.predecessors(vertex)
            elif direction == "all":
                return chain(
                    self.graph.successors(vertex), self.graph.predecessors(vertex)
                )
            else:
                raise ValueError(f"Invalid edge direction: {direction!r}")
        except NetworkXError as e:
            self._raise_vertex_not_found(vertex, e)

    def get_degree(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> int:
        if not self.graph.has_node(vertex):
            self._raise_vertex_not_found(vertex)

        if direction == "out":
            degree = self.graph.out_degree(vertex)
        elif direction == "in":
            degree = self.graph.in_degree(vertex)
        elif direction == "all":
            degree = self.graph.degree(vertex)
        else:
            raise ValueError(f"Invalid edge direction: {direction!r}")

        assert isinstance(degree, int)
        return degree

    def get_subcomponent(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> Iterable[V]:
        if not self.graph.has_node(vertex):
            self._raise_vertex_not_found(vertex)
        if direction == "out":
            return {vertex} | nx.descendants(self.graph, vertex)
        elif direction == "in":
            return {vertex} | nx.ancestors(self.graph, vertex)
        elif direction == "all":
            undirected = self.graph.to_undirected()
            return nx.node_connected_component(undirected, vertex)
        else:
            raise ValueError(f"Invalid edge direction: {direction!r}")

    # Graph operations --------------------------------------------------------------
    def _subgraph(self, vertices: Iterable[V]) -> _DiGraph[V]:
        for vertex in vertices:
            if not self.graph.has_node(vertex):
                self._raise_vertex_not_found(vertex)
        return cast(_DiGraph[V], self.graph.subgraph(list(vertices)).copy())

    def is_dag(self) -> bool:
        return nx.is_directed_acyclic_graph(self.graph)

    def get_sorted_vertices(self, direction: Literal["in", "out"]) -> Iterable[V]:
        try:
            sorted_vertices = list(nx.topological_sort(self.graph))
        except nx.NetworkXUnfeasible as e:
            raise ValueError(
                "Graph is not a DAG; topological sorting is not possible."
            ) from e

        if direction == "in":
            return reversed(sorted_vertices)
        elif direction == "out":
            return sorted_vertices
        else:
            raise ValueError(f"Invalid direction: {direction!r}")
