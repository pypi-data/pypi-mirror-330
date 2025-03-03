import finance_core as fc
import pytest


def test_init():

    with pytest.raises(ValueError, match="Period cannot be 0."):
        fc.Maximum(0)


def test_next():

    max = fc.Maximum(3)

    assert max.next(5.0) == 5.0
    assert max.next(2.0) == 5.0
    assert max.next(3.0) == 5.0
    assert max.next(4.0) == 4.0


def test_reset():

    max = fc.Maximum(3)

    assert max.next(5.0) == 5.0

    max.reset()
    assert max.next(4.0) == 4.0

    max.reset()
    assert max.next(3.0) == 3.0
