# 🚀 Quick Start Guide

## Get Started in 5 Minutes!

### 1️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note:** MediaPipe installs easily on all platforms - no special steps needed!

### 2️⃣ Generate Alarm Sound

**No facial model download needed!** MediaPipe is included in the dependencies.

#### Create Alarm Sound
```powershell
cd assets
python generate_alarm.py
```

**Or copy a Windows sound:**
```powershell
copy C:\Windows\Media\Alarm01.wav assets\alarm.wav
```

### 3️⃣ Run the Application

```powershell
python src\main.py
```

## ✅ Verification Checklist

Before running, ensure:
- [ ] Python 3.7+ installed
- [ ] All dependencies installed (`pip list`)
- [ ] `assets/shape_predictor_68_face_landmarks.dat` exists
- [ ] `assets/alarm.wav` exists
- [ ] Webcam is connected and not in use by other apps
- [ ] Camera permissions granted to Python

## 🎯 First Run

When you run the application:

1. **GUI Window Opens** → Application started successfully ✓
2. **Webcam Light Turns On** → Camera access granted ✓
3. **Face Box Appears** → Face detection working ✓
4. **Eye Landmarks Visible** → Landmark detection working ✓
5. **EAR Value Updates** → System fully operational ✓

## 🧪 Test the System

1. Click **"Test Alert"** → Should hear alarm sound
2. Close your eyes for 3 seconds → Alert should trigger
3. Check **Statistics Panel** → Should show FPS and counts

## ⚙️ Basic Configuration

Edit `config.py`:

```python
# Make detection more/less sensitive
EAR_THRESHOLD = 0.25          # Lower = more sensitive

# Adjust trigger time (frames at ~30 FPS)
EAR_CONSECUTIVE_FRAMES = 20   # Default: ~0.67 seconds

# Change camera if needed
CAMERA_INDEX = 0              # Try 1, 2 if default doesn't work
```

## 🛠️ Common Issues

### Camera Not Found
```python
# In config.py, change:
CAMERA_INDEX = 1  # Try different numbers
```

### MediaPipe Not Working
```powershell
# Reinstall MediaPipe:
pip uninstall mediapipe
pip install mediapipe==0.10.9
```

### No Alarm Sound
```powershell
# Generate it:
cd assets
python generate_alarm.py

# Or use Windows sound:
copy C:\Windows\Media\Alarm01.wav assets\alarm.wav
```

## 📦 Build Standalone EXE

```powershell
pyinstaller DrowsinessDetection.spec
```

Output: `dist\DrowsinessDetection.exe`

## 📚 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [BUILD.md](BUILD.md) for deployment options
- Customize settings in `config.py`
- Add your own alarm sound

## 💡 Tips

- Sit at normal viewing distance from camera
- Ensure good lighting on your face
- Avoid backlighting (window behind you)
- Adjust `EAR_THRESHOLD` for your eye shape
- Use in well-lit conditions for best accuracy

---

**Need Help?** Check the [Troubleshooting](README.md#troubleshooting) section in README.md
