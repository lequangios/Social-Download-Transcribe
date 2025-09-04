#!/usr/bin/env python3
"""
Custom build script for lightweight preset
Generated on 2025-09-04 20:57:02
"""

import subprocess
import sys
import os
from build_options import BuildOptions

def main():
    """Build with lightweight preset"""
    print("🚀 Building Social Downloader - LIGHTWEIGHT preset")
    print("=" * 50)
    
    options = BuildOptions()
    cmd = ['pyinstaller', '--onefile', '--windowed', '--clean', '--name', 'SocialDownloader', '--add-data', 'resource:resource', '--add-data', 'src:src', '--hidden-import', 'PIL', '--hidden-import', 'yt_dlp', '--hidden-import', 'ffmpeg', '--hidden-import', 'tqdm', '--hidden-import', 'numpy', '--hidden-import', 'tkinter', '--hidden-import', 'threading', '--icon', 'resource/img/main_logo.png', '--osx-bundle-identifier=com.socialdownloader.app', 'video_downloader_gui.py']
    
    print("📦 PyInstaller Command:")
    print(" ".join(cmd))
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
