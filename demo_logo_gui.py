#!/usr/bin/env python3
"""
Demo GUI with logo
"""

import tkinter as tk
from video_downloader_gui import ModernDownloaderApp

def demo_with_logo():
    """Demo the GUI with logo"""
    print("🎨 Creating GUI Demo with Logo...")
    
    root = tk.Tk()
    app = ModernDownloaderApp(root)
    
    # Pre-populate with sample data to show functionality
    app.url_entry.insert(0, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    app.on_url_change()
    
    app.transcribe_var.set(True)
    app.on_transcribe_change()
    
    app.model_var.set("base")
    app.on_model_change()
    
    # Set welcoming status
    app.status_label.config(text="🎨 Welcome! Logo-enhanced GUI ready to use", 
                           foreground="#27ae60")
    
    print("🚀 GUI Demo with Logo is running!")
    print("✨ Features:")
    print("  📥 Enhanced header with stylized logo")
    print("  🎨 Professional text-based branding")
    print("  🌈 Improved visual hierarchy")
    print("  💫 Better brand recognition")
    
    # Show window
    root.deiconify()
    root.lift()
    root.focus_force()
    
    root.mainloop()

if __name__ == "__main__":
    demo_with_logo()
