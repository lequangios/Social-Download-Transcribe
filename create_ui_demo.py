#!/usr/bin/env python3
"""
Create UI demo to showcase modern improvements
"""

import tkinter as tk
from video_downloader_gui import ModernDownloaderApp
import time

def demo_ui_features():
    """Demo the new UI features"""
    print("🎨 Creating Modern UI Demo...")
    
    root = tk.Tk()
    app = ModernDownloaderApp(root)
    
    # Pre-populate with sample data
    app.url_entry.insert(0, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    app.on_url_change()
    
    app.transcribe_var.set(True)
    app.on_transcribe_change()
    
    app.model_var.set("small")
    app.on_model_change()
    
    app.keep_audio_var.set(True)
    
    # Set status
    app.status_label.config(text="✨ Modern UI Ready - Try the new features!", 
                           foreground="#27ae60")
    
    print("🚀 Modern UI Demo is running!")
    print("📋 New Features:")
    print("  ✅ Modern design with better spacing")
    print("  ✅ Real-time URL validation")
    print("  ✅ Platform support information")
    print("  ✅ Advanced AI transcription settings")
    print("  ✅ Progress tracking")
    print("  ✅ Output management")
    print("  ✅ Better error handling")
    print("  ✅ Improved UX with tooltips and descriptions")
    
    # Show window
    root.deiconify()
    root.lift()
    root.focus_force()
    
    root.mainloop()

if __name__ == "__main__":
    demo_ui_features()
