"""
A simple Python library for creating local scopes.

This module consist of a single function
:func:`scope` that creates :class:`Scope` context manager, to be used
with Python's :code:`with` statement:

.. code:: python

    # Scope A

    with scope():
        # Scope B (includes A)

    # Scope A

Scroll below for usage examples.
"""


import ctypes
import inspect
from typing import Set


class Scope:
    """
    Context manager for encapsulating variables in a scope.

    See :func:`scope` for a detailed description.

    References
    ----------

    https://pydev.blogspot.com/2014/02/changing-locals-of-frame-frameflocals.html
    """

    def __init__(self, *names: str) -> None:
        self._delete: Set[str] = set(*names)
        self._keep: Set[str] = set()

    def __enter__(self) -> "Scope":
        self.__initial_scope = inspect.currentframe().f_back.f_locals.copy()  # type: ignore[union-attr]
        return self

    def __exit__(self, *exc) -> None:
        current_frame = inspect.currentframe().f_back  # type: ignore[union-attr]
        current_scope = current_frame.f_locals.copy()  # type: ignore[union-attr]
        initial_scope = self.__initial_scope

        f_locals = current_frame.f_locals  # type: ignore[union-attr]

        for key in current_scope.keys():
            if key in self._keep:
                continue
            elif key in initial_scope:
                f_locals[key] = initial_scope[key]  # type: ignore[union-attr]
            else:
                f_locals.pop(key)  # type: ignore[union-attr]

        for key in self._delete:
            if key not in self._keep:
                f_locals.pop(key)  # type: ignore[union-attr]

        ctypes.pythonapi.PyFrame_LocalsToFast(
            ctypes.py_object(current_frame), ctypes.c_int(1)
        )

        del current_frame

    def keep(self, *names: str) -> None:
        """
        Tells the context manager to keep specific variable names
        after the scope was exited.

        :param names: Variable names to be moved outside the scope.

        Examples
        --------

        >>> from varscope import scope
        >>> with scope() as s:
        ...     a = 1
        ...     b = 2
        ...     s.keep("a")
        ...
        >>> a
        1
        >>> b
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        NameError: name 'b' is not defined
        """
        self._keep.update(names)


def scope(*names: str) -> Scope:
    """
    Returns a context manager to encapsulate all the
    variables, making them inaccessible afterward.

    Variables that are created in a given scope will not
    be accessible outside of this scope.

    Optionally, you can specify variable names from outside the scope
    that must be moved inside. Upon exiting the scope, they will be deleted.

    :param names: Variable names to be moved inside the scope,
        as they were defined there.

    Examples
    --------

    >>> from varscope import scope
    >>> a = 1
    >>> with scope():
    ...     b = 2
    ...
    >>> a
    1
    >>> b
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'b' is not defined

    Variables that are redefined will get their original
    value back, as of when the scope was entered.

    >>> from varscope import scope
    >>> a = 1
    >>> with scope():
    ...     a = 2
    ...     print(a)
    2
    >>> a
    1

    Mutating an object will still keep its effects outside
    the scope.

    >>> from varscope import scope
    >>> d = {}
    >>> with scope():
    ...     d["a"] = 1
    ...
    >>> d
    {'a': 1}

    You can also specify variables (by name) that must be moved
    inside the scope, and deleted afterward.

    >>> from varscope import scope
    >>> a = 1
    >>> with scope("a"):
    ...     print(a)
    ...
    1
    >>> a
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'a' is not defined
    """
    return Scope(*names)
