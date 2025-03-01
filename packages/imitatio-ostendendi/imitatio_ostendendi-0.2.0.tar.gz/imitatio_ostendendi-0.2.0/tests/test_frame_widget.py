"""Tests for Frame widget functionality."""

import unittest
from unittest.mock import MagicMock

from imitatio_ostendendi.widgets import Frame, LabelFrame, Button
from imitatio_ostendendi.constants import NORMAL, DISABLED

class TestFrame(unittest.TestCase):
    """Test cases for Frame widget class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.frame = Frame()
        
    def test_initial_state(self):
        """Test frame widget initialization."""
        self.assertEqual(self.frame._state, NORMAL)
        self.assertEqual(self.frame._children, [])
        
    def test_child_widgets(self):
        """Test child widget management."""
        button1 = Button(self.frame)
        button2 = Button(self.frame)
        
        self.frame._children.extend([button1, button2])
        self.assertEqual(len(self.frame._children), 2)
        self.assertIn(button1, self.frame._children)
        self.assertIn(button2, self.frame._children)

class TestLabelFrame(unittest.TestCase):
    """Test cases for LabelFrame widget class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.frame = LabelFrame(text="Test Frame")
        
    def test_initial_state(self):
        """Test labelframe widget initialization."""
        self.assertEqual(self.frame._state, NORMAL)
        self.assertEqual(self.frame._children, [])
        self.assertEqual(self.frame._text, "Test Frame")
        
    def test_configure_text(self):
        """Test text configuration."""
        self.frame.configure(text="New Label")
        self.assertEqual(self.frame._text, "New Label")
        
    def test_child_widgets(self):
        """Test child widget management."""
        button = Button(self.frame, text="Click me!")
        
        self.frame._children.append(button)
        self.assertEqual(len(self.frame._children), 1)
        self.assertIn(button, self.frame._children)
        
if __name__ == '__main__':
    unittest.main()
