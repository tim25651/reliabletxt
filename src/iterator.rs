use pyo3::prelude::*;

const NEW_LINE: char = '\n';

/// Manages a cursor position while walking the characters of a ReliableTXT document.
#[pyclass]
pub struct ReliableTxtCharIterator {
    chars: Vec<char>,
    ix: usize,
}

#[pymethods]
impl ReliableTxtCharIterator {
    #[new]
    fn new(text: &str) -> Self {
        Self { chars: text.chars().collect(), ix: 0 }
    }

    #[getter]
    fn ix(&self) -> usize {
        self.ix
    }

    /// Advances the cursor by one character.
    fn forward(&mut self) {
        self.ix += 1;
    }

    /// Returns the zero-based line index and column of the cursor.
    fn get_line_info(&self) -> (usize, usize) {
        let mut line_ix = 0;
        let mut line_position = 0;
        for &c in &self.chars[..self.ix] {
            if c == NEW_LINE {
                line_ix += 1;
                line_position = 0;
            } else {
                line_position += 1;
            }
        }
        (line_ix, line_position)
    }

    /// Whether the cursor is at the end of the text.
    fn is_eof(&self) -> bool {
        self.ix >= self.chars.len()
    }

    /// Whether the character at the cursor is `c`.
    fn is_char(&self, c: char) -> bool {
        !self.is_eof() && self.chars[self.ix] == c
    }

    /// Whether the character at the cursor is `c`, advancing the cursor if so.
    fn try_read_char(&mut self, c: char) -> bool {
        if !self.is_char(c) {
            return false;
        }
        self.forward();
        true
    }
}
