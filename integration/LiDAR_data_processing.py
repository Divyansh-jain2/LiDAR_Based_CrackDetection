import subprocess

def run_script(script_name):
    try:
        # Run the script and wait for it to complete
        subprocess.run(['python', script_name], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")

# Specify your script names
data_processing_script = "D:\DP_model\LiDAR\LiDAR\post_processing.py"
crack_detection_script = "D:\DP_model\LiDAR\LiDAR\plot_processed_data.py"

# Run the data processing script first
run_script(data_processing_script)

# Run the crack detection script if data processing is successful
run_script(crack_detection_script)



# import subprocess
# import os

# def run_script(script_path):
#     # Check if the script file exists
#     if not os.path.isfile(script_path):
#         print(f"Error: {script_path} not found.")
#         return
    
#     try:
#         # Run the script and wait for it to complete
#         subprocess.run(['python', script_path], check=True)
#         print(f"{script_path} executed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error occurred while running {script_path}: {e}")

# # Absolute paths for your scripts
# data_processing_script = "/home/admin/dp/LiDAR/post_processing.py"
# crack_detection_script = "/home/admin/dp/LiDAR/plot_processed_data.py"

# # Run the data processing script first
# run_script(data_processing_script)

# # Run the crack detection script if data processing is successful
# run_script(crack_detection_script)
