"""Graph backend implementation using the py:mod:`igraph` library.

This module provides a concrete implementation of the :py:class:`GraphWrapper`
interface using :py:class:`igraph.Graph`.
"""

from typing import Any, Iterable, Literal, Mapping, Unpack, cast
from logging import getLogger


try:
    from igraph import Graph, Vertex  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    raise ImportError(
        "The igraph library is not available. "
        "Please install it through 'pip install igraph', "
        "or use the 'networkx' backend instead."
    )

from igraph._igraph import InternalError  # type: ignore[import-untyped]

from ..core.attribute import VertexAttributeName, VertexAttributes
from ..core.funccall import CallMode
from ..core.constant import NA, V
from ..core.graphwrapper import DEFAULT_EDGE_DIRECTION, EdgeDirection, GraphWrapper

logger = getLogger(__name__)


class IGraphWrapper(GraphWrapper[Graph, V]):
    """Graph backend for the igraph library."""

    # Private methods ================================================================
    def _get_v(self, vertex: V) -> Vertex:
        """Get the vertex object from its name.

        Args:
            vertex: the name of the vertex.

        Returns:
            the vertex object.

        Raises:
            VertexError: if the vertex is not found.
        """
        try:
            return self.graph.vs.find(name=vertex)
        except ValueError:
            self._raise_vertex_not_found(vertex)

    def _get_edge_index(self, source: V, target: V) -> int:
        """Get the index of an edge.

        Args:
            source: the source vertex.
            target: the target vertex.

        Returns:
            the index of the edge.

        Raises:
            VertexError: if the edge is not found.
        """

        source_index = self._get_v(source).index
        target_index = self._get_v(target).index

        try:
            return self.graph.get_eid(source_index, target_index)
        except InternalError as e:
            if "Cannot get edge ID, no such edge." in str(e):
                self._raise_edge_not_found(source, target, e)
            else:
                raise e  # pragma: no cover

    # Overridden methods =============================================================
    # Initialization -----------------------------------------------------------------
    @classmethod
    def initialize_empty(cls) -> Graph:
        return Graph(directed=True)

    def get_graph_copy(self) -> Graph:
        return self.graph.copy()

    # Construction ------------------------------------------------------------------
    def add_vertex(self, vertex: V, **attributes: Unpack[VertexAttributes[V]]) -> None:
        self.graph.add_vertex(name=vertex, **attributes)

    def add_edge(self, source: V, target: V) -> None:
        v1 = self._get_v(source)
        v2 = self._get_v(target)
        self.graph.add_edge(v1.index, v2.index)

    # Destruction -------------------------------------------------------------------
    def delete_vertex(self, *vertices: V) -> None:
        vs = self.graph.vs.select(name_in=vertices)
        if len(vs) != len(vertices):
            missing_vertices = set(vertices) - set(vs["name"])
            self._raise_vertex_not_found(missing_vertices.pop())
        self.graph.delete_vertices(vs)

    def delete_edge(self, source: V, target: V) -> None:
        edge_index = self._get_edge_index(source, target)
        self.graph.delete_edges(edge_index)

    # Vertex attributes -------------------------------------------------------------
    def get_vertex_attribute(self, vertex: V, key: VertexAttributeName) -> Any:
        return self._get_v(vertex)[key]

    def get_vertex_attributes(self, vertex: V) -> VertexAttributes[V]:
        return cast(
            VertexAttributes[V],
            {
                attr: value
                for attr, value in self._get_v(vertex).attributes().items()
                if attr != "name"
            },
        )

    def set_vertex_attribute(
        self, vertex: V, key: VertexAttributeName, value: Any
    ) -> None:
        v = self._get_v(vertex)
        v[key] = value

    def update_vertex_attributes(
        self, vertex: V, attributes: Mapping[VertexAttributeName, Any]
    ) -> None:
        v = self._get_v(vertex)
        for attr, value in attributes.items():
            v[attr] = value

    # call_mode attribute -----------------------------------------------------------
    @property
    def call_mode(self) -> CallMode | None:
        graph = self.graph
        if "call_mode" not in graph.attributes():
            graph["call_mode"] = None
            return None
        return cast(CallMode | None, graph["call_mode"])

    @call_mode.setter
    def call_mode(self, call_mode: CallMode | None) -> None:
        self._check_call_mode(call_mode)
        self.graph["call_mode"] = call_mode

    # Nodes and edges ---------------------------------------------------------------
    @property
    def _vertices(self) -> Iterable[V]:
        return self.graph.vs["name"]

    @property
    def _edges(self) -> Iterable[tuple[V, V]]:
        return (
            (self.graph.vs[e.source]["name"], self.graph.vs[e.target]["name"])
            for e in self.graph.es
        )

    def get_neighbors(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> Iterable[V]:
        self._check_edge_direction(direction)

        vertex_idx = self._get_v(vertex).index
        return self.graph.vs[self.graph.neighbors(vertex_idx, mode=direction)]["name"]

    def get_degree(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> int:
        self._check_edge_direction(direction)
        vertex_index = self._get_v(vertex).index
        return self.graph.degree(vertex_index, mode=direction)

    def get_subcomponent(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> Iterable[V]:
        self._check_edge_direction(direction)

        vertex_idx = self._get_v(vertex).index
        return self.graph.vs[self.graph.subcomponent(vertex_idx, mode=direction)][
            "name"
        ]

    # Graph operations --------------------------------------------------------------
    def _subgraph(self, vertices: Iterable[V]) -> Graph:
        return self.graph.subgraph([self._get_v(v).index for v in vertices])

    def is_dag(self) -> bool:
        return self.graph.is_dag()

    def reset(self) -> None:
        graph = self.graph
        n_vertices = len(graph.vs)
        logger.info("Resetting graph with %d vertices", n_vertices)
        graph.vs["func"] = [None] * n_vertices
        graph.vs["value"] = [NA] * n_vertices
        for attribute in graph.attributes():
            del graph[attribute]

    def get_sorted_vertices(self, direction: Literal["in", "out"]) -> Iterable[V]:
        if direction not in ("in", "out"):
            raise ValueError(
                f"Invalid direction {direction!r}. Valid directions are 'in' and 'out'."
            )

        if len(self.graph.vs) == 0:
            return []

        try:
            return self.graph.vs[self.graph.topological_sorting(mode=direction)]["name"]
        except InternalError as e:
            if "The graph has cycles" in str(e):
                raise ValueError(
                    "The graph is not a DAG. Cannot get topologically sorted vertices."
                ) from e
            raise e  # pragma: no cover
