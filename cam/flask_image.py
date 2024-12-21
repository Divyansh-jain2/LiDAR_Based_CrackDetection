from flask import Flask, send_file, render_template_string, make_response, jsonify
import os
import time
import subprocess
import threading
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from fevicol import update_timestamp, load_timestamps

app = Flask(__name__)

# Directory to store captured images
IMAGE_DIR = "/home/admin/dp/timelapse_images"
LATEST_IMAGE = "latest.jpg"
DEFAULT_IMAGE = "waiting.jpg"
ERROR_IMAGE = "error.jpg"

# Ensure the image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

def create_text_image(text, filename):
    img = Image.new('RGB', (640, 480), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except IOError:
        font = ImageFont.load_default()
    d.text((10,10), text, fill=(255,255,0), font=font, align="left")
    img.save(os.path.join(IMAGE_DIR, filename))

def capture_image():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.jpg"
    output_path = os.path.join(IMAGE_DIR, filename)
    latest_path = os.path.join(IMAGE_DIR, LATEST_IMAGE)
    try:
        result = subprocess.run(["rpicam-still", "-o", output_path, "-n"],
                                capture_output=True, text=True, check=True)
        print(f"Image captured: {output_path}")
        # Create a symbolic link to the latest image
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(output_path, latest_path)
        # Update timestamp in JSON file
        update_timestamp(filename, datetime.now().isoformat())
        return None
    except subprocess.CalledProcessError as e:
        error_msg = f"Error capturing image: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}"
        print(error_msg)
        create_text_image(error_msg, ERROR_IMAGE)
        return error_msg
    except FileNotFoundError:
        error_msg = "rpicam-still command not found. Make sure it's installed and in your PATH."
        print(error_msg)
        create_text_image(error_msg, ERROR_IMAGE)
        return error_msg

def continuous_capture():
    while True:
        error = capture_image()
        time.sleep(3)  # Wait for 3 seconds before next capture

# Create default image
create_text_image("Waiting for camera...", DEFAULT_IMAGE)

# Start the continuous capture in a separate thread
capture_thread = threading.Thread(target=continuous_capture, daemon=True)
capture_thread.start()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>RPi Camera Timelapse</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            #latest-image { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>RPi Camera Timelapse</h1>
        <img id="latest-image" src="{{ url_for('serve_latest_image') }}" alt="Latest Image">
        <p id="timestamp"></p>

        <script>
            function updateImage() {
                const img = document.getElementById('latest-image');
                img.src = '{{ url_for('serve_latest_image') }}?t=' + new Date().getTime();
                
                fetch('/latest_timestamp')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('timestamp').textContent = 'Captured at: ' + data.timestamp;
                    });
            }

            // Update image every 3 seconds
            setInterval(updateImage, 3000);
        </script>
    </body>
    </html>
    ''')

@app.route('/latest')
def serve_latest_image():
    latest_image_path = os.path.join(IMAGE_DIR, LATEST_IMAGE)
    default_image_path = os.path.join(IMAGE_DIR, DEFAULT_IMAGE)
    error_image_path = os.path.join(IMAGE_DIR, ERROR_IMAGE)

    if os.path.exists(latest_image_path):
        image_path = latest_image_path
    elif os.path.exists(error_image_path):
        image_path = error_image_path
    else:
        image_path = default_image_path

    try:
        response = make_response(send_file(image_path))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    except Exception as e:
        print(f"Error serving image: {e}")
        return "Error serving image", 500

@app.route('/latest_timestamp')
def get_latest_timestamp():
    timestamps = load_timestamps()
    if timestamps:
        latest_image = max(timestamps, key=timestamps.get)
        return jsonify({"timestamp": timestamps[latest_image]})
    return jsonify({"timestamp": "No images captured yet"})

@app.route('/diagnostics')
def diagnostics():
    try:
        camera_info = subprocess.run(["rpicam-hello"], capture_output=True, text=True, check=True)
        return f"<pre>{camera_info.stdout}</pre>"
    except Exception as e:
        return f"Error running diagnostics: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
