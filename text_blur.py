#!/usr/bin/env python3
"""
Text Blur - A tool to automatically blur specific text in images

This script uses OCR to find specified text in images and applies a blur effect to those areas.
Enhanced to better handle graphical images and different text styles.
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import os
import argparse
from typing import List, Tuple, Optional

def preprocess_image(image: np.ndarray, mode: str = 'default') -> List[np.ndarray]:
    """
    Preprocess the image to improve text detection using different techniques.
    Returns a list of preprocessed versions to try OCR on.
    
    Args:
        image: Input image in BGR format (OpenCV default)
        mode: Preprocessing mode ('default', 'aggressive', or 'all')
    
    Returns:
        List of preprocessed images
    """
    images = []
    
    # Original image
    images.append(image.copy())
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    images.append(gray)
    
    if mode in ['aggressive', 'all']:
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast = clahe.apply(gray)
        images.append(contrast)
        
        # Thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        images.append(binary)
        
        # Adaptive thresholding
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        images.append(adaptive)
        
        # Edge enhancement
        kernel = np.array([[-1,-1,-1],
                         [-1, 9,-1],
                         [-1,-1,-1]])
        sharpened = cv2.filter2D(gray, -1, kernel)
        images.append(sharpened)
        
        # Denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        images.append(denoised)
    
    return images

def detect_text_regions(image: np.ndarray, text_to_find: List[str], 
                       preprocessing_mode: str = 'default', 
                       min_confidence: int = 60) -> List[Tuple[str, List[Tuple[int, int, int, int]]]]:
    """
    Detect regions containing specified text using multiple preprocessing methods
    and OCR configurations.
    
    Args:
        image: Input image
        text_to_find: List of text strings to search for
        preprocessing_mode: Image preprocessing mode
        min_confidence: Minimum confidence score for text detection
    
    Returns:
        List of tuples containing (matched_text, list of bounding boxes)
    """
    # Prepare different OCR configurations
    configs = [
        '--oem 3 --psm 6',  # Assume uniform block of text
        '--oem 3 --psm 3',  # Fully automatic page segmentation
        '--oem 3 --psm 11',  # Sparse text - find as much text as possible
        '--oem 3 --psm 1',   # Automatic page segmentation with OSD
    ]
    
    # Process image with different methods
    preprocessed_images = preprocess_image(image, preprocessing_mode)
    
    results = []
    for text in text_to_find:
        text_boxes = []
        
        for img in preprocessed_images:
            for config in configs:
                try:
                    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=config)
                    
                    # Process each detected text block
                    for i, word in enumerate(data['text']):
                        if not word.strip():
                            continue
                            
                        conf = int(data['conf'][i])
                        if conf < min_confidence:
                            continue
                        
                        # Check for match (case insensitive)
                        word_lower = word.lower()
                        text_lower = text.lower()
                        
                        # Try different matching strategies
                        if (text_lower in word_lower or 
                            word_lower in text_lower or
                            text_lower.replace(' ', '') in word_lower.replace(' ', '') or
                            any(text_lower in ' '.join(data['text'][max(0, i-j):i+j+1]).lower() 
                                for j in range(3))):
                            
                            x = data['left'][i]
                            y = data['top'][i]
                            w = data['width'][i]
                            h = data['height'][i]
                            
                            # Add some padding
                            pad = int(h * 0.5)
                            box = (max(0, x - pad),
                                  max(0, y - pad),
                                  w + 2*pad,
                                  h + 2*pad)
                            
                            if box not in text_boxes:
                                text_boxes.append(box)
                                print(f"Found '{text}' in '{word}' with confidence {conf}%")
                
                except Exception as e:
                    print(f"Warning: OCR error with config {config}: {str(e)}")
                    continue
        
        if text_boxes:
            results.append((text, text_boxes))
    
    return results

def apply_blur(image: np.ndarray, regions: List[Tuple[str, List[Tuple[int, int, int, int]]]], 
               blur_strength: int = 51) -> np.ndarray:
    """
    Apply Gaussian blur to specified regions in the image.
    
    Args:
        image: Input image
        regions: List of (text, bounding boxes) tuples
        blur_strength: Strength of the Gaussian blur (must be odd number)
    
    Returns:
        Image with blurred regions
    """
    output = image.copy()
    
    for text, boxes in regions:
        for (x, y, w, h) in boxes:
            # Ensure coordinates are within image bounds
            y_end = min(y + h, image.shape[0])
            x_end = min(x + w, image.shape[1])
            
            if y_end > y and x_end > x:
                region = output[y:y_end, x:x_end]
                if region.size > 0:  # Make sure region is not empty
                    blurred = cv2.GaussianBlur(region, (blur_strength, blur_strength), 0)
                    output[y:y_end, x:x_end] = blurred
                    print(f"Blurred region for '{text}' at ({x}, {y}, {w}, {h})")
    
    return output

def blur_text_in_image(image_path: str, text_to_blur: List[str], output_path: Optional[str] = None,
                      preprocessing_mode: str = 'aggressive', min_confidence: int = 60,
                      blur_strength: int = 51) -> str:
    """
    Find and blur specific text in an image.
    
    Args:
        image_path: Path to the input image
        text_to_blur: List of text strings to find and blur
        output_path: Optional path for output image
        preprocessing_mode: Image preprocessing mode ('default', 'aggressive', or 'all')
        min_confidence: Minimum confidence score for text detection
        blur_strength: Strength of the Gaussian blur (must be odd number)
    
    Returns:
        Path to the output image with blurred text
    """
    # Validate blur strength
    if blur_strength % 2 == 0:
        blur_strength += 1
    
    # Set output path if not provided
    if output_path is None:
        name, ext = os.path.splitext(image_path)
        output_path = f"{name}_blurred{ext}"
    
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    # Convert text_to_blur to list if it's a string
    if isinstance(text_to_blur, str):
        text_to_blur = [text_to_blur]
    
    print(f"Processing image: {image_path}")
    print(f"Searching for text: {', '.join(text_to_blur)}")
    
    # Detect text regions
    regions = detect_text_regions(image, text_to_blur, 
                                preprocessing_mode=preprocessing_mode,
                                min_confidence=min_confidence)
    
    if not regions:
        print("No matching text found to blur")
        return output_path
    
    # Apply blur to detected regions
    output_image = apply_blur(image, regions, blur_strength)
    
    # Save the output image
    cv2.imwrite(output_path, output_image)
    print(f"Saved blurred image to {output_path}")
    
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Blur specific text in an image')
    parser.add_argument('image_path', help='Path to the input image')
    parser.add_argument('text', nargs='+', help='Text to find and blur')
    parser.add_argument('--output', '-o', help='Path to save the output image')
    parser.add_argument('--mode', '-m', choices=['default', 'aggressive', 'all'],
                      default='aggressive', help='Preprocessing mode')
    parser.add_argument('--confidence', '-c', type=int, default=60,
                      help='Minimum confidence score (0-100)')
    parser.add_argument('--blur', '-b', type=int, default=51,
                      help='Blur strength (odd number)')
    
    args = parser.parse_args()
    
    blur_text_in_image(args.image_path, args.text, args.output,
                      preprocessing_mode=args.mode,
                      min_confidence=args.confidence,
                      blur_strength=args.blur)

if __name__ == "__main__":
    main()
