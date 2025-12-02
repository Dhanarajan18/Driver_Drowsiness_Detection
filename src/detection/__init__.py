"""
__init__.py for detection module
Makes the detection package importable
"""

from .face_eye_detector import FaceEyeDetector
from .drowsiness_detector import DrowsinessDetector

__all__ = ['FaceEyeDetector', 'DrowsinessDetector']
