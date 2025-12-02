"""
Driver Drowsiness Detection System
Main Entry Point

This is the main application launcher for the Driver Drowsiness Detection System.
It initializes and runs the GUI application.

Author: Dhanarajan K
Project: Driver Drowsiness Detection
"""

import sys
import os

# Determine if running as a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
    # Add the src directory from the bundle to path
    src_path = os.path.join(application_path, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
else:
    # Running as script
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from ui.app import create_app


def check_dependencies():
    """
    Check if all required dependencies are installed.
    
    Returns:
        tuple: (success, missing_packages)
    """
    required_packages = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'scipy': 'scipy',
        'PIL': 'Pillow',
        'pygame': 'pygame',
        'numpy': 'numpy'
    }
    
    missing = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, missing


def print_banner():
    """Print application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     DRIVER DROWSINESS DETECTION SYSTEM                ║
    ║                                                       ║
    ║     Real-time Eye Aspect Ratio (EAR) Monitoring       ║
    ║     With Alert System                                 ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main application entry point."""
    # Setup error logging
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error_log.txt')
    
    # Determine project root
    if getattr(sys, 'frozen', False):
        project_root = sys._MEIPASS
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        print_banner()
        
        print("[INFO] Starting Driver Drowsiness Detection System...")
        print(f"[INFO] Python version: {sys.version}")
        print(f"[INFO] Project root: {project_root}")
        
        # Check dependencies
        print("\n[INFO] Checking dependencies...")
        success, missing = check_dependencies()
        
        if not success:
            print("\n[ERROR] Missing required packages:")
            for package in missing:
                print(f"  - {package}")
            print("\n[INFO] Install missing packages using:")
            print(f"  pip install {' '.join(missing)}")
            print("\n[INFO] Or install all requirements:")
            print("  pip install -r requirements.txt")
            
            input("\nPress Enter to exit...")
            sys.exit(1)
        
            print("[INFO] All dependencies satisfied")
        
        # Create and run the application
        print("\n[INFO] Initializing GUI application...")
        app, root = create_app()
        
        print("[INFO] Application started successfully!")
        print("[INFO] Press the 'Exit' button or close the window to quit.")
        
        # Run the application
        root.mainloop()
        
        print("\n[INFO] Application closed successfully")
        
    except KeyboardInterrupt:
        print("\n[INFO] Application interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        error_msg = f"\n[ERROR] An error occurred: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        
        # Write to log file
        try:
            with open('error_log.txt', 'w') as f:
                f.write(f"Driver Drowsiness Detection - Error Log\n")
                f.write(f"Time: {__import__('datetime').datetime.now()}\n")
                f.write(f"\nError: {e}\n\n")
                f.write(traceback.format_exc())
            print(f"\n[INFO] Error details written to: error_log.txt")
        except:
            pass
        
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
