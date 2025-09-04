#!/usr/bin/env python3
"""
Build script for creating portable executable
Social Downloader - Portable Build System
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path
from datetime import datetime

def log_with_timestamp(message, level="INFO"):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "PROGRESS": "🔄"}
    icon = icons.get(level, "📝")
    print(f"[{timestamp}] {icon} {message}")

def build_portable():
    """Build portable executable using PyInstaller"""
    start_time = time.time()
    log_with_timestamp("Starting Portable Social Downloader Build", "PROGRESS")
    print("=" * 60)
    
    # Check if we're in virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        log_with_timestamp("Not in virtual environment - consider using venv for cleaner build", "WARNING")
    else:
        log_with_timestamp("Running in virtual environment", "SUCCESS")
    
    # PyInstaller command
    log_with_timestamp("Preparing PyInstaller command", "PROGRESS")
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI app)
        "--name=SocialDownloader",      # Executable name
        "--add-data=resource:resource", # Include resource folder
        "--add-data=src:src",           # Include src folder
        "--hidden-import=PIL",          # Ensure PIL is included
        "--hidden-import=yt_dlp",       # Ensure yt-dlp is included
        "--hidden-import=whisper",      # Ensure whisper is included
        "--hidden-import=torch",        # Ensure torch is included
        "--hidden-import=torchaudio",   # Ensure torchaudio is included
        "--hidden-import=ffmpeg",       # Ensure ffmpeg-python is included
        "--hidden-import=tqdm",         # Ensure tqdm is included
        "--hidden-import=numpy",        # Ensure numpy is included
        "--clean",                      # Clean build cache
        "video_downloader_gui.py"       # Main script
    ]
    
    # Add icon if file exists
    if os.path.exists("resource/img/main_logo.png"):
        cmd.insert(-1, "--icon=resource/img/main_logo.png")
        log_with_timestamp("Logo icon found and will be included", "SUCCESS")
    else:
        log_with_timestamp("No icon file found, building without icon", "INFO")
    
    log_with_timestamp("PyInstaller command prepared", "SUCCESS")
    print("\n📦 PyInstaller Command:")
    print(" ".join(cmd))
    print()
    
    try:
        log_with_timestamp("Starting PyInstaller build process", "PROGRESS")
        log_with_timestamp("This may take 5-10 minutes depending on system performance", "INFO")
        
        # Run PyInstaller with real-time output
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            bufsize=1, 
            universal_newlines=True
        )
        
        # Stream output in real-time
        build_output = []
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Filter and display important messages
                output = output.strip()
                if output:
                    build_output.append(output)
                    # Show important progress messages
                    if any(keyword in output.lower() for keyword in [
                        'loading', 'analyzing', 'building', 'collecting', 
                        'copying', 'creating', 'writing', 'generating'
                    ]):
                        log_with_timestamp(f"PyInstaller: {output}", "PROGRESS")
        
        # Wait for process to complete
        return_code = process.poll()
        
        if return_code == 0:
            log_with_timestamp("PyInstaller build completed successfully!", "SUCCESS")
        else:
            log_with_timestamp(f"PyInstaller build failed with return code: {return_code}", "ERROR")
            # Show last few lines of output for debugging
            log_with_timestamp("Last few lines of build output:", "ERROR")
            for line in build_output[-5:]:
                print(f"    {line}")
            return False
        
        # Check if executable was created
        exe_path = "dist/SocialDownloader"
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            log_with_timestamp(f"Executable created: {exe_path}", "SUCCESS")
            log_with_timestamp(f"Executable size: {size:.1f} MB", "INFO")
            
            # Create portable package
            log_with_timestamp("Creating portable package", "PROGRESS")
            create_portable_package()
            
        else:
            log_with_timestamp("Executable not found in dist/ folder", "ERROR")
            return False
            
    except Exception as e:
        log_with_timestamp(f"Build failed with exception: {e}", "ERROR")
        return False
    
    # Calculate build time
    build_time = time.time() - start_time
    log_with_timestamp(f"Total build time: {build_time:.1f} seconds", "SUCCESS")
    
    return True

def create_portable_package():
    """Create portable package with all necessary files"""
    log_with_timestamp("Creating portable package", "PROGRESS")
    
    # Create portable directory
    portable_dir = "SocialDownloader_Portable"
    if os.path.exists(portable_dir):
        log_with_timestamp("Removing existing portable directory", "PROGRESS")
        shutil.rmtree(portable_dir)
    log_with_timestamp("Creating portable directory", "PROGRESS")
    os.makedirs(portable_dir)
    
    # Copy executable
    exe_source = "dist/SocialDownloader"
    exe_dest = f"{portable_dir}/SocialDownloader"
    log_with_timestamp("Copying executable file", "PROGRESS")
    shutil.copy2(exe_source, exe_dest)
    log_with_timestamp("Executable copied successfully", "SUCCESS")
    
    # Copy resource folder
    if os.path.exists("resource"):
        log_with_timestamp("Copying resource folder", "PROGRESS")
        shutil.copytree("resource", f"{portable_dir}/resource")
        log_with_timestamp("Resource folder copied successfully", "SUCCESS")
    else:
        log_with_timestamp("Resource folder not found", "WARNING")
    
    # Create output directory
    log_with_timestamp("Creating output directories", "PROGRESS")
    os.makedirs(f"{portable_dir}/output", exist_ok=True)
    os.makedirs(f"{portable_dir}/output/video", exist_ok=True)
    os.makedirs(f"{portable_dir}/output/audio", exist_ok=True)
    os.makedirs(f"{portable_dir}/output/transcribe", exist_ok=True)
    log_with_timestamp("Output directories created", "SUCCESS")
    
    # Create README for portable version
    readme_content = """# Social Downloader - Portable Version

