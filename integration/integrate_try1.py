import json
import os
from ultralytics import YOLO

# Load the YOLO model
weight_path = "/home/admin/dp/best3.pt"  # Use forward slashes
model = YOLO(weight_path)

# Path to the JSON file containing image timestamps
#timestamp_file = "/home/admin/dp/timelapse_images/image_timestamps.json"

# Directory where images are stored
#image_dir = "/home/admin/dp/timelapse_images"

# Directory to save the YOLO detection results
result_save_dir = "/home/admin/dp/crack-seg/results"

# Ensure the results directory exists
if not os.path.exists(result_save_dir):
    os.makedirs(result_save_dir)

# Load the image timestamps from the JSON file
#with open(timestamp_file, 'r') as f:
 #   image_timestamps = json.load(f)

# Iterate over each image in the JSON file
#for image_name, timestamp in image_timestamps.items():
    # Construct the full path to the image
#image_path = os.path("/home/admin/dp/bhagwan_bhrose.jpg")
image_path = "/home/admin/dp/bhgwan_bhrose.jpg"
image_name = "bhagwan_bhrose.jpg"    # Check if the image file exists
if not os.path.exists(image_path):
    print(f"Image {image_name} not found, skipping...")
#continue

    # Perform crack detection on the image
results = model.predict(image_path, save=True, save_dir=result_save_dir)

    # Determine if cracks are detected based on the results
crack_detected = 1 if len(results[0].boxes) > 0 else 0

    # Update the JSON entry with the crack detection result
 #   image_timestamps[image_name] = {
  #      "timestamp": timestamp,
   #     "crack_detected": crack_detected
    #}

print(f"Processed {image_name}: {'Crack detected' if crack_detected else 'No crack detected'}")

# Save the updated JSON file with the crack detection results
#with open(timestamp_file, 'w') as f:
 #   json.dump(image_timestamps, f, indent=4)

print(f"Detection results saved to {result_save_dir}")

