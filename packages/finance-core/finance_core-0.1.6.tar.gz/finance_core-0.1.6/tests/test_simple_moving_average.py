import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.SimpleMovingAverage(0)


def test_next():

    sma = fc.SimpleMovingAverage(3)

    assert sma.next(1.0) == 1.0
    assert sma.next(2.0) == 1.5
    assert sma.next(3.0) == 2.0
    assert sma.next(4.0) == 3.0


def test_reset():

    sma = fc.SimpleMovingAverage(3)

    assert sma.next(1.0) == 1.0

    sma.reset()
    assert sma.next(2.0) == 2.0

    sma.reset()
    assert sma.next(3.0) == 3.0
