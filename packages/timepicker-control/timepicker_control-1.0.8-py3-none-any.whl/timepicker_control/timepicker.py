from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal, QSettings, Property
from datetime import time
from .wheel_column import WheelColumn

class TimePicker(QWidget):
    """
    A modern, customizable time picker widget for PySide6 applications.
    Features smooth scrolling, themes, and persistent settings.
    """
    
    # Signal emitted when the time changes
    timeChanged = Signal(time)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize settings
        self.settings = QSettings('TimePicker', 'Widget')
        
        # Default values
        self.DEFAULT_VALUES = {
            'width': 180,
            'height': 120,
            'item_height': 40,
            'visible_items': 3,
            'text_color': "#000000",
            'background_color': "#FFFFFF",
            'highlight_color': "#E3F2FD",
            'scroll_speed': 18.0,
            'smoothness': 0.90,
            'animation_duration': 300
        }
        
        self.initUI()
        self.load_settings()
    
    def initUI(self):
        """Initialize the user interface"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create the hour wheel (1-12)
        hour_values = [str(i).zfill(2) for i in range(1, 13)]
        self.hour_wheel = WheelColumn(values=hour_values)
        layout.addWidget(self.hour_wheel)
        
        # Create the minute wheel (00-59)
        minute_values = [str(i).zfill(2) for i in range(60)]
        self.minute_wheel = WheelColumn(values=minute_values)
        layout.addWidget(self.minute_wheel)
        
        # Create the AM/PM wheel
        self.ampm_wheel = WheelColumn(values=['AM', 'PM'])
        layout.addWidget(self.ampm_wheel)
        
        # Connect signals
        self.hour_wheel.value_changed.connect(self._emit_time_changed)
        self.minute_wheel.value_changed.connect(self._emit_time_changed)
        self.ampm_wheel.value_changed.connect(self._emit_time_changed)
    
    def load_settings(self):
        """Load saved settings or use defaults"""
        # Load and apply size settings
        width = int(self.settings.value('width', self.DEFAULT_VALUES['width']))
        height = int(self.settings.value('height', self.DEFAULT_VALUES['height']))
        self.set_size(width, height)
        
        # Load and apply wheel settings
        item_height = int(self.settings.value('item_height', self.DEFAULT_VALUES['item_height']))
        visible_items = int(self.settings.value('visible_items', self.DEFAULT_VALUES['visible_items']))
        self.set_wheel_size(item_height, visible_items)
        
        # Load and apply colors
        text_color = self.settings.value('text_color', self.DEFAULT_VALUES['text_color'])
        background_color = self.settings.value('background_color', self.DEFAULT_VALUES['background_color'])
        highlight_color = self.settings.value('highlight_color', self.DEFAULT_VALUES['highlight_color'])
        self.set_custom_colors(text_color, background_color, highlight_color)
        
        # Load and apply scroll settings
        scroll_speed = float(self.settings.value('scroll_speed', self.DEFAULT_VALUES['scroll_speed']))
        smoothness = float(self.settings.value('smoothness', self.DEFAULT_VALUES['smoothness']))
        self.set_scroll_settings(scroll_speed, smoothness)
        
        # Load and apply animation settings
        animation_duration = int(self.settings.value('animation_duration', self.DEFAULT_VALUES['animation_duration']))
        self.set_animation_duration(animation_duration)
    
    def save_settings(self):
        """Save current settings"""
        self.settings.setValue('width', self.width())
        self.settings.setValue('height', self.height())
        self.settings.setValue('item_height', self.hour_wheel.item_height)
        self.settings.setValue('visible_items', self.hour_wheel.visible_items)
        self.settings.setValue('text_color', self.hour_wheel.text_color)
        self.settings.setValue('background_color', self.hour_wheel.background_color)
        self.settings.setValue('highlight_color', self.hour_wheel.highlight_color)
        self.settings.setValue('scroll_speed', self.hour_wheel.scroll_speed)
        self.settings.setValue('smoothness', self.hour_wheel.smoothness)
        self.settings.setValue('animation_duration', self.hour_wheel.animation_duration)
        self.settings.sync()
    
    def set_size(self, width, height):
        """Set the overall size of the time picker"""
        self.setFixedSize(width, height)
        # Adjust column widths - wider for hours/minutes, narrower for AM/PM
        hour_min_width = (width * 0.35)  # 35% of total width each for hours and minutes
        ampm_width = width * 0.3  # 30% of total width for AM/PM
        self.hour_wheel.setFixedWidth(int(hour_min_width))
        self.minute_wheel.setFixedWidth(int(hour_min_width))
        self.ampm_wheel.setFixedWidth(int(ampm_width))
    
    def set_wheel_size(self, item_height, visible_items):
        """Set the size of wheel items and number of visible items"""
        for wheel in [self.hour_wheel, self.minute_wheel, self.ampm_wheel]:
            wheel.set_item_size(item_height, visible_items)
    
    def set_custom_colors(self, text_color, background_color, highlight_color):
        """Set custom colors for the time picker"""
        for wheel in [self.hour_wheel, self.minute_wheel, self.ampm_wheel]:
            wheel.set_colors(text_color, background_color, highlight_color)
    
    def set_scroll_settings(self, speed, smoothness):
        """Set scrolling behavior settings"""
        for wheel in [self.hour_wheel, self.minute_wheel, self.ampm_wheel]:
            wheel.set_scroll_settings(speed, smoothness)
    
    def set_animation_duration(self, duration):
        """Set the animation duration for all wheels"""
        for wheel in [self.hour_wheel, self.minute_wheel, self.ampm_wheel]:
            wheel.set_animation_duration(duration)
    
    def reset_to_defaults(self):
        """Reset all settings to their default values"""
        for key, value in self.DEFAULT_VALUES.items():
            self.settings.setValue(key, value)
        self.settings.sync()
        self.load_settings()
    
    def get_time(self):
        """Get the current time as a datetime.time object"""
        hour = int(self.hour_wheel.value())
        minute = int(self.minute_wheel.value())
        is_pm = self.ampm_wheel.value() == 'PM'
        
        if is_pm and hour != 12:
            hour += 12
        elif not is_pm and hour == 12:
            hour = 0
            
        return time(hour, minute)
    
    def set_time(self, time_value):
        """Set the time picker to a specific time"""
        hour = time_value.hour
        minute = time_value.minute
        
        # Convert to 12-hour format
        is_pm = hour >= 12
        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12
            
        self.hour_wheel.set_value(str(hour).zfill(2))
        self.minute_wheel.set_value(str(minute).zfill(2))
        self.ampm_wheel.set_value('PM' if is_pm else 'AM')
    
    def _emit_time_changed(self):
        """Emit the timeChanged signal with the current time"""
        current_time = self.get_time()
        self.timeChanged.emit(current_time)
    
    # Properties for QML integration
    @Property(str)
    def currentTime(self):
        """Get the current time as a string (for QML)"""
        return self.get_time().strftime("%I:%M %p")
    
    @currentTime.setter
    def currentTime(self, time_str):
        """Set the current time from a string (for QML)"""
        from datetime import datetime
        try:
            parsed_time = datetime.strptime(time_str, "%I:%M %p").time()
            self.set_time(parsed_time)
        except ValueError:
            pass 