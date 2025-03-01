"""Test package for imitatio_ostendendi."""

from .test_base_widget import TestWidget
from .test_text_widget import TestText
from .test_entry_widget import TestEntry
from .test_button_widget import TestButton
from .test_frame_widget import TestFrame, TestLabelFrame

__all__ = [
    'TestWidget',
    'TestText',
    'TestEntry',
    'TestButton',
    'TestFrame',
    'TestLabelFrame',
]
