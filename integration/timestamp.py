import os
import json
from datetime import datetime

IMAGE_DIR = "/home/admin/dp/cam/timelapse_images"
TIMESTAMP_FILE = os.path.join(IMAGE_DIR, "image_timestamps.json")

def load_timestamps():
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_timestamps(timestamps):
    with open(TIMESTAMP_FILE, 'w') as f:
        json.dump(timestamps, f, indent=2)

def update_timestamp(image_filename, timestamp):
    timestamps = load_timestamps()
    timestamps[image_filename] = timestamp
    save_timestamps(timestamps)

def generate_timestamps_for_existing_images():
    timestamps = {}
    for filename in os.listdir(IMAGE_DIR):
        if filename.startswith("image_") and filename.endswith(".jpg"):
            # Extract timestamp from filename
            timestamp_str = filename[6:-4]  # Remove "image_" prefix and ".jpg" suffix
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S").isoformat()
                timestamps[filename] = timestamp
            except ValueError:
                print(f"Couldn't parse timestamp for file: {filename}")
    save_timestamps(timestamps)
    print(f"Generated timestamps for {len(timestamps)} images")

if __name__ == "__main__":
    generate_timestamps_for_existing_images()