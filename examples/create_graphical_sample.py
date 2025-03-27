#!/usr/bin/env python3
"""
Create a graphical sample image with text for testing the text blur tool
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_graphical_sample(output_path="graphical_sample.jpg"):
    """Create a sample graphical image with text"""
    
    # Create a gradient background
    width, height = 800, 400
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Create gradient background
    for y in range(height):
        r = int(255 * (1 - y / height))
        g = int(200 * (y / height))
        b = int(255 * (0.5 + 0.5 * np.sin(y / 30)))
        for x in range(width):
            draw.point((x, y), fill=(r, g, b))
    
    # Add some shapes
    draw.ellipse((50, 50, 200, 200), fill=(255, 200, 200, 128))
    draw.rectangle((400, 100, 700, 300), fill=(200, 255, 200, 128))
    
    # Try to use a stylized font, fall back to default if not available
    try:
        # Try different fonts that might be available
        font_options = ["Arial Bold", "Impact", "Verdana Bold", "Helvetica Bold"]
        font = None
        
        for font_name in font_options:
            try:
                font = ImageFont.truetype(font_name, 36)
                break
            except IOError:
                continue
                
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Add stylized text
    company_name = "ACME Corporation"
    slogan = "Building the Future"
    
    # Add shadow effect for text
    shadow_offset = 3
    draw.text((252, 153), company_name, fill="black", font=font)
    draw.text((252, 203), slogan, fill="black", font=font)
    
    # Add main text
    draw.text((250, 150), company_name, fill="white", font=font)
    draw.text((250, 200), slogan, fill="white", font=font)
    
    # Apply a slight blur to make it more challenging
    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Save the image
    image.save(output_path, quality=95)
    print(f"Created graphical sample image: {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)
    
    # Create sample image
    create_graphical_sample("examples/graphical_sample.jpg")
