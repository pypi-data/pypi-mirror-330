"""Tests for base widget functionality."""

import unittest
from unittest.mock import MagicMock

from imitatio_ostendendi.widgets import Widget, InvalidStateError
from imitatio_ostendendi.constants import NORMAL, DISABLED

class TestWidget(unittest.TestCase):
    """Test cases for base Widget class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.widget = Widget()
        
    def test_initial_state(self):
        """Test widget initialization."""
        self.assertEqual(self.widget._state, NORMAL)
        self.assertIsInstance(self.widget.pack, MagicMock)
        self.assertIsInstance(self.widget.grid, MagicMock)
        self.assertIsInstance(self.widget.place, MagicMock)
        
    def test_configure_state(self):
        """Test widget state configuration."""
        self.widget.configure(state=DISABLED)
        self.assertEqual(self.widget._state, DISABLED)
        
        self.widget.configure(state=NORMAL)
        self.assertEqual(self.widget._state, NORMAL)
        
        with self.assertRaises(InvalidStateError):
            self.widget.configure(state="invalid")
            
    def test_event_binding(self):
        """Test event binding functionality."""
        callback = MagicMock()
        self.widget.bind("<Button-1>", callback)
        
        self.assertIn("<Button-1>", self.widget._bindings)
        self.assertEqual(len(self.widget._bindings["<Button-1>"]), 1)
        self.assertEqual(self.widget._bindings["<Button-1>"][0], callback)
        
    def test_event_binding_add(self):
        """Test adding multiple event bindings."""
        callback1 = MagicMock()
        callback2 = MagicMock()
        
        self.widget.bind("<Button-1>", callback1)
        self.widget.bind("<Button-1>", callback2, add=True)
        
        self.assertEqual(len(self.widget._bindings["<Button-1>"]), 2)
        self.assertIn(callback1, self.widget._bindings["<Button-1>"])
        self.assertIn(callback2, self.widget._bindings["<Button-1>"])
        
    def test_event_unbinding(self):
        """Test event unbinding functionality."""
        callback = MagicMock()
        self.widget.bind("<Button-1>", callback)
        self.widget.unbind("<Button-1>")
        
        self.assertNotIn("<Button-1>", self.widget._bindings)
        
if __name__ == '__main__':
    unittest.main()
