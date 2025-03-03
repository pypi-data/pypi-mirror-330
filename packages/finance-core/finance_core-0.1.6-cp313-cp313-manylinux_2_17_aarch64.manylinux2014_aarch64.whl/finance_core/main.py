import finance_core as fc


max = fc.Maximum(3)

print(max.next(1))
print(max.next(4))
print(max.next(2))
print(max.next(5))


min = fc.Minimum(3)

print(min.next(1))
print(min.next(4))
print(min.next(2))
print(min.next(5))


sma = fc.SimpleMovingAverage(3)

print(sma.next(1))
print(sma.next(4))
print(sma.next(2))
print(sma.next(5))

macd = fc.MovingAverageConvergenceDivergence(26, 12, 9)

print(macd.next(1))
print(macd.next(4))
print(macd.next(2))
print(macd.next(5))
