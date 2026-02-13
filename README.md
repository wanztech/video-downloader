---
title: Universal Video Downloader
emoji: 🎬
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 5.16.0
app_file: app_gradio.py
pinned: false
---

# 🎬 Universal Video Downloader

A powerful video downloader supporting multiple platforms including YouTube, Facebook, Instagram, TikTok, and more.
Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) and FFmpeg.

## ✨ Features
- 🎥 Download videos up to 4K resolution
- 🎵 Extract audio (MP3, M4A, WAV, FLAC)
- 📝 Auto-embed subtitles (Softsubs)
- 🖼️ Embed thumbnails
- 🚀 Smart website detection
- ⚡ Fast processing with FFmpeg

## 🛠️ Supported Sites
- **Video Platforms:** YouTube, Dailymotion, Bilibili, Vimeo
- **Social Media:** Facebook, Instagram, TikTok, Twitter/X, Reddit
- **Anime:** GogoAnime, HiAnime
- **Drama/Movies:** Dramacool, KissAsian, FMovies

## 🚀 Running Locally

1. Clone the repository
```bash
git clone https://github.com/wanztech/video-downloader.git
cd video-downloader
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the App
```bash
# For Gradio (Recommended)
python app_gradio.py

# For Streamlit
streamlit run app.py
```

## ⚠️ Disclaimer
This tool is for educational and personal archiving purposes only. Please respect copyright laws and support content creators.
