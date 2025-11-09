from PyQt6.QtCore import Qt, QSize, QPoint, QTimer
from PyQt6.QtGui import QMouseEvent, QResizeEvent, QFont
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton


class DraggableHeaderStrip(QWidget):
    """Custom header widget that can be dragged to move the parent widget."""
    
    def __init__(self, parent_widget: QWidget) -> None:
        super().__init__()
        self.parent_widget: QWidget = parent_widget
        self.drag_position: QPoint = QPoint()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #d9d9d9; border-radius: 0px;")
    
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
        self.setMinimumSize(302, 600)
        self.setMaximumSize(302, 600)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #1f1f1f; border-radius: 4px;")
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Main layout with 28px padding around the whole component
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Header strip with light grey background
        header_strip = DraggableHeaderStrip(self)
        header_layout = QHBoxLayout(header_strip)
        header_layout.setContentsMargins(0, 0, 0, 25)
        header_layout.setSpacing(0)
        
        # Left-aligned text
        header_text = QLabel("Go to")
        header_font = QFont("Trebuchet MS", 16)
        header_font.setWeight(QFont.Weight.Bold)
        header_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 99.6)
        header_text.setFont(header_font)
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
        button_strip.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        button_layout = QHBoxLayout(button_strip)
        button_layout.setContentsMargins(0, 0, 0, 6)
        button_layout.setSpacing(0)
        
        date_button = QPushButton("Date")
        date_button.setFixedWidth(40)
        date_button.setMinimumHeight(0)
        date_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        date_font = QFont("Trebuchet MS", 12)
        date_font.setWeight(QFont.Weight.Bold)
        date_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 96)
        date_button.setFont(date_font)
        date_button.setStyleSheet("text-align: left; padding: 0; margin: 0; border: none; outline: none;")
        custom_range_button = QPushButton("Custom range")
        custom_range_button.setFixedWidth(105)
        custom_range_button.setMinimumHeight(0)
        custom_range_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        custom_font = QFont("Trebuchet MS", 12)
        custom_font.setWeight(QFont.Weight.Bold)
        custom_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 96)
        custom_range_button.setFont(custom_font)
        custom_range_button.setStyleSheet("text-align: left; padding: 0; margin: 0; border: none; outline: none;")
        
        button_layout.addWidget(date_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        button_gap = QWidget()
        button_gap.setFixedWidth(20)
        button_layout.addWidget(button_gap)
        button_layout.addWidget(custom_range_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        button_layout.addStretch()
        
        # Add square below buttons
        track_wrapper = QWidget()
        track_wrapper.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        track_wrapper.setStyleSheet("background-color: #1f1f1f;")
        track_wrapper_layout = QVBoxLayout(track_wrapper)
        track_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        track_wrapper_layout.setSpacing(0)
        
        track_container = QWidget()
        track_container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        track_container.setStyleSheet("background-color: #4a4a4a; border-radius: 2px;")
        track_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        track_container_layout = QHBoxLayout(track_container)
        track_container_layout.setContentsMargins(0, 0, 0, 0)
        track_container_layout.setSpacing(0)
        
        self.default_track_width = 262
        self.track_container = track_container
        
        self.left_spacer = QWidget()
        self.left_spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.left_spacer.setFixedWidth(0)
        
        sliding_indicator = QWidget()
        sliding_indicator.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        sliding_indicator.setFixedHeight(5)
        sliding_indicator.setStyleSheet("background-color: #dbdbdb; border-radius: 2px;")
        
        self.right_spacer = QWidget()
        self.right_spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.right_spacer.setFixedWidth(0)
        
        track_wrapper_layout.addWidget(track_container)
        
        # Store button widths and gap for dynamic resizing
        self.date_button_width = 38
        self.custom_range_button_width = 105
        self.button_gap = 20
        sliding_indicator.setFixedWidth(self.date_button_width)  # Default to Date width
        
        track_container_layout.addWidget(self.left_spacer)
        track_container_layout.addWidget(sliding_indicator)
        track_container_layout.addWidget(self.right_spacer)
        
        # Store references for button click handlers
        self.sliding_indicator = sliding_indicator
        self.current_position = 0  # Track current position for animation
        self.current_width = self.date_button_width  # Track current width for animation
        self._update_square_layout(self.current_position)
        
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
        button_container.setStyleSheet("background-color: #b0b0b0; border-radius: 0px;")
        button_container_layout = QVBoxLayout(button_container)
        button_container_layout.setContentsMargins(0, 0, 0, 0)
        button_container_layout.setSpacing(0)
        button_container_layout.addWidget(button_strip)
        button_container_layout.addWidget(track_wrapper)
        
        main_layout.addWidget(button_container)
        
        # Center content
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("helllo")
        label_font = QFont("Trebuchet MS")
        label_font.setWeight(QFont.Weight.Bold)
        label_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 96)
        label.setFont(label_font)
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
        
        # Update sliding indicator width during animation
        self.sliding_indicator.setFixedWidth(self.current_width)
        
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
        track_width = self.track_container.width() or self.default_track_width
        max_position = max(track_width - self.current_width, 0)
        clamped_position = max(0, min(position, max_position))
        
        self.left_spacer.setFixedWidth(clamped_position)
        
        remaining = max(track_width - clamped_position - self.current_width, 0)
        self.right_spacer.setFixedWidth(remaining)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        super().resizeEvent(a0)
        self._update_square_layout(self.current_position)

