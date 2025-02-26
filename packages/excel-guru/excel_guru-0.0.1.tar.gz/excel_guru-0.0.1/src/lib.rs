use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn diy(arg1: &str, arg2: &str) -> String {
    let mut result = String::new();
    result.push_str("DIY: ");
    result.push_str(arg1);
    result.push_str(", ");
    result.push_str(arg2);
    result
}

/// A Python module implemented in Rust.
#[pymodule]
fn excel_guru(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(diy, m)?)?;
    Ok(())
}
