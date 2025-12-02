"""
Drowsiness Detection Logic Module
Manages the state machine for drowsiness detection based on EAR values
"""

import time
import config


class DrowsinessDetector:
    """
    Detects drowsiness based on Eye Aspect Ratio (EAR) threshold and time duration.
    Maintains a state machine to track consecutive frames with closed eyes.
    """
    
    def __init__(self, ear_threshold=None, consecutive_frames=None):
        """
        Initialize the drowsiness detector.
        
        Args:
            ear_threshold: EAR value below which eyes are considered closed
            consecutive_frames: Number of consecutive frames to trigger alert
        """
        self.ear_threshold = ear_threshold or config.EAR_THRESHOLD
        self.consecutive_frames_threshold = consecutive_frames or config.EAR_CONSECUTIVE_FRAMES
        
        # State tracking
        self.frame_counter = 0
        self.is_drowsy = False
        self.total_drowsy_events = 0
        self.last_alert_time = 0
        
        # History tracking for analytics
        self.ear_history = []
        self.max_history_length = 100
        
        print(f"[INFO] Drowsiness Detector initialized")
        print(f"[INFO] EAR Threshold: {self.ear_threshold}")
        print(f"[INFO] Consecutive Frames: {self.consecutive_frames_threshold}")
    
    def update(self, ear_value):
        """
        Update the drowsiness state based on the current EAR value.
        
        Args:
            ear_value: Current Eye Aspect Ratio value
            
        Returns:
            bool: True if drowsiness is detected, False otherwise
        """
        # Add to history
        self._add_to_history(ear_value)
        
        # Check if EAR is below threshold
        if ear_value is not None and ear_value < self.ear_threshold:
            # Eyes are closed - increment counter
            self.frame_counter += 1
            
            # Check if threshold is exceeded
            if self.frame_counter >= self.consecutive_frames_threshold:
                if not self.is_drowsy:
                    # Just entered drowsy state
                    self.is_drowsy = True
                    self.total_drowsy_events += 1
                    print(f"[ALERT] Drowsiness detected! Event #{self.total_drowsy_events}")
                
                return True
        else:
            # Eyes are open - reset counter
            if self.frame_counter > 0:
                print(f"[INFO] Eyes opened - Frame counter reset from {self.frame_counter}")
            
            self.frame_counter = 0
            self.is_drowsy = False
        
        return False
    
    def _add_to_history(self, ear_value):
        """
        Add EAR value to history for analytics.
        
        Args:
            ear_value: Current EAR value
        """
        if ear_value is not None:
            self.ear_history.append(ear_value)
            
            # Maintain max history length
            if len(self.ear_history) > self.max_history_length:
                self.ear_history.pop(0)
    
    def should_play_alert(self):
        """
        Check if an alert should be played based on cooldown period.
        
        Returns:
            bool: True if alert should be played, False otherwise
        """
        current_time = time.time()
        
        if self.is_drowsy:
            # Check cooldown
            if current_time - self.last_alert_time >= config.ALERT_COOLDOWN:
                self.last_alert_time = current_time
                return True
        
        return False
    
    def get_status(self):
        """
        Get the current detection status.
        
        Returns:
            dict: Dictionary containing current status information
        """
        return {
            'is_drowsy': self.is_drowsy,
            'frame_counter': self.frame_counter,
            'total_events': self.total_drowsy_events,
            'ear_threshold': self.ear_threshold,
            'frames_threshold': self.consecutive_frames_threshold,
            'progress': min(100, (self.frame_counter / self.consecutive_frames_threshold) * 100)
        }
    
    def get_ear_statistics(self):
        """
        Get statistics about recent EAR values.
        
        Returns:
            dict: Dictionary with EAR statistics
        """
        if not self.ear_history:
            return {
                'average': 0,
                'min': 0,
                'max': 0,
                'current': 0
            }
        
        return {
            'average': sum(self.ear_history) / len(self.ear_history),
            'min': min(self.ear_history),
            'max': max(self.ear_history),
            'current': self.ear_history[-1] if self.ear_history else 0
        }
    
    def reset(self):
        """Reset the detector state."""
        self.frame_counter = 0
        self.is_drowsy = False
        self.last_alert_time = 0
        print("[INFO] Drowsiness detector reset")
    
    def reset_statistics(self):
        """Reset all statistics and history."""
        self.reset()
        self.total_drowsy_events = 0
        self.ear_history = []
        print("[INFO] All statistics reset")
    
    def get_frame_progress(self):
        """
        Get the progress towards drowsiness detection.
        
        Returns:
            float: Percentage (0-100) of frames counted towards threshold
        """
        return (self.frame_counter / self.consecutive_frames_threshold) * 100
    
    def set_threshold(self, ear_threshold):
        """
        Update the EAR threshold.
        
        Args:
            ear_threshold: New EAR threshold value
        """
        self.ear_threshold = ear_threshold
        print(f"[INFO] EAR threshold updated to {ear_threshold}")
    
    def set_consecutive_frames(self, consecutive_frames):
        """
        Update the consecutive frames threshold.
        
        Args:
            consecutive_frames: New consecutive frames value
        """
        self.consecutive_frames_threshold = consecutive_frames
        print(f"[INFO] Consecutive frames threshold updated to {consecutive_frames}")
