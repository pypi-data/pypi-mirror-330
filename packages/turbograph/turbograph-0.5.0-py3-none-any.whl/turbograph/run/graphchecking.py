"""Module for validating graph properties.

This module provides utility functions to check whether a given graph
meets certain structural constraints, such as being a Directed Acyclic Graph (DAG).

Note:
    This module is not yet complete and may be extended with additional
    graph validation functions in the future.
"""

from typing import Any

from ..core.graphwrapper import GraphWrapper


def _assert_dag(graph: GraphWrapper[Any, Any]) -> None:
    """Verify that the given graph is a Directed Acyclic Graph (DAG).

    Args:
        graph: The graph to validate.

    Raises:
        ValueError: If the graph contains cycles.
    """
    if not graph.is_dag():
        raise ValueError("The graph contains cycles.")


def check_graph(graph: GraphWrapper[Any, Any], dag: bool = True) -> None:
    """Perform sanity checks on the given graph.

    This function validates the structure of the graph based on the provided
    constraints.
    By default, it checks whether the graph is a Directed Acyclic Graph (DAG).

    Args:
        graph: The graph to check.
        dag: If True, verifies that the graph is a DAG. Defaults to True.

    Raises:
        ValueError: If the graph does not meet the specified constraints.
    """
    if dag:
        _assert_dag(graph)
