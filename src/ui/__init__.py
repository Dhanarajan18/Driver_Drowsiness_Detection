"""
__init__.py for ui module
Makes the UI package importable
"""

from .app import DrowsinessDetectionApp, create_app

__all__ = ['DrowsinessDetectionApp', 'create_app']
