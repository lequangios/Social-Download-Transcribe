import argparse
from facebook_video_downloader import FacebookVideoDownloader
import os

def main():
    parser = argparse.ArgumentParser(
        description="Download Facebook videos and optionally transcribe using Whisper"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', '-u', help='Facebook video URL to download')
    group.add_argument('--batch', '-b', help='Path to file (txt) containing a list of Facebook video URLs')

    parser.add_argument('--transcribe', '-t', action='store_true', help='Transcribe audio using Whisper')
    parser.add_argument('--model', '-m', default='base', help='Whisper model to use (tiny, base, small, medium, large)')
    parser.add_argument('--cookies', '-c', help='Path to cookies.txt file (for private videos)')
    parser.add_argument('--audio-only', '-a', action='store_true', help='Download audio only without transcription')
    parser.add_argument('--keep-audio', action='store_true', help='Keep .mp3 file after transcription')
    parser.add_argument('--segment', type=int, default=30, help='Max audio segment length in minutes (default: 30)')
    parser.add_argument('--no-title', action='store_true', help='Do not use video title as filename')

    args = parser.parse_args()

    downloader = FacebookVideoDownloader(
        auto_title=not args.no_title,
        cookie_file=args.cookies
    )

    urls = []

    if args.url:
        urls = [args.url]

    elif args.batch:
        if not os.path.exists(args.batch):
            print(f"❌ File not found: {args.batch}")
            return
        with open(args.batch, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]

    # Process all URLs
    for i, url in enumerate(urls, start=1):
        print(f"\n📌 Processing ({i}/{len(urls)}): {url}")
        if args.transcribe:
            downloader.transcribe_audio_from_facebook_video(
                url=url,
                model_name=args.model,
                segment_minutes=args.segment,
                keep_audio=args.keep_audio
            )
        else:
            downloader.download(
                url=url,
                extract_audio=args.audio_only
            )

if __name__ == '__main__':
    main()
