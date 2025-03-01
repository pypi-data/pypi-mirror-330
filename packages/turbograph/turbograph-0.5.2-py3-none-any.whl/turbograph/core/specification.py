"""This module defines vertex specifications used to construct a dependency graph."""

from __future__ import annotations
from typing import Any, Callable, Generic, Mapping, Sequence, TypeAlias
from logging import getLogger
from inspect import _ParameterKind, signature
from dataclasses import dataclass

from .constant import NA, V, VertexFunc, VertexPredecessors, VertexValue
from .attribute import VertexAttributes

logger = getLogger(__name__)


def _get_arg_names(
    func: Callable[..., Any], kinds: Sequence[_ParameterKind]
) -> tuple[str, ...]:
    """Retrieve the names of positional arguments of a function, filtering by parameter
    kind.

    Args:
        func: The function whose arguments are being extracted.
        kinds: The kinds of arguments to include (e.g., positional-only, keyword-only).

    Returns:
        A tuple containing the names of the selected arguments.

    Example:
        >>> def example(a, b, *, c): pass
        >>> _get_arg_names(example, kinds=[_ParameterKind.POSITIONAL_OR_KEYWORD])
        ('a', 'b')
    """
    if not kinds:
        return ()
    sig = signature(func)
    return tuple(name for name, param in sig.parameters.items() if param.kind in kinds)


@dataclass(frozen=True)
class VertexSpecification(Generic[V]):
    """Defines the specification for a vertex in a dependency graph."""

    func: VertexFunc = None
    """An optional function to compute the vertex value.

    If ``None``, the vertex does not have an associated computation function.
    """

    predecessors: VertexPredecessors[V] = ()
    """A sequence of predecessor vertices providing inputs for computation."""

    value: VertexValue = NA
    """The value of the vertex.

    The sentinel :py:data:`NA` is used to indicate that the value is missing
    or uncomputed.
    """

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> VertexSpecification[V]:
        """Create a vertex specification from a mapping.

        Args:
            value: A mapping containing `func`, `predecessors`, and `value`.

        Returns:
            A `VertexSpecification` instance.
        """
        return cls(**value)

    @classmethod
    def from_sequence(cls, value: Sequence[Any]) -> VertexSpecification[V]:
        """ "Create a vertex specification from a sequence.

        The sequence should follow the order: `(func, predecessors, value)`.

        Args:
            value: A sequence containing function, predecessors, and value.

        Returns:
            A `VertexSpecification` instance.
        """
        return cls(*value)

    @classmethod
    def from_func(
        cls, func: Callable[..., Any], *, kinds: Sequence[_ParameterKind] = ()
    ) -> VertexSpecification[V]:
        """Create a vertex specification from a function.

        The function's parameter names are used as its predecessor vertices.

        Args:
            func: The function defining the vertex computation.
            kinds: The types of parameters to consider as predecessors.

        Returns:
            A `VertexSpecification` with inferred predecessors.
        """
        predecessors = _get_arg_names(func, kinds=kinds)  # type: ignore[assignment]
        logger.debug("Guessing predecessors %r for function %r", predecessors, func)
        return cls(func, predecessors)  # type: ignore[arg-type]

    @classmethod
    def from_value(cls, value: Any) -> VertexSpecification[V]:
        """Create a vertex specification from a raw value.

        Args:
            value: A precomputed value.

        Returns:
            A `VertexSpecification` with the value set.
        """
        return cls(value=value)

    @classmethod
    def from_any(
        cls, value: RawVertexSpecification[Any], *, kinds: Sequence[_ParameterKind] = ()
    ) -> VertexSpecification[V]:
        """Create a vertex specification from a raw input of any supported type.

        Args:
            value: The raw input, which can be a dictionary, sequence, function,
                or value.
            kinds: The types of parameters to consider when inferring predecessors.

        Returns:
            A `VertexSpecification` instance.
        """
        if isinstance(value, dict):
            return cls.from_mapping(value)
        elif isinstance(value, Sequence):
            return cls.from_sequence(value)
        elif callable(value):
            return cls.from_func(value, kinds=kinds)
        else:
            return cls.from_value(value)

    def to_dict(self) -> VertexAttributes:
        """Convert the vertex specification into a dictionary of vertex attributes.

        Returns:
            A dictionary containing `func`, `value`, and `predecessors`.
        """
        return VertexAttributes(
            func=self.func, value=self.value, predecessors=self.predecessors
        )


RawVertexSpecification: TypeAlias = (
    # Already a VertexSpecification
    VertexSpecification[V]
    # A mapping: use `from_mapping`
    | Mapping[str, Any]
    # A sequence: use `from_sequence`
    | Sequence[Any]
    # A callable: use `from_func`
    | Callable[..., Any]
    # A value: use `from_value`
    | Any
)
"""A raw vertex specification that can be converted
into a :py:class:`VertexSpecification`.

It can be one of the following types:

- A :py:class:`VertexSpecification` (already structured).
- A mapping (dictionary), processed with :py:meth:`VertexSpecification.from_mapping`.
- A sequence (list, tuple), processed with :py:meth:`VertexSpecification.from_sequence`.
- A callable function, processed with :py:meth:`VertexSpecification.from_func`.
- Any other value, processed with :py:meth:`VertexSpecification.from_value`.
"""
