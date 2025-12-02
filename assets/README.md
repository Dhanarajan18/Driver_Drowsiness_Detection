# Alarm Sound Assets

## Required Files

### 1. alarm.wav
This is the alarm sound file that plays when drowsiness is detected.

## How to Get the Alarm Sound

### Option 1: Download a Free Alarm Sound
1. Visit a free sound library:
   - https://freesound.org/
   - https://mixkit.co/free-sound-effects/alarm/
   - https://www.zapsplat.com/sound-effect-category/alarms/

2. Download a WAV format alarm sound

3. Rename it to `alarm.wav` and place it in this `assets` folder

### Option 2: Generate a Simple Beep Sound (Python)
Run the following Python script to generate a simple beep sound:

```python
import numpy as np
from scipy.io import wavfile

# Parameters
sample_rate = 44100  # 44.1kHz
duration = 1.0  # 1 second
frequency = 1000  # 1000 Hz beep

# Generate beep
t = np.linspace(0, duration, int(sample_rate * duration))
beep = np.sin(2 * np.pi * frequency * t)

# Add fade in/out to avoid clicking
fade_samples = int(sample_rate * 0.05)  # 50ms fade
beep[:fade_samples] *= np.linspace(0, 1, fade_samples)
beep[-fade_samples:] *= np.linspace(1, 0, fade_samples)

# Convert to 16-bit integer
beep_int = (beep * 32767).astype(np.int16)

# Save
wavfile.write('alarm.wav', sample_rate, beep_int)
print("Alarm sound generated: alarm.wav")
```

### Option 3: Use Windows System Sound
You can copy a system sound from:
```
C:\Windows\Media\
```
Look for files like `Alarm01.wav`, `Alarm02.wav`, etc.

## About Face Detection

This project uses **MediaPipe Face Mesh** from Google, which provides:
- ✅ **No external model files needed** - Built into the mediapipe package
- ✅ **468 facial landmarks** - More accurate than traditional methods
- ✅ **Easy installation** - No compilation required
- ✅ **Fast performance** - Optimized for real-time processing
- ✅ **Cross-platform** - Works on Windows, Linux, Mac

**No additional downloads required for face detection!**

## Directory Structure

After setup, your assets folder should contain:
```
assets/
├── README.md (this file)
├── generate_alarm.py
└── alarm.wav (generated or downloaded)
```
