#!/usr/bin/env python3
"""
Build Options for Social Downloader
Provides different build configurations and presets
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

class BuildOptions:
    """Build configuration options for Social Downloader"""
    
    def __init__(self):
        self.base_options = {
            "name": "SocialDownloader",
            "main_script": "video_downloader_gui.py",
            "icon": "resource/img/main_logo.png",
            "add_data": [
                "resource:resource",
                "src:src"
            ],
            "hidden_imports": [
                "PIL", "yt_dlp", "whisper", "torch", "torchaudio",
                "ffmpeg", "tqdm", "numpy", "tkinter", "threading"
            ]
        }
        
        self.build_presets = {
            "standard": {
                "description": "Standard build with all features",
                "options": ["--onefile", "--windowed", "--clean"],
                "size_estimate": "~240MB",
                "features": "Full GUI, all platforms, AI transcription"
            },
            "lightweight": {
                "description": "Lightweight build without heavy dependencies",
                "options": ["--onefile", "--windowed", "--clean"],
                "exclude_modules": ["torch", "torchaudio", "whisper"],
                "size_estimate": "~50MB",
                "features": "GUI, basic download, no AI transcription"
            },
            "console": {
                "description": "Console version for debugging",
                "options": ["--onefile", "--clean"],
                "size_estimate": "~240MB",
                "features": "Console output, full features, debugging"
            },
            "directory": {
                "description": "Directory build for faster startup",
                "options": ["--onedir", "--windowed", "--clean"],
                "size_estimate": "~240MB (multiple files)",
                "features": "Faster startup, multiple files"
            },
            "development": {
                "description": "Development build with debug info",
                "options": ["--onedir", "--clean", "--debug=all"],
                "size_estimate": "~300MB",
                "features": "Debug info, development tools"
            }
        }
        
        self.platform_options = {
            "windows": {
                "icon_ext": ".ico",
                "exe_ext": ".exe",
                "additional_options": ["--uac-admin"]
            },
            "macos": {
                "icon_ext": ".icns",
                "exe_ext": "",
                "additional_options": ["--osx-bundle-identifier=com.socialdownloader.app"]
            },
            "linux": {
                "icon_ext": ".png",
                "exe_ext": "",
                "additional_options": []
            }
        }

    def get_current_platform(self):
        """Detect current platform"""
        if sys.platform.startswith('win'):
            return 'windows'
        elif sys.platform.startswith('darwin'):
            return 'macos'
        else:
            return 'linux'

    def generate_pyinstaller_command(self, preset="standard", custom_options=None):
        """Generate PyInstaller command based on preset and options"""
        if preset not in self.build_presets:
            raise ValueError(f"Unknown preset: {preset}")
        
        config = self.build_presets[preset].copy()
        platform = self.get_current_platform()
        
        # Start with base command
        cmd = ["pyinstaller"]
        
        # Add preset options
        cmd.extend(config.get("options", []))
        
        # Add name
        cmd.extend(["--name", self.base_options["name"]])
        
        # Add data files
        for data in self.base_options["add_data"]:
            cmd.extend(["--add-data", data])
        
        # Add hidden imports (exclude if specified)
        exclude_modules = config.get("exclude_modules", [])
        for imp in self.base_options["hidden_imports"]:
            if imp not in exclude_modules:
                cmd.extend(["--hidden-import", imp])
        
        # Add icon if exists
        icon_path = self.base_options["icon"]
        if os.path.exists(icon_path):
            cmd.extend(["--icon", icon_path])
        
        # Add platform-specific options
        platform_config = self.platform_options[platform]
        cmd.extend(platform_config["additional_options"])
        
        # Add custom options
        if custom_options:
            cmd.extend(custom_options)
        
        # Add main script
        cmd.append(self.base_options["main_script"])
        
        return cmd

    def list_presets(self):
        """List available build presets"""
        print("🎯 Available Build Presets:")
        print("=" * 50)
        
        for name, config in self.build_presets.items():
            print(f"\n📦 {name.upper()}")
            print(f"   Description: {config['description']}")
            print(f"   Size: {config['size_estimate']}")
            print(f"   Features: {config['features']}")
            if "exclude_modules" in config:
                print(f"   Excludes: {', '.join(config['exclude_modules'])}")

    def create_build_script(self, preset="standard", output_file="build_custom.py"):
        """Create a custom build script for specific preset"""
        cmd = self.generate_pyinstaller_command(preset)
        
        script_content = f'''#!/usr/bin/env python3
"""
Custom build script for {preset} preset
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import subprocess
import sys
import os
from build_options import BuildOptions

def main():
    """Build with {preset} preset"""
    print("🚀 Building Social Downloader - {preset.upper()} preset")
    print("=" * 50)
    
    options = BuildOptions()
    cmd = {cmd}
    
    print("📦 PyInstaller Command:")
    print(" ".join(cmd))
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {{e}}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
        
        with open(output_file, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(output_file, 0o755)
        
        print(f"✅ Custom build script created: {output_file}")
        return output_file

    def save_config(self, preset="standard", filename="build_config.json"):
        """Save build configuration to JSON file"""
        config = {
            "preset": preset,
            "timestamp": datetime.now().isoformat(),
            "platform": self.get_current_platform(),
            "pyinstaller_command": self.generate_pyinstaller_command(preset),
            "preset_config": self.build_presets[preset]
        }
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Build configuration saved: {filename}")
        return filename

    def load_config(self, filename="build_config.json"):
        """Load build configuration from JSON file"""
        if not os.path.exists(filename):
            print(f"❌ Configuration file not found: {filename}")
            return None
        
        with open(filename, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Build configuration loaded: {filename}")
        return config

def main():
    """Main CLI interface for build options"""
    parser = argparse.ArgumentParser(description="Social Downloader Build Options")
    parser.add_argument("--list", action="store_true", help="List available presets")
    parser.add_argument("--preset", default="standard", help="Build preset to use")
    parser.add_argument("--generate", action="store_true", help="Generate custom build script")
    parser.add_argument("--save-config", action="store_true", help="Save configuration to file")
    parser.add_argument("--load-config", help="Load configuration from file")
    parser.add_argument("--command", action="store_true", help="Show PyInstaller command")
    parser.add_argument("--custom", nargs="*", help="Custom PyInstaller options")
    
    args = parser.parse_args()
    
    options = BuildOptions()
    
    if args.list:
        options.list_presets()
        return
    
    if args.load_config:
        config = options.load_config(args.load_config)
        if config:
            print(f"Preset: {config['preset']}")
            print(f"Platform: {config['platform']}")
            print(f"Command: {' '.join(config['pyinstaller_command'])}")
        return
    
    if args.save_config:
        options.save_config(args.preset)
        return
    
    if args.command:
        cmd = options.generate_pyinstaller_command(args.preset, args.custom)
        print("📦 PyInstaller Command:")
        print(" ".join(cmd))
        return
    
    if args.generate:
        script_file = options.create_build_script(args.preset)
        print(f"\n💡 To build with this preset:")
        print(f"   python {script_file}")
        return
    
    # Default: show command for preset
    cmd = options.generate_pyinstaller_command(args.preset, args.custom)
    print(f"🎯 {args.preset.upper()} Preset Command:")
    print(" ".join(cmd))

if __name__ == "__main__":
    main()
