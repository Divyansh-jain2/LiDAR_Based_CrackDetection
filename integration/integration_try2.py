import json
import csv
import shutil
import os
from datetime import datetime, timedelta

# Load the image timestamps JSON file
with open('cam/timelapse_images/image_timestamps.json', 'r') as f:
    image_timestamps = json.load(f)

# Load the crack detection results CSV file
crack_detection_results = []
with open('LiDAR/LiDAR/crack_detection_results.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        crack_detection_results.append({
            'timestamp': row[0],
            'crack_detected': int(row[1])
        })

# Function to check if a crack is detected within 7 seconds
def is_crack_detected_within_7_seconds(image_timestamp, crack_detection_results):
    image_time = datetime.strptime(image_timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    for result in crack_detection_results:
        result_time = datetime.strptime(result['timestamp'], '%Y-%m-%d %H:%M:%S')
        if abs((result_time - image_time).total_seconds()) <= 7 and result['crack_detected'] == 1:
            return True
    return False

# Prepare the CSV output
output_data = []

# Directory where processed images are saved
result_save_dir = 'cam/results'
final_output_dir = 'final_result'

# Check each image in the JSON file
for image_name, data in image_timestamps.items():
    if data['crack_detected'] == 1:
        if is_crack_detected_within_7_seconds(data['timestamp'], crack_detection_results):
            # Save the processed image and YOLO result
            processed_image_path = os.path.join(result_save_dir, image_name)
            final_image_path = os.path.join(final_output_dir, image_name)
            
            if os.path.exists(processed_image_path):
                shutil.copy(processed_image_path, final_image_path)
            else:
                print(f"Processed image {processed_image_path} not found, skipping...")

            # Append the result to the output data
            output_data.append({
                'image_name': image_name,
                'timestamp': data['timestamp'],
                'true_crack_detected': 1
            })

# Write the output data to a CSV file
with open('final_result/true_crack_detection_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['image_name', 'timestamp', 'true_crack_detected'])
    writer.writeheader()
    writer.writerows(output_data)

print("True crack detection results saved to true_crack_detection_results.csv") 