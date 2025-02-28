"""A module for computing values from a dependency graph defined by vertex
specifications."""

from typing import Any, Iterable, Mapping
from logging import getLogger

from ..core.constant import V, VertexFunc, VertexValue
from ..core.specification import RawVertexSpecification
from ..core.funccall import CallMode, DEFAULT_CALL_MODE
from ..backend.factory import Backend
from .graphbuilding import build_graph
from .graphcomputing import compute_from_graph


logger = getLogger(__name__)


def compute(
    raw_specifications: Mapping[V, RawVertexSpecification[V]],
    vertices: Iterable[V] | None = None,
    values: Mapping[V, VertexValue] | None = None,
    funcs: Mapping[V, VertexFunc] | None | None = None,
    *,
    call_mode: CallMode = DEFAULT_CALL_MODE,
    auto_prune: bool = True,
    backend: Backend | None = None,
) -> dict[V, Any]:
    r"""Computes values from a dependency graph where each vertex represents
    a computation or value.

    This function constructs a directed acyclic graph (DAG) from the given
    ``raw_specifications`` and determines the correct execution order for computing
    values.
    It allows users to specify predefined values or override functions for specific
    vertices.

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

        vertices: The set of vertices to compute.

            - If ``None``, all vertices in the graph are computed.
            - If specified, only the listed vertices and their dependencies are
              computed.

        values: A mapping of vertex names to pre-defined values. If a vertex has
            an entry in this mapping,
            the given value is used instead of computing it from the graph.

        funcs: A mapping of vertex names to functions. If a vertex has an entry in this
            mapping, the provided function is used instead of the one in the graph.

        call_mode: Determines how dependencies are passed to functions:

            - ``"args"`` (default): Dependencies are passed as positional arguments.
            - ``"kwargs"``: Dependencies are passed as keyword arguments.
            - ``"arg"``: All dependencies are passed as a single dictionary argument.

        auto_prune: If ``True``, automatically removes intermediate vertices
            that are no longer needed after computation to optimize memory usage.

        backend: The graph backend to use. If ``None``, the first available backend is
        used.

    Returns:
        A mapping from vertex names to their computed values.

    Raises:
        ValueError: If the specified dependencies introduce a cyclic dependency,
        preventing execution.

    Example:
        Compute the sum of two numbers:

        >>> compute({"x": lambda: 3, "y": lambda: 4, "sum": lambda x, y: x + y})
        {'x': 3, 'y': 4, 'sum': 7}

        Compute only the sum, supplying values for ``a`` and ``b``, and explicitly
        defining dependencies:

        >>> compute(
        ...     {"sum": (lambda x, y: x + y, ["a", "b"])}, ["sum"], {"a": 1, "b": 2}
        ... )
        {'sum': 3}

        Use the ``"arg"`` call mode to pass dependencies as a single dictionary
        argument:

        >>> compute(
        ...     {
        ...         "sum": {
        ...             "func": lambda v: v["x"] + v["y"],
        ...             "predecessors": ["x", "y"],
        ...         },
        ...     },
        ...     ["sum"],
        ...     values={"x": 1, "y": 2},
        ...     call_mode="arg",
        ... )
        {'sum': 7}
    """
    graph = build_graph(
        raw_specifications, vertices, call_mode=call_mode, backend=backend
    )
    output = compute_from_graph(graph, vertices, values, funcs, auto_prune=auto_prune)
    return output
