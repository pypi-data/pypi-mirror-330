"""Tests for Text widget functionality."""

import unittest
from unittest.mock import MagicMock

from imitatio_ostendendi.widgets import Text, InvalidStateError
from imitatio_ostendendi.constants import NORMAL, DISABLED, END

class TestText(unittest.TestCase):
    """Test cases for Text widget class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.text = Text()
        
    def test_initial_state(self):
        """Test text widget initialization."""
        self.assertEqual(self.text._text, "")
        self.assertEqual(self.text._state, NORMAL)
        self.assertEqual(self.text._tags, {})
        
    def test_insert_text(self):
        """Test text insertion."""
        self.text.insert("1.0", "Hello")
        self.assertEqual(self.text._text, "Hello")
        
        self.text.insert(END, ", World!")
        self.assertEqual(self.text._text, "Hello, World!")
        
        self.text.insert(5, ", Python")
        self.assertEqual(self.text._text, "Hello, Python, World!")
        
    def test_delete_text(self):
        """Test text deletion."""
        self.text.insert("1.0", "Hello, World!")
        
        self.text.delete("1.0", "1.5")
        self.assertEqual(self.text._text, ", World!")
        
        self.text.delete("1.0", END)
        self.assertEqual(self.text._text, "")
        
    def test_get_text(self):
        """Test text retrieval."""
        self.text.insert("1.0", "Hello, World!")
        
        self.assertEqual(self.text.get("1.0", END), "Hello, World!")
        self.assertEqual(self.text.get("1.0", "1.5"), "Hello")
        
    def test_disabled_state(self):
        """Test widget behavior in disabled state."""
        self.text.insert("1.0", "Initial text")
        self.text.configure(state=DISABLED)
        
        with self.assertRaises(InvalidStateError):
            self.text.insert(END, "More text")
            
        with self.assertRaises(InvalidStateError):
            self.text.delete("1.0", END)
            
        # Get should still work in disabled state
        self.assertEqual(self.text.get("1.0", END), "Initial text")
        
    def test_tag_configuration(self):
        """Test text tag configuration."""
        self.text.tag_configure("bold", font=("Helvetica", "12", "bold"))
        
        self.assertIn("bold", self.text._tags)
        self.assertEqual(
            self.text._tags["bold"]["font"],
            ("Helvetica", "12", "bold")
        )
        
    def test_tag_add_remove(self):
        """Test adding and removing tags."""
        self.text.insert("1.0", "Hello, World!")
        self.text.tag_configure("bold", font=("Helvetica", "12", "bold"))
        
        self.text.tag_add("bold", "1.0", "1.5")
        self.assertIn("bold", self.text._tags)
        
        self.text.tag_remove("bold", "1.0", "1.5")
        self.assertNotIn("bold", self.text._tags)
        
    def test_mark_set(self):
        """Test mark setting."""
        self.text.insert("1.0", "Hello, World!")
        self.text.mark_set("insert", "1.5")
        
        self.assertEqual(self.text._marks["insert"], 5)
        
    def test_invalid_index(self):
        """Test handling of invalid indices."""
        with self.assertRaises(ValueError):
            self.text.insert("invalid", "text")
            
        with self.assertRaises(ValueError):
            self.text.delete("invalid")
            
        with self.assertRaises(ValueError):
            self.text.get("invalid")
            
if __name__ == '__main__':
    unittest.main()
