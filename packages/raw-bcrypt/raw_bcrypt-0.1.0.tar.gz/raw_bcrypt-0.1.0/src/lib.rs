use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyfunction]
fn bcrypt(cost: u32, salt: &[u8], password: &[u8]) -> PyResult<Vec<u8>> {
    if salt.len() != 16 {
        return Err(PyValueError::new_err("salt length must be 16 bytes!"))
    }
    Ok(::bcrypt::bcrypt(cost, salt.try_into().unwrap(), password).to_vec())
}

/// A Python module implemented in Rust.
#[pymodule]
fn raw_bcrypt(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crate::bcrypt, m)?)?;

    Ok(())
}
