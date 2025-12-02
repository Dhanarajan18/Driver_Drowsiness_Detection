"""
GUI Application Module
Tkinter-based user interface for Driver Drowsiness Detection System
"""

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time
import config
from src.detection.face_eye_detector import FaceEyeDetector
from src.detection.drowsiness_detector import DrowsinessDetector
from src.alert.alert_manager import AlertManager


class DrowsinessDetectionApp:
    """
    Main GUI application for drowsiness detection.
    Displays webcam feed with overlays and detection status.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize detection components
        self.face_detector = FaceEyeDetector()
        self.drowsiness_detector = DrowsinessDetector()
        self.alert_manager = AlertManager()
        
        # Video capture
        self.video_capture = None
        self.is_running = False
        self.processing_thread = None
        
        # Current frame data
        self.current_frame = None
        self.current_ear = 0.0
        self.fps = 0
        self.last_fps_time = time.time()
        self.frame_count = 0
        
        # Build the GUI
        self._build_gui()
        
        # Start video capture
        self.start_video()
    
    def _build_gui(self):
        """Build the GUI layout."""
        # Configure grid weights
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Left panel - Video feed
        self._build_video_panel()
        
        # Right panel - Status and controls
        self._build_control_panel()
        
        # Bottom status bar
        self._build_status_bar()
    
    def _build_video_panel(self):
        """Build the video display panel."""
        video_frame = ttk.LabelFrame(self.root, text="Live Video Feed", padding=10)
        video_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Video label
        self.video_label = ttk.Label(video_frame)
        self.video_label.pack(expand=True)
    
    def _build_control_panel(self):
        """Build the control and status panel."""
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Status section
        status_frame = ttk.LabelFrame(control_frame, text="Detection Status", padding=10)
        status_frame.pack(fill="x", pady=5)
        
        self.status_label = ttk.Label(
            status_frame, 
            text="ACTIVE", 
            font=(config.FONT_FAMILY, 24, "bold"),
            foreground="green"
        )
        self.status_label.pack(pady=10)
        
        # EAR Display
        ear_frame = ttk.LabelFrame(control_frame, text="Eye Aspect Ratio", padding=10)
        ear_frame.pack(fill="x", pady=5)
        
        self.ear_value_label = ttk.Label(
            ear_frame,
            text="0.00",
            font=(config.FONT_FAMILY, 32, "bold")
        )
        self.ear_value_label.pack()
        
        self.ear_threshold_label = ttk.Label(
            ear_frame,
            text=f"Threshold: {config.EAR_THRESHOLD}",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL)
        )
        self.ear_threshold_label.pack()
        
        # Progress bar
        ttk.Label(ear_frame, text="Drowsiness Progress:").pack(pady=(10, 0))
        self.progress_bar = ttk.Progressbar(
            ear_frame,
            mode='determinate',
            maximum=100
        )
        self.progress_bar.pack(fill="x", pady=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(control_frame, text="Statistics", padding=10)
        stats_frame.pack(fill="x", pady=5)
        
        self.fps_label = ttk.Label(stats_frame, text="FPS: 0")
        self.fps_label.pack(anchor="w")
        
        self.alert_count_label = ttk.Label(stats_frame, text="Alerts: 0")
        self.alert_count_label.pack(anchor="w")
        
        self.events_label = ttk.Label(stats_frame, text="Events: 0")
        self.events_label.pack(anchor="w")
        
        # Controls
        controls_frame = ttk.LabelFrame(control_frame, text="Controls", padding=10)
        controls_frame.pack(fill="x", pady=5)
        
        ttk.Button(
            controls_frame,
            text="Reset Statistics",
            command=self.reset_statistics
        ).pack(fill="x", pady=2)
        
        ttk.Button(
            controls_frame,
            text="Test Alert",
            command=self.test_alert
        ).pack(fill="x", pady=2)
        
        ttk.Button(
            controls_frame,
            text="Exit",
            command=self.on_closing
        ).pack(fill="x", pady=2)
    
    def _build_status_bar(self):
        """Build the bottom status bar."""
        status_bar_frame = ttk.Frame(self.root)
        status_bar_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.status_bar_label = ttk.Label(
            status_bar_frame,
            text="Initializing...",
            relief=tk.SUNKEN,
            anchor="w"
        )
        self.status_bar_label.pack(fill="x", padx=5, pady=2)
    
    def start_video(self):
        """Start video capture and processing."""
        try:
            self.video_capture = cv2.VideoCapture(config.CAMERA_INDEX)
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
            
            if not self.video_capture.isOpened():
                raise Exception("Could not open webcam")
            
            self.is_running = True
            
            # MediaPipe is always ready (no external model file needed)
            self.status_bar_label.config(text="System ready - Monitoring active (MediaPipe)")

            
            # Start processing thread
            self.processing_thread = threading.Thread(target=self.process_video, daemon=True)
            self.processing_thread.start()
            
            # Start GUI update loop
            self.update_gui()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start video capture:\n{str(e)}")
            self.on_closing()
    
    def process_video(self):
        """Process video frames in a separate thread."""
        while self.is_running:
            try:
                ret, frame = self.video_capture.read()
                
                if not ret:
                    print("[ERROR] Failed to read frame from webcam")
                    continue
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame
                self.process_frame(frame)
                
                # Calculate FPS
                self.frame_count += 1
                if time.time() - self.last_fps_time >= 1.0:
                    self.fps = self.frame_count
                    self.frame_count = 0
                    self.last_fps_time = time.time()
                
            except Exception as e:
                print(f"[ERROR] Error processing frame: {e}")
                time.sleep(0.1)
    
    def process_frame(self, frame):
        """
        Process a single frame for drowsiness detection.
        
        Args:
            frame: Input video frame
        """
        # Detect faces
        faces = self.face_detector.detect_faces(frame)
        
        ear_value = None
        
        if len(faces) > 0:
            # Process the first detected face (MediaPipe results)
            face_results = faces[0]
            
            # Get facial landmarks
            landmarks = self.face_detector.get_facial_landmarks(frame, face_results)
            
            if landmarks is not None:
                # Draw face rectangle
                self.face_detector.draw_face_rectangle(frame, landmarks, config.COLOR_GREEN)
                
                # Calculate EAR
                ear_value = self.face_detector.calculate_average_ear(landmarks)
                
                # Draw eye landmarks
                self.face_detector.draw_eye_contours(frame, landmarks, config.COLOR_GREEN, 2)
                self.face_detector.draw_eye_landmarks(frame, landmarks, config.COLOR_YELLOW, 2)
                
                # Update drowsiness detector
                is_drowsy = self.drowsiness_detector.update(ear_value)
                
                # Display EAR on frame
                cv2.putText(
                    frame,
                    f"EAR: {ear_value:.3f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    config.COLOR_GREEN,
                    2
                )
                
                # Check if alert should be played
                if self.drowsiness_detector.should_play_alert():
                    self.alert_manager.play_alert()
                
                # Draw drowsiness warning
                if is_drowsy:
                    cv2.putText(
                        frame,
                        "DROWSINESS DETECTED!",
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        config.COLOR_RED,
                        3
                    )
                    
                    # Draw red overlay
                    overlay = frame.copy()
                    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), config.COLOR_RED, -1)
                    cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)
        else:
            # No face detected
            cv2.putText(
                frame,
                "No face detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                config.COLOR_RED,
                2
            )
        
        # Store current frame and EAR
        self.current_frame = frame
        self.current_ear = ear_value if ear_value is not None else 0.0
    
    def update_gui(self):
        """Update GUI elements with current data."""
        if not self.is_running:
            return
        
        # Update video display
        if self.current_frame is not None:
            # Convert frame to RGB for Tkinter
            frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image=image)
            
            self.video_label.config(image=photo)
            self.video_label.image = photo
        
        # Update status
        status = self.drowsiness_detector.get_status()
        
        if status['is_drowsy']:
            self.status_label.config(text="DROWSY", foreground="red")
        else:
            self.status_label.config(text="ACTIVE", foreground="green")
        
        # Update EAR display
        self.ear_value_label.config(text=f"{self.current_ear:.3f}")
        
        # Update progress bar
        self.progress_bar['value'] = status['progress']
        
        # Update statistics
        self.fps_label.config(text=f"FPS: {self.fps}")
        self.alert_count_label.config(text=f"Alerts: {self.alert_manager.get_alert_count()}")
        self.events_label.config(text=f"Events: {status['total_events']}")
        
        # Schedule next update
        self.root.after(config.UI_UPDATE_INTERVAL, self.update_gui)
    
    def reset_statistics(self):
        """Reset all statistics."""
        self.drowsiness_detector.reset_statistics()
        self.alert_manager.reset_count()
        self.status_bar_label.config(text="Statistics reset")
    
    def test_alert(self):
        """Test the alert system."""
        self.alert_manager.test_alert()
    
    def on_closing(self):
        """Handle window closing event."""
        self.is_running = False
        
        # Wait for processing thread to finish
        if self.processing_thread is not None:
            self.processing_thread.join(timeout=1.0)
        
        # Release resources
        if self.video_capture is not None:
            self.video_capture.release()
        
        # Cleanup MediaPipe resources
        self.face_detector.cleanup()
        
        self.alert_manager.cleanup()
        
        # Destroy window
        self.root.destroy()


def create_app():
    """
    Create and return the application instance.
    
    Returns:
        DrowsinessDetectionApp: Application instance
    """
    root = tk.Tk()
    app = DrowsinessDetectionApp(root)
    return app, root
