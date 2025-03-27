# Text Blur Tool

A Python tool to automatically detect and blur specific text in images, including graphical images. This tool uses advanced Optical Character Recognition (OCR) with multiple preprocessing techniques to find text patterns in various types of images and applies a Gaussian blur to those areas.

## Features

- **Enhanced text detection** in graphical images and complex backgrounds
- Multiple image preprocessing techniques to improve OCR accuracy
- Support for different OCR modes to handle various text layouts
- Customizable confidence thresholds and blur strength
- Works with various image formats (JPG, PNG, etc.)
- Simple command-line interface

## Requirements

- Python 3.6+
- OpenCV
- Tesseract OCR
- Pillow (PIL)
- NumPy

## Installation

1. **Install Tesseract OCR**:
   - macOS: `brew install tesseract`
   - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

2. **Set up a Python virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Quick setup with the provided script**:
   ```bash
   ./setup.sh
   ```

## Usage

### Basic Usage

```bash
python text_blur.py path/to/image.jpg "Text to blur"
```

### Advanced Options

```bash
python text_blur.py path/to/image.jpg "Text to blur" --mode aggressive --confidence 50 --blur 31
```

### Command Line Arguments

- `image_path`: Path to the input image
- `text`: One or more text strings to find and blur
- `--output`, `-o`: Custom output path for the blurred image
- `--mode`, `-m`: Preprocessing mode (`default`, `aggressive`, or `all`)
- `--confidence`, `-c`: Minimum confidence score for text detection (0-100)
- `--blur`, `-b`: Blur strength (odd number)

## Examples

### Blur Text in a Standard Document

```bash
python text_blur.py examples/sample.jpg "John Smith"
```

### Blur Text in a Graphical Image

```bash
python text_blur.py examples/logo.jpg "Company Name" --mode aggressive --confidence 40
```

### Blur Multiple Text Elements with Custom Settings

```bash
python text_blur.py examples/screenshot.png "Password" "Username" --mode all --confidence 30 --blur 71
```

## How It Works

1. **Image Preprocessing**: The tool applies multiple preprocessing techniques to enhance text visibility:
   - Grayscale conversion
   - Contrast enhancement
   - Thresholding (binary and adaptive)
   - Edge enhancement
   - Denoising

2. **Multi-mode OCR**: Uses different Tesseract OCR configurations to handle various text layouts:
   - Standard block text
   - Full page analysis
   - Sparse text detection
   - Automatic page segmentation

3. **Flexible Text Matching**: Employs multiple strategies to match text:
   - Exact matching
   - Substring matching
   - Whitespace-normalized matching
   - Context-aware matching (looking at surrounding words)

4. **Region Blurring**: Applies Gaussian blur to detected regions with customizable strength

## Tips for Best Results

- For graphical images, use `--mode aggressive` or `--mode all`
- Lower the confidence threshold (`--confidence`) for difficult-to-detect text
- Increase blur strength (`--blur`) for more aggressive blurring
- Try different preprocessing modes if text isn't being detected
- For logos or stylized text, you may need to lower the confidence threshold significantly

## Customization

You can modify the script to:
- Add more preprocessing techniques
- Implement additional OCR engines
- Change the blurring method (e.g., pixelation instead of Gaussian blur)
- Add support for automatic language detection

## Troubleshooting

If text isn't being detected:
1. Try `--mode all` to use all preprocessing techniques
2. Lower the confidence threshold (e.g., `--confidence 30`)
3. Check that Tesseract OCR is properly installed and in your PATH
4. For very stylized or unusual fonts, you might need to train a custom Tesseract model

## License

This tool is provided as-is under the MIT License.
