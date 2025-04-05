# Quinfall Improved Manual XP Tracker

## Overview

This program helps you track your XP progress in Quinfall using a simple manual input approach with flat XP numbers, a dedicated calculate button, opacity control, and a separate countdown timer.

## Features

- **Flat XP Number Input**: Enter your starting and ending XP as actual numbers (e.g., 12353546)
- **Dedicated Calculate Button**: Calculate results when you're ready
- **Window Opacity Control**: Adjust the transparency of the tracker window
- **Elapsed Time Tracking**: Tracks how long you've been playing
- **XP Rate Calculation**: Shows XP gain per minute and per hour
- **Separate Countdown Timer**: Independent timer with auto-reset functionality
- **Overlay Interface**: Stays on top of your game for easy monitoring
- **Anti-cheat Safe**: No screen capture or game interaction, completely external

## Installation

1. Make sure you have Python 3.8+ installed on your system
2. Install the required dependency:
   ```
   pip install PyQt5
   ```

## Usage

1. Run the program:
   ```
   python improved_main.py
   ```

2. **XP Tracking**:
   - Enter your current XP number in the "Starting XP" field
   - Click "Start Tracking" to begin the timer
   - Play the game as normal
   - When you want to check your XP rate, click "Stop Tracking"
   - Enter your new XP number in the "Ending XP" field
   - Click the "Calculate" button to see your XP gain rates

3. **Window Opacity**:
   - Use the opacity slider to adjust how transparent the window is
   - Lower values make the window more transparent

4. **Countdown Timer**:
   - The countdown timer is completely separate from XP tracking
   - Set your desired countdown time using the minutes and seconds inputs
   - Click "Start Countdown" to begin the countdown
   - When the timer reaches zero, it will automatically reset and start again if "Auto Reset" is checked
   - This is useful for timing farming rotations or other timed activities

5. **Results**:
   - XP Gained: Total XP gained during the tracking period
   - XP/Minute: Your XP gain rate per minute
   - XP/Hour: Your XP gain rate per hour

## Tips for Accurate Tracking

1. For the most accurate results, track for at least 10-15 minutes
2. Make sure to enter your XP numbers exactly as shown in the game
3. Use the Reset button to start a new tracking session

## Anti-cheat Safety

This program is completely safe to use with Quinfall as it:
- Does not interact with the game in any way
- Does not capture your screen
- Does not access game memory or modify game files
- Only tracks what you manually input

## Support

If you encounter any issues or have suggestions for improvements, please provide feedback.
