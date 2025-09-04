#!/usr/bin/env python3
"""
Modern GUI for Social-Download-Transcribe
Enhanced UI/UX with better design and user experience
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread
import os
import subprocess
import platform
from src.modules.video_downloader_extended import FacebookVideoDownloader, YouTubeDownloader, TikTokDownloader, XDownloader

def detect_platform(url):
    """Detect social media platform from URL"""
    if "facebook.com" in url:
        return "facebook"
    elif "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "twitter.com" in url or "x.com" in url:
        return "x"
    else:
        return None

def get_downloader(platform):
    """Get appropriate downloader for platform"""
    if platform == "facebook":
        return FacebookVideoDownloader()
    elif platform == "youtube":
        return YouTubeDownloader()
    elif platform == "tiktok":
        return TikTokDownloader()
    elif platform == "x":
        return XDownloader()
    else:
        raise ValueError(f"Unsupported platform: {platform}")

class ModernDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.create_styles()
        self.create_widgets()
        self.selected_file = None
        
    def setup_window(self):
        """Setup main window properties"""
        self.master.title("📥 Social Media Downloader & Transcriber")
        
        # Set initial size - can be smaller since content is scrollable
        initial_width = 700
        initial_height = 600  # Reduced from 800 for better fit
        self.master.geometry(f"{initial_width}x{initial_height}")
        self.master.resizable(True, True)
        
        # Set minimum size to ensure usability
        self.master.minsize(600, 400)
        
        # Center window on screen
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (initial_width // 2)
        y = (screen_height // 2) - (initial_height // 2)
        self.master.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        
        # Configure window icon and background
        try:
            # Modern color scheme
            bg_color = "#f8f9fa"  # Slightly lighter for better contrast with scroll
            self.master.configure(bg=bg_color)
        except:
            pass
    
    def create_styles(self):
        """Create custom styles for modern look"""
        self.style = ttk.Style()
        
        # Configure modern theme
        available_themes = self.style.theme_names()
        if "clam" in available_themes:
            self.style.theme_use("clam")
        elif "alt" in available_themes:
            self.style.theme_use("alt")
        
        # Custom styles
        self.style.configure("Header.TLabel", 
                           font=("SF Pro Display", 18, "bold"),
                           foreground="#2c3e50")
        
        self.style.configure("Subheader.TLabel", 
                           font=("SF Pro Display", 14, "bold"),
                           foreground="#34495e")
        
        self.style.configure("Info.TLabel", 
                           font=("SF Pro Text", 11),
                           foreground="#7f8c8d")
        
        self.style.configure("Success.TLabel", 
                           font=("SF Pro Text", 11, "bold"),
                           foreground="#27ae60")
        
        self.style.configure("Error.TLabel", 
                           font=("SF Pro Text", 11, "bold"),
                           foreground="#e74c3c")
        
        self.style.configure("Modern.TButton", 
                           font=("SF Pro Text", 11, "bold"),
                           padding=(20, 10))
        
        self.style.configure("Primary.TButton", 
                           font=("SF Pro Text", 12, "bold"),
                           padding=(25, 12))
    
    def create_widgets(self):
        """Create and layout all GUI widgets with scrollable content"""
        # Main container with minimal padding
        main_container = ttk.Frame(self.master, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Fixed header section (always visible)
        header_container = ttk.Frame(main_container, padding="20")
        header_container.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))
        self.create_header(header_container)
        
        # Create scrollable frame for content
        self.create_scrollable_content(main_container)
    
    def create_scrollable_content(self, parent):
        """Create scrollable content area"""
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind canvas resize to update scrollable frame width
        def configure_scrollable_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', configure_scrollable_width)
        
        # Store canvas reference for event handlers
        self.canvas = canvas
        
        # Enhanced mousewheel handling for cross-platform compatibility
        def on_mousewheel(event):
            # Handle different platforms and event types
            try:
                if hasattr(event, 'delta') and event.delta:
                    # Windows and macOS with delta
                    delta = -1 * int(event.delta / 120)
                elif hasattr(event, 'num'):
                    # Linux button events
                    delta = -1 if event.num == 4 else 1
                else:
                    # Fallback
                    delta = -1
                
                # Scroll the canvas
                canvas.yview_scroll(delta, "units")
                return "break"  # Prevent event propagation
            except Exception as e:
                print(f"Mouse wheel error: {e}")
        
        # Enhanced event binding for better compatibility
        def bind_mousewheel_events(widget):
            """Bind mouse wheel events to widget"""
            # Primary mouse wheel events
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
            
        # Bind to multiple widgets for comprehensive coverage
        bind_mousewheel_events(canvas)
        bind_mousewheel_events(self.master)  # Global binding
        
        # Store reference to rebind later
        self.mousewheel_handler = on_mousewheel
        self.bind_mousewheel_func = bind_mousewheel_events
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable canvas to receive focus for events
        canvas.focus_set()
        canvas.configure(takefocus=True)
        
        # Add content to scrollable frame with padding
        content_frame = ttk.Frame(self.scrollable_frame, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create all content sections in scrollable area
        self.create_platform_info(content_frame)
        self.create_url_section(content_frame)
        self.create_settings_section(content_frame)
        self.create_action_section(content_frame)
        self.create_status_section(content_frame)
        self.create_output_section(content_frame)
        
        # Re-bind mousewheel after all widgets are created
        def rebind_mousewheel():
            """Rebind mouse wheel to all content widgets"""
            try:
                self.bind_mousewheel_func(self.scrollable_frame)
                # Bind to all child widgets recursively
                for widget in self.scrollable_frame.winfo_children():
                    self.bind_mousewheel_func(widget)
            except Exception as e:
                print(f"Rebind error: {e}")
        
        self.master.after(100, rebind_mousewheel)
    
    def create_header(self, parent):
        """Create header section with logo"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo and title container with horizontal layout
        logo_container = ttk.Frame(header_frame)
        logo_container.pack()
        
        # Create horizontal layout: text on left, logo on right
        logo_horizontal_frame = ttk.Frame(logo_container)
        logo_horizontal_frame.pack(pady=(0, 10))
        
        # Left side: Text content
        logo_text_frame = ttk.Frame(logo_horizontal_frame)
        logo_text_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Main logo text with larger font and styling
        logo_style = ttk.Style()
        logo_style.configure("Logo.TLabel", 
                           font=("SF Pro Display", 24, "bold"),
                           foreground="#2c3e50",
                           background="#ecf0f1")
        
        logo_text = ttk.Label(logo_text_frame,
                            text="📥 Social Downloader 🎵",
                            style="Logo.TLabel")
        logo_text.pack(anchor=tk.W)
        
        # Logo subtitle
        logo_subtitle = ttk.Label(logo_text_frame,
                                text="AI-Powered Transcription",
                                font=("SF Pro Text", 12, "italic"),
                                foreground="#7f8c8d")
        logo_subtitle.pack(anchor=tk.W)
        
        # Right side: Logo image (if available)
        logo_loaded = False
        logo_path = "resource/img/main_logo.png"
        
        if os.path.exists(logo_path):
            try:
                from PIL import Image, ImageTk
                # Load and resize logo with proper aspect ratio
                img = Image.open(logo_path)
                
                # Calculate proper dimensions maintaining aspect ratio
                original_width, original_height = img.size
                aspect_ratio = original_width / original_height
                
                # Set maximum dimensions
                max_width = 120
                max_height = 80
                
                # Calculate new dimensions maintaining aspect ratio
                if aspect_ratio > 1:  # Landscape
                    new_width = min(max_width, int(max_height * aspect_ratio))
                    new_height = int(new_width / aspect_ratio)
                else:  # Portrait or square
                    new_height = min(max_height, int(max_width / aspect_ratio))
                    new_width = int(new_height * aspect_ratio)
                
                # Resize with proper aspect ratio
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)
                
                # Create logo label on the right side
                logo_label = ttk.Label(logo_horizontal_frame, image=self.logo_image)
                logo_label.pack(side=tk.RIGHT, padx=(20, 0))
                logo_loaded = True
                
            except ImportError:
                print("PIL not available, logo image not displayed")
            except Exception as e:
                print(f"Could not load logo: {e}")
        
        # App title (temporarily hidden for cleaner header)
        # if not logo_loaded:
        #     title_label = ttk.Label(header_frame, 
        #                            text="🎥 Multi-Platform Video Processor", 
        #                            style="Header.TLabel")
        #     title_label.pack()
        
        # Subtitle (adjust text based on logo presence)
        # subtitle_text = "Download & transcribe videos with AI technology"
        # if logo_loaded:
        #     # More concise subtitle when logo is present
        #     subtitle_text = "YouTube • Facebook • TikTok • X/Twitter"
        
        # subtitle_label = ttk.Label(header_frame, 
        #                          text=subtitle_text, 
        #                          style="Info.TLabel")
        # subtitle_label.pack(pady=(5, 0))
    
    def create_platform_info(self, parent):
        """Create platform support information"""
        platform_frame = ttk.LabelFrame(parent, text="📱 Supported Platforms", padding="15")
        platform_frame.pack(fill=tk.X, pady=(0, 10))
        
        platforms = [
            ("📺 YouTube", "youtube.com, youtu.be"),
            ("📘 Facebook", "facebook.com/watch"),
            ("🎵 TikTok", "tiktok.com"),
            ("🐦 X/Twitter", "x.com, twitter.com")
        ]
        
        for i, (platform, description) in enumerate(platforms):
            row = i // 2
            col = i % 2
            
            platform_info = ttk.Frame(platform_frame)
            platform_info.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
            ttk.Label(platform_info, text=platform, font=("SF Pro Text", 11, "bold")).pack(anchor="w")
            ttk.Label(platform_info, text=description, style="Info.TLabel").pack(anchor="w")
        
        platform_frame.columnconfigure(0, weight=1)
        platform_frame.columnconfigure(1, weight=1)
    
    def create_url_section(self, parent):
        """Create URL input section"""
        url_frame = ttk.LabelFrame(parent, text="🔗 Video Source", padding="15")
        url_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Single URL option
        single_frame = ttk.Frame(url_frame)
        single_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(single_frame, text="Enter video URL:", style="Subheader.TLabel").pack(anchor="w")
        
        self.url_entry = ttk.Entry(single_frame, font=("SF Pro Text", 11), width=70)
        self.url_entry.pack(fill=tk.X, pady=(5, 0))
        self.url_entry.bind("<KeyRelease>", self.on_url_change)
        
        # URL validation indicator
        self.url_status = ttk.Label(single_frame, text="", style="Info.TLabel")
        self.url_status.pack(anchor="w", pady=(2, 0))
        
        # OR separator
        separator_frame = ttk.Frame(url_frame)
        separator_frame.pack(fill=tk.X, pady=10)
        
        ttk.Separator(separator_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        ttk.Label(separator_frame, text="OR", style="Info.TLabel").pack()
        ttk.Separator(separator_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        
        # Batch file option
        batch_frame = ttk.Frame(url_frame)
        batch_frame.pack(fill=tk.X)
        
        ttk.Label(batch_frame, text="Batch processing:", style="Subheader.TLabel").pack(anchor="w")
        
        file_button_frame = ttk.Frame(batch_frame)
        file_button_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.file_button = ttk.Button(file_button_frame, 
                                     text="📂 Select URLs File", 
                                     command=self.select_file,
                                     style="Modern.TButton")
        self.file_button.pack(side=tk.LEFT)
        
        self.clear_file_button = ttk.Button(file_button_frame, 
                                           text="✖ Clear", 
                                           command=self.clear_file,
                                           style="Modern.TButton")
        self.clear_file_button.pack(side=tk.LEFT, padx=(10, 0))
        
        self.file_label = ttk.Label(batch_frame, text="", style="Info.TLabel")
        self.file_label.pack(anchor="w", pady=(5, 0))
    
    def create_settings_section(self, parent):
        """Create settings section"""
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Download Settings", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Download mode
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(mode_frame, text="Download Mode:", style="Subheader.TLabel").pack(anchor="w")
        
        self.mode_var = tk.StringVar(value="video")
        mode_options_frame = ttk.Frame(mode_frame)
        mode_options_frame.pack(fill=tk.X, pady=(5, 0))
        
        modes = [
            ("🎬 Video", "video", "Download full video with audio"),
            ("🎵 Audio Only", "audio", "Extract audio as MP3"),
            ("⭐ Best Quality", "best", "Highest quality available")
        ]
        
        for i, (text, value, description) in enumerate(modes):
            col = i % 3
            mode_col = ttk.Frame(mode_options_frame)
            mode_col.grid(row=0, column=col, padx=10, sticky="w")
            
            ttk.Radiobutton(mode_col, text=text, variable=self.mode_var, 
                           value=value, command=self.on_mode_change).pack(anchor="w")
            ttk.Label(mode_col, text=description, style="Info.TLabel").pack(anchor="w")
        
        mode_options_frame.columnconfigure(0, weight=1)
        mode_options_frame.columnconfigure(1, weight=1)
        mode_options_frame.columnconfigure(2, weight=1)
        
        # AI Transcription section
        ai_frame = ttk.LabelFrame(settings_frame, text="🧠 AI Transcription", padding="10")
        ai_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Transcribe checkbox
        self.transcribe_var = tk.BooleanVar()
        self.transcribe_check = ttk.Checkbutton(ai_frame, 
                                               text="✨ Enable AI transcription", 
                                               variable=self.transcribe_var,
                                               command=self.on_transcribe_change)
        self.transcribe_check.pack(anchor="w", pady=(0, 10))
        
        # Model selection
        self.model_frame = ttk.Frame(ai_frame)
        self.model_frame.pack(fill=tk.X)
        
        model_label_frame = ttk.Frame(self.model_frame)
        model_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(model_label_frame, text="Whisper Model:", font=("SF Pro Text", 10, "bold")).pack(side=tk.LEFT)
        ttk.Label(model_label_frame, text="(affects speed vs accuracy)", style="Info.TLabel").pack(side=tk.LEFT, padx=(10, 0))
        
        self.model_var = tk.StringVar(value="base")
        self.model_dropdown = ttk.Combobox(self.model_frame, 
                                          textvariable=self.model_var,
                                          values=["tiny", "base", "small", "medium", "large"],
                                          state="readonly",
                                          width=15)
        self.model_dropdown.pack(anchor="w")
        
        # Model info
        model_info = {
            "tiny": "⚡ Fastest, less accurate (39MB)",
            "base": "⚖️ Balanced speed & accuracy (74MB)", 
            "small": "🎯 Good accuracy (244MB)",
            "medium": "🔥 High accuracy (769MB)",
            "large": "🏆 Best accuracy (1.5GB)"
        }
        
        self.model_info_label = ttk.Label(self.model_frame, 
                                         text=model_info["base"], 
                                         style="Info.TLabel")
        self.model_info_label.pack(anchor="w", pady=(2, 0))
        
        self.model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)
        # Improve UX: allow mouse click to open dropdown immediately
        def open_model_dropdown(event=None):
            try:
                # Open the dropdown list on mouse click or focus
                self.model_dropdown.event_generate('<Down>')
            except Exception:
                pass
        self.model_dropdown.bind('<Button-1>', open_model_dropdown)
        self.model_dropdown.bind('<FocusIn>', open_model_dropdown)
        
        # Additional options
        options_frame = ttk.Frame(ai_frame)
        options_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.keep_audio_var = tk.BooleanVar()
        self.keep_audio_check = ttk.Checkbutton(options_frame, 
                                               text="💾 Keep audio file after transcription", 
                                               variable=self.keep_audio_var)
        self.keep_audio_check.pack(anchor="w")
        
        # Initially disable AI options
        self.toggle_ai_options(False)
    
    def create_action_section(self, parent):
        """Create action buttons section"""
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Main download button
        self.download_button = ttk.Button(action_frame, 
                                         text="🚀 Start Download", 
                                         command=self.run_download,
                                         style="Primary.TButton")
        self.download_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear all button
        self.clear_button = ttk.Button(action_frame, 
                                      text="🧹 Clear All", 
                                      command=self.clear_all,
                                      style="Modern.TButton")
        self.clear_button.pack(side=tk.LEFT)
    
    def create_status_section(self, parent):
        """Create status and progress section"""
        status_frame = ttk.LabelFrame(parent, text="📊 Status", padding="15")
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Status label
        self.status_label = ttk.Label(status_frame, 
                                     text="Ready to download", 
                                     style="Info.TLabel")
        self.status_label.pack(anchor="w")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, 
                                           variable=self.progress_var,
                                           mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Progress info
        self.progress_info = ttk.Label(status_frame, text="", style="Info.TLabel")
        self.progress_info.pack(anchor="w", pady=(5, 0))
    
    def create_output_section(self, parent):
        """Create output management section"""
        output_frame = ttk.LabelFrame(parent, text="📁 Output Management", padding="15")
        output_frame.pack(fill=tk.X)
        
        # Output location info
        output_path = os.path.abspath("output")
        ttk.Label(output_frame, text=f"Files saved to: {output_path}", style="Info.TLabel").pack(anchor="w")
        
        # Output buttons
        button_frame = ttk.Frame(output_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.open_output_button = ttk.Button(button_frame, 
                                           text="📂 Open Output Folder", 
                                           command=self.open_output_folder,
                                           style="Modern.TButton")
        self.open_output_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_output_button = ttk.Button(button_frame, 
                                            text="🗑️ Clear Output", 
                                            command=self.clear_output,
                                            style="Modern.TButton")
        self.clear_output_button.pack(side=tk.LEFT)
    
    def on_url_change(self, event=None):
        """Handle URL entry changes"""
        url = self.url_entry.get().strip()
        if url:
            platform = detect_platform(url)
            if platform:
                self.url_status.config(text=f"✅ {platform.title()} URL detected", 
                                     foreground="#27ae60")
            else:
                self.url_status.config(text="❌ Unsupported URL format", 
                                     foreground="#e74c3c")
        else:
            self.url_status.config(text="")
    
    def on_mode_change(self):
        """Handle download mode changes"""
        mode = self.mode_var.get()
        if mode == "audio":
            self.transcribe_check.config(text="✨ Enable AI transcription (recommended for audio)")
        else:
            self.transcribe_check.config(text="✨ Enable AI transcription")
    
    def on_transcribe_change(self):
        """Handle transcription toggle"""
        enabled = self.transcribe_var.get()
        self.toggle_ai_options(enabled)
    
    def on_model_change(self, event=None):
        """Handle model selection changes"""
        model = self.model_var.get()
        model_info = {
            "tiny": "⚡ Fastest, less accurate (39MB)",
            "base": "⚖️ Balanced speed & accuracy (74MB)", 
            "small": "🎯 Good accuracy (244MB)",
            "medium": "🔥 High accuracy (769MB)",
            "large": "🏆 Best accuracy (1.5GB)"
        }
        self.model_info_label.config(text=model_info.get(model, ""))
    
    def toggle_ai_options(self, enabled):
        """Enable/disable AI transcription options"""
        # Keep combobox in 'readonly' when enabled so user selects by click,
        # and fully disabled otherwise
        if enabled:
            self.model_dropdown.config(state="readonly")
            self.keep_audio_check.config(state="normal")
        else:
            self.model_dropdown.config(state="disabled")
            self.keep_audio_check.config(state="disabled")
        
        if enabled:
            self.model_frame.pack(fill=tk.X)
        else:
            pass  # Keep visible but disabled
    
    def select_file(self):
        """Select batch URLs file"""
        file_path = filedialog.askopenfilename(
            title="Select URLs file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"📄 Selected: {filename}", foreground="#3498db")
            
            # Count URLs in file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    url_count = len([line for line in f if line.strip()])
                self.file_label.config(text=f"📄 {filename} ({url_count} URLs)")
            except:
                pass
    
    def clear_file(self):
        """Clear selected file"""
        self.selected_file = None
        self.file_label.config(text="")
    
    def clear_all(self):
        """Clear all inputs"""
        self.url_entry.delete(0, tk.END)
        self.clear_file()
        self.url_status.config(text="")
        self.status_label.config(text="Ready to download")
        self.progress_var.set(0)
        self.progress_info.config(text="")
    
    def run_download(self):
        """Start download process in separate thread"""
        Thread(target=self._run_download, daemon=True).start()
    
    def _run_download(self):
        """Main download logic"""
        # Disable button during download
        self.download_button.config(state="disabled")
        
        try:
            urls = []
            
            # Get URLs from file or entry
            if self.selected_file:
                try:
                    with open(self.selected_file, "r", encoding="utf-8") as f:
                        urls = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    messagebox.showerror("File Error", f"Failed to read file: {e}")
                    return
            else:
                url = self.url_entry.get().strip()
                if not url:
                    messagebox.showerror("Input Error", "Please enter a video URL or select a file.")
                    return
                urls.append(url)
            
            if not urls:
                messagebox.showerror("Input Error", "No valid URLs found.")
                return
            
            # Process each URL
            total_urls = len(urls)
            for i, url in enumerate(urls, 1):
                # Update progress
                progress = (i - 1) / total_urls * 100
                self.progress_var.set(progress)
                self.progress_info.config(text=f"Processing {i}/{total_urls}")
                
                # Detect platform
                platform = detect_platform(url)
                if not platform:
                    self.status_label.config(text=f"❌ Unsupported URL: {url[:50]}...", 
                                           foreground="#e74c3c")
                    continue
                
                # Update status
                self.status_label.config(text=f"⏳ Downloading from {platform.title()}...", 
                                       foreground="#f39c12")
                
                try:
                    downloader = get_downloader(platform)
                    
                    if self.transcribe_var.get():
                        result = downloader.transcribe(
                            url,
                            model_name=self.model_var.get(),
                            keep_audio=self.keep_audio_var.get()
                        )
                        self.status_label.config(text=f"✅ Transcribed: {platform.title()}", 
                                               foreground="#27ae60")
                    else:
                        result = downloader.download(url, mode=self.mode_var.get())
                        self.status_label.config(text=f"✅ Downloaded: {platform.title()}", 
                                               foreground="#27ae60")
                
                except Exception as e:
                    self.status_label.config(text=f"❌ Failed: {str(e)[:50]}...", 
                                           foreground="#e74c3c")
                    messagebox.showerror("Download Error", f"Failed to process {url}:\n{str(e)}")
                    continue
            
            # Final status
            self.progress_var.set(100)
            self.progress_info.config(text=f"Completed {total_urls} URLs")
            self.status_label.config(text="🎉 All downloads completed!", 
                                   foreground="#27ae60")
            
            # Show completion message
            messagebox.showinfo("Success", f"Successfully processed {total_urls} URL(s)!")
            
        finally:
            # Re-enable button
            self.download_button.config(state="normal")
    
    def open_output_folder(self):
        """Open output folder in file manager"""
        output_path = os.path.abspath("output")
        try:
            if platform.system() == "Windows":
                os.startfile(output_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", output_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", output_path])
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open folder: {e}")
    
    def clear_output(self):
        """Clear output folder contents"""
        result = messagebox.askyesno("Confirm", 
                                   "Are you sure you want to delete all downloaded files?")
        if result:
            try:
                output_path = "output"
                if os.path.exists(output_path):
                    import shutil
                    shutil.rmtree(output_path)
                    os.makedirs(output_path, exist_ok=True)
                    os.makedirs(os.path.join(output_path, "video"), exist_ok=True)
                    os.makedirs(os.path.join(output_path, "audio"), exist_ok=True)
                    os.makedirs(os.path.join(output_path, "transcribe"), exist_ok=True)
                messagebox.showinfo("Success", "Output folder cleared!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear folder: {e}")

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ModernDownloaderApp(root)
    
    # Handle window close
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
