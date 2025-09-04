
import yt_dlp
import os
import shutil
from tqdm import tqdm
import whisper
import ssl
import subprocess
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context


class BaseDownloader:
    def __init__(self, platform, auto_title=True, cookie_file=None):
        self.platform = platform
        self.auto_title = auto_title
        self.cookie_file = cookie_file
        self._tqdm_bar = None

        base_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        self.video_dir = os.path.abspath(os.path.join(base_dir, 'video'))
        self.audio_dir = os.path.abspath(os.path.join(base_dir, 'audio'))
        self.transcribe_dir = os.path.abspath(os.path.join(base_dir, 'transcribe'))

        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.transcribe_dir, exist_ok=True)

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)

            if self._tqdm_bar is None and total_bytes:
                self._tqdm_bar = tqdm(
                    total=total_bytes,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"📥 Downloading {self.platform}",
                    dynamic_ncols=True
                )

            if self._tqdm_bar:
                self._tqdm_bar.n = downloaded_bytes
                self._tqdm_bar.refresh()

        elif d['status'] == 'finished':
            if self._tqdm_bar:
                self._tqdm_bar.n = self._tqdm_bar.total
                self._tqdm_bar.refresh()
                self._tqdm_bar.close()
                self._tqdm_bar = None
            print(f"\n✅ Download completed: {d.get('filename', '')}")

    def _timestamped_filename(self, title, ext):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in "._-" else "_" for c in title)
        return f"{safe_title}_{ts}.{ext}"

    def download(self, url, mode='video'):
class FacebookVideoDownloader(BaseDownloader):
    def __init__(self, auto_title=True, cookie_file=None):
        super().__init__(platform='facebook', auto_title=auto_title, cookie_file=cookie_file)


class YouTubeDownloader(BaseDownloader):
    def __init__(self, auto_title=True):
        super().__init__(platform='youtube', auto_title=auto_title)


class TikTokDownloader(BaseDownloader):
    def __init__(self, auto_title=True):
        super().__init__(platform='tiktok', auto_title=auto_title)

class XDownloader(BaseDownloader):
    def __init__(self, auto_title=True):
        super().__init__(platform='x', auto_title=auto_title)


        # Updated download function with correct output path logic
        import yt_dlp
        import os
        from pathlib import Path
        from slugify import slugify

        mode = mode or "video"
        extract_audio = mode == "audio"
        output_type = "audio" if extract_audio else "video"

        # Create output directory based on mode
        output_dir = os.path.join(Path(__file__).resolve().parent.parent, "output", output_type)
        os.makedirs(output_dir, exist_ok=True)

        # Use yt_dlp to get video info
        options = {
            "quiet": True,
            "noplaylist": True,
            "format": "bestaudio/best" if extract_audio else "bestvideo+bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }] if extract_audio else [],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", f"video")
            ext = "mp3" if extract_audio else "mp4"
            filename = self._timestamped_filename(title, ext)
            full_path = os.path.join(output_dir, filename)

            # Update output path before downloading
            options["outtmpl"] = full_path
            ydl.params.update(options)

            # Download the file
            ydl.download([url])

            # Verify file exists
            if os.path.exists(full_path):
                print(f"✅ File saved: {full_path}")
                return full_path
            else:
                print(f"❌ File not found at {full_path}")
                return None
