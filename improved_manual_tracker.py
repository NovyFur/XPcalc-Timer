#!/usr/bin/env python3
"""
Quinfall XP Tracker - Improved Manual Tracker
A simple manual XP tracker with flat XP numbers, calculate button, opacity control,
and separate countdown timer functionality.
"""

import sys
import time
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QSpinBox, 
                            QFrame, QSizePolicy, QCheckBox, QLineEdit,
                            QFormLayout, QGroupBox, QSlider)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon

class ImprovedManualXPTracker(QMainWindow):
    """Main UI for the Improved Manual XP Tracker with separate timer functionality"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize tracking variables
        self.start_time = None
        self.end_time = None
        self.start_xp = None
        self.end_xp = None
        self.is_tracking = False
        self.elapsed_seconds = 0
        self.window_opacity = 0.8
        
        # Set up UI refresh timer
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.update_elapsed_time)
        
        # Set up countdown timer
        self.countdown_seconds = 0
        self.countdown_running = False
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        # Set up UI
        self.setup_ui()
        
        # For dragging the window
        self.dragging = False
        self.drag_position = None
    
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Quinfall Manual XP Tracker")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create a frame for the background
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setAutoFillBackground(True)
        
        # Set semi-transparent dark background
        palette = frame.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30, int(255 * self.window_opacity)))
        frame.setPalette(palette)
        
        frame_layout = QVBoxLayout(frame)
        
        # Header with title and controls
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Quinfall Manual XP Tracker")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        
        minimize_button = QPushButton("_")
        minimize_button.setFixedSize(20, 20)
        minimize_button.clicked.connect(self.showMinimized)
        
        close_button = QPushButton("X")
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(self.close)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(minimize_button)
        header_layout.addWidget(close_button)
        
        frame_layout.addLayout(header_layout)
        
        # Opacity control
        opacity_group = QGroupBox("Window Opacity")
        opacity_group.setStyleSheet("QGroupBox { color: white; }")
        opacity_layout = QVBoxLayout()
        
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(int(self.window_opacity * 100))
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        
        opacity_layout.addWidget(self.opacity_slider)
        opacity_group.setLayout(opacity_layout)
        frame_layout.addWidget(opacity_group)
        
        # XP Input Group
        xp_group = QGroupBox("XP Tracking")
        xp_group.setStyleSheet("QGroupBox { color: white; }")
        xp_layout = QFormLayout()
        
        # Starting XP input
        self.start_xp_input = QLineEdit()
        self.start_xp_input.setPlaceholderText("Enter starting XP (e.g., 12353546)")
        
        # Ending XP input
        self.end_xp_input = QLineEdit()
        self.end_xp_input.setPlaceholderText("Enter ending XP (e.g., 12453546)")
        self.end_xp_input.setEnabled(False)
        
        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_results)
        self.calculate_button.setEnabled(False)
        
        xp_layout.addRow("Starting XP:", self.start_xp_input)
        xp_layout.addRow("Ending XP:", self.end_xp_input)
        xp_layout.addRow("", self.calculate_button)
        
        xp_group.setLayout(xp_layout)
        frame_layout.addWidget(xp_group)
        
        # Timer Group
        timer_group = QGroupBox("XP Session Timer")
        timer_group.setStyleSheet("QGroupBox { color: white; }")
        timer_layout = QVBoxLayout()
        
        # Timer display
        self.timer_display = QLabel("00:00:00")
        self.timer_display.setFont(QFont("Arial", 24, QFont.Bold))
        self.timer_display.setStyleSheet("color: white;")
        self.timer_display.setAlignment(Qt.AlignCenter)
        
        # Timer controls
        timer_controls = QHBoxLayout()
        
        self.start_button = QPushButton("Start Tracking")
        self.start_button.clicked.connect(self.start_tracking)
        
        self.stop_button = QPushButton("Stop Tracking")
        self.stop_button.clicked.connect(self.stop_tracking)
        self.stop_button.setEnabled(False)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_tracking)
        
        timer_controls.addWidget(self.start_button)
        timer_controls.addWidget(self.stop_button)
        timer_controls.addWidget(self.reset_button)
        
        timer_layout.addWidget(self.timer_display)
        timer_layout.addLayout(timer_controls)
        
        timer_group.setLayout(timer_layout)
        frame_layout.addWidget(timer_group)
        
        # Countdown Timer Group (completely separate functionality)
        countdown_group = QGroupBox("Countdown Timer")
        countdown_group.setStyleSheet("QGroupBox { color: white; }")
        countdown_layout = QVBoxLayout()
        
        # Countdown timer settings
        countdown_settings = QHBoxLayout()
        
        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 60)
        self.minutes_input.setSingleStep(1)
        self.minutes_input.setValue(0)
        
        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setSingleStep(1)
        self.seconds_input.setValue(30)
        
        countdown_settings.addWidget(QLabel("Minutes:"))
        countdown_settings.addWidget(self.minutes_input)
        countdown_settings.addWidget(QLabel("Seconds:"))
        countdown_settings.addWidget(self.seconds_input)
        
        # Countdown display
        self.countdown_display = QLabel("00:00")
        self.countdown_display.setFont(QFont("Arial", 20, QFont.Bold))
        self.countdown_display.setStyleSheet("color: white;")
        self.countdown_display.setAlignment(Qt.AlignCenter)
        
        # Countdown controls
        countdown_controls = QHBoxLayout()
        
        self.countdown_start_button = QPushButton("Start Countdown")
        self.countdown_start_button.clicked.connect(self.start_countdown)
        
        self.countdown_stop_button = QPushButton("Stop Countdown")
        self.countdown_stop_button.clicked.connect(self.stop_countdown)
        self.countdown_stop_button.setEnabled(False)
        
        self.auto_reset_checkbox = QCheckBox("Auto Reset")
        self.auto_reset_checkbox.setStyleSheet("color: white;")
        self.auto_reset_checkbox.setChecked(True)
        
        countdown_controls.addWidget(self.countdown_start_button)
        countdown_controls.addWidget(self.countdown_stop_button)
        countdown_controls.addWidget(self.auto_reset_checkbox)
        
        countdown_layout.addLayout(countdown_settings)
        countdown_layout.addWidget(self.countdown_display)
        countdown_layout.addLayout(countdown_controls)
        
        countdown_group.setLayout(countdown_layout)
        frame_layout.addWidget(countdown_group)
        
        # Results Group
        results_group = QGroupBox("Results")
        results_group.setStyleSheet("QGroupBox { color: white; }")
        results_layout = QVBoxLayout()
        
        self.xp_gained_label = QLabel("XP Gained: --")
        self.xp_gained_label.setStyleSheet("color: white;")
        
        self.xp_per_minute_label = QLabel("XP/Minute: --")
        self.xp_per_minute_label.setStyleSheet("color: white;")
        
        self.xp_per_hour_label = QLabel("XP/Hour: --")
        self.xp_per_hour_label.setStyleSheet("color: white;")
        
        results_layout.addWidget(self.xp_gained_label)
        results_layout.addWidget(self.xp_per_minute_label)
        results_layout.addWidget(self.xp_per_hour_label)
        
        results_group.setLayout(results_layout)
        frame_layout.addWidget(results_group)
        
        # Status label
        self.status_label = QLabel("Ready. Enter your starting XP and click Start Tracking.")
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.status_label)
        
        main_layout.addWidget(frame)
        
        self.setCentralWidget(main_widget)
        self.resize(400, 700)
    
    def change_opacity(self, value):
        """Change the opacity of the window"""
        self.window_opacity = value / 100.0
        self.setWindowOpacity(self.window_opacity)
        
        # Update background color with new opacity
        frame = self.centralWidget().layout().itemAt(0).widget()
        palette = frame.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30, int(255 * self.window_opacity)))
        frame.setPalette(palette)
    
    def start_tracking(self):
        """Start XP tracking"""
        # Validate XP input
        try:
            self.start_xp = int(self.start_xp_input.text().strip())
        except ValueError:
            self.status_label.setText("Please enter a valid starting XP number.")
            return
        
        self.start_time = datetime.now()
        self.is_tracking = True
        self.elapsed_seconds = 0
        
        # Update UI
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.start_xp_input.setEnabled(False)
        self.end_xp_input.setEnabled(False)
        self.calculate_button.setEnabled(False)
        
        # Start timer
        self.refresh_timer.start(1000)  # Update every second
        
        self.status_label.setText(f"Tracking started at {self.start_time.strftime('%H:%M:%S')} with XP: {self.start_xp:,}")
    
    def stop_tracking(self):
        """Stop XP tracking"""
        self.end_time = datetime.now()
        self.is_tracking = False
        
        # Stop timer
        self.refresh_timer.stop()
        
        # Update UI
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.start_xp_input.setEnabled(True)
        self.end_xp_input.setEnabled(True)
        self.calculate_button.setEnabled(True)
        
        self.status_label.setText(f"Tracking stopped at {self.end_time.strftime('%H:%M:%S')}. Enter your ending XP and click Calculate.")
    
    def reset_tracking(self):
        """Reset all tracking data"""
        self.start_time = None
        self.end_time = None
        self.start_xp = None
        self.end_xp = None
        self.is_tracking = False
        self.elapsed_seconds = 0
        
        # Stop timer
        self.refresh_timer.stop()
        
        # Reset UI
        self.timer_display.setText("00:00:00")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.start_xp_input.setEnabled(True)
        self.start_xp_input.clear()
        self.end_xp_input.setEnabled(False)
        self.end_xp_input.clear()
        self.calculate_button.setEnabled(False)
        
        # Reset results
        self.xp_gained_label.setText("XP Gained: --")
        self.xp_per_minute_label.setText("XP/Minute: --")
        self.xp_per_hour_label.setText("XP/Hour: --")
        
        self.status_label.setText("Reset complete. Enter your starting XP and click Start Tracking.")
    
    def update_elapsed_time(self):
        """Update the elapsed time display"""
        if not self.is_tracking:
            return
        
        self.elapsed_seconds += 1
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        self.timer_display.setText(f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
    
    def start_countdown(self):
        """Start the countdown timer"""
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        
        self.countdown_seconds = minutes * 60 + seconds
        if self.countdown_seconds <= 0:
            self.status_label.setText("Please set a countdown time greater than zero.")
            return
        
        self.countdown_running = True
        
        # Update UI
        self.countdown_start_button.setEnabled(False)
        self.countdown_stop_button.setEnabled(True)
        self.minutes_input.setEnabled(False)
        self.seconds_input.setEnabled(False)
        
        # Start timer
        self.update_countdown()
        self.countdown_timer.start(1000)  # Update every second
        
        self.status_label.setText(f"Countdown started: {minutes} minutes and {seconds} seconds")
    
    def stop_countdown(self):
        """Stop the countdown timer"""
        self.countdown_running = False
        
        # Stop timer
        self.countdown_timer.stop()
        
        # Update UI
        self.countdown_start_button.setEnabled(True)
        self.countdown_stop_button.setEnabled(False)
        self.minutes_input.setEnabled(True)
        self.seconds_input.setEnabled(True)
        
        self.status_label.setText("Countdown stopped.")
    
    def update_countdown(self):
        """Update the countdown timer display"""
        if not self.countdown_running:
            return
        
        self.countdown_seconds -= 1
        
        if self.countdown_seconds <= 0:
            # Timer reached zero
            minutes, seconds = 0, 0
            
            # Play sound or notification here if needed
            
            # Auto reset if enabled
            if self.auto_reset_checkbox.isChecked():
                # Reset to original time
                minutes = self.minutes_input.value()
                seconds = self.seconds_input.value()
                self.countdown_seconds = minutes * 60 + seconds
                self.status_label.setText(f"Countdown reset: {minutes} minutes and {seconds} seconds")
            else:
                # Stop the countdown
                self.stop_countdown()
                self.countdown_display.setText("00:00")
                self.status_label.setText("Countdown finished!")
                return
        else:
            # Calculate remaining time
            minutes, seconds = divmod(self.countdown_seconds, 60)
        
        # Update display
        self.countdown_display.setText(f"{int(minutes):02d}:{int(seconds):02d}")
    
    def calculate_results(self):
        """Calculate XP gain results based on input values"""
        # Validate XP input
        try:
            self.end_xp = int(self.end_xp_input.text().strip())
        except ValueError:
            self.status_label.setText("Please enter a valid ending XP number.")
            return
        
        if self.start_xp is None or self.end_xp is None:
            self.status_label.setText("Please enter both starting and ending XP values.")
            return
        
        if self.start_time is None or self.end_time is None:
            self.status_label.setText("You must start and stop tracking before calculating results.")
            return
        
        # Calculate time difference
        time_diff = (self.end_time - self.start_time).total_seconds()
        
        if time_diff <= 0:
            self.status_label.setText("Error: Time difference is zero or negative.")
            return
        
        # Calculate XP change
        xp_change = self.end_xp - self.start_xp
        
        # Calculate rates
        xp_per_second = xp_change / time_diff
        xp_per_minute = xp_per_second * 60
        xp_per_hour = xp_per_second * 3600
        
        # Update UI with formatted numbers
        self.xp_gained_label.setText(f"XP Gained: {xp_change:,}")
        self.xp_per_minute_label.setText(f"XP/Minute: {int(xp_per_minute):,}")
        self.xp_per_hour_label.setText(f"XP/Hour: {int(xp_per_hour):,}")
        
        self.status_label.setText(f"Results calculated for {time_diff:.1f} seconds of tracking.")
    
    def mousePressEvent(self, event):
        """Handle mouse press events for dragging the window"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging the window"""
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events for dragging the window"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImprovedManualXPTracker()
    window.show()
    sys.exit(app.exec_())
