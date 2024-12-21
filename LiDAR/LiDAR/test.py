import csv
import time
from rplidar import RPLidar

lidar = RPLidar('COM5')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

# Open a CSV file to write data
with open('lidar_data_with_timestamp_high.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header for the CSV file
    writer.writerow(['Timestamp', 'Quality', 'Angle (degrees)', 'Distance (mm)'])
    
    try:
        lidar._set_pwm(660)
        for scan in lidar.iter_scans(scan_type="express"):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # Get current timestamp
            print(f'Time: {timestamp} | Got {len(scan)} measurements')
            for measurement in scan:
                # Each measurement is a tuple of (quality, angle, distance)
                quality, angle, distance = measurement[0], measurement[1], measurement[2]
                writer.writerow([timestamp, quality, angle, distance])
    except KeyboardInterrupt:
        print("Stopping the script...")
    
# Stop the lidar and disconnect
lidar.stop()
lidar.stop_motor()
lidar.disconnect()

