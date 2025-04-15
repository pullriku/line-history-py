fn main() -> pyo3_stub_gen::Result<()> {
    let stub = ::line_history::stub_info()?;
    stub.generate()?;
    Ok(())
}
