from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Qt, QTimer, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QLinearGradient

class WheelColumn(QWidget):
    """A widget that displays a vertical scrolling wheel of values."""
    
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
        self.text_color = QColor("#000000")
        self.background_color = QColor("#FFFFFF")
        self.highlight_color = QColor("#E3F2FD")
        self.scroll_speed = 18.0
        self.smoothness = 0.90
        self.animation_duration = 300
        
        # Scrolling properties
        self._scroll_position = 0
        self.dragging = False
        self.last_y = 0
        self.velocity = 0
        self.min_scroll = float('-inf')
        self.max_scroll = float('inf')
        
        # Setup widget
        self.setFixedSize(80, self.item_height * self.visible_items)
        self.setMouseTracking(True)
        
        # Setup animation and timer
        self.deceleration_timer = QTimer(self)
        self.deceleration_timer.timeout.connect(self.update_scroll)
        self.animation = QPropertyAnimation(self, b"scrollPos")
        self.animation.setEasingCurve(QEasingCurve.OutQuint)
        self.animation.setDuration(self.animation_duration)
        self.animation.valueChanged.connect(self.update)
        
    def get_wrapped_index(self, index):
        """Convert any integer index into a valid array index by wrapping around"""
        if not self._values:
            return 0
        if index < 0:
            index = index + ((abs(index) // len(self._values) + 1) * len(self._values))
        return index % len(self._values)
    
    @Property(float)
    def scrollPos(self):
        return self._scroll_position
    
    @scrollPos.setter
    def scrollPos(self, pos):
        self._scroll_position = pos
        raw_index = int(round(pos / self.item_height))
        self._current_index = self.get_wrapped_index(raw_index)
        self.update()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_y = event.position().y()
            self.velocity = 0
            if self.animation.state() == QPropertyAnimation.Running:
                self.animation.stop()
            if self.deceleration_timer.isActive():
                self.deceleration_timer.stop()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            delta_y = event.position().y() - self.last_y
            self.velocity = delta_y
            new_pos = self.scrollPos - delta_y
            self.scrollPos = new_pos
            self.last_y = event.position().y()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            if abs(self.velocity) > 0.1:
                self.deceleration_timer.start(16)  # ~60 FPS
            else:
                self.snap_to_nearest()
    
    def wheelEvent(self, event):
        if self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
        
        delta = event.angleDelta().y()
        self.velocity = delta / self.scroll_speed
        new_pos = self.scrollPos - delta / (self.scroll_speed / 2)
        self.scrollPos = new_pos
        self.update()
        
        if not self.deceleration_timer.isActive():
            self.deceleration_timer.start(16)
    
    def update_scroll(self):
        if abs(self.velocity) < 0.2:  # Velocity threshold
            self.deceleration_timer.stop()
            self.snap_to_nearest()
            return
        
        self.velocity *= self.smoothness
        new_pos = self.scrollPos - self.velocity
        self.scrollPos = new_pos
        self.update()
    
    def snap_to_nearest(self):
        target_pos = round(self.scrollPos / self.item_height) * self.item_height
        
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(self.scrollPos)
        self.animation.setEndValue(target_pos)
        self.animation.finished.connect(self._on_snap_finished)
        self.animation.start()
    
    def _on_snap_finished(self):
        self.value_changed.emit(self.value())
        self.animation.finished.disconnect(self._on_snap_finished)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self.background_color)
        
        # Draw the selection highlight
        highlight_rect = QColor(self.highlight_color)
        highlight_rect.setAlpha(180)
        painter.fillRect(0, self.height() // 2 - self.item_height // 2,
                        self.width(), self.item_height, highlight_rect)
        
        # Calculate base index and offset
        base_index = int(self.scrollPos / self.item_height)
        offset = -(self.scrollPos % self.item_height)
        
        # Draw the items
        for i in range(-2, self.visible_items + 2):
            y_pos = self.height() // 2 + (i * self.item_height) + offset - self.item_height // 2
            display_index = self.get_wrapped_index(base_index + i)
            
            # Calculate opacity based on distance from center
            distance = abs(y_pos + self.item_height // 2 - self.height() // 2)
            max_distance = self.height() // 2
            opacity = max(0.3, min(1.0, 1.0 - (distance / max_distance) ** 1.5))
            
            # Set font size and weight based on position
            is_center = abs(y_pos + self.item_height // 2 - self.height() // 2) < self.item_height / 2
            font = QFont("Segoe UI", 14 if is_center else 12)
            font.setBold(is_center)
            painter.setFont(font)
            
            # Draw text with opacity
            text = str(self._values[display_index])
            text_color = QColor(self.text_color)
            text_color.setAlpha(int(255 * opacity))
            painter.setPen(text_color)
            
            text_width = painter.fontMetrics().horizontalAdvance(text)
            text_x = (self.width() - text_width) // 2
            text_y = int(y_pos + self.item_height // 2 + painter.fontMetrics().ascent() // 2)
            
            if 0 <= text_y <= self.height():
                painter.drawText(text_x, text_y, text)
        
        # Draw top and bottom gradients
        gradient = QLinearGradient(0, 0, 0, self.item_height)
        gradient.setColorAt(0, QColor(self.background_color.red(), 
                                    self.background_color.green(),
                                    self.background_color.blue(), 255))
        gradient.setColorAt(1, QColor(self.background_color.red(),
                                    self.background_color.green(),
                                    self.background_color.blue(), 0))
        painter.fillRect(0, 0, self.width(), self.item_height, gradient)
        
        gradient = QLinearGradient(0, self.height() - self.item_height, 0, self.height())
        gradient.setColorAt(0, QColor(self.background_color.red(),
                                    self.background_color.green(),
                                    self.background_color.blue(), 0))
        gradient.setColorAt(1, QColor(self.background_color.red(),
                                    self.background_color.green(),
                                    self.background_color.blue(), 255))
        painter.fillRect(0, self.height() - self.item_height, self.width(), self.item_height, gradient)
        
        # Draw separator lines
        painter.setPen(QPen(QColor(self.text_color.red(),
                                 self.text_color.green(),
                                 self.text_color.blue(), 50), 1))
        painter.drawLine(0, self.height() // 2 - self.item_height // 2,
                        self.width(), self.height() // 2 - self.item_height // 2)
        painter.drawLine(0, self.height() // 2 + self.item_height // 2,
                        self.width(), self.height() // 2 + self.item_height // 2)
    
    def value(self):
        """Get the current value."""
        return self._values[self._current_index]
    
    def set_value(self, value):
        """Set the current value."""
        if isinstance(value, str):
            if value in self._values:
                target_index = self._values.index(value)
                target_pos = target_index * self.item_height
                
                self.animation.setDuration(self.animation_duration)
                self.animation.setStartValue(self.scrollPos)
                self.animation.setEndValue(target_pos)
                self.animation.start()
    
    def set_item_size(self, item_height, visible_items):
        """Set the size of wheel items and number of visible items."""
        self.item_height = item_height
        self.visible_items = visible_items
        self.setFixedHeight(item_height * visible_items)
        self.update()
    
    def set_colors(self, text_color, background_color, highlight_color):
        """Set custom colors for the wheel."""
        self.text_color = QColor(text_color)
        self.background_color = QColor(background_color)
        self.highlight_color = QColor(highlight_color)
        self.update()
    
    def set_scroll_settings(self, speed, smoothness):
        """Set scrolling behavior settings."""
        self.scroll_speed = speed
        self.smoothness = smoothness
    
    def set_animation_duration(self, duration):
        """Set the duration for animations."""
        self.animation_duration = duration