use pyo3::prelude::*;
use selectic::SelectionError;

/// Get the currently selected text
#[pyfunction]
fn get_text() -> PyResult<String> {
    match selectic::get_text() {
        Ok(text) => Ok(text),
        Err(err) => Err(map_error(err)),
    }
}

// Map Rust errors to Python exceptions
fn map_error(err: SelectionError) -> PyErr {
    match err {
        SelectionError::UnsupportedPlatform => {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Platform not supported")
        }
        SelectionError::InvalidContentType { expected, received } => {
            PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                "Invalid content type: expected {}, received {}",
                expected, received
            ))
        }
        SelectionError::NoFocusedElement => {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("No focused UI element found")
        }
        SelectionError::NoSelectedContent => PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "No selected content in focused element",
        ),
        SelectionError::AppleScriptError(msg) => {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("AppleScript error: {}", msg))
        }
        SelectionError::AccessibilityError(msg) => {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                "Accessibility API error: {}",
                msg
            ))
        }
        SelectionError::ClipboardError(msg) => {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Clipboard error: {}", msg))
        }
        SelectionError::IoError(err) => {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("IO error: {}", err))
        }
        SelectionError::Utf8Error(err) => PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            format!("UTF-8 conversion error: {}", err),
        ),
        SelectionError::Other(msg) => {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Selection error: {}", msg))
        }
    }
}

#[pymodule]
fn selectic_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_text, _py)?)?;
    Ok(())
}
