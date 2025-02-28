"""This module adapts API-level data structures to internal representations for
dependency graph computations.

It provides utilities to:
- Convert raw vertex specifications into structured `VertexSpecification` objects.
- Map function call modes to their corresponding parameter kinds.
"""

from inspect import _ParameterKind
from typing import Mapping, Sequence

from .funccall import CallMode

from .specification import RawVertexSpecification, VertexSpecification
from .constant import V

CALL_MODE_TO_PARAMETER_KINDS: dict[CallMode, tuple[_ParameterKind, ...]] = {
    "args": (
        _ParameterKind.POSITIONAL_ONLY,
        _ParameterKind.POSITIONAL_OR_KEYWORD,
    ),
    "kwargs": (_ParameterKind.POSITIONAL_OR_KEYWORD, _ParameterKind.KEYWORD_ONLY),
    "arg": (),
}
"""Mapping of function call modes to the corresponding parameter kinds.

This dictionary defines which function parameter kinds are used for each call mode:

- `"args"`: Includes positional-only and positional-or-keyword arguments.
- `"kwargs"`: Includes positional-or-keyword and keyword-only arguments.
- `"arg"`: Does not consider any specific argument types.
"""


def get_parameter_kinds(call_mode: CallMode) -> tuple[_ParameterKind, ...]:
    """Retrieve the parameter kinds associated with a given function call mode,
    with proper error handling.

    The parameter kinds are defined in the :py:data:`CALL_MODE_TO_PARAMETER_KINDS`
    dictionary.
    """
    try:
        return CALL_MODE_TO_PARAMETER_KINDS[call_mode]
    except KeyError:
        raise ValueError(f"Invalid call mode: {call_mode!r}")


def _format_specifications(
    raw_specifications: Mapping[V, RawVertexSpecification[V]],
    kinds: Sequence[_ParameterKind] = (),
) -> dict[V, VertexSpecification[V]]:
    """Convert raw vertex specifications into structured `VertexSpecification` objects.

    This function processes a mapping of raw vertex specifications and converts
    each entry into a structured :py:class:`VertexSpecification`.

    Args:
        raw_specifications: A mapping of vertex identifiers to raw vertex
            specifications.
        kinds: A sequence of `_ParameterKind` values specifying which parameters
               should be considered as predecessors when inferring dependencies.

    Returns:
        A dictionary mapping vertex identifiers to formatted
        :py:class:`VertexSpecification` objects.
    """

    return {
        vertex: VertexSpecification.from_any(specification, kinds=kinds)
        for vertex, specification in raw_specifications.items()
    }


def format_specifications(
    raw_specifications: Mapping[V, RawVertexSpecification[V]],
    call_mode: CallMode,
) -> dict[V, VertexSpecification[V]]:
    """Convert raw vertex specifications into structured `VertexSpecification` objects
    based on a given function call mode.

    This function ensures that the correct parameter kinds are considered when
    formatting vertex specifications, based on the provided call mode.

    Args:
        raw_specifications: A mapping of vertex identifiers to raw vertex
            specifications.
        call_mode: The function call mode which determines how function arguments
            are interpreted.

    Returns:
        A dictionary mapping vertex identifiers
        to :py:class:`VertexSpecification` objects.
    """
    kinds = get_parameter_kinds(call_mode)
    return _format_specifications(raw_specifications, kinds=kinds)
