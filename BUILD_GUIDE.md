# Build Guide - Social Downloader

## 🎯 Overview

This guide explains how to build portable executables for Social Downloader using the automated build system.

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Activate virtual environment
source venv/bin/activate

# Install PyInstaller
pip install pyinstaller
```

### 2. Build Portable
```bash
# Run build script
python build_portable.py
```

### 3. Result
- **Executable**: `dist/SocialDownloader`
- **Package**: `SocialDownloader_Portable/`
- **Size**: ~240MB (self-contained)

## 📋 Build Script Features

### `build_portable.py`

#### **🔍 Requirements Check**
- Python version verification
- Required files validation
- PyInstaller installation check
- Dependencies verification

#### **🧹 Clean Build**
- Removes previous build artifacts
- Cleans cache files
- Removes old .spec files

#### **📦 PyInstaller Build**
- Single executable file (`--onefile`)
- No console window (`--windowed`)
- Includes all resources
- Hidden imports for dependencies

#### **📁 Package Creation**
- Creates portable folder structure
- Copies executable and resources
- Creates output directories
- Generates user documentation

## 🛠️ Build Process

### Step 1: Requirements Check
```python
def check_requirements():
    # Check Python version (3.8+)
    # Verify required files exist
    # Check PyInstaller installation
    # Validate dependencies
```

### Step 2: Clean Previous Builds
```python
def clean_build():
    # Remove build/ directory
    # Remove dist/ directory
    # Remove __pycache__/
    # Remove *.spec files
```

### Step 3: PyInstaller Build
```bash
pyinstaller --onefile --windowed \
  --name=SocialDownloader \
  --add-data=resource:resource \
  --add-data=src:src \
  --hidden-import=PIL \
  --hidden-import=yt_dlp \
  --hidden-import=whisper \
  --hidden-import=torch \
  --hidden-import=torchaudio \
  --hidden-import=ffmpeg \
  --hidden-import=tqdm \
  --hidden-import=numpy \
  --clean \
  video_downloader_gui.py
```

### Step 4: Package Creation
```python
def create_portable_package():
    # Create SocialDownloader_Portable/
    # Copy executable
    # Copy resources
    # Create output folders
    # Generate README.txt
    # Create run.sh script
```

## 📁 Output Structure

```
SocialDownloader_Portable/
├── SocialDownloader          # Main executable (240MB)
├── resource/                 # App resources
│   └── img/
│       └── main_logo.png     # Logo file
├── output/                   # Download folders
│   ├── video/
│   ├── audio/
│   └── transcribe/
├── README.txt               # User instructions
└── run.sh                   # Launcher script
```

## ⚙️ Configuration

### PyInstaller Options

#### **Basic Options**
- `--onefile`: Single executable file
- `--windowed`: No console window (GUI)
- `--name`: Executable name
- `--clean`: Clean build cache

#### **Data Files**
- `--add-data=resource:resource`: Include resources
- `--add-data=src:src`: Include source modules

#### **Hidden Imports**
- `--hidden-import=PIL`: Pillow for image processing
- `--hidden-import=yt_dlp`: Video downloader
- `--hidden-import=whisper`: AI transcription
- `--hidden-import=torch`: PyTorch for AI
- `--hidden-import=torchaudio`: Audio processing
- `--hidden-import=ffmpeg`: FFmpeg wrapper
- `--hidden-import=tqdm`: Progress bars
- `--hidden-import=numpy`: Numerical computing

#### **Icon (Optional)**
- `--icon=resource/img/main_logo.png`: App icon

## 🎯 Build Types

### Standard Build (Default)
```bash
python build_portable.py
```
- **Size**: ~240MB
- **Features**: Full functionality
- **Use case**: Complete standalone app

### Custom Builds
You can modify the script for different build types:

#### Lightweight Build
```python
# Remove large dependencies
"--exclude-module=torch",
"--exclude-module=torchaudio",
```

#### Console Build
```python
# Remove --windowed for debug output
# Keep console window visible
```

#### Directory Build
```python
# Change --onefile to --onedir
# Faster startup, multiple files
```

## 🔧 Troubleshooting

### Common Issues

#### **Import Errors**
```bash
# Add missing modules to --hidden-import
--hidden-import=missing_module
```

#### **Missing Files**
```bash
# Add data files with --add-data
--add-data=source:destination
```

#### **Large File Size**
```bash
# Exclude unused modules
--exclude-module=unused_module
```

#### **Build Failures**
```bash
# Check requirements
python -c "from build_portable import check_requirements; check_requirements()"

# Clean and retry
rm -rf build/ dist/ *.spec
python build_portable.py
```

### Debug Mode
```python
# Modify build_portable.py
# Remove --windowed to see console output
# Add --debug=all for verbose output
```

## 📊 Build Statistics

### File Sizes
- **Executable**: ~240MB
- **Package**: ~240MB
- **Resources**: ~1MB
- **Dependencies**: ~239MB

### Build Time
- **Clean build**: ~5-10 minutes
- **Incremental**: ~2-3 minutes
- **Dependencies**: Most time spent on PyTorch

### Memory Usage
- **Build process**: ~2-4GB RAM
- **Runtime**: ~500MB-1GB RAM
- **Model loading**: Additional 1-2GB

## 🚀 Distribution

### For End Users
1. **Download**: Get `SocialDownloader_Portable` folder
2. **Extract**: Unzip if compressed
3. **Run**: Double-click `SocialDownloader`
4. **Use**: No installation required

### For Developers
1. **Build**: Run build script
2. **Test**: Verify functionality
3. **Package**: Compress folder
4. **Distribute**: Share portable package

## 💡 Best Practices

### Build Optimization
1. **Use virtual environment** for clean builds
2. **Test thoroughly** before distribution
3. **Include all resources** in package
4. **Provide clear instructions** for users
5. **Monitor file sizes** for distribution

### User Experience
1. **Single executable** for simplicity
2. **Clear folder structure** for organization
3. **README file** with instructions
4. **Launcher script** for convenience
5. **Output folder** pre-created

### Maintenance
1. **Version control** build scripts
2. **Document changes** in build process
3. **Test on multiple systems** if possible
4. **Update dependencies** regularly
5. **Monitor for security updates**

## 🎉 Success Metrics

### Build Success Indicators
- ✅ Executable created in `dist/` folder
- ✅ Package created in `SocialDownloader_Portable/`
- ✅ All resources included
- ✅ Executable runs without errors
- ✅ GUI opens successfully

### Distribution Ready
- ✅ Single folder contains everything
- ✅ No external dependencies
- ✅ Clear user instructions
- ✅ Proper file permissions
- ✅ Tested on target system

---

**🎯 The build system makes it easy to create professional, portable executables for Social Downloader!**
