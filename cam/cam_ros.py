import os
from datetime import datetime
from ultralytics import YOLO
import rospy
from sensor_msgs.msg import LaserScan
import cv2
import numpy as np

# ROS node initialization
rospy.init_node('crack_detection_node', anonymous=True)

# LiDAR data storage
lidar_data = None

# Callback function for LiDAR data
def lidar_callback(data):
    global lidar_data
    lidar_data = data

# Subscribe to LiDAR topic
rospy.Subscriber('/scan', LaserScan, lidar_callback)

# Load YOLO model
weight_path = "D:/DP_model/DP_1/crack-seg/best3.pt"
model = YOLO(weight_path)

# Directory for storing results
result_dir = "D:/DP_model/results"
os.makedirs(result_dir, exist_ok=True)

def calculate_crack_length(mask):
    # Use skeletonization to get the centerline of the crack
    skeleton = cv2.ximgproc.thinning(mask.astype(np.uint8))
    # Find non-zero pixels in the skeleton
    points = np.column_stack(np.where(skeleton > 0))
    # Calculate the total length of the skeleton
    length = np.sum(np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1)))
    return length

def process_image_and_lidar(image_path):
    # Get image timestamp
    timestamp = datetime.fromtimestamp(os.path.getctime(image_path))
    
    # Perform crack detection
    results = model.predict(image_path, save=False)
    
    # Wait for LiDAR data
    rate = rospy.Rate(10)  # 10 Hz
    while lidar_data is None and not rospy.is_shutdown():
        rate.sleep()
    
    if rospy.is_shutdown():
        return
    
    # Load the image
    image = cv2.imread(image_path)
    
    # Process detection results
    for r in results:
        masks = r.masks.data.cpu().numpy()
        
        for i, mask in enumerate(masks):
            # Convert float mask to binary
            binary_mask = (mask > 0.5).astype(np.uint8) * 255
            
            # Calculate crack length
            crack_length = calculate_crack_length(binary_mask)
            
            # Find crack endpoints
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                contour = max(contours, key=cv2.contourArea)
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                
                # Calculate midpoint of the crack
                mid_x = int(np.mean(box[:, 0]))
                mid_y = int(np.mean(box[:, 1]))
                
                # Map LiDAR data to image coordinates (simplified)
                lidar_index = int(mid_x / image.shape[1] * len(lidar_data.ranges))
                crack_depth = lidar_data.ranges[lidar_index]
            
            # Overlay crack on the image
            overlay = image.copy()
            cv2.drawContours(overlay, [contour], 0, (0, 0, 255), 2)
            cv2.addWeighted(overlay, 0.4, image, 0.6, 0, image)
            
            # Add text information
            cv2.putText(image, f"Crack {i+1}", (mid_x, mid_y - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(image, f"Length: {crack_length:.2f}px", (mid_x, mid_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(image, f"Depth: {crack_depth:.2f}m", (mid_x, mid_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Save the result
    result_filename = f"crack_result_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
    result_path = os.path.join(result_dir, result_filename)
    cv2.imwrite(result_path, image)
    
    # Save metadata
    metadata_filename = f"crack_metadata_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    metadata_path = os.path.join(result_dir, metadata_filename)
    with open(metadata_path, 'w') as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Image Path: {image_path}\n")
        f.write(f"Number of cracks detected: {len(masks)}\n")
        for i, mask in enumerate(masks):
            crack_length = calculate_crack_length(mask)
            f.write(f"Crack {i+1} - Length: {crack_length:.2f}px, Depth: {crack_depth:.2f}m\n")

# Process a single image
image_path = "D:/DP_model/DP_1/crack-seg/t5.jpg"
process_image_and_lidar(image_path)

print("Processing complete. Results saved in:", result_dir)