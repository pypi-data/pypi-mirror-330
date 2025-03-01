"""Mock implementations of tkinter/ttk widgets."""

from typing import Optional, Any, Callable, Dict, List, Union
import logging
from unittest.mock import MagicMock
from .constants import NORMAL, DISABLED, END

# Set up logger
logger = logging.getLogger(__name__)

class WidgetError(Exception):
    """Base exception for widget-related errors."""
    pass

class InvalidStateError(WidgetError):
    """Exception raised when widget is in invalid state."""
    pass

class Widget:
    """Base class for all mock widgets.
    
    Attributes:
        _state: Current state of the widget (NORMAL or DISABLED)
        pack: MagicMock for pack geometry manager
        grid: MagicMock for grid geometry manager
        place: MagicMock for place geometry manager
        
    Example:
        >>> widget = Widget(state=NORMAL)
        >>> widget.pack(side='top', fill='x')
        >>> widget.configure(state=DISABLED)
    """
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        self._state = kwargs.get('state', NORMAL)
        self._bindings: Dict[str, List[Callable]] = {}
        self.pack = MagicMock()
        self.grid = MagicMock()
        self.place = MagicMock()
        self.configure = MagicMock(side_effect=self._configure)
        self.bind = MagicMock(side_effect=self._bind)
        self.unbind = MagicMock(side_effect=self._unbind)
        
    def _configure(self, **kwargs: Any) -> None:
        """Handle widget configuration.
        
        Args:
            **kwargs: Configuration options for the widget
        
        Raises:
            InvalidStateError: If an invalid state is provided
        """
        if 'state' in kwargs:
            state = kwargs['state']
            if state not in (NORMAL, DISABLED):
                raise InvalidStateError(f"Invalid state: {state}")
            self._state = state
            
    def _bind(self, sequence: str, func: Callable, add: bool = False) -> None:
        """Bind function to event sequence.
        
        Args:
            sequence: Event sequence to bind to
            func: Callback function
            add: If True, add this binding to existing bindings
        """
        if sequence not in self._bindings:
            self._bindings[sequence] = []
        if add:
            self._bindings[sequence].append(func)
        else:
            self._bindings[sequence] = [func]
            
    def _unbind(self, sequence: str) -> None:
        """Remove all bindings for event sequence.
        
        Args:
            sequence: Event sequence to unbind
        """
        if sequence in self._bindings:
            del self._bindings[sequence]

class Text(Widget):
    """Mock Text widget."""
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self._text = ""
        self._tags = {}
        self.delete = MagicMock(side_effect=self._delete)
        self.insert = MagicMock(side_effect=self._insert)
        self.get = MagicMock(side_effect=self._get)
        self.tag_configure = MagicMock(side_effect=self._tag_configure)
        self.tag_add = MagicMock(side_effect=self._tag_add)
        self.tag_remove = MagicMock(side_effect=self._tag_remove)
        self.yview = MagicMock()
        self.yview_moveto = MagicMock()
        self.yview_scroll = MagicMock()
        
    def _delete(self, first: Union[str, int], last: Optional[Union[str, int]] = None) -> None:
        """Delete text from widget."""
        if self._state == DISABLED:
            return
            
        # Convert indices
        if first == "1.0":
            start = 0
        elif isinstance(first, str) and first.lower() == END.lower():
            start = len(self._text)
        else:
            try:
                start = int(first)
            except (ValueError, TypeError):
                logger.error(f"Invalid first index in Text._delete: {first}")
                return
                
        if last is None:
            end = start + 1
        elif isinstance(last, str) and last.lower() == END.lower():
            end = len(self._text)
        else:
            try:
                end = int(last)
            except (ValueError, TypeError):
                logger.error(f"Invalid last index in Text._delete: {last}")
                return
                
        # Delete the text
        self._text = self._text[:start] + self._text[end:]
        logger.debug(f"Deleted text from {start} to {end}")
        
    def _insert(self, index: Union[str, int], text: str, *tags: str) -> None:
        """Insert text into widget."""
        if self._state == DISABLED:
            return
            
        try:
            if isinstance(index, str):
                if index == END or index.lower() == END.lower():
                    pos = len(self._text)
                elif index == "1.0":
                    pos = 0
                else:
                    pos = int(index)
            else:
                pos = int(index)
                
            self._text = self._text[:pos] + text + self._text[pos:]
            logger.debug(f"Inserted text at position {pos}")
            
            # Apply tags if provided
            for tag in tags:
                self._tag_add(tag, pos, pos + len(text))
                
        except (ValueError, TypeError) as e:
            logger.error(f"Error in Text._insert: {e}")
            
    def _get(self, start: str = "1.0", end: str = END) -> str:
        """Get text from widget."""
        return self._text
        
    def _tag_configure(self, tag_name: str, **kwargs: Any) -> None:
        """Configure tag properties."""
        if tag_name not in self._tags:
            self._tags[tag_name] = {}
        self._tags[tag_name].update(kwargs)
        
    def _tag_add(self, tag_name: str, start: Union[str, int], end: Union[str, int]) -> None:
        """Add tag to text range."""
        if tag_name not in self._tags:
            self._tags[tag_name] = {}
            
    def _tag_remove(self, tag_name: str, start: Union[str, int], end: Union[str, int]) -> None:
        """Remove tag from text range."""
        if tag_name in self._tags:
            del self._tags[tag_name]

