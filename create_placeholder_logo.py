#!/usr/bin/env python3
"""
Create a placeholder logo for the application
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_logo():
    """Create a simple placeholder logo"""
    # Create image
    width, height = 200, 80
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Background gradient effect
    for y in range(height):
        alpha = int(255 * (1 - y / height * 0.3))
        color = (52, 152, 219, alpha)  # Blue gradient
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add border
    draw.rectangle([2, 2, width-3, height-3], outline=(41, 128, 185, 255), width=2)
    
    # Add text
    try:
        # Try to use a nice font
        font_size = 16
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Main text
    text = "Social Downloader"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 8
    
    # Add shadow
    draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 128))
    # Main text
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    # Subtitle
    try:
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 10)
    except:
        small_font = ImageFont.load_default()
    
    subtitle = "AI-Powered Transcription"
    bbox = draw.textbbox((0, 0), subtitle, font=small_font)
    sub_width = bbox[2] - bbox[0]
    sub_x = (width - sub_width) // 2
    sub_y = y + text_height + 2
    
    draw.text((sub_x, sub_y), subtitle, font=small_font, fill=(230, 230, 230, 255))
    
    # Add some decorative elements
    # Top-left icon
    draw.ellipse([10, 10, 25, 25], fill=(46, 204, 113, 255))
    draw.text((13, 12), "📥", fill=(255, 255, 255, 255))
    
    # Top-right icon  
    draw.ellipse([width-25, 10, width-10, 25], fill=(231, 76, 60, 255))
    draw.text((width-22, 12), "🎵", fill=(255, 255, 255, 255))
    
    # Save logo
    output_path = "resource/main_logo.png"
    image.save(output_path, "PNG")
    print(f"✅ Logo created: {output_path}")
    
    return output_path

if __name__ == "__main__":
    try:
        create_placeholder_logo()
    except ImportError:
        print("❌ PIL (Pillow) not available. Creating a simple text-based logo.")
        # Create a simple text file as fallback
        with open("resource/main_logo.txt", "w") as f:
            f.write("📥 SOCIAL DOWNLOADER 🎵\nAI-Powered Transcription")
        print("✅ Text-based logo created: resource/main_logo.txt")
