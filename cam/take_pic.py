import time
from datetime import datetime
from pathlib import Path
from rpicam import RPiCamera

# Initialize the camera
camera = RPiCamera()

# Set the directory to save images
save_dir = Path("/home/admin/dp/cam/timelapse_images")
save_dir.mkdir(exist_ok=True)

def capture_image():
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Capture the image
    filename = save_dir / f"image_{timestamp}.jpg"
    camera.capture(str(filename))
    
    print(f"Image captured: {filename}")

def main():
    try:
        while True:
            capture_image()
            time.sleep(3)  # Wait for 3 seconds before next capture
    except KeyboardInterrupt:
        print("Timelapse capture stopped.")
    finally:
        camera.close()

if __name__ == "__main__":
    main()