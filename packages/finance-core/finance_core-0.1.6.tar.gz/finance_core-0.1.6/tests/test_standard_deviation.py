import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.StandardDeviation(0)


def test_next():

    sma = fc.StandardDeviation(3)

    assert sma.next(1.0) == 0.0
    assert sma.next(2.0) == 0.5
    assert round(sma.next(3.0), 4) == 0.8165
    assert round(sma.next(4.0), 4) == 0.8165


def test_reset():

    sma = fc.StandardDeviation(3)

    assert sma.next(1.0) == 0.0

    sma.reset()
    assert sma.next(2.0) == 0.0

    sma.reset()
    assert sma.next(3.0) == 0.0
