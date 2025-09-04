
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
        print(f"\n▶️ Downloading from: {url}")
        if mode == 'audio':
            output_dir = self.audio_dir
            extract_audio = True
            audio_format = 'mp3'
            ydl_format = 'bestaudio/best'
            postprocessors = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }]
        elif mode == 'best':
            output_dir = self.video_dir
            extract_audio = False
            ydl_format = 'best'
            postprocessors = []
        else:
            output_dir = self.video_dir
            extract_audio = False
            ydl_format = 'bestvideo+bestaudio/best'
            postprocessors = []

        options = {
            'format': ydl_format,
            'quiet': True,
            'noplaylist': True,
            'progress_hooks': [self._progress_hook],
            'postprocessors': postprocessors,
        }

        if self.cookie_file:
            options['cookiefile'] = self.cookie_file

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', f'{self.platform}_video')
                ext = 'mp3' if extract_audio else 'mp4'
                filename = self._timestamped_filename(title, ext)
                full_path = os.path.join(output_dir, filename)
                options['outtmpl'] = full_path
                ydl.params.update(options)
                ydl.download([url])
                print(f"🎉 Download successful: {full_path}")
                return full_path
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return None

    def transcribe(self, url, model_name="base", segment_minutes=30, keep_audio=False):
        audio_path = self.download(url, mode='audio')
        if not audio_path:
            print("❌ Audio download failed.")
            return None

        print("🎬 Splitting audio into segments using ffmpeg...")
        segment_seconds = segment_minutes * 60
        temp_dir = os.path.join(self.audio_dir, "temp_segments")
        os.makedirs(temp_dir, exist_ok=True)

        segment_template = os.path.join(temp_dir, "part_%03d.mp3")
        split_cmd = [
            "ffmpeg", "-i", audio_path, "-f", "segment", "-segment_time", str(segment_seconds),
            "-c", "copy", segment_template,
            "-hide_banner", "-loglevel", "error"
        ]

        try:
            subprocess.run(split_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ ffmpeg split failed: {e}")
            return None

        print(f"🧠 Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        transcript_name = os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
        final_transcript_path = os.path.join(self.transcribe_dir, transcript_name)

        with open(final_transcript_path, 'w', encoding='utf-8') as final_out:
            parts = sorted([f for f in os.listdir(temp_dir) if f.endswith(".mp3")])
            for idx, part_file in enumerate(parts, start=1):
                part_path = os.path.join(temp_dir, part_file)
                print(f"🧠 Transcribing {part_file} ({idx}/{len(parts)})...")
                result = model.transcribe(part_path)
                final_out.write(result['text'].strip() + '\n\n')

        shutil.rmtree(temp_dir)

        if not keep_audio and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"🗑️ Removed audio file: {audio_path}")

        print(f"✅ Transcript saved at: {final_transcript_path}")
        return final_transcript_path


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
