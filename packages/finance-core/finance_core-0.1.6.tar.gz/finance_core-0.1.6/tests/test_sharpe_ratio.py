import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.SharpeRatio(0, 0.01)


def test_next():

    sr = fc.SharpeRatio(3, 0.01)

    assert sr.next(1.0) == 0.0
    assert sr.next(0.5) == 2.96
    assert round(sr.next(0.33), 4) == 2.1099
    assert round(sr.next(0.25), 4) == 3.3575


def test_reset():

    sr = fc.SharpeRatio(3, 0.01)

    assert sr.next(1.0) == 0.0

    sr.reset()
    assert sr.next(2.0) == 0.0

    sr.reset()
    assert sr.next(3.0) == 0.0
