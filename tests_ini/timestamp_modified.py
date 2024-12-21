import os
import json
from datetime import datetime

IMAGE_DIR = "/home/admin/dp/cam/timelapse_images"
TIMESTAMP_FILE = os.path.join(IMAGE_DIR, "image_timestamps.json")


def get_last_modification_time():
    """Get the last modification time of the TIMESTAMP_FILE."""
    if os.path.exists(TIMESTAMP_FILE):
        return datetime.fromtimestamp(os.path.getmtime(TIMESTAMP_FILE))
    return None


def save_timestamps(timestamps):
    """Save the timestamps to the TIMESTAMP_FILE."""
    with open(TIMESTAMP_FILE, 'w') as f:
        json.dump(timestamps, f, indent=2)


def generate_timestamps_for_new_images():
    """Generate timestamps for images added after the last modification of TIMESTAMP_FILE."""
    last_mod_time = get_last_modification_time()
    timestamps = {}

    # Iterate through images in the directory
    for filename in os.listdir(IMAGE_DIR):
        if filename.startswith("image_") and filename.endswith(".jpg"):
            # Extract timestamp from filename
            timestamp_str = filename[6:-4]  # Remove "image_" prefix and ".jpg" suffix
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                if not last_mod_time or timestamp > last_mod_time:
                    timestamps[filename] = timestamp.isoformat()
            except ValueError:
                print(f"Couldn't parse timestamp for file: {filename}")

    # Save only new timestamps
    save_timestamps(timestamps)
    print(f"Generated timestamps for {len(timestamps)} new images")


if __name__ == "__main__":
    generate_timestamps_for_new_images()
