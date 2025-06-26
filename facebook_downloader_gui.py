import tkinter as tk
from tkinter import filedialog, messagebox
from facebook_video_downloader import FacebookVideoDownloader

class FacebookDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Video Downloader")
        self.root.geometry("500x300")
        self.url = tk.StringVar()
        self.model = tk.StringVar(value="base")
        self.keep_audio = tk.BooleanVar(value=False)
        self.transcribe = tk.BooleanVar(value=True)

        tk.Label(root, text="Facebook Video URL:").pack(pady=5)
        tk.Entry(root, textvariable=self.url, width=60).pack()

        tk.Checkbutton(root, text="Transcribe Audio", variable=self.transcribe).pack()
        tk.Checkbutton(root, text="Keep Audio File", variable=self.keep_audio).pack()

        tk.Label(root, text="Whisper Model (tiny, base, small, medium, large):").pack(pady=5)
        tk.Entry(root, textvariable=self.model).pack()

        tk.Button(root, text="Start Download", command=self.download).pack(pady=20)

    def download(self):
        url = self.url.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid Facebook video URL.")
            return

        try:
            downloader = FacebookVideoDownloader()
            if self.transcribe.get():
                result = downloader.transcribe_audio_from_facebook_video(
                    url=url,
                    model_name=self.model.get(),
                    keep_audio=self.keep_audio.get()
                )
            else:
                result = downloader.download(url, extract_audio=True)

            messagebox.showinfo("Done", f"Finished!\nSaved to:\n{result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookDownloaderGUI(root)
    root.mainloop()