## 🚀 Quick Start
1. Double-click `SocialDownloader` to run
2. Enter video URL or select batch file
3. Choose download settings
4. Click "Start Download"

## 📁 Folders
- `output/` - Downloaded files
- `resource/` - App resources and logo

## 🎯 Supported Platforms
- YouTube (youtube.com, youtu.be)
- Facebook (facebook.com/watch)
- TikTok (tiktok.com)
- X/Twitter (x.com, twitter.com)

## ⚙️ Requirements
- macOS 10.13+ (for this build)
- Internet connection
- FFmpeg (for audio processing)

## 🆘 Troubleshooting
- If app won't start, try running from Terminal
- Check internet connection
- Ensure FFmpeg is installed system-wide

## 📝 Notes
- First run may be slower (model download)
- Large models (medium/large) require more disk space
- Audio files are saved in MP3 format
- Transcripts are saved as TXT files

Enjoy using Social Downloader! 🎉
"""
    
    log_with_timestamp("Creating README.txt file", "PROGRESS")
    with open(f"{portable_dir}/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    log_with_timestamp("README.txt created successfully", "SUCCESS")
    
    # Create run script for easy execution
    log_with_timestamp("Creating launcher script", "PROGRESS")
    run_script = """#!/bin/bash
# Social Downloader Launcher
echo "🚀 Starting Social Downloader..."
./SocialDownloader
"""
    
    with open(f"{portable_dir}/run.sh", "w") as f:
        f.write(run_script)
    
    # Make run script executable
    os.chmod(f"{portable_dir}/run.sh", 0o755)
    log_with_timestamp("Launcher script created and made executable", "SUCCESS")
    
    log_with_timestamp(f"Portable package created: {portable_dir}/", "SUCCESS")
    log_with_timestamp("Package contents:", "INFO")
    print(f"   • SocialDownloader (executable)")
    print(f"   • resource/ (app resources)")
    print(f"   • output/ (download folder)")
    print(f"   • README.txt (instructions)")
    print(f"   • run.sh (launcher script)")
    
    # Calculate total size
    log_with_timestamp("Calculating package size", "PROGRESS")
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(portable_dir):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1
    
    log_with_timestamp(f"Total package size: {total_size / (1024 * 1024):.1f} MB", "INFO")
    log_with_timestamp(f"Total files: {file_count}", "INFO")

def check_requirements():
    """Check if all requirements are met"""
    log_with_timestamp("Checking build requirements", "PROGRESS")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        log_with_timestamp("Python 3.8+ required", "ERROR")
        return False
    log_with_timestamp(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}", "SUCCESS")
    
    # Check if main files exist
    required_files = [
        "video_downloader_gui.py",
        "src/modules/video_downloader_extended.py",
        "requirements.txt"
    ]
    
    log_with_timestamp("Checking required files", "PROGRESS")
    for file in required_files:
        if os.path.exists(file):
            log_with_timestamp(f"Found: {file}", "SUCCESS")
        else:
            log_with_timestamp(f"Missing: {file}", "ERROR")
            return False
    
    # Check if PyInstaller is installed
    log_with_timestamp("Checking PyInstaller installation", "PROGRESS")
    try:
        import PyInstaller
        log_with_timestamp(f"PyInstaller {PyInstaller.__version__}", "SUCCESS")
    except ImportError:
        log_with_timestamp("PyInstaller not installed", "ERROR")
        log_with_timestamp("Install with: pip install pyinstaller", "INFO")
        return False
    
    # Check if key dependencies are available
    log_with_timestamp("Checking key dependencies", "PROGRESS")
    dependencies = ["PIL", "yt_dlp", "whisper", "torch", "tqdm", "numpy"]
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            log_with_timestamp(f"Dependency {dep} available", "SUCCESS")
        except ImportError:
            missing_deps.append(dep)
            log_with_timestamp(f"Dependency {dep} missing", "WARNING")
    
    if missing_deps:
        log_with_timestamp(f"Missing dependencies: {', '.join(missing_deps)}", "WARNING")
        log_with_timestamp("Some features may not work properly", "WARNING")
    
    log_with_timestamp("Requirements check completed", "SUCCESS")
    return True

def clean_build():
    """Clean previous build files"""
    log_with_timestamp("Cleaning previous build files", "PROGRESS")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_removed = 0
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            log_with_timestamp(f"Removing directory: {dir_name}/", "PROGRESS")
            shutil.rmtree(dir_name)
            log_with_timestamp(f"Removed {dir_name}/", "SUCCESS")
            files_removed += 1
    
    # Clean .spec files
    log_with_timestamp("Cleaning .spec files", "PROGRESS")
    spec_files = list(Path(".").glob("*.spec"))
    for spec_file in spec_files:
        log_with_timestamp(f"Removing {spec_file}", "PROGRESS")
        spec_file.unlink()
        log_with_timestamp(f"Removed {spec_file}", "SUCCESS")
        files_removed += 1
    
    if files_removed == 0:
        log_with_timestamp("No previous build files found to clean", "INFO")
    else:
        log_with_timestamp(f"Cleaned {files_removed} build artifacts", "SUCCESS")

def main():
    """Main build process"""
    start_time = time.time()
    log_with_timestamp("Social Downloader - Portable Build System", "PROGRESS")
    print("=" * 60)
    
    # Check requirements
    log_with_timestamp("Starting build process", "PROGRESS")
    if not check_requirements():
        log_with_timestamp("Requirements check failed!", "ERROR")
        log_with_timestamp("Please fix the issues above and try again", "INFO")
        return False
    
    # Clean previous builds
    log_with_timestamp("Cleaning previous builds", "PROGRESS")
    clean_build()
    
    # Build portable
    log_with_timestamp("Starting portable build", "PROGRESS")
    if build_portable():
        total_time = time.time() - start_time
        log_with_timestamp("Portable build completed successfully!", "SUCCESS")
        log_with_timestamp(f"Total process time: {total_time:.1f} seconds", "SUCCESS")
        print("\n🎉 Build Summary:")
        print("   ✅ Executable created successfully")
        print("   ✅ Portable package ready for distribution")
        print("   ✅ All resources included")
        print("\n📦 Distribution Ready:")
        print("   • SocialDownloader_Portable/ folder contains everything")
        print("   • Users just need to double-click SocialDownloader to run")
        print("   • No installation required")
        print("\n📋 Next Steps:")
        print("   1. Test the executable: ./SocialDownloader_Portable/SocialDownloader")
        print("   2. Compress the folder for distribution")
        print("   3. Share with users who need the application")
        return True
    else:
        total_time = time.time() - start_time
        log_with_timestamp("Build failed!", "ERROR")
        log_with_timestamp(f"Process time: {total_time:.1f} seconds", "INFO")
        print("\n❌ Build Failed - Common Solutions:")
        print("   • Ensure all dependencies are installed: pip install -r requirements.txt")
        print("   • Check that all source files exist")
        print("   • Verify PyInstaller is working: pip install pyinstaller")
        print("   • Check available disk space (need ~1GB)")
        print("   • Try running in a clean virtual environment")
        return False

if __name__ == "__main__":
    main()