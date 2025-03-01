"""Widget package for tkinter/ttk mocks."""

from .base import Widget, WidgetError, InvalidStateError
from .text import Text
from .entry import Entry
from .buttons import Button
from .frames import Frame, LabelFrame

__all__ = [
    'Widget',
    'WidgetError',
    'InvalidStateError',
    'Text',
    'Entry',
    'Button',
    'Frame',
    'LabelFrame',
]
