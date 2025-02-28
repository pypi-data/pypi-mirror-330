use pyo3::prelude::*;

mod board;

#[pyfunction]
fn hello_world() {
    println!("Hello World!");
}

#[pymodule(name="rspy_chess")]
fn rspy_chess(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<board::Board>()?;
    m.add_class::<board::Move>()?;
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    Ok(())
}