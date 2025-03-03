use pyo3::{exceptions::PyValueError, prelude::*};

use crate::traits::{Next, Period, Reset};

#[pyclass]
pub struct RelativeStrengthIndex {
    period: usize,
    index: usize,
    count: usize,
    prev_val: f64,
    deque: Vec<f64>,
}

#[pymethods]
impl RelativeStrengthIndex {
    #[new]
    pub fn new(period: usize) -> PyResult<Self> {
        match period {
            0 => Err(PyValueError::new_err("Period cannot be 0.")),
            _ => Ok(Self {
                period,
                index: 0,
                count: 0,
                prev_val: 0.0,
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
        Reset::reset_rs(self);
    }
}

impl Period for RelativeStrengthIndex {
    fn period_rs(&self) -> usize {
        self.period
    }
}

impl Next<f64> for RelativeStrengthIndex {
    type Output = f64;

    fn next_rs(&mut self, input: f64) -> Self::Output {

        let ret = input - self.prev_val;
        self.prev_val = input;

        self.deque[self.index] = ret;

        self.index = if self.index + 1 < self.period {
            self.index + 1
        } else {
            0
        };

        if self.count < self.period {
            self.count += 1
        }

        let (total_gain, total_loss) = self.deque
            .iter()
            .fold((0.0, 0.0), |(gain_sum, loss_sum), &value | {
                if value > 0.0 {
                    (gain_sum + value, loss_sum)
                } else {
                    (gain_sum, loss_sum - value)
                }
            });

        let average_gain = total_gain / self.count as f64;
        let average_loss = total_loss / self.count as f64;

        let rs = average_gain / average_loss;


        100.0 - (100.0 / (1.0 + rs))
    

    }

}

impl Reset for RelativeStrengthIndex {
    fn reset_rs(&mut self) {
        self.index = 0;
        self.count = 0;
        self.prev_val = 0.0;
        for i in 0..self.period {
            self.deque[i] = 0.0
        }
    }
}