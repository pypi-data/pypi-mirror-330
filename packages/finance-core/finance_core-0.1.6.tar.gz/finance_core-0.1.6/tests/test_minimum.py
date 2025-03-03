import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.Minimum(0)


def test_next():

    min = fc.Minimum(3)

    assert min.next(4.0) == 4.0
    assert min.next(3.0) == 3.0
    assert min.next(2.0) == 2.0
    assert min.next(5.0) == 2.0


def test_reset():

    min = fc.Minimum(3)

    assert min.next(3.0) == 3.0

    min.reset()
    assert min.next(4.0) == 4.0

    min.reset()
    assert min.next(5.0) == 5.0
