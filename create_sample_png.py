#!/usr/bin/env python3
"""
Create a sample PNG logo using tkinter (no PIL needed)
"""

import tkinter as tk
from tkinter import Canvas
import os

def create_sample_png():
    """Create a sample PNG using tkinter canvas export"""
    print("🎨 Creating sample PNG logo...")
    
    # Create hidden root window
    root = tk.Tk()
    root.withdraw()
    
    # Create canvas
    width, height = 400, 160
    canvas = Canvas(root, width=width, height=height, bg='#f8f9fa')
    
    # Create gradient-like background with multiple rectangles
    for i in range(0, height, 5):
        intensity = int(240 + (15 * i / height))
        color = f"#{intensity:02x}{intensity:02x}{255:02x}"
        canvas.create_rectangle(0, i, width, i+5, fill=color, outline=color)
    
    # Add main border
    canvas.create_rectangle(8, 8, width-8, height-8, 
                          outline="#2980b9", width=4, fill="")
    
    # Add inner border
    canvas.create_rectangle(12, 12, width-12, height-12, 
                          outline="#3498db", width=2, fill="")
    
    # Main logo text
    canvas.create_text(width//2, height//2 - 25, 
                      text="📥 Social Downloader 🎵", 
                      font=("Arial", 22, "bold"),
                      fill="#2c3e50")
    
    # Subtitle
    canvas.create_text(width//2, height//2 + 5, 
                      text="AI-Powered Transcription", 
                      font=("Arial", 16, "italic"),
                      fill="#7f8c8d")
    
    # Brand tagline
    canvas.create_text(width//2, height//2 + 30, 
                      text="Multi-Platform • Fast • Accurate", 
                      font=("Arial", 11),
                      fill="#95a5a6")
    
    # Decorative corner elements
    # Top-left: Download icon
    canvas.create_oval(25, 25, 55, 55, fill="#27ae60", outline="#2c3e50", width=2)
    canvas.create_text(40, 40, text="⬇", font=("Arial", 18, "bold"), fill="white")
    
    # Top-right: Audio icon
    canvas.create_oval(width-55, 25, width-25, 55, fill="#e74c3c", outline="#2c3e50", width=2)
    canvas.create_text(width-40, 40, text="🎵", font=("Arial", 18), fill="white")
    
    # Bottom-left: Video icon
    canvas.create_oval(25, height-55, 55, height-25, fill="#f39c12", outline="#2c3e50", width=2)
    canvas.create_text(40, height-40, text="📺", font=("Arial", 18), fill="white")
    
    # Bottom-right: AI icon
    canvas.create_oval(width-55, height-55, width-25, height-25, fill="#9b59b6", outline="#2c3e50", width=2)
    canvas.create_text(width-40, height-40, text="🧠", font=("Arial", 18), fill="white")
    
    # Add some decorative lines
    canvas.create_line(70, 50, width-70, 50, fill="#bdc3c7", width=2)
    canvas.create_line(70, height-50, width-70, height-50, fill="#bdc3c7", width=2)
    
    # Try to save as PostScript first (then can be converted)
    output_eps = "resource/img/sample_logo.eps"
    canvas.postscript(file=output_eps)
    print(f"✅ Sample logo saved as {output_eps}")
    
    # Create instructions for PNG conversion
    instructions = f"""
# Sample Logo Created

A sample logo has been created as an EPS file: {output_eps}

## To convert to PNG (if needed):

### Option 1: Using ImageMagick (if installed)
```bash
convert {output_eps} resource/img/main_logo.png
```

### Option 2: Using online converter
1. Upload {output_eps} to an online EPS to PNG converter
2. Download as PNG
3. Save as resource/img/main_logo.png

### Option 3: Using GIMP
1. Open {output_eps} in GIMP
2. Export as PNG
3. Save as resource/img/main_logo.png

## Current Status
The GUI will use the text-based logo until main_logo.png is available.
"""
    
    with open("resource/img/conversion_instructions.txt", "w") as f:
        f.write(instructions)
    
    print("📝 Conversion instructions saved to resource/img/conversion_instructions.txt")
    print("💡 GUI will use text-based logo until main_logo.png is available")
    
    root.destroy()

if __name__ == "__main__":
    create_sample_png()
