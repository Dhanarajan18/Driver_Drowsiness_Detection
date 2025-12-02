# Build Instructions for Windows Executable

## Prerequisites
1. Install all dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

2. Ensure you have the required asset files:
   - `assets/alarm.wav` (alarm sound)
   - `assets/shape_predictor_68_face_landmarks.dat` (facial landmark model)

## Method 1: Using the Spec File (Recommended)

The spec file is already configured for optimal building.

```powershell
pyinstaller DrowsinessDetection.spec
```

The executable will be created in the `dist` folder.

## Method 2: Using Command Line

### Option A: Single File Executable
```powershell
pyinstaller --onefile --windowed `
  --add-data "assets;assets" `
  --add-data "config.py;." `
  --hidden-import scipy.special.cython_special `
  --hidden-import PIL._tkinter_finder `
  --name DrowsinessDetection `
  src\main.py
```

### Option B: With Console (for debugging)
```powershell
pyinstaller --onefile `
  --add-data "assets;assets" `
  --add-data "config.py;." `
  --hidden-import scipy.special.cython_special `
  --hidden-import PIL._tkinter_finder `
  --name DrowsinessDetection `
  src\main.py
```

## After Building

1. The executable will be in the `dist` folder:
   ```
   dist\DrowsinessDetection.exe
   ```

2. Test the executable:
   ```powershell
   .\dist\DrowsinessDetection.exe
   ```

3. For distribution, copy the entire `dist` folder or just the `.exe` file

## Troubleshooting

### Missing DLL Errors
If you get DLL errors, install Visual C++ Redistributable:
https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads

### Large File Size
The executable will be ~200-300 MB due to:
- OpenCV libraries
- dlib model
- Python runtime

To reduce size, you can use UPX compression (already enabled in spec file).

### Camera Not Working
Make sure the camera is not being used by another application.

### Model File Not Found
Ensure `shape_predictor_68_face_landmarks.dat` is in the `assets` folder before building.

## Clean Build

If you need to rebuild from scratch:

```powershell
# Remove build artifacts
Remove-Item -Recurse -Force build, dist
Remove-Item *.spec

# Rebuild
pyinstaller DrowsinessDetection.spec
```

## Creating an Installer (Optional)

You can use Inno Setup to create a Windows installer:

1. Download Inno Setup: https://jrsoftware.org/isdl.php
2. Create a script to package your executable
3. Build the installer

This will give you a professional `.exe` installer for easy distribution.
