"""This module defines core types and constants used in the Turbograph library."""

from typing import Any, Callable, Hashable, Sequence, TypeAlias, TypeVar


class _NA:
    """Sentinel value representing a missing vertex value.

    This singleton is used to distinguish between explicitly set ``None`` values
    and missing values. It helps differentiate uninitialized vertex attributes
    from those intentionally assigned ``None``.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return "<NA>"


NA: _NA = _NA()
"""A sentinel value representing a missing vertex 'value'.

This singleton is used to indicate that a vertex does not yet have a computed
or assigned value. It prevents ambiguity when ``None`` is a valid assigned value.
"""

V = TypeVar("V", bound=Hashable)
"""Generic vertex type.

Vertices in a dependency graph must be hashable, as they are used as keys in
internal mappings such as dictionaries for storing attributes.
"""


VertexFunc: TypeAlias = Callable[..., Any] | None
"""Type alias for a vertex's computation function.

A vertex function determines how a vertex's value is computed from its predecessors.
If `None`, no function is assigned to the vertex.
"""

VertexPredecessors: TypeAlias = Sequence[V]
"""Type alias for the predecessors of a vertex.

Predecessors are the vertices that provide input values for a given vertex's
computation.
"""

VertexValue: TypeAlias = Any | _NA
"""Type alias for the value of a vertex.

A vertex value can be:
- Any computed or assigned value.
- The sentinel `NA`, indicating that the value is missing.
"""
