# Imitatio Ostendendi

*Latin for "Display Imitation" - A comprehensive mocking library for tkinter/ttk testing*

## Features

- Mock implementations of common tkinter/ttk widgets
- Support for basic widget operations (insert, delete, configure)
- Event simulation capabilities
- Logging for better test debugging
- Easy integration with unittest.mock

## Installation

```bash
pip install imitatio-ostendendi
```

## Usage

```python
from imitatio_ostendendi.widgets import Text, Entry, Button
from imitatio_ostendendi.constants import END, NORMAL, DISABLED

class TestMyGUIApp(TestCase):
    def setUp(self):
        # Create mock widgets
        self.text = Text()
        self.entry = Entry()
        self.button = Button()
        
    def test_text_operations(self):
        # Insert text
        self.text.insert("1.0", "Hello World")
        self.assertEqual(self.text._text, "Hello World")
        
        # Delete text
        self.text.delete("1.0", END)
        self.assertEqual(self.text._text, "")
        
    def test_entry_state(self):
        # Test state changes
        self.entry.configure(state=DISABLED)
        self.assertEqual(self.entry._state, DISABLED)
```

## Widget Support

Currently supported widgets:
- Text
- Entry
- Button
- Frame
- LabelFrame
- Label
- Scrollbar
- Notebook
- StringVar
- IntVar
- BooleanVar

## Why "Imitatio Ostendendi"?

The name comes from Latin:
- "Imitatio" meaning "imitation" or "mock"
- "Ostendendi" meaning "to display" or "to show"

Together, they form "Display Imitation" - a fitting name for a library that provides mock implementations of display widgets.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
