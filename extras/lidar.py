import csv
import time
from rplidar import RPLidar

# Define the port name (change to the correct one for your system)
PORT_NAME = 'COM18'  # On Windows, it might be something like 'COM3'

# Create an instance of the RPLidar
lidar = RPLidar(PORT_NAME, baudrate=57600)

# File to save the data
csv_file = 'rplidar_data_with_timestamp.csv'

# Define the headers for the CSV file
csv_headers = ['timestamp', 'angle', 'distance']

# Open the CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the headers
    writer.writerow(csv_headers)
    
    try:
        # Iterate over scans and save data with timestamp
        for scan in lidar.iter_scans():
            # Get the current timestamp
            current_time = time.time()  # Time in seconds since the epoch
            for (_, angle, distance) in scan:
                writer.writerow([current_time, angle, distance])
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Stop the lidar and disconnect
        lidar.stop()
        lidar.disconnect()