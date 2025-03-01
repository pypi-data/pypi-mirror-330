"""
Factory module for selecting and managing graph backends.

This module provides functions to:
- Check the availability of graph backends (``networkx`` and ``igraph``).
- Automatically determine the best available backend.
- Retrieve the appropriate backend wrapper class for graph operations.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Type

if TYPE_CHECKING:  # pragma: no cover
    from .igraph_backend import IGraphWrapper
    from .networkx_backend import NetworkXWrapper

Backend = Literal["networkx", "igraph"]
"""Enumeration of supported graph backends."""

BACKENDS: tuple[Backend, ...] = ("networkx", "igraph")
"""Tuple of available graph backends.

The first available backend is selected as the default unless explicitly specified.
"""

backend_to_module: dict[Backend, str] = {
    "igraph": "igraph",
    "networkx": "networkx",
}
"""Mapping of backend names to their corresponding module names.

This mapping is used to dynamically check the availability of backend libraries.
"""


def _is_available(backend: Backend) -> bool:
    r"""Check if the specified backend is installed and available for use.

    Args:
        backend: The name of the backend (``"igraph"`` or ``"networkx"``).

    Returns:
        True if the backend's Python package is installed, False otherwise.

    Raises:
        ValueError: If an unrecognized backend name is provided.

    Example:
        >>> _is_available("igraph")
        True  # If 'igraph' is installed
    """
    import importlib.util

    try:
        module_name = backend_to_module[backend]
    except KeyError:
        raise ValueError(
            f"Backend {backend!r} is not recognized. "
            "Valid backends are: " + ", ".join(backend_to_module.keys())
        )

    return importlib.util.find_spec(module_name) is not None


def get_backend_auto() -> Backend:
    """Automatically select the best available graph backend.

    Returns:
        The first available backend from the predefined list (:py:data:`BACKENDS`).

    Raises:
        ImportError: If no supported backend is installed.

    Example:
        >>> get_backend_auto()
        'networkx'  # If 'networkx' is installed
    """
    for backend in BACKENDS:
        if _is_available(backend):
            return backend

    raise ImportError(
        "No available graph backend. "
        "Please install either 'networkx' or 'igraph' library."
    )


def get_graph_backend(
    backend: Literal["igraph", "networkx"] | None = None,
) -> Type[NetworkXWrapper | IGraphWrapper]:
    """Retrieve the appropriate backend wrapper class for graph operations.

    Args:
        backend: The backend to use. If `None`, the best available backend is
            selected automatically using :py:func:`get_backend_auto`.

    Returns:
        The backend wrapper class.

    Raises:
        ValueError: If an unrecognized backend name is provided.
        ImportError: If no supported backend is installed.
    """
    if backend is None:
        backend = get_backend_auto()

    if backend == "igraph":
        from .igraph_backend import IGraphWrapper

        return IGraphWrapper
    elif backend == "networkx":
        from .networkx_backend import NetworkXWrapper

        return NetworkXWrapper
    else:
        raise ValueError(f"Backend {backend!r} is not recognized.")
