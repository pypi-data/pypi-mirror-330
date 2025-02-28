"""TurboGraph is a simple Python library, for defining and computing values based
on dependencies.
It automatically builds a dependency graph from function argument names
or explicit specifications, ensuring computations run in the correct order.

Here's a simple example showing how TurboGraph automatically infers dependencies:

.. code-block:: python

    from turbograph import compute

    specifications = {
        "a": 2,
        "sum": lambda a, b: a + b,  # Depends on "a" and "b"
    }

    result = compute(specifications, ["sum"], {"b": 3})
    print(result)  # {"sum": 5}


TurboGraph analyzes the function signatures and determines that ``"sum"`` depends
on ``"a"`` and ``"b"``, executing the computations in the correct order.
"""

from .core.specification import NA
from .run.graphbuilding import build_graph
from .run.graphupdating import rebuild_graph
from .run.graphcomputing import compute_from_graph
from .run.computing import compute

__all__ = ["compute", "build_graph", "compute_from_graph", "NA", "rebuild_graph"]

__version__ = "0.5.0"
