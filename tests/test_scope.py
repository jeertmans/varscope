from multiprocessing import Process, Value

import pytest

from varscope import scope


def test_variable_unaccessible_outside_scope():
    with scope():
        a = 1

    with pytest.raises(UnboundLocalError):
        _ = a


def test_variables_unaccessible_outside_scope():
    a = 1
    with scope():
        b = 1
        c = a * b

    assert a == 1

    with pytest.raises(UnboundLocalError):
        _ = b

    with pytest.raises(UnboundLocalError):
        _ = c


def test_variable_unaccessible_outside_scope_after_move():
    a = 1
    with scope("a"):
        pass

    with pytest.raises(UnboundLocalError):
        _ = a


def test_variable_reassigned_inside_scope():
    a = 1
    with scope():
        a = 2

    assert a == 1


def test_variable_mutated_inside_scope():
    d = {}
    with scope():
        d["a"] = 1

    assert d["a"] == 1


def test_variable_accessible_outside_scope_with_keep():
    with scope() as s:
        a = 1
        s.keep("a")

    assert a == 1


def test_variables_accessible_outside_scope_with_keep():
    a = 1
    with scope() as s:
        a = 2
        b = 3
        s.keep("a", "b")

    assert a == 2
    assert b == 3


def test_scope_can_run_processes():
    v = Value("i", 0)
    with scope() as s:
        a = 1

        def f(x, v):
            v.value = x

        p = Process(target=f, args=(1, v))
        s.keep("p")
        p.start()

    with pytest.raises(UnboundLocalError):
        _ = a

    with pytest.raises(UnboundLocalError):
        _ = f

    p.join()

    assert v.value == 1
