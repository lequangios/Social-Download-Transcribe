# Portable Build Guide

## 🎯 Overview

Social Downloader can be packaged into portable executables for easy distribution and deployment without requiring Python installation.

## 📦 Build Types

### 1. Standard Portable (Recommended)
- **Size**: ~240MB
- **Features**: Full functionality with all models
- **Use case**: Complete standalone application
- **Command**: `python build_portable.py`

### 2. Lightweight Version
- **Size**: ~50MB
- **Features**: Basic functionality, smaller models only
- **Use case**: Quick deployment, limited resources
- **Command**: `python build_options.py --type lightweight`

### 3. Console Version
- **Size**: ~240MB
- **Features**: Full functionality with debug output
- **Use case**: Development, troubleshooting
- **Command**: `python build_options.py --type console`

### 4. Directory Version
- **Size**: ~300MB (folder)
- **Features**: Faster startup, multiple files
- **Use case**: Local deployment, frequent updates
- **Command**: `python build_options.py --type directory`

## 🚀 Quick Build

### Standard Build
```bash
# Activate virtual environment
source venv/bin/activate

# Install PyInstaller
pip install pyinstaller

# Build portable
python build_portable.py
```

### Advanced Build Options
```bash
# Build all versions
python build_options.py --type all

# Build specific version
python build_options.py --type lightweight
python build_options.py --type console
python build_options.py --type directory
```

## 📁 Output Structure

```
SocialDownloader_Portable/
├── SocialDownloader          # Main executable
├── resource/                 # App resources
│   └── img/
│       └── main_logo.png     # Logo file
├── output/                   # Download folder
│   ├── video/
│   ├── audio/
│   └── transcribe/
├── README.txt               # User instructions
└── run.sh                   # Launcher script
```

## 🎯 Distribution

### For End Users
1. **Download**: Get the `SocialDownloader_Portable` folder
2. **Extract**: Unzip if compressed
3. **Run**: Double-click `SocialDownloader`
4. **Use**: No installation required!

### For Developers
1. **Build**: Use build scripts
2. **Test**: Verify functionality
3. **Package**: Compress folder
4. **Distribute**: Share portable package

## ⚙️ Requirements

### Build Requirements
- Python 3.11+
- Virtual environment with all dependencies
- PyInstaller
- macOS (for macOS builds)

### Runtime Requirements
- macOS 10.13+ (for macOS builds)
- Internet connection
- FFmpeg (system-wide installation)
- Sufficient disk space for models

## 🔧 Build Process

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Build Execution
```bash
# Standard build
python build_portable.py

# Advanced builds
python build_options.py --type all
```

### 3. Testing
```bash
# Test executable
./SocialDownloader_Portable/SocialDownloader

# Test with timeout
timeout 5 ./SocialDownloader_Portable/SocialDownloader
```

## 📊 Build Comparison

| Version | Size | Startup | Features | Use Case |
|---------|------|---------|----------|----------|
| **Standard** | 240MB | Medium | Full | General use |
| **Lightweight** | 50MB | Fast | Basic | Limited resources |
| **Console** | 240MB | Medium | Full + Debug | Development |
| **Directory** | 300MB | Fast | Full | Local deployment |

## 🎨 Customization

### Adding Icon
```bash
# Place icon file
cp your_icon.png resource/img/main_logo.png

# Rebuild
python build_portable.py
```

### Excluding Modules
```python
# In build script, add:
"--exclude-module=module_name"
```

### Adding Data Files
```python
# In build script, add:
"--add-data=source:destination"
```

## 🚨 Troubleshooting

### Build Issues
- **Import errors**: Check `--hidden-import` flags
- **Missing files**: Verify `--add-data` paths
- **Size too large**: Use `--exclude-module` for unused modules
- **Icon not found**: Remove `--icon` flag or add icon file

### Runtime Issues
- **App won't start**: Check system requirements
- **Missing FFmpeg**: Install system-wide FFmpeg
- **Permission denied**: Run `chmod +x SocialDownloader`
- **Slow startup**: First run downloads models

### Performance Optimization
- **Reduce size**: Use lightweight build
- **Faster startup**: Use directory build
- **Debug issues**: Use console build
- **Memory usage**: Monitor with Activity Monitor

## 📈 Advanced Features

### Code Signing (macOS)
```bash
# Sign executable
codesign --force --deep --sign "Developer ID" SocialDownloader

# Verify signature
codesign --verify --verbose SocialDownloader
```

### Notarization (macOS)
```bash
# Create archive
ditto -c -k --keepParent SocialDownloader_Portable SocialDownloader.zip

# Submit for notarization
xcrun altool --notarize-app --primary-bundle-id "com.yourcompany.socialdownloader" --username "your@email.com" --password "@keychain:AC_PASSWORD" --file SocialDownloader.zip
```

### Cross-Platform Builds
- **Windows**: Use Windows machine with PyInstaller
- **Linux**: Use Linux machine with PyInstaller
- **macOS**: Use macOS machine (current setup)

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

---

**🎯 Portable builds make Social Downloader easy to distribute and use without technical setup!**
