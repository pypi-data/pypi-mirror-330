import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.RateOfChange(0)


def test_next():

    roc = fc.RateOfChange(3)

    assert roc.next(4.0) == 0.0
    assert roc.next(5.0) == 0.25
    assert roc.next(6.0) == 0.5
    assert roc.next(7.0) == 0.75


def test_reset():

    roc = fc.RateOfChange(3)

    assert roc.next(3.0) == 0.0

    roc.reset()
    assert roc.next(4.0) == 0.0

    roc.reset()
    assert roc.next(5.0) == 0.0
