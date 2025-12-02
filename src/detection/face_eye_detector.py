"""
Face and Eye Detection Module
Handles facial landmark detection and Eye Aspect Ratio (EAR) calculation using MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import config


class FaceEyeDetector:
    """
    Detects faces and eyes in video frames and calculates Eye Aspect Ratio (EAR).
    Uses MediaPipe's Face Mesh for 468-point facial landmark detection.
    """
    
    def __init__(self):
        """Initialize the face and eye detector with MediaPipe."""
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.predictor_loaded = True
        
        # MediaPipe landmark indices for eyes
        # Left eye indices (6 points)
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        # Right eye indices (6 points)
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        print(f"[INFO] MediaPipe Face Mesh initialized successfully")
    
    def detect_faces(self, frame):
        """
        Detect faces in the given frame.
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            list: List of detected faces (MediaPipe results)
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.face_mesh.process(rgb_frame)
        
        # Return results (will be None if no face detected)
        return [results] if results.multi_face_landmarks else []
    
    def get_facial_landmarks(self, frame, face_results):
        """
        Get facial landmarks for a detected face.
        
        Args:
            frame: Input image frame (BGR format)
            face_results: MediaPipe face mesh results
            
        Returns:
            numpy.ndarray: Array of (x, y) coordinates for facial landmarks
            None: If no landmarks found
        """
        if not face_results or not face_results.multi_face_landmarks:
            return None
        
        # Get first face landmarks
        face_landmarks = face_results.multi_face_landmarks[0]
        
        # Convert to pixel coordinates
        h, w = frame.shape[:2]
        landmarks = []
        
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            landmarks.append([x, y])
        
        return np.array(landmarks)
    
    def calculate_ear(self, eye_landmarks):
        """
        Calculate Eye Aspect Ratio (EAR) for a single eye.
        
        EAR Formula:
        EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
        
        Where p1-p6 are the 6 facial landmarks for one eye.
        
        Args:
            eye_landmarks: Array of 6 (x,y) coordinates for eye landmarks
            
        Returns:
            float: Eye Aspect Ratio value
        """
        # Compute the euclidean distances between the vertical eye landmarks
        vertical_1 = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
        vertical_2 = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
        
        # Compute the euclidean distance between the horizontal eye landmarks
        horizontal = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
        
        # Calculate the eye aspect ratio
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        
        return ear
    
    def get_eye_landmarks(self, landmarks):
        """
        Extract left and right eye landmarks from full facial landmarks.
        
        Args:
            landmarks: Full MediaPipe facial landmarks (468 points)
            
        Returns:
            tuple: (left_eye, right_eye) landmark arrays
        """
        if landmarks is None:
            return None, None
        
        # Extract eye landmarks using MediaPipe indices
        left_eye = np.array([landmarks[i] for i in self.LEFT_EYE])
        right_eye = np.array([landmarks[i] for i in self.RIGHT_EYE])
        
        return left_eye, right_eye
    
    def calculate_average_ear(self, landmarks):
        """
        Calculate the average EAR for both eyes.
        
        Args:
            landmarks: Full MediaPipe facial landmarks
            
        Returns:
            float: Average EAR value
            None: If landmarks are not available
        """
        if landmarks is None:
            return None
        
        # Get eye landmarks
        left_eye, right_eye = self.get_eye_landmarks(landmarks)
        
        # Calculate EAR for each eye
        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)
        
        # Return average EAR
        return (left_ear + right_ear) / 2.0
    
    def draw_face_rectangle(self, frame, landmarks, color=config.COLOR_GREEN, thickness=2):
        """
        Draw a rectangle around the detected face.
        
        Args:
            frame: Input image frame
            landmarks: Facial landmarks array
            color: BGR color tuple
            thickness: Line thickness
        """
        if landmarks is None:
            return
        
        # Get face bounding box from landmarks
        x_coords = landmarks[:, 0]
        y_coords = landmarks[:, 1]
        
        x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
        y_min, y_max = int(np.min(y_coords)), int(np.max(y_coords))
        
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, thickness)
    
    def draw_eye_landmarks(self, frame, landmarks, color=config.COLOR_GREEN, radius=2):
        """
        Draw circles on eye landmark points.
        
        Args:
            frame: Input image frame
            landmarks: Full facial landmarks
            color: BGR color tuple
            radius: Circle radius
        """
        if landmarks is None:
            return
        
        # Draw left eye landmarks
        for idx in self.LEFT_EYE:
            cv2.circle(frame, tuple(landmarks[idx]), radius, color, -1)
        
        # Draw right eye landmarks
        for idx in self.RIGHT_EYE:
            cv2.circle(frame, tuple(landmarks[idx]), radius, color, -1)
    
    def draw_eye_contours(self, frame, landmarks, color=config.COLOR_GREEN, thickness=1):
        """
        Draw contours around the eyes.
        
        Args:
            frame: Input image frame
            landmarks: Full facial landmarks
            color: BGR color tuple
            thickness: Line thickness
        """
        if landmarks is None:
            return
        
        left_eye, right_eye = self.get_eye_landmarks(landmarks)
        
        # Draw contours
        cv2.polylines(frame, [left_eye], True, color, thickness)
        cv2.polylines(frame, [right_eye], True, color, thickness)
    
    def is_model_loaded(self):
        """
        Check if the facial landmark predictor model is loaded.
        
        Returns:
            bool: True if model is loaded, False otherwise
        """
        return self.predictor_loaded
    
    def cleanup(self):
        """Release MediaPipe resources."""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
            print("[INFO] MediaPipe Face Mesh resources released")
