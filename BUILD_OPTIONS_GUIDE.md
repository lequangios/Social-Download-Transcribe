# Build Options Guide - Social Downloader

## 🎯 Overview

`build_options.py` provides flexible build configurations and presets for creating different types of Social Downloader executables.

## 🚀 Quick Start

### List Available Presets
```bash
python build_options.py --list
```

### Generate Build Command
```bash
# Standard build
python build_options.py --preset standard --command

# Lightweight build
python build_options.py --preset lightweight --command

# Console build
python build_options.py --preset console --command
```

### Create Custom Build Script
```bash
python build_options.py --preset lightweight --generate
python build_custom.py
```

## 📦 Available Presets

### 1. **Standard** (Default)
- **Size**: ~240MB
- **Features**: Full GUI, all platforms, AI transcription
- **Use Case**: Complete standalone application
- **Options**: `--onefile --windowed --clean`

### 2. **Lightweight**
- **Size**: ~50MB
- **Features**: GUI, basic download, no AI transcription
- **Use Case**: Quick download without AI features
- **Excludes**: `torch`, `torchaudio`, `whisper`

### 3. **Console**
- **Size**: ~240MB
- **Features**: Console output, full features, debugging
- **Use Case**: Development and debugging
- **Options**: `--onefile --clean` (no `--windowed`)

### 4. **Directory**
- **Size**: ~240MB (multiple files)
- **Features**: Faster startup, multiple files
- **Use Case**: Frequent usage, faster startup
- **Options**: `--onedir --windowed --clean`

### 5. **Development**
- **Size**: ~300MB
- **Features**: Debug info, development tools
- **Use Case**: Development and testing
- **Options**: `--onedir --clean --debug=all`

## 🛠️ Command Line Options

### Basic Usage
```bash
python build_options.py [OPTIONS]
```

### Available Options

#### `--list`
List all available build presets with descriptions.

#### `--preset PRESET`
Specify which preset to use (default: standard).

#### `--command`
Show the PyInstaller command for the specified preset.

#### `--generate`
Generate a custom build script for the specified preset.

#### `--save-config`
Save the current configuration to a JSON file.

#### `--load-config FILE`
Load configuration from a JSON file.

#### `--custom OPTIONS`
Add custom PyInstaller options to the command.

## 📋 Usage Examples

### 1. List All Presets
```bash
python build_options.py --list
```

### 2. Show Standard Build Command
```bash
python build_options.py --preset standard --command
```

### 3. Create Lightweight Build Script
```bash
python build_options.py --preset lightweight --generate
python build_custom.py
```

### 4. Save Configuration
```bash
python build_options.py --preset console --save-config
```

### 5. Load Configuration
```bash
python build_options.py --load-config build_config.json
```

### 6. Custom Options
```bash
python build_options.py --preset standard --custom --debug=all --strip
```

## 🔧 Configuration Files

### JSON Configuration Format
```json
{
  "preset": "standard",
  "timestamp": "2025-09-04T20:57:08.830273",
  "platform": "macos",
  "pyinstaller_command": [...],
  "preset_config": {
    "description": "Standard build with all features",
    "options": ["--onefile", "--windowed", "--clean"],
    "size_estimate": "~240MB",
    "features": "Full GUI, all platforms, AI transcription"
  }
}
```

### Custom Build Script Format
```python
#!/usr/bin/env python3
"""
Custom build script for [PRESET] preset
Generated on [TIMESTAMP]
"""

import subprocess
import sys
from build_options import BuildOptions

def main():
    # Build logic here
    pass

if __name__ == "__main__":
    main()
```

## 🎯 Platform-Specific Options

### macOS
- **Icon**: `.icns` format
- **Bundle ID**: `com.socialdownloader.app`
- **Additional**: Bundle identifier

### Windows
- **Icon**: `.ico` format
- **UAC**: Admin privileges
- **Additional**: UAC elevation

### Linux
- **Icon**: `.png` format
- **Additional**: Standard options

## 📊 Build Comparison

| Preset | Size | Startup | Features | Use Case |
|--------|------|---------|----------|----------|
| Standard | ~240MB | Medium | Full | Production |
| Lightweight | ~50MB | Fast | Basic | Quick downloads |
| Console | ~240MB | Medium | Full + Debug | Development |
| Directory | ~240MB | Fast | Full | Frequent use |
| Development | ~300MB | Slow | Full + Debug | Testing |

## 🔍 Advanced Usage

### Custom Preset Creation
```python
from build_options import BuildOptions

options = BuildOptions()

# Add custom preset
options.build_presets["custom"] = {
    "description": "Custom build configuration",
    "options": ["--onefile", "--windowed"],
    "exclude_modules": ["whisper"],
    "size_estimate": "~200MB",
    "features": "Custom configuration"
}

# Generate command
cmd = options.generate_pyinstaller_command("custom")
```

### Integration with build_portable.py
```python
from build_options import BuildOptions
from build_portable import build_portable

# Use lightweight preset
options = BuildOptions()
cmd = options.generate_pyinstaller_command("lightweight")

# Modify build_portable.py to use custom command
# Replace the hardcoded cmd with the generated one
```

## 🚀 Workflow Examples

### Development Workflow
```bash
# 1. Test with console build
python build_options.py --preset console --generate
python build_custom.py

# 2. Create lightweight for testing
python build_options.py --preset lightweight --generate
python build_custom.py

# 3. Final production build
python build_portable.py
```

### CI/CD Integration
```bash
# Save configuration
python build_options.py --preset standard --save-config

# Load and build in CI
python build_options.py --load-config build_config.json --command
```

### Multiple Builds
```bash
# Create different builds
python build_options.py --preset lightweight --generate
mv build_custom.py build_lightweight.py

python build_options.py --preset console --generate
mv build_custom.py build_console.py

python build_options.py --preset standard --generate
mv build_custom.py build_standard.py
```

## 💡 Best Practices

### 1. **Choose the Right Preset**
- **Standard**: For end users
- **Lightweight**: For quick downloads
- **Console**: For debugging
- **Directory**: For frequent use
- **Development**: For testing

### 2. **Save Configurations**
```bash
# Save your preferred configuration
python build_options.py --preset standard --save-config
```

### 3. **Test Different Builds**
```bash
# Test lightweight first
python build_options.py --preset lightweight --generate
python build_custom.py

# Then standard
python build_portable.py
```

### 4. **Use Custom Options**
```bash
# Add debugging to standard build
python build_options.py --preset standard --custom --debug=all --command
```

## 🔧 Troubleshooting

### Common Issues

#### **Preset Not Found**
```bash
# List available presets
python build_options.py --list
```

#### **Custom Options Not Working**
```bash
# Check PyInstaller documentation
pyinstaller --help
```

#### **Configuration File Issues**
```bash
# Validate JSON
python -m json.tool build_config.json
```

### Debug Mode
```bash
# Use development preset for debugging
python build_options.py --preset development --generate
python build_custom.py
```

## 📈 Performance Tips

### 1. **Use Lightweight for Testing**
- Faster builds
- Smaller size
- Quick iteration

### 2. **Use Directory for Development**
- Faster startup
- Easier debugging
- Multiple files

### 3. **Use Standard for Production**
- Single file
- All features
- Professional distribution

---

**🎯 build_options.py makes it easy to create different types of builds for different use cases!**
