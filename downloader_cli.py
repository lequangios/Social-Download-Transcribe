
import argparse
import re
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

def process_url(url, mode, transcribe, model, keep_audio):
    url = url.strip()
    if not url:
        return
    platform = detect_platform(url)
    if not platform:
        print(f"❌ Could not detect platform from URL: {url}")
        return
    print(f"▶️ Processing [{platform.upper()}] {url}")
    downloader = get_downloader(platform)
    if transcribe:
        downloader.transcribe(url, model_name=model, keep_audio=keep_audio)
    else:
        downloader.download(url, mode=mode)

def main():
    parser = argparse.ArgumentParser(
        description="📥 Multi-Platform Video Downloader with Whisper Transcription (Batch Supported)",
        epilog="""
Examples:
  python downloader_cli.py "https://www.youtube.com/watch?v=xyz123"
  python downloader_cli.py --file urls.txt --mode audio --transcribe --model small
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("url", nargs="?", help="Video URL (YouTube, Facebook, TikTok, or X)")
    parser.add_argument("--file", help="Path to text file containing multiple URLs (one per line)")
    parser.add_argument("--mode", choices=["video", "audio", "best"], default="video", help="Download mode (default: video)")
    parser.add_argument("--transcribe", action="store_true", help="Transcribe audio after download")
    parser.add_argument("--model", default="base", help="Whisper model to use (default: base)")
    parser.add_argument("--keep-audio", action="store_true", help="Keep audio file after transcription")

    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                for line in f:
                    process_url(line.strip(), args.mode, args.transcribe, args.model, args.keep_audio)
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
    elif args.url:
        process_url(args.url, args.mode, args.transcribe, args.model, args.keep_audio)
    else:
        print("❌ Please provide a URL or use --file to specify a list of URLs.")

if __name__ == "__main__":
    main()
