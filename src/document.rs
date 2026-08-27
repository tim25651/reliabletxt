use std::fs;
use std::path::PathBuf;

use pyo3::exceptions::{PyUnicodeDecodeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyBytes;

const BOM: char = '\u{feff}';

/// Encodes text as UTF-8 bytes.
#[pyfunction]
pub fn encode<'py>(py: Python<'py>, text: &str) -> Bound<'py, PyBytes> {
    PyBytes::new(py, text.as_bytes())
}

/// Decodes UTF-8 bytes into text, stripping a leading BOM if present.
///
/// # Errors
///
/// Returns `Err` if content is not valid UTF-8.
#[pyfunction]
pub fn decode(py: Python<'_>, content: &[u8]) -> PyResult<String> {
    match std::str::from_utf8(content) {
        Ok(text) => Ok(text.strip_prefix(BOM).unwrap_or(text).to_string()),
        Err(err) => Err(PyUnicodeDecodeError::new_utf8(py, content, err)?.into()),
    }
}

/// Manages the text content of a ReliableTXT document.
#[pyclass]
pub struct ReliableTxtDocument {
    text: String,
    read_only: bool,
}

#[pymethods]
impl ReliableTxtDocument {
    #[new]
    #[pyo3(signature = (text=String::new(), read_only=false))]
    fn new(text: String, read_only: bool) -> Self {
        Self { text, read_only }
    }

    #[getter]
    fn read_only(&self) -> bool {
        self.read_only
    }

    #[getter]
    fn text(&self) -> &str {
        &self.text
    }

    #[setter]
    fn set_text(&mut self, text: String) -> PyResult<()> {
        if self.read_only {
            return Err(PyValueError::new_err("The document is read-only"));
        }
        self.text = text;
        Ok(())
    }

    #[getter]
    fn content<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        encode(py, &self.text)
    }

    /// Writes the text as UTF-8 to `file_path`, without a BOM.
    fn save(&self, file_path: PathBuf) -> PyResult<()> {
        fs::write(file_path, &self.text)?;
        Ok(())
    }

    /// Loads a document from `file_path`, stripping a leading BOM if present.
    ///
    /// # Errors
    ///
    /// Returns `Err` if the file content is not valid UTF-8.
    #[staticmethod]
    fn load(py: Python<'_>, file_path: PathBuf) -> PyResult<Self> {
        let content = fs::read(file_path)?;
        let text = decode(py, &content)?;
        Ok(Self { text, read_only: false })
    }
}
