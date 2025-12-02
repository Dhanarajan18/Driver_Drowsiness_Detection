# -*- mode: python ; coding: utf-8 -*-
import os
import mediapipe

block_cipher = None

# Get MediaPipe modules path
mediapipe_path = os.path.dirname(mediapipe.__file__)
mediapipe_modules = os.path.join(mediapipe_path, 'modules')

# Define all source files explicitly
a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets\\alarm.wav', 'assets'),
        ('config.py', '.'),
        (mediapipe_modules, 'mediapipe/modules'),
    ],
    hiddenimports=[
        'mediapipe',
        'cv2',
        'scipy',
        'scipy.spatial',
        'scipy.spatial.distance',
        'pygame',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'numpy',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        '_tkinter',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add all Python files from src directory
a.datas += Tree('src', prefix='src')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DrowsinessDetection',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if you have one
)