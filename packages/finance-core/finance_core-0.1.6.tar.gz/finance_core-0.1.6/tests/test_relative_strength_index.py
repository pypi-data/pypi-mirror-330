import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.RelativeStrengthIndex(0)


def test_next():

    rsi = fc.RelativeStrengthIndex(3)

    assert rsi.next(1.0) == 100.0
    assert round(rsi.next(0.5), 4) == 66.6667
    assert round(rsi.next(2.0), 4) == 83.3333
    assert round(rsi.next(1.5), 4) == 60


def test_reset():

    rsi = fc.RelativeStrengthIndex(3)

    assert rsi.next(1.0) == 100.0
    assert round(rsi.next(0.5), 4) == 66.6667

    rsi.reset()
    assert rsi.next(1.0) == 100.0
    assert round(rsi.next(0.5), 4) == 66.6667