class Entry(Widget):
    """Mock Entry widget."""
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self._text = ""
        self._textvariable = kwargs.get('textvariable', None)
        if self._textvariable:
            self._text = str(self._textvariable.get())
        self.delete = MagicMock(side_effect=self._delete)
        self.insert = MagicMock(side_effect=self._insert)
        self.get = MagicMock(side_effect=lambda: self._text)
        
    def _delete(self, first: Union[str, int], last: Optional[Union[str, int]] = None) -> None:
        """Delete text from entry."""
        if self._state == DISABLED:
            return
            
        # Convert indices
        if first == 0:
            start = 0
        elif isinstance(first, str) and first.lower() == END.lower():
            start = len(self._text)
        else:
            try:
                start = int(first)
            except (ValueError, TypeError):
                logger.error(f"Invalid first index in Entry._delete: {first}")
                return
                
        if last is None:
            end = start + 1
        elif isinstance(last, str) and last.lower() == END.lower():
            end = len(self._text)
        else:
            try:
                end = int(last)
            except (ValueError, TypeError):
                logger.error(f"Invalid last index in Entry._delete: {last}")
                return
                
        # Delete the text
        self._text = self._text[:start] + self._text[end:]
        if self._textvariable:
            self._textvariable.set(self._text)
        logger.debug(f"Deleted text from {start} to {end}")
        
    def _insert(self, index: Union[str, int], string: str) -> None:
        """Insert text into entry."""
        if self._state == DISABLED:
            return
            
        try:
            if isinstance(index, str) and index.lower() == END.lower():
                pos = len(self._text)
            else:
                pos = int(index)
                
            self._text = self._text[:pos] + string + self._text[pos:]
            if self._textvariable:
                self._textvariable.set(self._text)
            logger.debug(f"Inserted text at position {pos}")
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error in Entry._insert: {e}")

class Button(Widget):
    """Mock Button widget."""
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self._command = kwargs.get('command', None)
        self.invoke = MagicMock(side_effect=self._invoke)
        
    def _invoke(self) -> None:
        """Execute button command."""
        if self._state != DISABLED and self._command:
            self._command()

class Frame(Widget):
    """Mock Frame widget."""
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self._children = []

class LabelFrame(Frame):
    """Mock LabelFrame widget."""
    pass

class Label(Widget):
    """Mock Label widget."""
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self._text = kwargs.get('text', '')
        
    def configure(self, **kwargs: Any) -> None:
        super()._configure(**kwargs)
        if 'text' in kwargs:
            self._text = kwargs['text']

class Scrollbar(Widget):
    """Mock Scrollbar widget."""
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self._orient = kwargs.get('orient', 'vertical')
        self._command = kwargs.get('command', None)
        self.set = MagicMock()

