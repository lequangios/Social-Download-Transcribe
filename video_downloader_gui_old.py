
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread
import os
import subprocess
import platform
from src.modules.video_downloader_extended import FacebookVideoDownloader, YouTubeDownloader, TikTokDownloader, XDownloader

def detect_platform(url):
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

class DownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("📥 Multi-Platform Video Downloader")
        master.geometry("500x380")

        self.url_label = ttk.Label(master, text="Video URL:")
        self.url_label.pack(pady=(10, 0))
        self.url_entry = ttk.Entry(master, width=60)
        self.url_entry.pack()

        self.or_label = ttk.Label(master, text="— OR —")
        self.or_label.pack(pady=4)

        self.file_button = ttk.Button(master, text="📂 Select File (Batch URLs)", command=self.select_file)
        self.file_button.pack()

        self.selected_file = None
        self.file_label = ttk.Label(master, text="", foreground="blue")
        self.file_label.pack()

        self.mode_label = ttk.Label(master, text="Download Mode:")
        self.mode_label.pack()
        self.mode_var = tk.StringVar(value="video")
        self.mode_dropdown = ttk.Combobox(master, textvariable=self.mode_var, values=["video", "audio", "best"])
        self.mode_dropdown.pack()

        self.model_label = ttk.Label(master, text="Whisper Model (for transcript):")
        self.model_label.pack()
        self.model_entry = ttk.Entry(master)
        self.model_entry.insert(0, "base")
        self.model_entry.pack()

        self.transcribe_var = tk.BooleanVar()
        self.transcribe_check = ttk.Checkbutton(master, text="Transcribe", variable=self.transcribe_var)
        self.transcribe_check.pack(pady=(10, 0))

        self.keep_audio_var = tk.BooleanVar()
        self.keep_audio_check = ttk.Checkbutton(master, text="Keep Audio File", variable=self.keep_audio_var)
        self.keep_audio_check.pack()

        self.download_button = ttk.Button(master, text="Start Download", command=self.run_download)
        self.download_button.pack(pady=10)

        self.status_label = ttk.Label(master, text="", foreground="green")
        self.status_label.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"📄 {file_path}")

    def run_download(self):
        Thread(target=self._run_download).start()

    def _run_download(self):
        urls = []
        if self.selected_file:
            try:
                with open(self.selected_file, "r", encoding="utf-8") as f:
                    urls = [line.strip() for line in f if line.strip()]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")
                return
        else:
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a video URL or select a file.")
                return
            urls.append(url)

        for url in urls:
            platform = detect_platform(url)
            if not platform:
                messagebox.showerror("Error", f"Could not detect platform from URL: {url}")
                continue
            self.status_label.config(text=f"⏳ Downloading from {platform}...")
            try:
                downloader = get_downloader(platform)
                if self.transcribe_var.get():
                    downloader.transcribe(
                        url,
                        model_name=self.model_entry.get().strip(),
                        keep_audio=self.keep_audio_var.get()
                    )
                else:
                    downloader.download(url, mode=self.mode_var.get())
                self.status_label.config(text="✅ Completed successfully!")
            except Exception as e:
                self.status_label.config(text="❌ Failed")
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()


import subprocess
import platform

class LogWindow:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("📄 Download Log")
        self.text = tk.Text(self.top, wrap="word", height=20, width=80)
        self.text.pack(padx=10, pady=10)
        self.text.insert("end", "Log initialized...\n")
        self.text.config(state="disabled")

    def write(self, msg):
        self.text.config(state="normal")
        self.text.insert("end", msg + "\n")
        self.text.see("end")
        self.text.config(state="disabled")


class DownloaderAppWithLog(DownloaderApp):
    def __init__(self, master):
        super().__init__(master)
        self.log_window = LogWindow(master)

        self.open_output_btn = ttk.Button(master, text="📂 Open Output Folder", command=self.open_output)
        self.open_output_btn.pack(pady=(5, 10))

    def log(self, msg):
        print(msg)
        self.log_window.write(msg)

    def _run_download(self):
        urls = []
        if self.selected_file:
            try:
                with open(self.selected_file, "r", encoding="utf-8") as f:
                    urls = [line.strip() for line in f if line.strip()]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")
                return
        else:
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a video URL or select a file.")
                return
            urls.append(url)

        for url in urls:
            platform_name = detect_platform(url)
            if not platform_name:
                self.log(f"❌ Could not detect platform for URL: {url}")
                continue
            self.status_label.config(text=f"⏳ Downloading from {platform_name}...")
            self.log(f"▶️ Starting download for {url} ({platform_name})")
            try:
                downloader = get_downloader(platform_name)
                if self.transcribe_var.get():
                    result = downloader.transcribe(
                        url,
                        model_name=self.model_entry.get().strip(),
                        keep_audio=self.keep_audio_var.get()
                    )
                    self.log(f"✅ Transcription saved to: {result}")
                else:
                    result = downloader.download(url, mode=self.mode_var.get())
                    self.log(f"✅ Download saved to: {result}")
                self.status_label.config(text="✅ Completed successfully!")
            except Exception as e:
                self.status_label.config(text="❌ Failed")
                self.log(f"❌ Error for {url}: {str(e)}")
                messagebox.showerror("Error", str(e))

    def open_output(self):
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
        try:
            if platform.system() == "Windows":
                os.startfile(output_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", output_path])
            else:
                subprocess.Popen(["xdg-open", output_path])
        except Exception as e:
            self.log(f"❌ Cannot open output folder: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderAppWithLog(root)
    root.mainloop()
