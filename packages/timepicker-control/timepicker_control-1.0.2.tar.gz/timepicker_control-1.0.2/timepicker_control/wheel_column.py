from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QIntValidator

class WheelColumn(QWidget):
    """A widget that displays a vertical column of numbers with up/down buttons and direct input."""
    
    value_changed = Signal(str)  # Changed to emit string values
    
    def __init__(self, values=None, min_value=0, max_value=59, parent=None):
        super().__init__(parent)
        if values is not None:
            self._values = values
            self._min_value = 0
            self._max_value = len(values) - 1
            self._is_numeric = False
        else:
            self._values = [str(i).zfill(2) for i in range(min_value, max_value + 1)]
            self._min_value = min_value
            self._max_value = max_value
            self._is_numeric = True
            
        self._current_index = 0
        self._setup_ui()
        self._setup_connections()
        
    def _setup_ui(self):
        """Set up the user interface components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Up button
        self.up_button = QPushButton("▲")
        self.up_button.setFixedHeight(20)
        layout.addWidget(self.up_button)
        
        # Value display/input
        self.value_edit = QLineEdit()
        self.value_edit.setAlignment(Qt.AlignCenter)
        if self._is_numeric:
            self.value_edit.setValidator(QIntValidator(self._min_value, self._max_value))
        self.value_edit.setFixedWidth(40)
        layout.addWidget(self.value_edit)
        
        # Down button
        self.down_button = QPushButton("▼")
        self.down_button.setFixedHeight(20)
        layout.addWidget(self.down_button)
        
        self._update_display()
        
    def _setup_connections(self):
        """Set up signal/slot connections."""
        self.up_button.clicked.connect(self.increment)
        self.down_button.clicked.connect(self.decrement)
        self.value_edit.editingFinished.connect(self._on_edit_finished)
        
    def _update_display(self):
        """Update the display with the current value."""
        self.value_edit.setText(self._values[self._current_index])
        
    def _on_edit_finished(self):
        """Handle when user finishes editing the value."""
        text = self.value_edit.text()
        if self._is_numeric:
            try:
                value = int(text)
                if self._min_value <= value <= self._max_value:
                    self._current_index = value - self._min_value
                    self._update_display()
                    self.value_changed.emit(self._values[self._current_index])
                else:
                    self._update_display()
            except ValueError:
                self._update_display()
        else:
            if text in self._values:
                self._current_index = self._values.index(text)
                self._update_display()
                self.value_changed.emit(text)
            else:
                self._update_display()
            
    def increment(self):
        """Increment the current value."""
        self._current_index = (self._current_index + 1) % len(self._values)
        self._update_display()
        self.value_changed.emit(self._values[self._current_index])
        
    def decrement(self):
        """Decrement the current value."""
        self._current_index = (self._current_index - 1) % len(self._values)
        self._update_display()
        self.value_changed.emit(self._values[self._current_index])
        
    def set_value(self, value):
        """Set the current value."""
        if isinstance(value, str):
            if value in self._values:
                self._current_index = self._values.index(value)
                self._update_display()
                self.value_changed.emit(value)
        elif isinstance(value, int) and self._is_numeric:
            if self._min_value <= value <= self._max_value:
                self._current_index = value - self._min_value
                self._update_display()
                self.value_changed.emit(self._values[self._current_index])
            
    def value(self):
        """Get the current value."""
        return self._values[self._current_index]
        
    def keyPressEvent(self, event):
        """Handle keyboard events."""
        if event.key() == Qt.Key_Up:
            self.increment()
        elif event.key() == Qt.Key_Down:
            self.decrement()
        else:
            super().keyPressEvent(event)