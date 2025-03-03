import finance_core as fc


def test_init():

    tr = fc.TrueRange()

    assert isinstance(tr, fc.TrueRange)


def test_next():

    tr = fc.TrueRange()

    bar1 = fc.Bar(
        open=1.0,
        high=3.0,
        low=1.0,
        close=3.0,
        volume=0
    )

    assert tr.next(bar1) == 2.0

    bar2 = fc.Bar(
        open=2.0,
        high=6.0,
        low=2.0,
        close=6.0,
        volume=0
    )

    assert tr.next(bar2) == 4.0


def test_reset():

    tr = fc.TrueRange()

    bar1 = fc.Bar(
        open=1.0,
        high=3.0,
        low=1.0,
        close=3.0,
        volume=0
    )

    assert tr.next(bar1) == 2.0

    tr.reset()
    bar2 = fc.Bar(
        open=2.0,
        high=1.0,
        low=2.0,
        close=1.0,
        volume=0
    )

    assert tr.next(bar2) == -1.0
