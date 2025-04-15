fn main() -> pyo3_stub_gen::Result<()> {
    let stub = ::line_history_py::stub_info()?;
    stub.generate()?;
    Ok(())
}
