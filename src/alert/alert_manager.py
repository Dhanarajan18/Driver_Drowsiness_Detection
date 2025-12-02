"""
Alert Manager Module
Handles audio alerts and warning notifications
"""

import os
import time
import threading
import config

# Try to import pygame for audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("[WARNING] pygame not available. Audio alerts will not work.")
    print("[WARNING] Install pygame: pip install pygame")


class AlertManager:
    """
    Manages audio alerts and warning notifications for drowsiness detection.
    Uses pygame for cross-platform audio playback.
    """
    
    def __init__(self, alarm_sound_path=None):
        """
        Initialize the alert manager.
        
        Args:
            alarm_sound_path: Path to the alarm sound file
        """
        self.alarm_sound_path = alarm_sound_path or config.ALARM_SOUND_PATH
        self.is_playing = False
        self.last_alert_time = 0
        self.alert_count = 0
        self.pygame_initialized = False
        
        # Initialize pygame mixer if available
        if PYGAME_AVAILABLE:
            self._initialize_pygame()
        else:
            print("[WARNING] Alert manager running without audio support")
    
    def _initialize_pygame(self):
        """Initialize pygame mixer for audio playback."""
        try:
            pygame.mixer.init()
            self.pygame_initialized = True
            print("[INFO] Audio system initialized successfully")
            
            # Check if alarm file exists
            if os.path.exists(self.alarm_sound_path):
                print(f"[INFO] Alarm sound loaded from: {self.alarm_sound_path}")
            else:
                print(f"[WARNING] Alarm sound file not found: {self.alarm_sound_path}")
                print("[WARNING] Alert manager will work without sound")
                
        except Exception as e:
            print(f"[ERROR] Failed to initialize audio system: {e}")
            self.pygame_initialized = False
    
    def play_alert(self, force=False):
        """
        Play the alert sound.
        
        Args:
            force: If True, bypass cooldown period
            
        Returns:
            bool: True if alert was played, False otherwise
        """
        current_time = time.time()
        
        # Check cooldown period
        if not force and (current_time - self.last_alert_time) < config.ALERT_COOLDOWN:
            return False
        
        # Play sound in a separate thread to avoid blocking
        if self.pygame_initialized and os.path.exists(self.alarm_sound_path):
            thread = threading.Thread(target=self._play_sound_thread)
            thread.daemon = True
            thread.start()
        else:
            # Fallback: just print alert
            self._console_alert()
        
        self.last_alert_time = current_time
        self.alert_count += 1
        
        return True
    
    def _play_sound_thread(self):
        """Play sound in a separate thread."""
        try:
            self.is_playing = True
            
            # Load and play the sound
            pygame.mixer.music.load(self.alarm_sound_path)
            pygame.mixer.music.set_volume(config.ALERT_VOLUME)
            pygame.mixer.music.play()
            
            # Wait for sound to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            self.is_playing = False
            
        except Exception as e:
            print(f"[ERROR] Failed to play alert sound: {e}")
            self.is_playing = False
            self._console_alert()
    
    def _console_alert(self):
        """Print alert to console as fallback."""
        print("=" * 50)
        print("⚠️  DROWSINESS ALERT! ⚠️")
        print("=" * 50)
    
    def stop_alert(self):
        """Stop the currently playing alert."""
        if self.pygame_initialized:
            try:
                pygame.mixer.music.stop()
                self.is_playing = False
            except Exception as e:
                print(f"[ERROR] Failed to stop alert: {e}")
    
    def is_alert_playing(self):
        """
        Check if an alert is currently playing.
        
        Returns:
            bool: True if alert is playing, False otherwise
        """
        return self.is_playing
    
    def get_alert_count(self):
        """
        Get the total number of alerts played.
        
        Returns:
            int: Total alert count
        """
        return self.alert_count
    
    def reset_count(self):
        """Reset the alert counter."""
        self.alert_count = 0
        print("[INFO] Alert count reset")
    
    def test_alert(self):
        """Test the alert system by playing the sound once."""
        print("[INFO] Testing alert system...")
        if self.pygame_initialized and os.path.exists(self.alarm_sound_path):
            self.play_alert(force=True)
            return True
        else:
            print("[ERROR] Cannot test alert - audio system not available")
            self._console_alert()
            return False
    
    def set_volume(self, volume):
        """
        Set the alert volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.pygame_initialized:
            try:
                volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
                pygame.mixer.music.set_volume(volume)
                print(f"[INFO] Alert volume set to {volume}")
            except Exception as e:
                print(f"[ERROR] Failed to set volume: {e}")
    
    def cleanup(self):
        """Clean up audio resources."""
        if self.pygame_initialized:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                print("[INFO] Alert manager cleaned up")
            except Exception as e:
                print(f"[ERROR] Error during cleanup: {e}")
