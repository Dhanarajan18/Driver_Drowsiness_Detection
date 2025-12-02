# 🚗 Driver Drowsiness Detection System

A real-time computer vision application that detects driver drowsiness using Eye Aspect Ratio (EAR) analysis and alerts the driver when drowsiness is detected.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Building Executable](#building-executable)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Driver Drowsiness Detection System is a production-ready desktop application designed to prevent accidents caused by driver fatigue. It uses computer vision techniques to monitor the driver's eyes in real-time and triggers an alarm when signs of drowsiness are detected.

### Key Technologies
- **OpenCV**: Real-time video processing
- **MediaPipe**: 468-point facial landmark detection (Google)
- **Tkinter**: Cross-platform GUI
- **pygame**: Audio alert system
- **NumPy/SciPy**: Numerical computations

## ✨ Features

- ✅ **Real-time Detection**: Processes webcam feed at ~30 FPS
- 👁️ **Eye Aspect Ratio (EAR)**: Scientific metric for eye closure detection
- 🔔 **Audio Alerts**: Plays alarm sound when drowsiness detected
- 📊 **Live Statistics**: FPS, EAR value, event count, alert count
- 🎨 **Visual Overlays**: Face box, eye landmarks, drowsiness warning
- 🎛️ **Interactive GUI**: Status display, progress bar, control buttons
- ⚙️ **Configurable**: Adjust thresholds and parameters easily
- 📦 **Standalone Executable**: Build Windows .exe for easy distribution
- 🛡️ **Fail-safe**: Handles missing camera gracefully
- ⚡ **Easy Setup**: No external model files needed (MediaPipe is self-contained)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Driver Drowsiness Detection              │
│                         Main Application                     │
└─────────────────────────────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
        ┌───────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
        │ Video Input  │ │   GUI    │ │   Alert    │
        │  (OpenCV)    │ │ (Tkinter)│ │  (pygame)  │
        └───────┬──────┘ └────┬─────┘ └─────▲──────┘
                │              │              │
        ┌───────▼──────────────▼──────┐      │
        │   Face & Eye Detector        │      │
        │   (MediaPipe 468 landmarks)  │      │
        └───────┬──────────────────────┘      │
                │                             │
        ┌───────▼──────────────────────┐      │
        │   EAR Calculation            │      │
        │   (Scipy Distance)           │      │
        └───────┬──────────────────────┘      │
                │                             │
        ┌───────▼──────────────────────┐      │
        │   Drowsiness Detector        │      │
        │   (State Machine)            │──────┘
        └──────────────────────────────┘
```

### Project Structure

```
Driver_Drowsiness_Detection/
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   │
│   ├── detection/
│   │   ├── __init__.py
│   │   ├── face_eye_detector.py   # Facial landmarks & EAR
│   │   └── drowsiness_detector.py # Drowsiness logic
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   └── app.py                 # Tkinter GUI
│   │
│   └── alert/
│       ├── __init__.py
│       └── alert_manager.py       # Audio alert system
│
├── assets/
│   ├── README.md                  # Asset instructions
│   ├── generate_alarm.py          # Alarm sound generator
│   └── alarm.wav                  # Alert sound (to be generated)
│
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
├── DrowsinessDetection.spec       # PyInstaller spec file
├── BUILD.md                       # Build instructions
├── MEDIAPIPE_UPGRADE.md           # MediaPipe migration guide
└── README.md                      # This file
```

## 🔧 Installation

### Prerequisites

- **Python 3.7+** (Recommended: Python 3.9 or 3.10)
- **Webcam** (built-in or external)
- **Windows OS** (or compatible platform)

### Step 1: Clone or Download the Repository

```powershell
git clone https://github.com/Dhanarajan18/Driver_Drowsiness_Detection.git
cd Driver_Drowsiness_Detection
```

### Step 2: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

**That's it!** All dependencies (including MediaPipe) install easily with no special configuration needed.

### Step 3: Generate Alarm Sound

**Good news:** No facial model download needed! MediaPipe is self-contained.

**Option 1 - Generate (Recommended):**
```powershell
cd assets
python generate_alarm.py
```

**Option 2 - Download:**
- Download a free alarm sound from [Freesound](https://freesound.org/) or [Mixkit](https://mixkit.co/free-sound-effects/alarm/)
- Save as `alarm.wav` in the `assets/` folder

**Option 3 - Use Windows Sound:**
```powershell
copy C:\Windows\Media\Alarm01.wav assets\alarm.wav
```

## 🚀 Usage

### Running in Development Mode

```powershell
python src\main.py
```

Or:

```powershell
cd src
python main.py
```

### Using the Application

1. **Start**: Launch the application - your webcam will activate
2. **Position**: Sit in front of the camera with your face visible
3. **Monitor**: The system displays:
   - Live video feed with overlays
   - Current EAR value
   - Detection status (ACTIVE/DROWSY)
   - Progress bar showing drowsiness progression
   - Statistics (FPS, alerts, events)
4. **Alert**: When drowsiness is detected, an alarm plays and a red warning appears
5. **Controls**:
   - **Reset Statistics**: Clear event counters
   - **Test Alert**: Preview the alarm sound
   - **Exit**: Close the application

### GUI Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Driver Drowsiness Detection System                         │
├─────────────────────────────────┬───────────────────────────┤
│                                 │  Detection Status         │
│                                 │  ┌─────────────────────┐  │
│                                 │  │      ACTIVE         │  │
│      Live Video Feed            │  └─────────────────────┘  │
│    (with overlays)              │                           │
│                                 │  Eye Aspect Ratio         │
│                                 │  ┌─────────────────────┐  │
│                                 │  │       0.285         │  │
│                                 │  │  Threshold: 0.25    │  │
│                                 │  │  [Progress Bar]     │  │
│                                 │  └─────────────────────┘  │
│                                 │                           │
│                                 │  Statistics               │
│                                 │  - FPS: 30                │
│                                 │  - Alerts: 0              │
│                                 │  - Events: 0              │
│                                 │                           │
│                                 │  Controls                 │
│                                 │  [Reset Statistics]       │
│                                 │  [Test Alert]             │
│                                 │  [Exit]                   │
└─────────────────────────────────┴───────────────────────────┘
│ Status: System ready - Monitoring active                    │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Building Executable

Create a standalone Windows executable that can run without Python installed.

### Quick Build

```powershell
pyinstaller DrowsinessDetection.spec
```

The executable will be in `dist\DrowsinessDetection.exe`

### Detailed Instructions

See [BUILD.md](BUILD.md) for complete build instructions, troubleshooting, and customization options.

## ⚙️ Configuration

Edit `config.py` to customize behavior:

```python
# Detection thresholds
EAR_THRESHOLD = 0.25              # Lower = more sensitive
EAR_CONSECUTIVE_FRAMES = 20       # Frames before alert (~0.67s at 30 FPS)

# Camera settings
CAMERA_INDEX = 0                  # Change if using external webcam
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Alert settings
ALERT_COOLDOWN = 2.0              # Seconds between alerts
ALERT_VOLUME = 1.0                # 0.0 to 1.0
```

### Adjusting Sensitivity

- **More Sensitive**: Lower `EAR_THRESHOLD` (e.g., 0.23)
- **Less Sensitive**: Raise `EAR_THRESHOLD` (e.g., 0.27)
- **Faster Alert**: Lower `EAR_CONSECUTIVE_FRAMES` (e.g., 15)
- **Slower Alert**: Raise `EAR_CONSECUTIVE_FRAMES` (e.g., 30)

## 🔬 How It Works

### Eye Aspect Ratio (EAR)

The system uses the Eye Aspect Ratio metric from the paper:
["Real-Time Eye Blink Detection using Facial Landmarks"](http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf) by Soukupová and Čech (2016).

**Formula:**

```
        ||p2 - p6|| + ||p3 - p5||
EAR = ───────────────────────────
            2 * ||p1 - p4||
```

Where `p1-p6` are the 6 facial landmarks around one eye.

**Interpretation:**
- Open eye: EAR ≈ 0.3
- Closed eye: EAR ≈ 0.1-0.15
- Threshold: 0.25 (configurable)

### Detection Algorithm

1. **Face Detection**: Detect face using dlib's HOG-based detector
2. **Landmark Detection**: Identify 68 facial landmarks
3. **Eye Extraction**: Extract points for left eye (42-47) and right eye (36-41)
4. **EAR Calculation**: Compute EAR for both eyes
5. **Averaging**: Average the left and right EAR values
6. **Threshold Check**: Compare against threshold (default: 0.25)
7. **Frame Counting**: Count consecutive frames below threshold
8. **Alert Trigger**: If count exceeds threshold (default: 20 frames), trigger alert

### State Machine

```
          EAR > threshold
┌──────┐ ─────────────────> ┌────────┐
│ OPEN │                    │ CLOSED │
│ EYES │ <───────────────── │  EYES  │
└──────┘  EAR < threshold   └────────┘
                                  │
                                  │ counter >= 20
                                  ▼
                             ┌─────────┐
                             │ DROWSY  │
                             │  ALERT  │
                             └─────────┘
```

## 📸 Screenshots

### Normal Operation
*(Placeholder: Add screenshot showing normal detection with open eyes)*

### Drowsiness Detection
*(Placeholder: Add screenshot showing red alert with closed eyes)*

### GUI Interface
*(Placeholder: Add screenshot of full application window)*

## 🔧 Troubleshooting

### Camera Not Working

**Problem:** "Could not open webcam" error

**Solutions:**
- Check if camera is being used by another application
- Change `CAMERA_INDEX` in `config.py` (try 0, 1, 2)
- Grant camera permissions to Python

### Model File Not Found

**Problem:** "Shape predictor not loaded" warning

**Solution:**
- Download `shape_predictor_68_face_landmarks.dat.bz2`
- Extract and place in `assets/` folder
- See [Installation](#step-3-download-required-assets)

### No Sound

**Problem:** Alert doesn't play sound

**Solutions:**
- Check if `alarm.wav` exists in `assets/` folder
- Verify system volume is not muted
- Run alarm generator: `python assets\generate_alarm.py`
- Install pygame: `pip install pygame`

### Slow Performance

**Problem:** Low FPS or laggy video

**Solutions:**
- Reduce `CAMERA_WIDTH` and `CAMERA_HEIGHT` in `config.py`
- Set `FRAME_SKIP = 1` to process every other frame
- Close other applications using camera/CPU
- Use a faster computer

### Import Errors

**Problem:** `ModuleNotFoundError` or `ImportError`

**Solution:**
```powershell
pip install -r requirements.txt --upgrade
```

### dlib Installation Fails

**Problem:** Error installing dlib on Windows

**Solutions:**

**Option 1:** Install Visual Studio Build Tools
1. Download [VS Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
2. Install "Desktop development with C++"
3. Retry: `pip install dlib`

**Option 2:** Use pre-compiled wheel
```powershell
# For Python 3.9, 64-bit
pip install https://github.com/sachadee/Dlib/raw/main/dlib-19.22.99-cp39-cp39-win_amd64.whl
```

**Option 3:** Use Anaconda
```powershell
conda install -c conda-forge dlib
```

## 🚀 Future Improvements

- [ ] Add yawn detection using mouth aspect ratio
- [ ] Implement head pose estimation for distraction detection
- [ ] Add data logging and analytics dashboard
- [ ] Support for multiple camera sources
- [ ] Mobile app version (Android/iOS)
- [ ] Cloud-based monitoring for fleet management
- [ ] Integration with vehicle systems (CAN bus)
- [ ] Machine learning model for personalized thresholds
- [ ] Night vision support with IR camera
- [ ] Multi-language support
- [ ] Customizable alert sounds
- [ ] Email/SMS notifications
- [ ] Driver identification and profiles
- [ ] Fatigue trend analysis over time

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup

```powershell
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Driver_Drowsiness_Detection.git

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Dhanarajan K**
- GitHub: [@Dhanarajan18](https://github.com/Dhanarajan18)

## 🙏 Acknowledgments

- **dlib**: Davis King for the excellent facial landmark detection library
- **OpenCV**: For comprehensive computer vision tools
- **Soukupová & Čech**: For the EAR algorithm research paper
- **Tkinter**: For the built-in Python GUI framework
- **pygame**: For cross-platform audio support

## 📚 References

1. Soukupová, T., & Čech, J. (2016). Real-Time Eye Blink Detection using Facial Landmarks. In CVWW (pp. 1-8).
2. [dlib Documentation](http://dlib.net/)
3. [OpenCV Documentation](https://docs.opencv.org/)
4. [Eye Aspect Ratio Research](http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)

## 📞 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search [existing issues](https://github.com/Dhanarajan18/Driver_Drowsiness_Detection/issues)
3. Open a [new issue](https://github.com/Dhanarajan18/Driver_Drowsiness_Detection/issues/new)

---

**⚠️ Disclaimer:** This system is designed as a driver assistance tool and should not replace proper rest and safe driving practices. Always ensure adequate sleep before driving long distances.

**Made with ❤️ for road safety**
