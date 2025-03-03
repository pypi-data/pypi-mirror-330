use pyo3::prelude::*;

use crate::traits::{Next, Period, Reset};

use crate::{SimpleMovingAverage, StandardDeviation};


#[pyclass]
pub struct SharpeRatio {
    er: SimpleMovingAverage,
    sd: StandardDeviation,
    rf: f64,
    count: usize,
}

#[pymethods]
impl SharpeRatio {
    #[new]
    pub fn new(period: usize, rf: f64) -> PyResult<Self> {
        Ok(Self{
            er: SimpleMovingAverage::new(period)?,
            sd: StandardDeviation::new(period)?,
            rf,
            count: 0,
        })
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

impl Period for SharpeRatio {
    fn period_rs(&self) -> usize {
        self.er.period_rs()
    }
}

impl Next<f64> for SharpeRatio {
    type Output = f64;

    fn next_rs(&mut self, input: f64) -> Self::Output {

        let er = self.er.next_rs(input);
        let sd = self.sd.next_rs(input);

        self.count += 1;

        if self.count > 1 {
            (er - self.rf) / sd
        } else {
            0.0
        }
        
    }
}

impl Reset for SharpeRatio {
    fn reset_rs(&mut self) {
        self.er.reset_rs();
        self.sd.reset_rs();
        self.count = 0;
    }
}