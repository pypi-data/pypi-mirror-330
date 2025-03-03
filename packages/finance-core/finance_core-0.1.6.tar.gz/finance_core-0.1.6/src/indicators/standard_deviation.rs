use pyo3::{exceptions::PyValueError, prelude::*};

use crate::traits::{Next, Period, Reset};

#[pyclass]
pub struct StandardDeviation {
    period: usize,
    index: usize,
    count: usize,
    sum: f64,
    sum_sq: f64,
    deque: Vec<f64>,
}

#[pymethods]
impl StandardDeviation {
    #[new]
    pub fn new(period: usize) -> PyResult<Self> {
        match period {
            0 => Err(PyValueError::new_err("Period cannot be 0.")),
            _ => Ok(Self {
                period,
                index: 0,
                count: 0,
                sum: 0.0,
                sum_sq: 0.0,
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

impl Period for StandardDeviation {
    fn period_rs(&self) -> usize {
        self.period
    }
}

impl Next<f64> for StandardDeviation {
    type Output = f64;

    fn next_rs(&mut self, input: f64) -> Self::Output {
        let old_value = self.deque[self.index];
        self.deque[self.index] = input;

        self.index = if self.index + 1 < self.period {
            self.index + 1
        } else {
            0
        };

        if self.count < self.period {
            self.count += 1
        };
        
        self.sum += input - old_value;
        self.sum_sq += input.powf(2.0) -  old_value.powf(2.0);

        // Calculate mean and standard deviation
        let mean = self.sum / self.count as f64;
        let variance = (self.sum_sq / self.count as f64) - (mean * mean);
        variance.sqrt() // Standard deviation
    }
}

impl Reset for StandardDeviation {
    fn reset_rs(&mut self) {
        self.index = 0;
        self.count = 0;
        self.sum = 0.0;
        self.sum_sq = 0.0;
        for i in 0..self.period {
            self.deque[i] = 0.0;
        }
    }
}
