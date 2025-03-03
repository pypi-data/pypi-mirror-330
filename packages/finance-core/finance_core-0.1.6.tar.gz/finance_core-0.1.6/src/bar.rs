use pyo3::prelude::*;

use crate::traits::{Open, High, Low, Close, Volume};

#[pyclass]
pub struct Bar {
    open: f64,
    high: f64,
    low: f64,
    close: f64,
    volume: usize
}

#[pymethods]
impl Bar {
    #[new]
    pub fn new(
        open: f64,
        high: f64,
        low: f64,
        close: f64,
        volume: usize
    ) -> PyResult<Self> {
        Ok( Self {
            open,
            high,
            low,
            close,
            volume,
        })
    }

    pub fn open(&self) -> f64 {
        Open::open_rs(self)
    }

    pub fn high(&self) -> f64 {
        High::high_rs(self)
    }

    pub fn low(&self) -> f64 {
        Low::low_rs(self)
    }

    pub fn close(&self) -> f64 {
        Close::close_rs(self)
    }

    pub fn volume(&self) -> usize {
        Volume::volume_rs(self)
    }
}

impl Open for Bar {
    fn open_rs(&self) -> f64 {
        self.open
    }
}

impl High for Bar {
    fn high_rs(&self) -> f64 {
        self.high
    }
}

impl Low for Bar {
    fn low_rs(&self) -> f64 {
        self.low
    }
}

impl Close for Bar {
    fn close_rs(&self) -> f64 {
        self.close
    }
}

impl Volume for Bar {
    fn volume_rs(&self) -> usize {
        self.volume
    }
}