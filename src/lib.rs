mod document;
mod iterator;

use pyo3::prelude::*;

use document::{decode, encode, ReliableTxtDocument};
use iterator::ReliableTxtCharIterator;

#[pymodule]
fn _reliabletxt(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encode, m)?)?;
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    m.add_class::<ReliableTxtDocument>()?;
    m.add_class::<ReliableTxtCharIterator>()?;
    Ok(())
}
