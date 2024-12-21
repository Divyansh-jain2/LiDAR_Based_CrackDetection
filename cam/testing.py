import json
import os
from datetime import datetime

def generate_timestamped_json(folder_path, output_json):
    # Initialize an empty dictionary to store image details
    images_data = {}

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Generate a timestamp in the specified format
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"image_{timestamp}.jpg"
            images_data[filename] = new_filename

    # Save the images_data dictionary to the output JSON file
    with open(output_json, 'w') as json_file:
        json.dump(images_data, json_file, indent=4)
# Example usage
folder_path = 'cam/timelapse_images'
output_json = 'cam/timelapse_images/image_timestamps.json'
generate_timestamped_json(folder_path, output_json)
