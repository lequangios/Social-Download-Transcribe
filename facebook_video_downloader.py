import yt_dlp
import os
from pydub import AudioSegment
import tempfile
import shutil
from tqdm import tqdm
import whisper
import ssl
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context

class FacebookVideoDownloader:
    def __init__(self, auto_title=True, cookie_file=None):
        """
        Initialize downloader with output folder as ./dist/
        :param auto_title: Use original video title as filename
        :param cookie_file: Path to Facebook cookies.txt file
        """
        self.auto_title = auto_title
        self.cookie_file = cookie_file
        self._tqdm_bar = None

        # Set output directory to ./dist relative to this file
        self.output_dir = os.path.join(os.path.dirname(__file__), 'dist')
        os.makedirs(self.output_dir, exist_ok=True)

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
                    desc="📥 Downloading",
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

    def _get_ydl_options(self, extract_audio=False, audio_format='mp3'):
        title_template = '%(title)s.%(ext)s' if self.auto_title else 'facebook_video.%(ext)s'
        outtmpl = os.path.join(self.output_dir, title_template)

        options = {
            'outtmpl': outtmpl,
            'format': 'bestaudio/best' if extract_audio else 'bestvideo+bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'progress_hooks': [self._progress_hook],
        }

        if extract_audio:
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }]

        if self.cookie_file:
            options['cookiefile'] = self.cookie_file

        return options

    def download(self, url, extract_audio=False):
        """
        Download a Facebook video (or extract audio only) and save it in ./dist
        :param url: Facebook video URL
        :param extract_audio: Set True to download as .mp3 only
        :return: Full path to the downloaded file
        """
        print(f"\n▶️ Downloading from: {url}")
        options = self._get_ydl_options(extract_audio=extract_audio)
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                if extract_audio:
                    file_path = os.path.splitext(file_path)[0] + '.mp3'
                print("🎉 Download complete!")
                return file_path
            except Exception as e:
                if self._tqdm_bar:
                    self._tqdm_bar.close()
                print(f"❌ Download failed: {e}")
                return None

    def transcribe_audio_from_facebook_video(self, url, model_name="base", segment_minutes=30, keep_audio=False):
        """
        Download Facebook video as audio and transcribe it using Whisper.
        Audio is processed in chunks (default 30 min) using ffmpeg to minimize RAM usage.
        """
        print(f"🎧 Downloading audio from: {url}")
        audio_path = self.download(url, extract_audio=True)
        if not audio_path:
            print("❌ Failed to download audio.")
            return None

        print("🎬 Splitting audio into segments using ffmpeg...")

        # Setup
        segment_seconds = segment_minutes * 60
        temp_dir = os.path.join(self.output_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Use ffmpeg to split audio without loading full file into RAM
        segment_template = os.path.join(temp_dir, "part_%03d.mp3")
        split_cmd = [
            "ffmpeg",
            "-i", audio_path,
            "-f", "segment",
            "-segment_time", str(segment_seconds),
            "-c", "copy",
            segment_template,
            "-hide_banner", "-loglevel", "error"
        ]

        try:
            subprocess.run(split_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ ffmpeg split failed: {e}")
            return None

        # Transcribe
        print(f"🧠 Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        final_transcript_path = audio_path.replace('.mp3', '.txt')

        with open(final_transcript_path, 'w', encoding='utf-8') as final_out:
            parts = sorted([f for f in os.listdir(temp_dir) if f.endswith(".mp3")])
            for idx, part_file in enumerate(parts, start=1):
                part_path = os.path.join(temp_dir, part_file)
                print(f"🧠 Transcribing {part_file} ({idx}/{len(parts)})...")
                result = model.transcribe(part_path)
                final_out.write(result['text'].strip() + "\n\n")

        # Cleanup
        shutil.rmtree(temp_dir)
        if not keep_audio and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"🗑️ Removed audio file: {audio_path}")

        print(f"✅ Full transcript saved at: {final_transcript_path}")
        return final_transcript_path

