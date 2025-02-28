"""A module for constructing and validating directed acyclic graphs (DAGs)
of quantities.

This module provides functions to create a dependency graph where vertices represent
quantities, and directed edges define dependencies between them. The graph ensures that
there are no cyclic dependencies and can be built from various vertex specifications.
"""

from typing import Any, Iterable, Mapping
from logging import getLogger

from ..backend.factory import Backend, get_graph_backend
from ..core.funccall import DEFAULT_CALL_MODE, CallMode
from ..core.graphwrapper import GraphWrapper
from ..core.constant import V
from ..core.specification import RawVertexSpecification, VertexSpecification
from ..core.adapter import format_specifications
from .graphchecking import check_graph


logger = getLogger(__name__)


def _build_graph(
    specifications: Mapping[V, VertexSpecification[V]],
    vertices: Iterable[V] | None = None,
    *,
    call_mode: CallMode = DEFAULT_CALL_MODE,
    backend: Backend | None = None,
) -> GraphWrapper[Any, V]:
    r"""Constructs a directed acyclic graph (DAG) from formatted vertex specifications.

    This function builds a graph where vertices represent quantities and directed edges
    represent dependencies between them.

    Args:
        specifications: A mapping from vertex names to their specifications.
            Each specification defines how the vertex is computed and its dependencies.

        vertices: An optional subset of vertices to include in the graph.
            If ``None``, all vertices in ``specifications`` are included.
            If specified, only these vertices and their ancestors are included.

        call_mode: The mode used to handle function inputs. This determines how inputs
            are passed when computing vertex values and is stored as a graph attribute.

        backend: The graph backend to use. If ``None``, the first available backend is
            used.

    Returns:
        A :py:class:`GraphWrapper` object representing the constructed dependency graph.

    Notes:
        The graph is not validated at this stage.
    """
    specifications = dict(specifications)
    graph = get_graph_backend(backend=backend)()
    graph.call_mode = call_mode

    if vertices is None:
        vertices = specifications.keys()

    vertices_to_add: set[V] = set(vertices)
    edges_to_add_later: set[tuple[V, V]] = set()

    # Add vertices to the graph
    while vertices_to_add:
        vertex = vertices_to_add.pop()
        try:
            vertex_specification = specifications.pop(vertex)
        except KeyError:
            vertex_specification = VertexSpecification[V]()

        attributes = vertex_specification.to_dict()
        logger.debug("Adding vertex %r with attributes %r", vertex, attributes)
        graph.add_vertex(vertex, **attributes)

        predecessors = attributes["predecessors"]
        for predecessor in predecessors:
            logger.debug("Handling predecessor %r", predecessor)
            edges_to_add_later.add((predecessor, vertex))
            if predecessor not in graph.vertices:
                vertices_to_add.add(predecessor)

    # Add edges to the graph
    logger.debug("Adding edges: %r", edges_to_add_later)
    # graph.add_edges(edges_to_add_later)
    for edge in edges_to_add_later:
        logger.debug("Adding edge %r -> %r", *edge)
        graph.add_edge(*edge)

    if specifications:
        logger.debug(
            "Some vertices were not added to the graph: %r",
            specifications.keys(),
        )

    return graph


def build_graph(
    raw_specifications: Mapping[V, RawVertexSpecification[V]],
    vertices: Iterable[V] | None = None,
    *,
    call_mode: CallMode = DEFAULT_CALL_MODE,
    backend: Backend | None = None,
) -> GraphWrapper[Any, V]:
    r"""Builds a validated directed acyclic graph (DAG) from raw vertex specifications.

    This function processes raw vertex specifications to construct a dependency graph.
    Each vertex represents a quantity, and directed edges indicate dependencies.
    The graph is validated to ensure it is acyclic.

    Args:
        raw_specifications: A mapping of vertex names to their specifications, defining
            how each vertex is computed and its dependencies.
            Specifications can take one of four forms:

            - **Function:** The function's signature determines dependencies:
                - If ``call_mode='args'``, positional arguments are considered
                  predecessors.
                - If ``call_mode='kwargs'``, keyword arguments are considered
                  predecessors.

            - **Value:** A non-callable value for the vertex.

            - **Dictionary:** A more explicit definition:

                - ``func`` is an optional function computing the vertex
                  (default: ``None``).
                - ``predecessors`` is an optional list of dependency names
                  (default: ``()``).
                - ``value`` is an optional precomputed value
                  (default: :py:data:`turbograph.NA`).

            - **Sequence:**: A tuple of up to three elements
              ``(func, predecessors, value)``.

        vertices: An optional subset of vertices to include in the graph.
            If ``None``, all vertices in ``raw_specifications`` are included.
            Otherwise, only the specified vertices and their ancestors are retained.

        call_mode: The mode used for passing input values to functions, stored
            as a graph attribute:

            - ``"args"`` (default): Inputs are passed as positional arguments.
            - ``"kwargs"``: Inputs are passed as keyword arguments.
            - ``"arg"``: Inputs are passed as a single dictionary argument.

        backend: The graph backend to use. If ``None``, the first available backend is
            used.

    Returns:
        A ``GraphWrapper`` object representing the constructed dependency graph.

        The graph contains:

        - Vertices with attributes:
            - ``"func"``: Function computing the vertex (or ``None`` if absent).
            - ``"value"``: Precomputed value, or a default placeholder
              :py:data:`turbograph.NA` if absent.
            - ``"predecessors"``: Ordered list of predecessor vertices.

        - Directed edges representing dependencies.
        - The ``call_mode`` stored as a graph attribute.

    Raises:
        ValueError: If the specified dependencies create a cyclic graph.
        ValueError: If the graph contains isolated vertices.

    Example:
        Construct a simple graph computing ``a - b``:

        >>> graph = build_graph({"sub": lambda a, b: a - b})
        >>> compute_from_graph(graph, values={"a": 5, "b": 3}, vertices=["sub"])
        {'sub': 2}

        Construct a graph with precomputed values:

        >>> graph = build_graph(
        ...     {"a": 10, "b": 5, "sub": lambda a, b: a - b},
        ...     vertices=["sub"]
        ... )
        >>> compute_from_graph(graph)
        {'a': 10, 'b': 5, 'sub': 5}
    """
    logger.debug("Format the vertex specifications")
    specifications = format_specifications(raw_specifications, call_mode)
    logger.debug("Build the graph")
    graph = _build_graph(
        specifications, vertices=vertices, call_mode=call_mode, backend=backend
    )
    logger.debug("Check the graph sanity")
    check_graph(graph)
    return graph
