"""This module provides functions to compute values in a directed acyclic graph (DAG)
based on defined dependencies and vertex-specific functions and values.
"""

from typing import Any, Callable, Iterable, Mapping, TypeVar
from logging import getLogger

from ..core.constant import NA, V, VertexFunc, VertexValue
from ..core.attribute import VertexAttributes
from ..core.graphwrapper import GraphWrapper
from ..core.funccall import CallMode, DEFAULT_CALL_MODE, call_func
from .graphupdating import rebuild_graph

logger = getLogger(__name__)

NAType = TypeVar("NAType")
"""Type representing a missing value in vertex attributes."""


def _get_vertex_func(vertex: Any, vertex_attrs: VertexAttributes) -> Callable[..., Any]:
    """Retrieve the computation function associated with a vertex, with error handling.

    Args:
        vertex: The vertex whose function is being retrieved.
        vertex_attrs: The attributes of the vertex, which may include a function.

    Returns:
        The function used to compute the vertex value.

    Raises:
        ValueError: If no function is associated with the vertex.
    """
    if (func := vertex_attrs.get("func")) is None:
        raise ValueError(
            f"Function to compute vertex {vertex!r} is not provided. "
            "Please provide a function to compute the vertex."
        )
    return func


def _compute_vertex(
    graph: GraphWrapper[Any, V],
    vertex: V,
    func: Callable[..., Any],
    *,
    call_mode: CallMode,
) -> Any:
    r"""Compute the value of a vertex based on its dependencies.

    This function retrieves the values of a vertex's predecessors and uses them
    as inputs to compute the vertex's value.

    Args:
        graph: The dependency graph.
        vertex: The vertex to compute.
        func: The function that defines how to compute the vertex value.
        call_mode: The mode used to pass inputs to the function.

            - ``"args"``: Pass values as positional arguments.
            - ``"kwargs"``: Pass values as keyword arguments.
            - ``"arg"``: Pass values as a single dictionary argument.

    Returns:
        The computed value of the vertex.

    Raises:
        TypeError: If there is an issue with the function signature.
    """
    # Get the values of the predecessors, to be passed to the function
    ordered_precedecessors = graph.get_vertex_attribute(vertex, "predecessors")
    arguments = {
        predecessor: graph.get_vertex_attribute(predecessor, "value")
        for predecessor in ordered_precedecessors
    }

    # Compute the value of the vertex
    logger.debug("Computing vertex %r with arguments %r", vertex, arguments)
    try:
        return call_func(func, arguments, call_mode)
    except TypeError as e:
        raise TypeError(
            f"Error when computing vertex {vertex!r} "
            f"with arguments {arguments!r}. "
            "Make sure that the function signature is correct."
        ) from e


def compute_from_graph(
    graph: GraphWrapper[Any, V],
    vertices: Iterable[V] | None = None,
    values: Mapping[V, VertexValue] | None = None,
    funcs: Mapping[V, VertexFunc] | None = None,
    *,
    call_mode: CallMode | None = None,
    auto_prune: bool = True,
) -> dict[V, Any]:
    r"""Compute values in a dependency graph.

    This function evaluates the specified vertices in a directed acyclic graph (DAG),
    ensuring that computations follow the correct dependency order. It allows overriding
    values, updating functions dynamically, and pruning unnecessary intermediate values.

    Args:
        graph: The dependency graph.

        vertices: The set of vertices to compute.

            - If ``None``, all vertices in the graph are computed.
            - If specified, only the listed vertices and their dependencies are
              computed.

        values: A mapping from vertex names to precomputed values. If provided,
            these values override the existing ones in the graph.

        funcs: A mapping from vertex names to updated functions. If provided,
            these functions override the existing ones in the graph.

        call_mode: The mode used to pass dependencies to functions.
            If ``None``, the mode is inferred from the graph.

            - ``"args"``: Dependencies are passed as positional arguments.
            - ``"kwargs"``: Dependencies are passed as keyword arguments.
            - ``"arg"``: Dependencies are passed as a single dictionary.

        auto_prune: If ``True``, automatically removes intermediate vertices
            that are no longer needed after computation to optimize memory usage.

    Returns:
        A dictionary mapping vertex names to their computed values.

    Raises:
        ValueError: If cycles are detected in the graph.

    Example:
        Compute values from a dependency graph.

        >>> from turbograph import compute_from_graph, build_graph
        >>> deps = {"a": [], "b": [], "c": ["a", "b"], "d": ["c"]}
        >>> funcs = {
        ...     "a": lambda: 5,
        ...     "b": lambda: 10,
        ...     "c": lambda a, b: a + b,
        ...     "d": lambda c: c * 2,
        ... }
        >>> graph = build_graph(deps, funcs=funcs)
        >>> compute_from_graph(graph)
        {'a': 5, 'b': 10, 'c': 15, 'd': 30}

        Override a vertex value before computation:

        >>> compute_from_graph(graph, values={"a": 7})
        {'a': 7, 'b': 10, 'c': 17, 'd': 34}

        Modify a function before computation:

        >>> compute_from_graph(graph, funcs={"c": lambda a, b: a * b})
        {'a': 5, 'b': 10, 'c': 50, 'd': 100}

        Compute only a specific vertex:

        >>> compute_from_graph(graph, vertices=["c"])
        {'c': 50}

    Notes:
        If both a function update and a precomputed value are provided for a vertex,
        the precomputed value takes precedence.
    """
    vertices = set(vertices) if vertices is not None else graph.vertices

    if not vertices:
        logger.warning("No vertex to compute.")
        return {}

    requested_values: dict[V, Any] = {}

    graph = rebuild_graph(
        graph, vertices, values, funcs, call_mode=call_mode, reduce=True
    )
    call_mode = (
        call_mode if (call_mode := graph.call_mode) is not None else DEFAULT_CALL_MODE
    )
    assert call_mode is not None

    # Compute the quantities
    ordered_vertices = graph.get_sorted_vertices(direction="out")

    logger.info(
        "Compute vertices %s in call mode %r. "
        "Vertices are computed in the following order: %r",
        vertices,
        call_mode,
        ordered_vertices,
    )

    for vertex in ordered_vertices:
        vertex_attrs = graph.get_vertex_attributes(vertex)
        logger.debug("Handling vertex %r", vertex_attrs)

        if (found_value := vertex_attrs.get("value", NA)) is not NA:
            logger.debug(
                "Found already computed value %r for vertex %r", found_value, vertex
            )
            value = found_value
        else:
            func = _get_vertex_func(vertex, vertex_attrs)
            value = _compute_vertex(graph, vertex, func, call_mode=call_mode)

        # Store the value of the computed vertex in the graph and in the output
        graph.set_vertex_attribute(vertex, "value", value)
        if vertex in vertices:
            logger.debug("Storing value %r of vertex %r", value, vertex)
            requested_values[vertex] = value

        # Remove the predecessors of the computed vertex
        # if they are not needed anymore
        # i.e., remove the values stored in the graph
        if auto_prune:
            for predecessor in list(graph.get_neighbors(vertex, direction="in")):
                # Remove the vertex if it is isolated
                if graph.get_degree(predecessor) == 1:
                    logger.debug(
                        "Remove predecessor %r of vertex %r", predecessor, vertex
                    )
                    graph.delete_vertex(predecessor)
                else:
                    # Remove the edge predecessor -> vertex
                    logger.debug("Remove edge %r -> %r", predecessor, vertex)
                    graph.delete_edge(predecessor, vertex)

    return requested_values
