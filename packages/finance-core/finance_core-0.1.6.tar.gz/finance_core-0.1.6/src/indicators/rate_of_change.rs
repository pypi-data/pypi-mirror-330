use pyo3::{exceptions::PyValueError, prelude::*};

use crate::traits::{Next, Period, Reset};

#[pyclass]
pub struct RateOfChange {
    period: usize,
    index: usize,
    count: usize,
    deque: Vec<f64>,
}

#[pymethods]
impl RateOfChange {
    #[new]
    pub fn new(period: usize) -> PyResult<Self> {
        match period {
            0 => Err(PyValueError::new_err("Period cannot be 0.")),
            _ => Ok(Self {
                period,
                index: 0,
                count: 0,
                deque: vec![0.0; period],
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

impl Period for RateOfChange {
    fn period_rs(&self) -> usize {
        self.period
    }
}

impl Next<f64> for RateOfChange {
    type Output = f64;

    fn next_rs(&mut self, input: f64) -> Self::Output {
        let previous = if self.count > self.period {
            self.deque[self.index]
        } else {
            self.count += 1;
            if self.count == 1 {
                input
            } else {
                self.deque[0]
            }
        };
        self.deque[self.index] = input;

        self.index = if self.index + 1 < self.period {
            self.index + 1
        } else {
            0
        };

        (input - previous) / previous
    }
}

impl Reset for RateOfChange {
    fn reset_rs(&mut self) {
        self.index = 0;
        self.count = 0;
        for i in 0..self.period {
            self.deque[i] = 0.0;
        }
    }
}
