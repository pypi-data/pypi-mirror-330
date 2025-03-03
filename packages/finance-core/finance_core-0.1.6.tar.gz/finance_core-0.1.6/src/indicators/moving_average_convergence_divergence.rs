use pyo3::prelude::*;

use crate::traits::{Next, Reset};

use crate::ExponentialMovingAverage;


#[pyclass]
pub struct MovingAverageConvergenceDivergence {
    long_ema: ExponentialMovingAverage,
    short_ema: ExponentialMovingAverage,
    signal_ema: ExponentialMovingAverage,
}


#[pymethods]
impl MovingAverageConvergenceDivergence {
    #[new]
    pub fn new(
        long_period: usize, 
        short_period: usize,
        signal_period: usize,
    ) -> PyResult<Self> {
        Ok( Self {
            long_ema: ExponentialMovingAverage::new(long_period)?,
            short_ema: ExponentialMovingAverage::new(short_period)?,
            signal_ema: ExponentialMovingAverage::new(signal_period)?,
        })
    }

    pub fn next(&mut self, input: f64) -> (f64, f64, f64) {
        Next::next_rs(self, input)
    }

    pub fn reset(&mut self) {
        Reset::reset_rs(self)
    }
}

impl Next<f64> for MovingAverageConvergenceDivergence {
    type Output = (f64, f64, f64);

    fn next_rs(&mut self, input: f64) -> Self::Output {
        let long_val = self.long_ema.next_rs(input);
        let short_val = self.short_ema.next_rs(input);
        
        let macd = short_val - long_val;
        let signal = self.signal_ema.next_rs(macd);
        let histogram = macd - signal;

        (macd, signal, histogram)
        
    }

}

impl Reset for MovingAverageConvergenceDivergence {

    fn reset_rs(&mut self) {
        self.long_ema.reset_rs();
        self.short_ema.reset_rs();
        self.signal_ema.reset_rs();
    }

}
