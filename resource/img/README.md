# Resource Images

This directory contains image assets for the Social Media Downloader application.

## Files

### Logo Files
- `main_logo.png` - Main application logo (PNG format, 200x80px recommended)
- `main_logo.eps` - Vector version of the logo (PostScript format)
- `main_logo.txt` - Text-based logo content for fallback

### Icon Files (Future)
- `app_icon.png` - Application icon
- `platform_icons/` - Platform-specific icons

### Documentation
- `logo_info.txt` - Logo design specifications and guidelines

## Usage

The application automatically detects and uses `main_logo.png` if available. If not found, it falls back to a stylized text-based logo.

### Adding Your Logo

1. Save your logo as `main_logo.png` in this directory
2. Recommended size: 200x80 pixels
3. Format: PNG with transparent background
4. The GUI will automatically detect and display it

### Design Guidelines

- Keep the design clean and professional
- Use colors that work well with the blue theme (#2c3e50)
- Ensure readability at small sizes
- Consider the application's purpose (social media downloading & transcription)

## Technical Notes

- Supports PNG, JPG, and other PIL-compatible formats
- Automatic resizing to 200x80 pixels
- Graceful fallback to text logo if image loading fails
- Cross-platform compatible display
