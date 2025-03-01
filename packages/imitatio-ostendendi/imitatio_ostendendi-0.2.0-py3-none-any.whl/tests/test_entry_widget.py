"""Tests for Entry widget functionality."""

import unittest
from unittest.mock import MagicMock

from imitatio_ostendendi.widgets import Entry, InvalidStateError
from imitatio_ostendendi.constants import NORMAL, DISABLED, END

class TestEntry(unittest.TestCase):
    """Test cases for Entry widget class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.entry = Entry()
        
    def test_initial_state(self):
        """Test entry widget initialization."""
        self.assertEqual(self.entry._text, "")
        self.assertEqual(self.entry._state, NORMAL)
        self.assertIsNone(self.entry._textvariable)
        
    def test_insert_text(self):
        """Test text insertion."""
        self.entry.insert(0, "Hello")
        self.assertEqual(self.entry._text, "Hello")
        
        self.entry.insert(END, ", World!")
        self.assertEqual(self.entry._text, "Hello, World!")
        
        self.entry.insert(5, ", Python")
        self.assertEqual(self.entry._text, "Hello, Python, World!")
        
    def test_delete_text(self):
        """Test text deletion."""
        self.entry.insert(0, "Hello, World!")
        
        self.entry.delete(0, 5)
        self.assertEqual(self.entry._text, ", World!")
        
        self.entry.delete(0, END)
        self.assertEqual(self.entry._text, "")
        
    def test_get_text(self):
        """Test text retrieval."""
        self.entry.insert(0, "Hello, World!")
        self.assertEqual(self.entry.get(), "Hello, World!")
        
    def test_disabled_state(self):
        """Test widget behavior in disabled state."""
        self.entry.insert(0, "Initial text")
        self.entry.configure(state=DISABLED)
        
        with self.assertRaises(InvalidStateError):
            self.entry.insert(END, "More text")
            
        with self.assertRaises(InvalidStateError):
            self.entry.delete(0, END)
            
        # Get should still work in disabled state
        self.assertEqual(self.entry.get(), "Initial text")
        
    def test_textvariable(self):
        """Test textvariable integration."""
        var = MagicMock()
        var.get.return_value = "Initial"
        
        entry = Entry(textvariable=var)
        self.assertEqual(entry._text, "Initial")
        
        entry.insert(END, " text")
        var.set.assert_called_with("Initial text")
        
        entry.delete(0, END)
        var.set.assert_called_with("")
        
    def test_invalid_index(self):
        """Test handling of invalid indices."""
        with self.assertRaises(ValueError):
            self.entry.insert("invalid", "text")
            
        with self.assertRaises(ValueError):
            self.entry.delete("invalid")
            
if __name__ == '__main__':
    unittest.main()
