import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.AverageTrueRange(0)


def test_next():

    atr = fc.AverageTrueRange(3)

    bar1 = fc.Bar(open=7.0, high=10.0, low=7.0, close=9.0, volume=0)
    bar2 = fc.Bar(open=9.0, high=12.0, low=8.0, close=10.0, volume=0)
    bar3 = fc.Bar(open=10.0, high=15.0, low=9.0, close=11.0, volume=0)
    bar4 = fc.Bar(open=11.0, high=18.5, low=8.5, close=10.5, volume=0)

    assert atr.next(bar1) == 3.0
    assert atr.next(bar2) == 3.5
    assert atr.next(bar3) == 4.75
    assert atr.next(bar4) == 7.375


def test_reset():

    atr = fc.AverageTrueRange(3)

    bar1 = fc.Bar(open=7.0, high=10.0, low=7.0, close=9.0, volume=0)
    assert atr.next(bar1) == 3.0

    atr.reset()
    bar2 = fc.Bar(open=9.0, high=12.0, low=8.0, close=10.0, volume=0)
    assert atr.next(bar2) == 4.0

    atr.reset()
    bar3 = fc.Bar(open=10.0, high=15.0, low=9.0, close=11.0, volume=0)
    assert atr.next(bar3) == 6.0

    atr.reset()
    bar4 = fc.Bar(open=11.0, high=18.5, low=8.5, close=10.5, volume=0)
    assert atr.next(bar4) == 10.0
