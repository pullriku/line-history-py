use pyo3::exceptions::PyOSError;
use pyo3::prelude::*;

#[pyclass]
pub struct LineContent {
    #[pyo3(get)]
    date: chrono::NaiveDate,
    #[pyo3(get)]
    line_count: usize,
    #[pyo3(get)]
    line: String,
}

#[pymethods]
impl LineContent {
    #[new]
    fn new(date: chrono::NaiveDate, line_count: usize, line: String) -> Self {
        Self {
            date,
            line_count,
            line,
        }
    }
}

impl From<::line_history::line_content::LineContent> for LineContent {
    fn from(line_content: ::line_history::line_content::LineContent) -> Self {
        let ::line_history::line_content::LineContent {
            date,
            line_count,
            line,
        } = line_content;
        Self {
            date,
            line_count,
            line,
        }
    }
}

#[pyclass]
struct History {
    history: ::line_history::history::History,
}

#[pymethods]
impl History {
    #[new]
    fn new(data: &str) -> Self {
        Self {
            history: ::line_history::history::History::new(data),
        }
    }

    #[staticmethod]
    fn read_from_file(path: &str) -> PyResult<Self> {
        let Ok(history) = ::line_history::history::History::read_from_file(path) else {
            return Err(PyOSError::new_err("Failed to read from file"));
        };

        Ok(Self { history })
    }

    #[staticmethod]
    fn from_lines(lines: Vec<String>) -> Self {
        let result = ::line_history::history::History::from_lines(lines);
        Self { history: result }
    }

    fn len(&self) -> usize {
        self.history.len()
    }

    fn is_empty(&self) -> bool {
        self.history.is_empty()
    }

    fn search_by_date(&self, date: chrono::NaiveDate) -> PyResult<Option<String>> {
        let result = self.history.search_by_date(&date);
        Ok(result)
    }

    fn search_by_keyword(&self, keyword: &str) -> PyResult<Vec<LineContent>> {
        let result = self
            .history
            .search_by_keyword(keyword)
            .into_iter()
            .map(|line_content| line_content.into())
            .collect();

        Ok(result)
    }

    fn search_by_random(&self) -> PyResult<String> {
        let result = self.history.search_by_random();
        Ok(result)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn line_history(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<LineContent>()?;
    m.add_class::<History>()?;
    Ok(())
}
