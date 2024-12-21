
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load data
df = pd.read_csv('D:\DP_model\LiDAR\LiDAR\lidar_data_processed.csv')
selected_columns = df.iloc[:, 20:35].apply(pd.to_numeric, errors='coerce').to_numpy()
timestamps = pd.to_datetime(df.iloc[:, 0]).to_numpy()

def detect_significant_changes(data, prominence_threshold=1.5):
    """
    Detect significant peaks and troughs in time series data.
    
    Parameters:
    data : array-like
        Input time series data
    prominence_threshold : float
        Minimum prominence for a peak/trough to be considered significant
        
    Returns:
    tuple
        (peak_indices, trough_indices)
    """
    # Convert to numpy array if not already
    data = np.array(data)
    
    # Find peaks
    peaks, peak_properties = find_peaks(
        data,
        prominence=prominence_threshold
    )
    
    # Find troughs by inverting the signal
    troughs, trough_properties = find_peaks(
        -data,
        prominence=prominence_threshold
    )
    
    return peaks, troughs

def detect_crack_by_difference(data, timestamps):
    """
    Detect crack patterns in the time series data.
    
    Parameters:
    data : 2D numpy array
        Input time series data
    timestamps : numpy array
        Corresponding timestamps for the data
        
    Returns:
    dict
        {'crack_detected': list, 'time_ranges': list}
    """
    crack_detected = []
    time_ranges = []
    
    for column_data in data.T:
        peaks, troughs = detect_significant_changes(column_data, prominence_threshold=1.0)
        
        # Detect crack pattern
        column_crack_detected = 1 if len(peaks) > 0 and len(troughs) > 0 else 0
        crack_detected.append(column_crack_detected)
        
        # Get time ranges for detected cracks
        if column_crack_detected:
            peak_times = timestamps[peaks]
            trough_times = timestamps[troughs]
            time_ranges.append((peak_times[0], trough_times[-1]))
        else:
            time_ranges.append(None)
    
    # Filter out the None values from the time_ranges list
    time_ranges = [tr for tr in time_ranges if tr is not None]
    
    return {'crack_detected': crack_detected, 'time_ranges': time_ranges}

# Run crack detection on selected columns
result = detect_crack_by_difference(selected_columns, timestamps)
crack_detected = result['crack_detected']
time_ranges = result['time_ranges']

print(result)

# Create a DataFrame with timestamps and crack detection results
crack_df = pd.DataFrame({
    'Timestamp': timestamps
})
crack_df['Crack'] = 0

for start_time, end_time in time_ranges:
    crack_df.loc[(crack_df['Timestamp'] >= start_time) & (crack_df['Timestamp'] <= end_time), 'Crack'] = 1

# Display the DataFrame
print(crack_df)

# Optional: Save the DataFrame to a CSV file
crack_df.to_csv('crack_detection_results.csv', index=False)

print("Crack pattern detected:" if 1 in crack_df['Crack'].values else "No crack pattern detected.")
print("Time ranges for detected cracks:", time_ranges)
