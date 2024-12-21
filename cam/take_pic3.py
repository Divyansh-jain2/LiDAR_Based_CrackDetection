import time
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Set the directory to save images
save_dir = Path("/home/admin/dp/cam/timelapse_images")
save_dir.mkdir(exist_ok=True)

def capture_image():
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate filenames
    filename = f"image_{timestamp}.jpg"
    output_path = save_dir / filename
    latest_path = save_dir / "latest.jpg"

    # Capture the image using the rpicam-still command
    try:
        result = subprocess.run(
            ["rpicam-still", "-o", str(output_path), "-n"],
            capture_output=True, text=True, check=True
        )
        print(f"Image captured: {output_path}")

        # Create a symbolic link to the latest image
        if latest_path.exists():
            latest_path.unlink()  # Remove the existing symlink
        latest_path.symlink_to(output_path)  # Create new symlink to latest image
        
        # Optionally update a timestamp in a JSON file
        update_timestamp(filename, datetime.now().isoformat())

    except subprocess.CalledProcessError as e:
        print(f"Failed to capture image: {e}")

def update_timestamp(filename, timestamp):
    # Placeholder for updating timestamp in JSON file (implementation needed)
    pass

def main():
    try:
        while True:
            capture_image()
            time.sleep(3)  # Wait for 3 seconds before next capture
    except KeyboardInterrupt:
        print("Timelapse capture stopped.")

if __name__ == "__main__":
    main()

