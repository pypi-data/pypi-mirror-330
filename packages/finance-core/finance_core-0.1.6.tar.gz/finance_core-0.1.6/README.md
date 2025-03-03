# Finance core

Financial indicators implemented in Rust with a Python interface.

## Install
```bash
pip install finance_core
```

## Example usage
```python
import finance_core as fc


max_three_days = fc.Maximum(3)

print(max_three_days.next(1)) # >> 1
print(max_three_days.next(4)) # >> 4
print(max_three_days.next(2)) # >> 4
print(max_three_days.next(5)) # >> 5


min_three_days = fc.Minimum(3)

print(min_three_days.next(1)) # >> 1
print(min_three_days.next(4)) # >> 1
print(min_three_days.next(2)) # >> 1
print(min_three_days.next(5)) # >> 2


sma_three_days = fc.SimpleMovingAverage(3)

print(sma_three_days.next(1)) # >> 1
print(sma_three_days.next(4)) # >> 2.5
print(sma_three_days.next(2)) # >> 2.33
print(sma_three_days.next(5)) # >> 3.66
```

## Indicators

- Averge true range (ATR)
- Exponential moving average (EMA)
- Maximum
- Minimum
- Moving average convergence/divergence (MACD)
- Rate of change (ROC)
- Relative strength index (RSI)
- Sharpe ratio (SR)
- Simple moving average (SMA)
- Standard deviation, population (SD)
- True range (TR)

## Data classes

- Bar (open, high, low, close, volume)

## Contribute

Install Docker and open this repo in DevContainer.

```bash
# create virtual environment
python -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

Useful commands:
- `make build-dev` to build the package during development
- `make build-prod` to perform an optimised build for benchmarking