from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QIntValidator, QPalette

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
        self.item_height = 50
        self.visible_items = 7
        self.text_color = "#000000"
        self.background_color = "#FFFFFF"
        self.highlight_color = "#E3F2FD"
        self.scroll_speed = 18.0
        self.smoothness = 0.90
        self.animation_duration = 950
        
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
            
    def set_item_size(self, item_height, visible_items):
        """Set the size of wheel items and number of visible items."""
        self.item_height = item_height
        self.visible_items = visible_items
        self.setFixedHeight(item_height * visible_items)
        
    def set_colors(self, text_color, background_color, highlight_color):
        """Set custom colors for the wheel."""
        self.text_color = text_color
        self.background_color = background_color
        self.highlight_color = highlight_color
        
        # Apply colors to widgets
        palette = self.palette()
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Window, background_color)
        palette.setColor(QPalette.Highlight, highlight_color)
        self.setPalette(palette)
        
        for widget in [self.up_button, self.down_button, self.value_edit]:
            widget.setPalette(palette)
            
    def set_scroll_settings(self, speed, smoothness):
        """Set scrolling behavior settings."""
        self.scroll_speed = speed
        self.smoothness = smoothness
        
    def set_animation_duration(self, duration):
        """Set the duration for animations."""
        self.animation_duration = duration