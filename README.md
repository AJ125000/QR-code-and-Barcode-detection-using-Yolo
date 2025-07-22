# QR Code & Barcode Detection System

A web-based application that uses YOLO models to detect QR codes and barcodes in uploaded images. The system features a modern drag-and-drop interface and provides real-time detection results with visual feedback.

## Features

- **Dual Detection**: Simultaneously detects both QR codes and barcodes in images
- **Modern UI**: Drag-and-drop file upload with progress indicators
- **Real-time Results**: Instant detection of results 
- **Multiple File Support**: Upload and process multiple images at once
- **File Validation**: Automatic file size and type validation
- **Visual Feedback**: Shows detection results with images
- **Auto Cleanup**: Automatically removes processed images to save storage

## Prerequisites

- Python 3.8 or higher
- YOLO models (see Model Requirements section)

## Installation

1. **Clone or download the project**
   ```bash
   git clone https://github.com/AJ125000/QR-code-and-Barcode-detection-using-Yolo.git
   cd qr-barcode-detection
   ```
2. **Create and activate a virtual environment**
   Create:
   ```bash
   python -m venv venv
   ```
   Activate:
   For windows:
   ```bash
   venv/Scripts/activate
   ```
   For linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the directory structure**
   The application will automatically create necessary directories, but ensure you have:
   ```
   app/
   ├── models/
   │   ├── best_qr_github.pt
   │   └── best_barcode_github2.pt
   ├── static/
   │   └── predictions/
   ├── templates/
   │   └── index.html
   ├── uploads/
   ├── app.py
   └── requirements.txt
   ```

## Model Requirements

Place the trained YOLO models in the `models/` directory:
- `best_qr_github.pt` - QR code detection model
- `best_barcode_github2.pt` - Barcode detection model

These are YOLO model files trained specifically for QR code and barcode detection.

## Dependencies

The application requires the Python packages as mentioned in `requirements.txt`

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   Open your browser and navigate to `http://localhost:5000`

3. **Upload images**
   - Drag and drop image files onto the upload area, or
   - Click "Browse Files" to select images from your device

4. **View results**
   - Each uploaded image will show detection status for both QR codes and barcodes
   - Visual results with bounding boxes are displayed
   - Green status indicates successful detection
   - Red status indicates detection errors
     
## Supported File Formats

- **Image Types**: JPG, JPEG, PNG, GIF, SVG
- **PDF**: Also supported for document processing
- **File Size Limit**: 50MB per file

## API Endpoints

### POST /predict
Uploads and processes an image for QR code and barcode detection.

**Request**: Multipart form data with image file
```javascript
FormData: {
  file: <image_file>
}
```

**Response**: JSON
```json
{
  "qr_result": "QR code present|absent",
  "barcode_result": "Barcode present|absent", 
  "image_url": "/static/predictions/unique_filename.jpg"
}
```

### POST /delete_prediction
Removes processed prediction images from server storage.

**Request**: JSON
```json
{
  "filename": "unique_filename.jpg"
}
```

**Response**: JSON
```json
{
  "status": "deleted"
}
```

## Project Structure

```
app/
├── models/                 # YOLO model files
│   ├── best_qr_github.pt
│   └── best_barcode_github2.pt
├── static/                 # Static web assets
│   └── predictions/        # Temporary prediction images
├── templates/              # HTML templates
│   └── index.html         # Main web interface
├── uploads/               # Temporary upload directory
├── app.py                # Flask application
└── requirements.txt      # Python dependencies
```

## Configuration

The application runs with the following default settings:
- **Host**: `0.0.0.0` (accessible from any network interface)
- **Port**: `5000`
- **Max File Size**: 50MB
- **Upload Directory**: `uploads/`
- **Predictions Directory**: `static/predictions/`

To modify these settings, edit the configuration variables in `app.py`.

## Technical Details

- **Framework**: Flask web framework
- **ML Models**: YOLO via Ultralytics
- **Image Processing**: PIL (Python Imaging Library)
- **Frontend**: HTML5, CSS3, JavaScript with Tailwind CSS
- **File Handling**: Automatic cleanup of temporary files

## Features in Detail

### File Upload
- Drag-and-drop interface with visual feedback
- Multiple file selection support
- Real-time file validation
- Progress indicators during upload

### Detection Processing
- Parallel QR code and barcode detection
- Visual annotation of detected objects
- Unique filename generation to prevent conflicts
- Automatic cleanup of processed files

### Results Display
- Status indicators (success/error/uploading)
- Visual results with bounding boxes
- File information (name, size)
- Individual file removal options

## Troubleshooting

### Model Loading Issues
- Ensure model files are in the correct `models/` directory
- Verify model files are valid YOLO format (.pt files)
- Check file permissions

### Upload Failures
- Verify file size is under 50MB limit
- Ensure file format is supported
- Check server storage space

### Memory Issues
- Large images may require more RAM
- Consider resizing images before processing
- Monitor server resources during bulk uploads

## Performance Notes

- Processing time depends on image size and complexity
- Multiple concurrent uploads are supported
- Temporary files are automatically cleaned up
- Consider implementing rate limiting for production use


## License

MIT License
