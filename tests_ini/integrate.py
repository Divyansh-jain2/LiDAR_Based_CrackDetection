import json
import csv
import shutil
import os
from datetime import datetime

# Paths
base_path = "/home/admin/dp/integration/runs/seg"
final_results_dir = "/home/admin/dp/integration/finalresults"
json_file = "/home/admin/dp/cam/timelapse_images/image_timestamps.json"
crack_results_file = "/home/admin/dp/integration/crack_detection_results.csv"
output_csv_file = os.path.join(final_results_dir, "true_crack_detection_results.csv")

# Ensure the final results directory exists
os.makedirs(final_results_dir, exist_ok=True)

# Load the image timestamps JSON file
with open(json_file, 'r') as f:
    image_timestamps = json.load(f)

# Load the crack detection results CSV file
crack_detection_results = []
with open(crack_results_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        crack_detection_results.append({
            'timestamp': datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
            'crack_detected': int(row[1])
        })

# Function to check if a crack is detected within 7 seconds
def is_crack_detected_within_7_seconds(image_timestamp, crack_detection_results):
    image_time = datetime.strptime(image_timestamp, '%Y-%m-%dT%H:%M:%S')  # Handle ISO 8601 format
    for result in crack_detection_results:
        if abs((result['timestamp'] - image_time).total_seconds()) <= 7 and result['crack_detected'] == 1:
            return True
    return False

# Prepare the CSV output
output_data = []

# Check each image in the JSON file
for image_name, data in image_timestamps.items():
    if data['crack_detected'] == 1:
        if is_crack_detected_within_7_seconds(data['timestamp'], crack_detection_results):
            output_data.append({
                'image_name': image_name,
                'timestamp': data['timestamp'],
                'true_crack_detected': 1
            })

# Write the output data to a CSV file
with open(output_csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['image_name', 'timestamp', 'true_crack_detected'])
    writer.writeheader()
    writer.writerows(output_data)

print(f"CSV created: {output_csv_file}")

# Get the latest YOLO results directory
latest_dir = max(
    (os.path.join(base_path, d) for d in os.listdir(base_path) if d.startswith("predict")),
    key=os.path.getctime
)

# Create a subdirectory for copied images inside the final results directory
final_images_dir = os.path.join(final_results_dir, "images")
os.makedirs(final_images_dir, exist_ok=True)

# Copy images from the latest directory to the final results directory
with open(output_csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        image_name = row['image_name']
        src = os.path.join(latest_dir, image_name)
        dest = os.path.join(final_images_dir, image_name)

        if os.path.exists(src):
            shutil.copy(src, dest)
            print(f"Copied: {image_name}")
        else:
            print(f"File not found: {image_name}")

print(f"Images and CSV stored in: {final_results_dir}")
