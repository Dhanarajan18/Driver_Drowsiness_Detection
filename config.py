"""
Configuration file for Driver Drowsiness Detection System
Contains all thresholds, constants, and settings for the application
"""

import os
import sys


def get_base_path():
    """
    Get the base path of the application.
    Works correctly both in development and when packaged with PyInstaller.
    
    Returns:
        str: The base directory path
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys._MEIPASS
    else:
        # Running in development
        return os.path.dirname(os.path.abspath(__file__))


# ==================== PATH CONFIGURATION ====================
BASE_DIR = get_base_path()
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
ALARM_SOUND_PATH = os.path.join(ASSETS_DIR, 'alarm.wav')

# ==================== DETECTION PARAMETERS ====================
# Eye Aspect Ratio (EAR) threshold - eyes are considered closed if EAR is below this
EAR_THRESHOLD = 0.25

# Number of consecutive frames the EAR must be below threshold to trigger alert
EAR_CONSECUTIVE_FRAMES = 20  # At ~30 FPS, this is about 0.67 seconds

# ==================== CAMERA SETTINGS ====================
CAMERA_INDEX = 0  # Default webcam
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# ==================== UI SETTINGS ====================
WINDOW_TITLE = "Driver Drowsiness Detection System"
UI_UPDATE_INTERVAL = 10  # milliseconds
FONT_FAMILY = "Arial"
FONT_SIZE_LARGE = 16
FONT_SIZE_MEDIUM = 12
FONT_SIZE_SMALL = 10

# Color scheme (BGR format for OpenCV)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (0, 255, 255)

# ==================== ALERT SETTINGS ====================
ALERT_COOLDOWN = 2.0  # Seconds between alert replays
ALERT_VOLUME = 1.0  # 0.0 to 1.0

# ==================== LOGGING SETTINGS ====================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
ENABLE_PERFORMANCE_LOGGING = False

# ==================== PERFORMANCE SETTINGS ====================
ENABLE_THREADING = True  # Use threading for video processing
FRAME_SKIP = 0  # Skip frames for better performance (0 = process all frames)
