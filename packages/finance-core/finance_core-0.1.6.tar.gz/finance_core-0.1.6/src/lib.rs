use pyo3::prelude::*;

mod traits;
pub use crate::traits::*;

mod indicators;
pub use crate::indicators::{
    AverageTrueRange,
    ExponentialMovingAverage, 
    Maximum, 
    Minimum, 
    MovingAverageConvergenceDivergence,
    RateOfChange,
    RelativeStrengthIndex,
    SharpeRatio,
    SimpleMovingAverage, 
    StandardDeviation,
    TrueRange
};

mod bar;
pub use crate::bar::Bar;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn _finance_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Bar>()?;
    m.add_class::<AverageTrueRange>()?;
    m.add_class::<ExponentialMovingAverage>()?;    
    m.add_class::<Maximum>()?;
    m.add_class::<Minimum>()?;
    m.add_class::<MovingAverageConvergenceDivergence>()?;
    m.add_class::<RateOfChange>()?;
    m.add_class::<RelativeStrengthIndex>()?;
    m.add_class::<SharpeRatio>()?;
    m.add_class::<SimpleMovingAverage>()?;
    m.add_class::<StandardDeviation>()?;
    m.add_class::<TrueRange>()?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
