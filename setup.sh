#!/bin/bash

# Setup script for Text Blur Tool

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "Tesseract OCR is required but not installed."
    echo "On macOS, install with: brew install tesseract"
    echo "On Ubuntu/Debian, install with: sudo apt-get install tesseract-ocr"
    echo "On Windows, download from: https://github.com/UB-Mannheim/tesseract/wiki"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required Python packages..."
pip install -r requirements.txt

# Create example images
echo "Creating example images..."
python examples/create_sample.py
python examples/create_graphical_sample.py

echo ""
echo "Setup complete! You can now use the Text Blur Tool."
echo ""
echo "To use the tool, run:"
echo "source venv/bin/activate"
echo "python text_blur.py path/to/image.jpg \"Text to blur\""
echo ""
echo "For graphical images, try:"
echo "python text_blur.py examples/graphical_sample.jpg \"ACME Corporation\" --mode aggressive"
echo ""
echo "For more information, see the README.md file."
