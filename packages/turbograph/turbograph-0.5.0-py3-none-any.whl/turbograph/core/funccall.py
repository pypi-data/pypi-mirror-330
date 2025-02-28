"""This module defines function call modes and a utility function for invoking
functions with different input-passing strategies.

Call modes determine how input values are passed to a function:
- ``"args"``: Positional arguments (e.g., ``func(a, b, c)``).
- ``"kwargs"``: Keyword arguments (e.g., ``func(a=a, b=b, c=c)``).
- ``"arg"``: A single dictionary argument (e.g., ``func({"a": a, "b": b, "c": c})``).
"""

from typing import Any, Callable, Literal, TypeVar

CallMode = Literal["args", "kwargs", "arg"]
"""Enumeration of valid call modes for function execution."""

CALL_MODES: set[CallMode] = {"args", "kwargs", "arg"}
"""Tuple of valid function call modes."""

DEFAULT_CALL_MODE: Literal["args"] = "args"
"""The default function call mode."""

Out = TypeVar("Out")
"""Generic output type for function return values."""


def call_func(
    func: Callable[..., Out],
    inputs: dict[Any, Any],
    call_mode: CallMode = DEFAULT_CALL_MODE,
) -> Out:
    r"""Invoke a function with dynamically passed inputs based on the specified call
    mode.

    Args:
        func: The function to invoke.
        inputs: A dictionary mapping input names to their values.
        call_mode: The input passing strategy.

            - `"args"` (default): Pass input values as positional arguments.
            - `"kwargs"`: Pass input values as keyword arguments.
            - `"arg"`: Pass all inputs as a single dictionary argument.

    Returns:
        The output of the function.

    Raises:
        ValueError: If an invalid call mode is provided.

    Example:
        Using different call modes with the same function:

        >>> def example_func(a, b, c):
        ...     return a + b + c
        >>> inputs = {"a": 1, "b": 2, "c": 3}

        Call with positional arguments:
        >>> call_func(example_func, inputs, call_mode="args")
        6

        Call with keyword arguments:
        >>> call_func(example_func, inputs, call_mode="kwargs")
        6

        Call with a single dictionary argument:
        >>> def dict_func(data):
        ...     return sum(data.values())
        >>> call_func(dict_func, inputs, call_mode="arg")
        6
    """
    if call_mode == "args":
        return func(*inputs.values())
    elif call_mode == "kwargs":
        return func(**inputs)  # type: ignore[arg-type]
    elif call_mode == "arg":
        return func(inputs)
    else:
        raise ValueError(
            f"Invalid call mode: {call_mode!r}. "
            "Valid call modes are: " + ", ".join(map(repr, CALL_MODES))
        )
