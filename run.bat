@echo off
REM Run script for Driver Drowsiness Detection System
REM Double-click this file to run the application

echo ====================================================
echo    Driver Drowsiness Detection System
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Check if dependencies are installed
echo [INFO] Checking dependencies...
python -c "import cv2, dlib, scipy, PIL, pygame" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Some dependencies are missing
    echo.
    set /p INSTALL="Would you like to install them now? (Y/N): "
    if /i "%INSTALL%"=="Y" (
        echo.
        echo [INFO] Installing dependencies...
        pip install -r requirements.txt
        echo.
    ) else (
        echo.
        echo [INFO] Please install dependencies manually:
        echo   pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo [INFO] All dependencies satisfied
echo.

REM Check for required assets
if not exist "assets\shape_predictor_68_face_landmarks.dat" (
    echo [WARNING] Facial landmark model not found!
    echo.
    echo Please download shape_predictor_68_face_landmarks.dat from:
    echo http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    echo.
    echo Extract and place it in the 'assets' folder
    echo.
    pause
)

if not exist "assets\alarm.wav" (
    echo [WARNING] Alarm sound not found!
    echo.
    set /p GENERATE="Would you like to generate a basic alarm sound? (Y/N): "
    if /i "%GENERATE%"=="Y" (
        echo.
        echo [INFO] Generating alarm sound...
        cd assets
        python generate_alarm.py
        cd ..
        echo.
    )
)

echo [INFO] Starting application...
echo.
echo Press Ctrl+C or close the window to exit
echo.

REM Run the application
python src\main.py

echo.
echo [INFO] Application closed
echo.
pause
