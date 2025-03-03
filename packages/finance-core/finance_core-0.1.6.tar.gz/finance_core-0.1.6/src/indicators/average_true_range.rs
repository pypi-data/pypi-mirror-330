use pyo3::prelude::*;

use crate::traits::{Next, Period, Reset, High, Low, Close};

use crate::{Bar, TrueRange, ExponentialMovingAverage};

#[pyclass]
pub struct AverageTrueRange {
    tr: TrueRange,
    ema: ExponentialMovingAverage
}

#[pymethods]
impl AverageTrueRange {
    #[new]
    pub fn new(period: usize) -> PyResult<Self> {
        Ok(Self {
            tr: TrueRange::new()?,
            ema: ExponentialMovingAverage::new(period)?,
        })
    }

    pub fn period(&mut self) -> usize {
        Period::period_rs(self)
    }

    pub fn next(&mut self, input: &Bar) -> f64 {
        Next::next_rs(self, input)
    }

    pub fn reset(&mut self) {
        Reset::reset_rs(self)
    }
}

impl Period for AverageTrueRange {

    fn period_rs(&self) -> usize {
        self.ema.period_rs()
    }
}

impl<T: High + Low + Close> Next <&T> for AverageTrueRange {
    type Output = f64;

    fn next_rs(&mut self, input: &T) -> Self::Output {
        self.ema.next_rs(self.tr.next_rs(input))
    }

}

impl Reset for AverageTrueRange {

    fn reset_rs(&mut self) {
        self.ema.reset_rs();
    }
}