#!/usr/bin/env python3
"""
Quick start script for HARP Firmware Updater GUI

This script provides a simple way to launch the application.
"""

import sys
from pathlib import Path

# Add src to path if running directly
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

from harp_regulator_gui.main import start_app

if __name__ == "__main__":
    start_app()
