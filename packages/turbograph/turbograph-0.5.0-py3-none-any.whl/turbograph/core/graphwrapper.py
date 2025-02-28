"""Graph wrapper base class.

This module defines the abstract base class :py:class:`GraphWrapper`
and related exceptions for managing and manipulating graph structures.

The py:class:`GraphWrapper` class provides a common interface for graph operations used
in the TurboGraph library. It allows defining various backends for different graph
libraries, implemented in the :py:mod:`turbograph.backend` package.
"""

from abc import ABC, abstractmethod
from typing import (
    Any,
    Generic,
    Iterable,
    Literal,
    Mapping,
    NoReturn,
    Self,
    TypeVar,
    Unpack,
)
from logging import getLogger

from .attribute import VertexAttributeName, VertexAttributes
from .funccall import CALL_MODES, CallMode
from .constant import NA, V

logger = getLogger(__name__)


G = TypeVar("G")
"""Type representing the graph."""


class VertexError(Exception):
    """Exception raised for a missing vertex."""

    def __init__(self, vertex: Any, message: str) -> None:
        """Initialize the exception with the vertex and a message.

        Args:
            vertex: The vertex that caused the error.
            message: The error message.
        """
        self.vertex = vertex
        super().__init__(message)


class EdgeError(Exception):
    """Exception raised for a missing edge."""

    def __init__(self, edge: Any, message: str) -> None:
        """Initialize the exception with the edge and a message.

        Args:
            edge: The edge that caused the error.
            message: The error message.
        """
        self.edge = edge
        super().__init__(message)


EdgeDirection = Literal["in", "out", "all"]
"""Represents the direction of an edge in the graph."""

EDGE_DIRECTIONS = ("in", "out", "all")
"""Tuple of all possible edge directions in the graph."""

DEFAULT_EDGE_DIRECTION: Literal["all"] = "all"
"""Default edge direction used in graph wrapper methods."""


