"""
VarScope's IPython Magic
========================

.. toctree::
    :hidden:

    magic_example

IPython magic, automatically registered with importing ``varscope`` in a Notebook.
"""

import argparse
from typing import Any, Dict

from IPython.core.magic import needs_local_scope, register_cell_magic

parser = argparse.ArgumentParser(
    prog="scope", description="Create per-cell scopes", add_help=False
)

parser.add_argument("--move", metavar="NAME", default=[], nargs="+")
parser.add_argument("--keep", metavar="NAME", default=[], nargs="+")


@needs_local_scope
@register_cell_magic
def scope(line: str, cell: str, local_ns: Dict[str, Any]):
    """
    Magic to create a scope for a given cell.

    Equivalent to wrapping the whole cell with some:

    .. code-block:: python

        with scope():
            # cell content

    Usage: ``%%scope [--move NAME [NAME ...]]  [--keep NAME [NAME ...]]``

    where you can optionally specify some variable names to move inside the
    scope, and some to keep after the scope was exited.
    """
    initial_scope = local_ns.copy()
    exec(cell, local_ns)
    current_scope = local_ns.copy()

    if line := line.strip():
        args = parser.parse_args(line.strip().split(" "))
        delete = set(args.move)
        keep = set(args.keep)
    else:
        delete = set()
        keep = set()

    for key in current_scope.keys():
        if key in keep:
            continue
        elif key in initial_scope:
            local_ns[key] = initial_scope[key]
        else:
            local_ns.pop(key)

    for key in delete:
        if key not in keep:
            local_ns.pop(key)
