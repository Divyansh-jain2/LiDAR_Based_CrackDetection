from flask import Flask, render_template, send_from_directory
import os
import csv

app = Flask(__name__)

# Change these paths
IMAGE_FOLDER = "/home/admin/dp/integration/finalresults/images"
CSV_FILE = "/home/admin/dp/integration/crack_detection_results.csv"

@app.route('/')
def index():
    # List all image files in the folder
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Read CSV content
    csv_data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)
            csv_data = list(reader)

    return render_template('index.html', images=image_files, csv_data=csv_data)

@app.route('/images/<filename>')
def images(filename):
    # Serve the image files
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
