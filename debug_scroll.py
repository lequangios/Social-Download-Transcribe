#!/usr/bin/env python3
"""
Debug mouse wheel events
"""

import tkinter as tk
import platform

def debug_mousewheel():
    """Debug mouse wheel events with simple interface"""
    
    root = tk.Tk()
    root.title("🖱️ Mouse Wheel Debug")
    root.geometry("400x300")
    
    # Create scrollable text area for testing
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Canvas and scrollbar
    canvas = tk.Canvas(frame, bg="white")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    # Add lots of content to make it scrollable
    for i in range(30):
        label = tk.Label(scrollable_frame, 
                        text=f"📄 Line {i+1} - This is scrollable content",
                        anchor="w", padx=10, pady=5)
        label.pack(fill="x")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Mouse wheel event handler with debug output
    def on_mousewheel(event):
        print(f"🖱️ Mouse wheel event detected!")
        print(f"   Platform: {platform.system()}")
        print(f"   Event type: {event.type}")
        print(f"   Event num: {getattr(event, 'num', 'N/A')}")
        print(f"   Event delta: {getattr(event, 'delta', 'N/A')}")
        
        # Scroll the canvas
        if hasattr(event, 'delta') and event.delta:
            delta = -1 * (event.delta / 120)
        else:
            delta = -1 if getattr(event, 'num', 5) == 4 else 1
        
        canvas.yview_scroll(int(delta), "units")
        
        # Visual feedback
        root.title(f"🖱️ Mouse Wheel Debug - Scroll detected! Delta: {delta}")
        root.after(2000, lambda: root.title("🖱️ Mouse Wheel Debug"))
    
    # Comprehensive event binding
    events_to_bind = [
        "<MouseWheel>",      # Windows/macOS
        "<Button-4>",        # Linux scroll up  
        "<Button-5>",        # Linux scroll down
        "<Shift-MouseWheel>", # macOS trackpad
        "<Control-MouseWheel>" # macOS gestures
    ]
    
    for event in events_to_bind:
        try:
            canvas.bind(event, on_mousewheel)
            scrollable_frame.bind(event, on_mousewheel)
            root.bind(event, on_mousewheel)
            print(f"✅ Bound event: {event}")
        except Exception as e:
            print(f"❌ Failed to bind {event}: {e}")
    
    # Configure canvas width
    def configure_canvas_width(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind('<Configure>', configure_canvas_width)
    
    # Layout
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Instructions
    instruction_frame = tk.Frame(root)
    instruction_frame.pack(fill="x", padx=10, pady=5)
    
    instruction_label = tk.Label(instruction_frame, 
                               text="🎯 Try scrolling with mouse wheel or trackpad\nCheck terminal for debug output",
                               justify="center", fg="blue")
    instruction_label.pack()
    
    print(f"🖥️ Running on: {platform.system()}")
    print("🎯 Try scrolling and watch for debug output...")
    print("=" * 50)
    
    # Enable focus
    canvas.focus_set()
    canvas.configure(takefocus=True)
    
    root.mainloop()

if __name__ == "__main__":
    debug_mousewheel()
