import os
import uuid
from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
from PIL import Image
import logging

# --- Setup ---
app = Flask(__name__, static_folder='static', template_folder='templates')
logging.basicConfig(level=logging.INFO)

# --- Create Directories ---
UPLOADS_DIR = 'uploads'
PREDICTIONS_DIR = os.path.join('static', 'predictions')
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(PREDICTIONS_DIR, exist_ok=True)

# --- Load Models ---
try:
    logging.info("Loading YOLOv9 models...")
    qr_model = YOLO('models/best_qr_github.pt')
    barcode_model = YOLO('models/best_barcode_github2.pt')
    logging.info("Models loaded successfully!")
except Exception as e:
    logging.error(f"Error loading models: {e}")
    qr_model = None
    barcode_model = None

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and qr_model and barcode_model:
        # Generate a unique filename to prevent browser caching issues and overwrites
        unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(UPLOADS_DIR, unique_filename)
        file.save(filepath)
        logging.info(f"File saved to {filepath}")

        try:
            # --- Run Inference ---
            qr_results = qr_model.predict(filepath, verbose=False)
            qr_present = len(qr_results[0].boxes) > 0
            qr_status = "QR code present" if qr_present else "QR code absent"

            barcode_results = barcode_model.predict(filepath, verbose=False)
            barcode_present = len(barcode_results[0].boxes) > 0
            barcode_status = "Barcode present" if barcode_present else "Barcode absent"

            # --- Save the Visual Result ---
            # Use the plot() method from the results object to get an image with bounding boxes
            # We will use the QR code results for plotting, but you can choose either.
            result_plot = qr_results[0].plot()  # Returns a NumPy array (BGR)
            
            # Convert from BGR (used by OpenCV) to RGB (used by PIL)
            result_plot_rgb = Image.fromarray(result_plot[..., ::-1])

            # Save the plotted image to the static predictions directory
            output_image_path = os.path.join(PREDICTIONS_DIR, unique_filename)
            result_plot_rgb.save(output_image_path)
            
            # The URL path that the browser will use to fetch the image
            image_url = f'/static/predictions/{unique_filename}'

            
            
            # --- Clean up and Respond ---
            os.remove(filepath)

            return jsonify({
                'qr_result': qr_status,
                'barcode_result': barcode_status,
                'image_url': image_url # Send the URL back to the frontend
            })

        except Exception as e:
            logging.error(f"An error occurred during prediction: {e}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': 'Failed to process the image.'}), 500

    return jsonify({'error': 'Server error: Models not loaded'}), 500

@app.route('/delete_prediction', methods=['POST'])
def delete_prediction():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    file_path = os.path.join(PREDICTIONS_DIR, filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'status': 'deleted'})
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting file {file_path}: {e}")
        return jsonify({'error': 'Failed to delete file'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)