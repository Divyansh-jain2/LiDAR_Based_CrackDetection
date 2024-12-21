import subprocess
import os

def run_script(script_path):
    # Check if the script file exists
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} not found.")
        return
    
    try:
        # Run the script and wait for it to complete
        subprocess.run(['python', script_path], check=True)
        print(f"{script_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")

# Absolute paths for your scripts
LiDAR_script = "/home/admin/dp/integration/LiDAR_combined.py"
timestamp_script = "/home/admin/dp/integration/timestamp_modified.py"
cam_script = "/home/admin/dp/integration/cam_crack_detect.py"
integration_script = "/home/admin/dp/integration/integrate.py"
display_script = "/home/admin/dp/integration/display_results.py"

run_script(LiDAR_script)
run_script(timestamp_script)
run_script(cam_script)
run_script(integration_script)
run_script(display_script)

