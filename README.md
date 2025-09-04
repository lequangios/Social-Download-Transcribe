# 📥 Social-Download-Transcribe

**Công cụ đa nền tảng để download video/audio và trích xuất transcript từ YouTube, Facebook, TikTok, và X (Twitter) sử dụng AI Whisper.**

![Platform Support](https://img.shields.io/badge/Platform-YouTube%20%7C%20Facebook%20%7C%20TikTok%20%7C%20X-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![AI](https://img.shields.io/badge/AI-OpenAI%20Whisper-orange)

## ✨ Tính năng chính

🎯 **Multi-Platform Support**: Hỗ trợ YouTube, Facebook, TikTok, X/Twitter  
🧠 **AI Transcription**: Sử dụng OpenAI Whisper để transcript chính xác  
⚡ **Batch Processing**: Xử lý hàng loạt URLs từ file  
🎮 **Dual Interface**: Cả GUI và CLI interface  
📊 **Progress Tracking**: Hiển thị tiến trình download real-time  
🔧 **Flexible Output**: Multiple download modes và quality options  
📁 **Auto Organization**: Tự động tổ chức files theo loại  

## 🚀 Cài đặt nhanh

### 1. Clone repository
```bash
git clone <repository-url>
cd Social-Download-Transcribe
```

### 2. Setup environment
```bash
# Sử dụng script cài đặt tự động
chmod +x install.sh
./install.sh

# Hoặc cài đặt thủ công
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip uninstall numpy
pip install "numpy<2.0"
```

### 3. Kích hoạt environment
```bash
source venv/bin/activate
```

## 📖 Cách sử dụng

### 🎮 GUI Interface

#### GUI đa nền tảng (Khuyến nghị)
```bash
python video_downloader_gui.py
```

#### GUI riêng cho Facebook
```bash
python src/ui/facebook_downloader_gui.py
```

### ⌨️ Command Line Interface

#### Cú pháp cơ bản
```bash
python downloader_cli.py [URL] [OPTIONS]
```

#### Các tham số

| Tham số | Mô tả | Mặc định |
|---------|-------|----------|
| `url` | URL video (YouTube, Facebook, TikTok, X) | - |
| `--file` | File text chứa nhiều URLs (mỗi URL một dòng) | - |
| `--mode` | Chế độ download: `video`, `audio`, `best` | `video` |
| `--transcribe` | Bật tính năng transcription | `False` |
| `--model` | Model Whisper: `tiny`, `base`, `small`, `medium`, `large` | `base` |
| `--keep-audio` | Giữ file audio sau khi transcribe | `False` |

## 🎬 Ví dụ sử dụng

### Download đơn giản
```bash
# Download video YouTube
python downloader_cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download chỉ audio
python downloader_cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mode audio

# Download chất lượng tốt nhất
python downloader_cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --mode best
```

### Transcription với AI
```bash
# Transcribe với model cơ bản
python downloader_cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --transcribe

# Transcribe với model chính xác cao
python downloader_cli.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --transcribe --model large --keep-audio

# Transcribe audio dài (tự động chia segments)
python downloader_cli.py "https://www.youtube.com/watch?v=long_video" --transcribe --model medium
```

### Batch processing
```bash
# Tạo file URLs
echo "https://www.youtube.com/watch?v=video1" > urls.txt
echo "https://www.tiktok.com/@user/video/123" >> urls.txt
echo "https://x.com/user/status/456" >> urls.txt

# Chạy batch với transcription
python downloader_cli.py --file urls.txt --transcribe --model small
```

### Multi-platform examples
```bash
# YouTube
python downloader_cli.py "https://www.youtube.com/watch?v=xyz" --transcribe

# TikTok  
python downloader_cli.py "https://www.tiktok.com/@user/video/123" --mode video

# Facebook
python downloader_cli.py "https://www.facebook.com/watch/?v=123" --transcribe --model medium

# X/Twitter
python downloader_cli.py "https://x.com/user/status/123" --mode audio
```

## 🎛️ Whisper Models

| Model | Kích thước | Tốc độ | Độ chính xác | RAM cần |
|-------|------------|--------|--------------|---------|
| `tiny` | 39 MB | Rất nhanh | Thấp | ~1 GB |
| `base` | 74 MB | Nhanh | Trung bình | ~1 GB |
| `small` | 244 MB | Trung bình | Tốt | ~2 GB |
| `medium` | 769 MB | Chậm | Rất tốt | ~5 GB |
| `large` | 1550 MB | Rất chậm | Xuất sắc | ~10 GB |

**Khuyến nghị:**
- `tiny/base`: Video ngắn, cần tốc độ
- `small/medium`: Video dài, cần độ chính xác tốt
- `large`: Content quan trọng, cần độ chính xác cao nhất

## 📁 Cấu trúc Output

```
output/
├── video/          # Video files (.mp4, .webm)
├── audio/          # Audio files (.mp3, 192kbps) 
└── transcribe/     # Transcript files (.txt)
```

**Format tên file**: `{platform}_{timestamp}.{ext}`
- Ví dụ: `youtube_20250127-143025.mp4`

## 🏗️ Kiến trúc dự án

```
Social-Download-Transcribe/
├── src/
│   ├── modules/
│   │   ├── video_downloader.py          # Base classes
│   │   └── video_downloader_extended.py # Enhanced version
│   └── ui/
│       └── facebook_downloader_gui.py   # FB-specific GUI
├── output/                              # Downloaded files
├── downloader_cli.py                    # CLI interface
├── video_downloader_gui.py              # Main GUI
├── requirements.txt                     # Dependencies
└── install.sh                          # Setup script
```

## 🔧 Dependencies

### Core Libraries
- `yt-dlp>=2024.4.9` - Video download engine
- `openai-whisper>=20231117` - AI transcription  
- `torch>=2.0.0` - PyTorch for Whisper
- `torchaudio>=2.0.1` - Audio processing
- `ffmpeg-python>=0.2.0` - Audio manipulation
- `tqdm>=4.66.1` - Progress bars
- `numpy<2.0` - Numerical computing
- `tk` - GUI framework

### System Requirements
- **Python**: 3.11+
- **FFmpeg**: Required cho audio processing
- **RAM**: 1-10GB tùy Whisper model
- **Storage**: Tùy theo video size

## 🎯 Use Cases

🎬 **Content Creators**: Download và transcript videos cho editing  
🔬 **Researchers**: Thu thập và phân tích content social media  
♿ **Accessibility**: Tạo subtitles cho video content  
📚 **Archive**: Backup và lưu trữ content quan trọng  
🌍 **Language Learning**: Transcript để học ngôn ngữ  
📊 **Data Analysis**: Phân tích content text từ videos  

## ⚡ Workflow Process

1. **Input**: URL hoặc file chứa URLs
2. **Platform Detection**: Tự động nhận diện từ URL pattern
3. **Download**: Sử dụng yt-dlp với options tối ưu
4. **Transcription** (nếu được chọn):
   - Download audio format
   - Split thành segments bằng FFmpeg (30 phút/segment)
   - Process từng segment với Whisper
   - Combine thành transcript hoàn chỉnh
5. **Output**: Lưu vào thư mục tương ứng với timestamp

## 🔍 Troubleshooting

### Lỗi thường gặp

**1. SSL Certificate Error**
```bash
# Đã được xử lý tự động trong code
ssl._create_default_https_context = ssl._create_unverified_context
```

**2. FFmpeg not found**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian  
sudo apt update && sudo apt install ffmpeg

# Windows
# Download từ https://ffmpeg.org/download.html
```

**3. Out of Memory (Whisper)**
```bash
# Sử dụng model nhỏ hơn
python downloader_cli.py "URL" --transcribe --model tiny
```

**4. Platform không được hỗ trợ**
```
❌ Could not detect platform from URL: [URL]
```
**Giải pháp**: Kiểm tra URL format, hỗ trợ: youtube.com, youtu.be, facebook.com, tiktok.com, twitter.com, x.com

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful video downloader
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition AI
- [FFmpeg](https://ffmpeg.org/) - Multimedia framework
- [tqdm](https://github.com/tqdm/tqdm) - Progress bars

---

**Made with ❤️ for the community**

*Nếu project này hữu ích, hãy ⭐ star repository!*