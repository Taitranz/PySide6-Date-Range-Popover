from PyQt6.QtCore import Qt, QSize, QPoint, QTimer
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton


class DraggableHeaderStrip(QWidget):
    """Custom header widget that can be dragged to move the parent widget."""
    
    def __init__(self, parent_widget: QWidget) -> None:
        super().__init__()
        self.parent_widget: QWidget = parent_widget
        self.drag_position: QPoint = QPoint()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #d9d9d9;")
    
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        """Handle mouse press to start drag."""
        if a0 and a0.button() == Qt.MouseButton.LeftButton:
            self.drag_position = a0.globalPosition().toPoint() - self.parent_widget.pos()
    
    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        """Handle mouse move to drag the parent widget."""
        if a0 and a0.buttons() == Qt.MouseButton.LeftButton:
            self.parent_widget.move(a0.globalPosition().toPoint() - self.drag_position)


class DateRangePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(320, 600)
        self.setMaximumSize(320, 600)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #1f1f1f;")
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Main layout with 28px padding around the whole component
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 28, 28, 28)
        main_layout.setSpacing(0)
        
        # Header strip with light grey background
        header_strip = DraggableHeaderStrip(self)
        header_layout = QHBoxLayout(header_strip)
        header_layout.setContentsMargins(0, 0, 0, 25)
        header_layout.setSpacing(0)
        
        # Left-aligned text
        header_text = QLabel("Date Range")
        header_layout.addWidget(header_text, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Right-aligned button
        header_button = QPushButton("X")
        header_button.setMaximumWidth(30)
        header_layout.addWidget(header_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        main_layout.addWidget(header_strip)
        
        # Button strip with Date and Custom Range buttons
        button_strip = QWidget()
        button_strip.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        button_strip.setStyleSheet("background-color: #b0b0b0;")
        button_layout = QHBoxLayout(button_strip)
        button_layout.setContentsMargins(0, 8, 0, 10)
        button_layout.setSpacing(0)
        
        date_button = QPushButton("Date")
        date_button.setFixedWidth(36)
        date_button.setStyleSheet("text-align: left; padding-left: 5px;")
        custom_range_button = QPushButton("Custom Range")
        custom_range_button.setFixedWidth(90)
        custom_range_button.setStyleSheet("text-align: left; padding-left: 5px;")
        
        button_layout.addWidget(date_button, alignment=Qt.AlignmentFlag.AlignLeft)
        button_gap = QWidget()
        button_gap.setFixedWidth(24)
        button_layout.addWidget(button_gap)
        button_layout.addWidget(custom_range_button, alignment=Qt.AlignmentFlag.AlignLeft)
        button_layout.addStretch()
        
        # Add square below buttons
        square_container = QWidget()
        square_container_layout = QHBoxLayout(square_container)
        square_container_layout.setContentsMargins(0, 0, 0, 0)
        square_container_layout.setSpacing(0)
        
        square = QWidget()
        square.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        square.setFixedSize(262, 5)
        square.setStyleSheet("background-color: #82b8ff;")
        
        inner_square = QWidget()
        inner_square.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        inner_square.setFixedHeight(5)
        inner_square.setStyleSheet("background-color: #2962ff; border-radius: 2px;")
        
        # Store button widths and gap for dynamic resizing
        self.date_button_width = 36
        self.custom_range_button_width = 90
        self.button_gap = 24
        inner_square.setFixedWidth(self.date_button_width)  # Default to Date width
        
        square_container_layout.addWidget(square)
        square_container_layout.addWidget(inner_square)
        square_container_layout.addStretch()
        
        # Store references for button click handlers
        self.inner_square = inner_square
        self.square_container_layout = square_container_layout
        self.current_position = 0  # Track current position for animation
        self.current_width = self.date_button_width  # Track current width for animation
        
        # Create animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_step)  # type: ignore
        self.target_position = 0
        self.target_width = self.date_button_width
        self.animation_duration = 40  # milliseconds
        self.animation_elapsed = 0
        
        # Connect button click events
        date_button.clicked.connect(self._on_date_clicked)  # type: ignore
        custom_range_button.clicked.connect(self._on_custom_range_clicked)  # type: ignore
        
        # Set Date as default selection
        self._on_date_clicked()
        
        # Create a container for the button strip and square
        button_container = QWidget()
        button_container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        button_container.setStyleSheet("background-color: #b0b0b0;")
        button_container_layout = QVBoxLayout(button_container)
        button_container_layout.setContentsMargins(0, 0, 0, 0)
        button_container_layout.setSpacing(0)
        button_container_layout.addWidget(button_strip)
        button_container_layout.addWidget(square_container, alignment=Qt.AlignmentFlag.AlignLeft)
        
        main_layout.addWidget(button_container)
        
        # Center content
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("helllo")
        center_layout.addWidget(label)
        
        main_layout.addLayout(center_layout, 1)

    def sizeHint(self) -> QSize:
        return QSize(320, 600)
    
    def _on_date_clicked(self) -> None:
        """Handle Date button click - animate inner square to Date position."""
        self.target_position = 0
        self.target_width = self.date_button_width
        self._start_animation()
    
    def _on_custom_range_clicked(self) -> None:
        """Handle Custom Range button click - animate inner square to Custom Range position."""
        self.target_position = self.date_button_width + self.button_gap
        self.target_width = self.custom_range_button_width
        self._start_animation()
    
    def _start_animation(self) -> None:
        """Start the animation to move the inner square."""
        self.animation_elapsed = 0
        self.animation_timer.start(16)  # ~60 FPS
    
    def _animate_step(self) -> None:
        """Update animation frame."""
        self.animation_elapsed += 16
        
        # Calculate progress (0 to 1)
        progress = min(self.animation_elapsed / self.animation_duration, 1.0)
        
        # Store initial position and width on first frame
        if not hasattr(self, '_animation_start_position'):
            self._animation_start_position = self.current_position
            self._animation_start_width = self.current_width
        
        # Linear interpolation between start and target position
        self.current_position = int(self._animation_start_position + (self.target_position - self._animation_start_position) * progress)
        
        # Linear interpolation between start and target width
        self.current_width = int(self._animation_start_width + (self.target_width - self._animation_start_width) * progress)
        
        # Update inner square width during animation
        self.inner_square.setFixedWidth(self.current_width)
        
        # Update layout with current position
        self._update_square_layout(self.current_position)
        
        # Stop animation when complete
        if progress >= 1.0:
            self.animation_timer.stop()
            self.current_position = self.target_position
            self.current_width = self.target_width
            delattr(self, '_animation_start_position')
            delattr(self, '_animation_start_width')
            
            # Final layout update
            self._update_square_layout(self.current_position)
    
    def _update_square_layout(self, position: int) -> None:
        """Update the square container layout with the current position."""
        # Remove all widgets from layout
        while self.square_container_layout.count():
            item = self.square_container_layout.takeAt(0)
            widget = item.widget() if item else None
            if widget:
                widget.hide()
        
        # Add spacer for position, inner square, and remaining spacer
        if position > 0:
            spacer1 = QWidget()
            spacer1.setFixedWidth(position)
            self.square_container_layout.addWidget(spacer1)
        
        self.square_container_layout.addWidget(self.inner_square)
        
        # Calculate remaining space
        if position == 0:
            remaining = 262 - self.date_button_width
        else:
            remaining = 262 - position - self.custom_range_button_width
        
        if remaining > 0:
            spacer2 = QWidget()
            spacer2.setFixedWidth(remaining)
            self.square_container_layout.addWidget(spacer2)
        
        self.square_container_layout.addStretch()
        self.inner_square.show()

