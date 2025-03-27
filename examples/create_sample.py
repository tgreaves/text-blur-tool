#!/usr/bin/env python3
"""
Create a sample image with text for testing the text blur tool
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_sample_image(output_path="sample.jpg"):
    """Create a sample image with text"""
    
    # Create a white image
    width, height = 800, 400
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a common font, fall back to default if not available
    try:
        font = ImageFont.truetype("Arial", 24)
    except IOError:
        font = ImageFont.load_default()
    
    # Add text to the image
    text = [
        "Sample Text Document",
        "",
        "Name: John Smith",
        "Phone: (555) 123-4567",
        "Email: john.smith@email.com",
        "",
        "Confidential Information"
    ]
    
    y_position = 50
    for line in text:
        draw.text((50, y_position), line, fill="black", font=font)
        y_position += 30
    
    # Save the image
    image.save(output_path)
    print(f"Created sample image: {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)
    
    # Create sample image
    create_sample_image("examples/sample.jpg")
