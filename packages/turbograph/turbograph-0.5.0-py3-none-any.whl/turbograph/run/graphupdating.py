"""This module provides functionality to update and refine dependency graphs."""

from itertools import chain
from logging import getLogger
from typing import Any, Callable, Iterable, Mapping

from ..core.graphwrapper import GW, GraphWrapper
from ..core.funccall import CallMode
from ..core.constant import _NA, V

logger = getLogger(__name__)


def _remove_in_edges_for_vertices_with_value(graph: GraphWrapper[Any, V]) -> None:
    """Remove inbound edges for vertices that already have a known value. In-place.

    Args:
        graph: The dependency graph.
    """
    # Get vertices with a known value
    known_vertices = graph.get_vertices_with_known_value()

    if known_vertices:
        # Remove the in-edges of vertices with a known value
        for vertex in known_vertices:
            for predecessor in list(graph.get_neighbors(vertex, direction="in")):
                logger.debug(
                    "Remove edge from vertex %r to vertex %r because %r has "
                    "a known value",
                    predecessor,
                    vertex,
                    vertex,
                )
                graph.delete_edge(predecessor, vertex)


def rebuild_graph(
    graph: GW,
    vertices: Iterable[V] | None = None,
    values: Mapping[V, Any | _NA] | None = None,
    funcs: Mapping[V, Callable[..., Any] | None] | None = None,
    reduce: bool = False,
    *,
    call_mode: CallMode | None = None,
) -> GW:
    """Update an existing dependency graph with new functions, values,
    or a subset of vertices.

    This function allows modifying a computation graph by:

    - Retaining only a subset of vertices.
    - Updating functions assigned to vertices.
    - Assigning or overriding precomputed values.
    - Setting a new function call mode.
    - Reducing the graph by treating known values as constants.

    Args:
        graph: The dependency graph to update.

        vertices: The set of vertices to retain. If specified, only these vertices
            and their ancestors are kept.

        values: A mapping from vertex names to precomputed values. If provided,
            these values override the existing ones in the graph.

        funcs: A mapping from vertex names to updated functions. If provided,
            these functions override the existing ones in the graph.

        reduce: If ``True``, removes inbound edges for vertices with known values.
            This treats these vertices as constants and prevents unnecessary
            recomputation.

        call_mode: The mode used to pass inputs to functions.
            If ``None``, the call mode remains unchanged.

            - ``"args"`` (default): Dependencies are passed as positional arguments.
            - ``"kwargs"``: Dependencies are passed as keyword arguments.
            - ``"arg"``: Dependencies are passed as a single dictionary.

        reduce: If ``True``, removes inbound edges for vertices with known values,
            treating them as constants.
            This ensures that these vertices no longer depend on their predecessors,
            preventing unnecessary computations

    Returns:
        The updated graph object with the modified functions, values, and vertices.

    Example:
        Update a graph with new functions and values.

        >>> from turbograph import rebuild_graph, compute_from_graph, build_graph
        >>> graph = build_graph(
        ...     {"sum": ["a", "b"]},
        ...     funcs={"sum": lambda a, b: a + b},
        ...     values={"a": 1, "b": 2},
        ... )
        >>> compute_from_graph(graph)  # 1 + 2 = 3
        {'a': 1, 'b': 2, 'sum': 3}
        >>> updated_graph = rebuild_graph(
        ...     graph, funcs={"sum": lambda a, b: a * b}, values={"a": 10}
        ... )
        >>> compute_from_graph(updated_graph)  # 10 * 2 = 20
        {'a': 10, 'b': 2, 'sum': 20}

        Reduce the graph to retain only `"b"` and its dependencies.

        >>> graph = build_graph(
        ...     {"b": ["a"], "c": ["b"]},
        ...     funcs={"b": lambda x: x + 1, "c": lambda x: x + 2},
        ...     values={"a": 1},
        ... )
        >>> smaller_graph = rebuild_graph(graph, vertices=["b"])
        >>> compute_from_graph(smaller_graph)
        {'a': 1, 'b': 2}

    Notes:
        - If both a function update and a precomputed value are provided for a vertex,
          the precomputed value takes precedence.
        - If `vertices` is specified, computations are limited to those vertices
          and their ancestors.
        - If `reduce` is enabled, vertices with known values will not be recomputed.
    """
    if call_mode is not None:
        graph.call_mode = call_mode

    graph = graph.copy()

    # Update the values
    if values:
        graph.set_attribute_to_vertices("value", values)

    if reduce:
        _remove_in_edges_for_vertices_with_value(graph)

    # Only keep the vertices and their ancestors
    if vertices is not None:
        vertices = set(vertices)
        ancestors = set(
            chain(
                *(graph.get_subcomponent(vertex, direction="in") for vertex in vertices)
            )
        )
        logger.debug("Keep vertices %r and their ancestors: %r", vertices, ancestors)
        graph = graph.subgraph(ancestors)

    # Update the functions
    if funcs:
        graph.set_attribute_to_vertices("func", funcs)

    return graph