class Notebook(Widget):
    """Mock Notebook widget."""
    def __init__(self, master: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self._tabs = {}
        self.add = MagicMock(side_effect=self._add)
        self.select = MagicMock(side_effect=self._select)
        self._selected = None
        
    def _add(self, child: Any, **kwargs: Any) -> None:
        """Add a new tab."""
        self._tabs[child] = kwargs
        if not self._selected:
            self._selected = child
            
    def _select(self, tab_id: Any) -> None:
        """Select a tab."""
        if tab_id in self._tabs:
            self._selected = tab_id

class Variable:
    """Base class for tkinter variable types.
    
    Attributes:
        _value: Current variable value
        _trace_callbacks: List of registered trace callbacks
        
    Example:
        >>> var = Variable(value="initial")
        >>> def callback(var, index, mode): print(f"Value changed to: {var.get()}")
        >>> var.trace_add("write", callback)
        >>> var.set("new value")
        Value changed to: new value
    """
    def __init__(self, master: Optional[Any] = None, value: Any = None, name: Optional[str] = None) -> None:
        self._value = value
        self._trace_callbacks: List[Dict[str, Any]] = []
        self._name = name
        
    def get(self) -> Any:
        """Get current value."""
        return self._value
        
    def set(self, value: Any) -> None:
        """Set new value and trigger callbacks.
        
        Args:
            value: New value for variable
        """
        if self._value != value:
            self._value = value
            self._notify_traces("w")
            
    def trace_add(self, mode: str, callback: Callable) -> str:
        """Add a trace callback.
        
        Args:
            mode: Trace mode ('w' for write, 'r' for read, 'u' for undefined)
            callback: Callback function
            
        Returns:
            Trace identifier
        """
        import uuid
        trace_id = str(uuid.uuid4())
        self._trace_callbacks.append({
            "mode": mode,
            "callback": callback,
            "id": trace_id
        })
        return trace_id
        
    def trace_remove(self, mode: str, trace_id: str) -> None:
        """Remove a trace callback.
        
        Args:
            mode: Trace mode
            trace_id: Trace identifier to remove
        """
        self._trace_callbacks = [
            cb for cb in self._trace_callbacks
            if not (cb["mode"] == mode and cb["id"] == trace_id)
        ]
        
    def _notify_traces(self, mode: str) -> None:
        """Notify all registered trace callbacks.
        
        Args:
            mode: Trace mode that triggered notification
        """
        for cb in self._trace_callbacks:
            if cb["mode"] in (mode, ""):
                try:
                    cb["callback"](self, "", mode)
                except Exception as e:
                    logger.error(f"Error in trace callback: {e}")

class StringVar(Variable):
    """Mock StringVar for string values.
    
    Example:
        >>> var = StringVar(value="hello")
        >>> print(var.get())
        hello
        >>> var.set("world")
        >>> print(var.get())
        world
    """
    def __init__(
        self,
        master: Optional[Any] = None,
        value: str = "",
        name: Optional[str] = None
    ) -> None:
        super().__init__(master, str(value), name)
        
    def get(self) -> str:
        """Get current string value."""
        return str(self._value)
        
    def set(self, value: str) -> None:
        """Set new string value.
        
        Args:
            value: New string value
        """
        super().set(str(value))

class IntVar(Variable):
    """Mock IntVar for integer values.
    
    Example:
        >>> var = IntVar(value=42)
        >>> print(var.get())
        42
        >>> var.set(123)
        >>> print(var.get())
        123
    """
    def __init__(
        self,
        master: Optional[Any] = None,
        value: int = 0,
        name: Optional[str] = None
    ) -> None:
        super().__init__(master, int(value), name)
        
    def get(self) -> int:
        """Get current integer value."""
        return int(self._value)
        
    def set(self, value: int) -> None:
        """Set new integer value.
        
        Args:
            value: New integer value
            
        Raises:
            ValueError: If value cannot be converted to int
        """
        super().set(int(value))

class BooleanVar(Variable):
    """Mock BooleanVar for boolean values.
    
    Example:
        >>> var = BooleanVar(value=True)
        >>> print(var.get())
        True
        >>> var.set(False)
        >>> print(var.get())
        False
    """
    def __init__(
        self,
        master: Optional[Any] = None,
        value: bool = False,
        name: Optional[str] = None
    ) -> None:
        super().__init__(master, bool(value), name)
        
    def get(self) -> bool:
        """Get current boolean value."""
        return bool(self._value)
        
    def set(self, value: bool) -> None:
        """Set new boolean value.
        
        Args:
            value: New boolean value
        """
        super().set(bool(value))
