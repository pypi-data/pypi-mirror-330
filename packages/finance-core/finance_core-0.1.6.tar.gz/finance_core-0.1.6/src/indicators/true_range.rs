use pyo3::prelude::*;

use crate::traits::{Next, Reset, High, Low, Close};

use crate::bar::Bar;

#[pyclass]
pub struct TrueRange {
    prev_close: Option<f64>
}

#[pymethods]
impl TrueRange {
    #[new]
    pub fn new() -> PyResult<Self> {
        Ok( Self {
            prev_close: None
            }
        )
    }

    pub fn next(&mut self, input: &Bar) -> f64 {
        Next::next_rs(self, input)
    } 

    pub fn reset(&mut self) {
        Reset::reset_rs(self)
    }
}

impl<T: High + Low + Close> Next <&T> for TrueRange {
    type Output = f64;

    fn next_rs(&mut self, input: &T) -> Self::Output {
        let max_dist = match self.prev_close {
            Some(prev_close) => {
                let dist1 = input.high_rs() - input.low_rs();
                let dist2 = (input.high_rs() - prev_close).abs();
                let dist3 = (input.low_rs() - prev_close).abs();
                dist1.max(dist2).max(dist3)
            }
            None => input.high_rs() - input.low_rs(),
        };
        self.prev_close = Some(input.close_rs());
        max_dist

    }

}

impl Reset for TrueRange {

    fn reset_rs(&mut self) {
        self.prev_close = None
    }

}