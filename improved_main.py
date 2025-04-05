#!/usr/bin/env python3
"""
Quinfall XP Tracker - Improved Manual Tracker Main
This is the main entry point for the improved manual XP tracking program.
"""

import sys
from PyQt5.QtWidgets import QApplication
from improved_manual_tracker import ImprovedManualXPTracker

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = ImprovedManualXPTracker()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
