"""Tests for Button widget functionality."""

import unittest
from unittest.mock import MagicMock

from imitatio_ostendendi.widgets import Button, InvalidStateError
from imitatio_ostendendi.constants import NORMAL, DISABLED

class TestButton(unittest.TestCase):
    """Test cases for Button widget class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.callback = MagicMock()
        self.button = Button(command=self.callback)
        
    def test_initial_state(self):
        """Test button widget initialization."""
        self.assertEqual(self.button._state, NORMAL)
        self.assertEqual(self.button._command, self.callback)
        self.assertEqual(self.button._text, "")
        
    def test_invoke(self):
        """Test button invocation."""
        self.button.invoke()
        self.callback.assert_called_once()
        
    def test_disabled_state(self):
        """Test button behavior in disabled state."""
        self.button.configure(state=DISABLED)
        
        with self.assertRaises(InvalidStateError):
            self.button.invoke()
            
        self.callback.assert_not_called()
        
    def test_configure_command(self):
        """Test command configuration."""
        new_callback = MagicMock()
        self.button.configure(command=new_callback)
        
        self.button.invoke()
        new_callback.assert_called_once()
        self.callback.assert_not_called()
        
    def test_configure_text(self):
        """Test text configuration."""
        self.button.configure(text="Click me!")
        self.assertEqual(self.button._text, "Click me!")
        
    def test_no_command(self):
        """Test button behavior without command."""
        button = Button()
        # Should not raise any error
        button.invoke()
        
if __name__ == '__main__':
    unittest.main()
