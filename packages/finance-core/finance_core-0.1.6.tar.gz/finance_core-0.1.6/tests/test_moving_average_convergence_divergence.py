import finance_core as fc
import pytest


def _round(nums: tuple[float, float, float]) -> tuple[float, float, float]:
    """Round to four digits."""
    n0 = round(nums[0], 4)
    n1 = round(nums[1], 4)
    n2 = round(nums[2], 4)
    return (n0, n1, n2)


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.MovingAverageConvergenceDivergence(0, 12, 9)

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.MovingAverageConvergenceDivergence(26, 0, 9)

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.MovingAverageConvergenceDivergence(26, 12, 0)


def test_next():

    macd = fc.MovingAverageConvergenceDivergence(26, 12, 9)

    assert macd.next(3.0) == (0.0, 0.0, 0.0)
    assert _round(macd.next(4.0)) == (0.0798, 0.016, 0.0638)
    assert _round(macd.next(5.0)) == (0.2211, 0.0570, 0.1641)
    assert _round(macd.next(6.0)) == (0.4091, 0.1274, 0.2817)


def test_reset():

    macd = fc.MovingAverageConvergenceDivergence(26, 12, 9)

    assert _round(macd.next(3.0)) == (0.0, 0.0, 0.0)
    assert _round(macd.next(4.0)) == (0.0798, 0.016, 0.0638)

    macd.reset()
    assert _round(macd.next(3.0)) == (0.0, 0.0, 0.0)
    assert _round(macd.next(4.0)) == (0.0798, 0.016, 0.0638)

    macd.reset()
    assert _round(macd.next(3.0)) == (0.0, 0.0, 0.0)
    assert _round(macd.next(4.0)) == (0.0798, 0.016, 0.0638)