class GraphWrapper(ABC, Generic[G, V]):
    """Abstract base class for graph operations in TurboGraph.

    This class defines the essential methods for interacting with graph data
    structures, used to construct and manipulate dependency graphs in TurboGraph.
    """

    def __init__(self, graph: G | None = None) -> None:
        """Initialize the graph wrapper with an optional graph instance.

        Args:
            graph: An optional graph instance to initialize the wrapper with.
                   If not provided, an empty graph is initialized.
        """
        self.graph = graph if graph is not None else self.initialize_empty()
        """The actual graph instance."""

    # Abstract methods ==============================================================
    @classmethod
    @abstractmethod
    def initialize_empty(cls) -> G:
        """Initialize and return an empty graph."""
        ...

    @abstractmethod
    def get_graph_copy(self) -> G:
        """Return a copy of the internal graph."""
        ...

    # Construction ------------------------------------------------------------------
    @abstractmethod
    def add_vertex(self, vertex: V, **attributes: Unpack[VertexAttributes[V]]) -> None:
        r"""Add a vertex with specified attributes to the graph.

        Args:
            vertex: The vertex to add.
            **attributes: Keyword arguments representing the vertex attributes.
        """
        ...

    @abstractmethod
    def add_edge(self, source: V, target: V) -> None:
        """Add an edge between the source and target vertices.

        Args:
            source: The source vertex.
            target: The target vertex.
        """
        ...

    # Destruction -------------------------------------------------------------------
    @abstractmethod
    def delete_vertex(self, *vertices: V) -> None:
        r"""Delete specified vertices from the graph.

        Args:
            *vertices: The vertices to delete.

        Raises:
            VertexError: If a vertex is not found in the graph.
        """
        ...

    @abstractmethod
    def delete_edge(self, source: V, target: V) -> None:
        """Delete an edge between the source and target vertices.

        Args:
            source: The source vertex.
            target: The target vertex.

        Raises:
            EdgeError: If the edge is not found in the graph.
        """
        ...

    # Vertex attributes -------------------------------------------------------------
    @abstractmethod
    def get_vertex_attribute(self, vertex: V, key: VertexAttributeName) -> Any:
        """Get the value of a specific attribute of a vertex.

        Args:
            vertex: The vertex whose attribute is to be retrieved.
            key: The attribute key.

        Raises:
            VertexError: If the vertex is not found in the graph.
        """
        ...

    @abstractmethod
    def get_vertex_attributes(self, vertex: V) -> VertexAttributes[V]:
        """Get all attributes of a vertex.

        Args:
            vertex: The vertex whose attributes are to be retrieved.

        Raises:
            VertexError: If the vertex is not found in the graph.
        """
        ...

    @abstractmethod
    def set_vertex_attribute(
        self, vertex: V, key: VertexAttributeName, value: Any
    ) -> None:
        """Set the value of a specific attribute of a vertex.

        Args:
            vertex: The vertex whose attribute is to be set.
            key: The attribute key.
            value: The value to set.

        Raises:
            VertexError: If the vertex is not found in the graph.
        """
        ...

    @abstractmethod
    def update_vertex_attributes(
        self, vertex: V, attributes: Mapping[VertexAttributeName, Any]
    ) -> None:
        """Update multiple attributes of a vertex.

        Args:
            vertex: The vertex whose attributes are to be updated.
            attributes: A mapping of attribute keys to values.

        Raises:
            VertexError: If the vertex is not found in the graph.
        """
        ...

    # Nodes and edges ---------------------------------------------------------------
    @property
    @abstractmethod
    def _vertices(self) -> Iterable[V]:
        """Get all vertices of the graph."""
        ...

    @property
    @abstractmethod
    def _edges(self) -> Iterable[tuple[V, V]]:
        """Get all edges of the graph."""
        ...

    @abstractmethod
    def get_neighbors(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> Iterable[V]:
        """Get the neighbors of a vertex in the specified direction.

        Args:
            vertex: The vertex whose neighbors are to be retrieved.
            direction: The direction of the edges to consider ("in", "out", or "all").

        Raises:
            VertexError: If the vertex is not found in the graph.
        """
        ...

    @abstractmethod
    def get_degree(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> int:
        """Get the degree of a vertex in the specified direction.

        Args:
            vertex: The vertex whose degree is to be retrieved.
            direction: The direction of the edges to consider ("in", "out", or "all").

        Raises:
            VertexError: If the vertex is not found in the graph.
        """
        ...

    @abstractmethod
    def get_subcomponent(
        self, vertex: V, direction: EdgeDirection = DEFAULT_EDGE_DIRECTION
    ) -> Iterable[V]:
        """Get the subcomponent of a vertex in the specified direction.

        Args:
            vertex: The vertex whose subcomponent is to be retrieved.
            direction: The direction of the edges to consider ("in", "out", or "all").

        Raises:
            VertexError: If the vertex is not found in the graph.
        """
        ...

    # Call mode ---------------------------------------------------------------------
    @property
    @abstractmethod
    def call_mode(self) -> CallMode | None:
        """Return the current call mode of the graph."""
        ...

    @call_mode.setter
    @abstractmethod
    def call_mode(self, call_mode: CallMode | None) -> None:
        """Set the call mode of the graph."""
        ...

    # Graph operations --------------------------------------------------------------
    @abstractmethod
    def _subgraph(self, vertices: Iterable[V]) -> G:
        """Create a subgraph containing the specified vertices.

        Args:
            vertices: The vertices to include in the subgraph.

        Raises:
            KeyError: If a vertex is not found in the graph.
        """
        ...

    @abstractmethod
    def is_dag(self) -> bool:
        """Check if the graph is a directed acyclic graph (DAG)."""
        ...

    @abstractmethod
    def get_sorted_vertices(self, direction: Literal["in", "out"]) -> Iterable[V]:
        """Get the vertices sorted topologically in the specified direction.

        Args:
            direction: The direction of the edges to consider ("in" or "out").
        """
        ...

    # Private methods ===============================================================
    # Exception handling ------------------------------------------------------------
    def _raise_vertex_not_found(
        self, vertex: V, origin: Exception | None = None
    ) -> NoReturn:
        """Raise an exception indicating that the vertex was not found.

        Args:
            vertex: The vertex that was not found.
        """
        raise VertexError(
            vertex,
            f"Vertex {vertex!r} not found in the graph. "
            "Valid vertices are: " + ", ".join(map(repr, self.vertices)),
        ) from origin

    def _raise_edge_not_found(
        self, source: V, target: V, origin: Exception | None = None
    ) -> NoReturn:
        """Raise an exception indicating that the edge was not found.

        Args:
            source: The source vertex of the edge.
            target: The target vertex of the edge.
        """
        raise EdgeError(
            (source, target),
            f"Edge from {source!r} to {target!r} not found in the graph. "
            "Valid edges are: " + ", ".join(map(repr, self.edges)),
        ) from origin

    def _check_call_mode(self, call_mode: Any) -> None:
        """Check if the call mode is valid.

        Args:
            call_mode: The call mode to check.

        Raises:
            ValueError: If the call mode is invalid
        """
        if call_mode is not None and call_mode not in CALL_MODES:
            raise ValueError(
                f"Invalid call mode {call_mode!r}. "
                f"Valid modes are: {', '.join(CALL_MODES)}"
            )

    def _check_edge_direction(self, direction: EdgeDirection) -> None:
        if direction not in EDGE_DIRECTIONS:
            raise ValueError(
                f"Invalid edge direction {direction!r}. "
                f"Valid directions are: {', '.join(EDGE_DIRECTIONS)}"
            )

    # Concrete methods ==============================================================
    # Vertices and edges ------------------------------------------------------------
    @property
    def vertices(self) -> set[V]:
        """Return a set of all vertices in the graph."""
        return set(self._vertices)

    @property
    def edges(self) -> set[tuple[V, V]]:
        """Return a set of all edges in the graph."""
        return set(self._edges)

    def has_vertex(self, vertex: V) -> bool:
        """Check if the vertex exists in the graph.

        Args:
            vertex: The vertex to check.
        """
        return vertex in self.vertices

    def has_edge(self, source: V, target: V) -> bool:
        """Check if the edge exists in the graph.

        Args:
            source: The source vertex of the edge.
            target: The target vertex of the edge.
        """
        return (source, target) in self.edges

    # Vertex attributes -------------------------------------------------------------
    def get_vertices_with_known_value(self) -> set[V]:
        """Return a set of vertices that have a known value
        (i.e., not :py:data:`NA`).
        """
        return {
            vertex
            for vertex in self._vertices
            if self.get_vertex_attribute(vertex, "value") is not NA
        }

    def set_attribute_to_vertices(
        self, key: VertexAttributeName, vertex_to_value: Mapping[V, Any]
    ) -> None:
        """Set a specific attribute for multiple vertices.

        Args:
            key: The attribute key.
            vertex_to_value: A mapping of vertices to values.

        Raises:
            KeyError: If a vertex is not found in the graph.
        """
        for vertex, value in vertex_to_value.items():
            logger.debug("Setting attribute %r to vertex %r", key, vertex)
            self.set_vertex_attribute(vertex, key, value)

    def get_all_vertex_attributes(self) -> dict[V, VertexAttributes[V]]:
        """Return a dictionary of all vertex attributes."""
        return {vertex: self.get_vertex_attributes(vertex) for vertex in self._vertices}

    # Graph operations --------------------------------------------------------------
    def copy(self) -> Self:
        """Create and return a copy of the graph wrapper,
        including the graph instance.
        """
        return self.__class__(self.get_graph_copy())

    def subgraph(self, vertices: Iterable[V]) -> Self:
        """Create and return a subgraph containing the specified vertices.

        Args:
            vertices: The vertices to include in the subgraph.
        """
        return self.__class__(self._subgraph(vertices))

    def reset(self) -> None:
        """Reset the graph by removing all functions, computed values,
        and graph attributes.

        This method clears the stored functions and values from all vertices
        while preserving the graph's structure and dependencies.
        """
        # Clear vertex attributes.
        for vertex in self._vertices:
            self.set_vertex_attribute(vertex, "func", None)
            self.set_vertex_attribute(vertex, "value", NA)

        # Clear graph attributes.
        self.call_mode = None

    def __eq__(self, other: Any) -> bool:
        """Check if the graph wrapper is equal to another object."""
        if not isinstance(other, self.__class__):
            return False

        return (
            self.edges == other.edges
            and self.call_mode == other.call_mode
            and self.get_all_vertex_attributes() == other.get_all_vertex_attributes()
        )


GW = TypeVar("GW", bound=GraphWrapper[Any, Any])
"""Type of the graph wrapper."""
