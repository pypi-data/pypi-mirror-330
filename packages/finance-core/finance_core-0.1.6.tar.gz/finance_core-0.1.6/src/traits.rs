pub trait Reset {
    fn reset_rs(&mut self);
}

pub trait Period {
    fn period_rs(&self) -> usize;
}

pub trait Next<T> {
    type Output;
    fn next_rs(&mut self, input: T) -> Self::Output;
}

pub trait Open {
    fn open_rs(&self) -> f64;
}

pub trait High {
    fn high_rs(&self) -> f64;
}

pub trait Low {
    fn low_rs(&self) -> f64;
}

pub trait Close {
    fn close_rs(&self) -> f64;
}

pub trait Volume {
    fn volume_rs(&self) -> usize;
}