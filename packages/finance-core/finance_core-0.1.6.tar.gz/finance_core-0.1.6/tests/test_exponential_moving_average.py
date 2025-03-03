import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.ExponentialMovingAverage(0)


def test_next():

    ema = fc.ExponentialMovingAverage(3)

    assert ema.next(2.0) == 2.0
    assert ema.next(5.0) == 3.5
    assert ema.next(7.0) == 5.25
    assert ema.next(6.0) == 5.625


def test_reset():

    ema = fc.ExponentialMovingAverage(3)

    assert ema.next(2.0) == 2.0
    assert ema.next(5.0) == 3.5
    assert ema.next(7.0) == 5.25
    assert ema.next(6.0) == 5.625

    ema.reset()
    assert ema.next(2.0) == 2.0

    ema.reset()
    assert ema.next(4.0) == 4.0
