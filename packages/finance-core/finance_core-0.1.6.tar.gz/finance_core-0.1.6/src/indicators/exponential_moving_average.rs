use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

use crate::traits::{Next, Period, Reset};


#[pyclass]
pub struct ExponentialMovingAverage {
    period: usize,
    s: f64,
    current: f64,
    is_new: bool,
}

#[pymethods]
impl ExponentialMovingAverage {
    #[new]
    pub fn new(period: usize) -> PyResult<Self> {
        match period {
            0 => Err(PyValueError::new_err("Period cannot be 0.")),
            _ => Ok(Self {
                period,
                s: 2.0 / (1 + period) as f64,
                current: 0.0,
                is_new: true,
            })
        }
    }

    pub fn period(&mut self) -> usize {
        Period::period_rs(self)
    }

    pub fn next(&mut self, input: f64) -> f64 {
        Next::next_rs(self, input)
    }

    pub fn reset(&mut self) {
        Reset::reset_rs(self)
    }
}

impl Period for ExponentialMovingAverage {
    fn period_rs(&self) -> usize {
        self.period
    }
}

impl Next<f64> for ExponentialMovingAverage {
    type Output = f64;

    fn next_rs(&mut self, input: f64) -> Self::Output {
        if self.is_new {
            self.is_new = false;
            self.current = input;
        } else {
            self.current = input * self.s + self.current * (1.0 - self.s)
        }

        return self.current;
    }
}

impl Reset for ExponentialMovingAverage {
    fn reset_rs(&mut self) {
        self.current = 0.0;
        self.is_new = true;
    }
}
