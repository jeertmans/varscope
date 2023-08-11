class Scope:
    """
    Context manager for encapsulating variables in a scope.

    Variables that are created in a given scope will not
    be accessible outside of this scope.

    >>> from varscope import scope
    >>> a = 1
    >>> with scope():
            b = 2
    >>> a
    1
    >>> b
    NameError

    Variables that are redefined will get their original
    value back, as of when the scope was entered.

    >>> from varscope import scope
    >>> a = 1
    >>> with scope():
            a = 2
            print(a)
    2
    >>> a
    1

    Mutating an object will still keep its effects outside
    the scope.

    >>> from varscope import scope
    >>> d = {}
    >>> with scope():
            d["a"] = 1
    >>> d
    {"a": 1}
    """

    def __init__(self):
        self.initial_scope = None
        self._keep = set()

    def __enter__(self):
        self.__initial_scope = globals().copy()
        return self

    def __exit__(self, *exc):
        current_scope = globals().copy()
        initial_scope = self.__initial_scope

        for key in current_scope.keys():
            if key in self._keep:
                continue
            if value := initial_scope.get(key, None):
                globals()[key] = value
            else:
                del globals()[key]

    def keep(self, *objects: object) -> None:
        """
        Tells the context manager to keep specific objects
        after the scope was exited.

        >>> from varscope import scope
        >>> with scope() as s:
                a = 1
                b = 2
                s.keep(a)
        >>> a
        1
        >>> b
        NameError
        """
        self._keep.update(obj.__name__ for obj in objects)


def scope() -> Scope:
    """
    Returns a context manager to encaplusate all the
    variables, making them inaccessible afterward.
    """
    return Scope()
