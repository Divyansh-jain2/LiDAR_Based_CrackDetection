
import time
import csv
import threading
import subprocess
from datetime import datetime
from pathlib import Path
from rplidar import RPLidar

# Set up directories and file paths
save_dir = Path("/home/admin/dp/cam/timelapse_images")
save_dir.mkdir(exist_ok=True)
lidar_csv_file = 'lidar_data_with_timestamp_high.csv'

# LiDAR setup
lidar = RPLidar('COM5')

def capture_image():
    """Captures an image and saves it to the specified directory"""
    while True:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.jpg"
        output_path = save_dir / filename
        latest_path = save_dir / "latest.jpg"

        try:
            result = subprocess.run(
                ["rpicam-still", "-o", str(output_path), "-n"],
                capture_output=True, text=True, check=True
            )
            print(f"Image captured: {output_path}")

            # Create a symbolic link to the latest image
            if latest_path.exists():
                latest_path.unlink()
            latest_path.symlink_to(output_path)

        except subprocess.CalledProcessError as e:
            print(f"Failed to capture image: {e}")

        time.sleep(3)  # Wait for 3 seconds before the next capture

def record_lidar_data():
    """Records LiDAR data to a CSV file with timestamps"""
    # Open the CSV file to write data
    with open(lidar_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Quality', 'Angle (degrees)', 'Distance (mm)'])
        
        try:
            lidar._set_pwm(660)
            for scan in lidar.iter_scans(scan_type="express"):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'Time: {timestamp} | Got {len(scan)} measurements')
                for measurement in scan:
                    quality, angle, distance = measurement
                    writer.writerow([timestamp, quality, angle, distance])

        except KeyboardInterrupt:
            print("Stopping LiDAR recording...")

        finally:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()

def main():
    # Create threads for image capture and LiDAR recording
    image_thread = threading.Thread(target=capture_image)
    lidar_thread = threading.Thread(target=record_lidar_data)

    # Start both threads
    image_thread.start()
    lidar_thread.start()

    # Wait for both threads to complete
    image_thread.join()
    lidar_thread.join()

if __name__ == "__main__":
    main()
