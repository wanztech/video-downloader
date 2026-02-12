# 🎬 Universal Video Downloader

Web app video downloader yang menggunakan yt-dlp + ffmpeg. Boleh download dari YouTube, streaming sites, dan banyak lagi.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🚀 Deploy ke Streamlit Cloud (FREE)

### Langkah 1: Create GitHub Account
1. Pergi ke https://github.com
2. Klik "Sign up" (free)
3. Verify email

### Langkah 2: Create New Repository
1. Klik "+" → "New repository"
2. Nama: `video-downloader`
3. Pilih "Public"
4. Klik "Create repository"

### Langkah 3: Upload Files
Upload 3 fail ini ke repository:
- `app.py`
- `requirements.txt`
- `README.md`

**Cara upload:**
1. Klik "Add file" → "Upload files"
2. Drag & drop 3 fail tu
3. Klik "Commit changes"

### Langkah 4: Deploy ke Streamlit Cloud
1. Pergi ke https://share.streamlit.io
2. Klik "Sign in with GitHub"
3. Authorize Streamlit
4. Klik "New app"
5. Isi:
   - Repository: `video-downloader`
   - Branch: `main`
   - Main file path: `app.py`
6. Klik "Deploy!"

### Langkah 5: Tunggu & Selesai!
- Tunggu 2-3 minit untuk build
- Website anda akan live di: `https://your-app-name.streamlit.app`

---

## 📋 Features

- ✅ Download dari YouTube, TikTok, Twitter, dll
- ✅ Auto-detect website (Anime/Movie/Drama)
- ✅ Pilih kualiti (1080p/720p/480p/Audio Only)
- ✅ UI cantik & responsive
- ✅ FREE hosting selamanya

---

## ⚠️ Limitasi

- Tidak boleh bypass DRM (Netflix, Disney+, dll)
- Tidak boleh solve CAPTCHA
- Website yang perlu login mungkin tak berfungsi
- Memory limit: 1GB (Streamlit Cloud free tier)

---

## 🛠️ Run Locally (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Install ffmpeg (required for 1080p+)
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# Run app
streamlit run app.py
```

---

## 📝 Credits

- Created by **wanztech**
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Hosted on [Streamlit Cloud](https://streamlit.io/cloud)

---

## 📜 License

MIT License - Use freely for educational purposes.

---

## ❓ FAQ

**Q: Kenapa download gagal?**
A: Cuba guna URL yang berbeza. Sesetengah website ada protection.

**Q: Kenapa tiada audio?**
A: Install ffmpeg di server. Untuk Streamlit Cloud, ffmpeg dah pre-installed.

**Q: Boleh download dari Netflix?**
A: Tidak. Netflix ada DRM protection.

**Q: Berapa lama proses deploy?**
A: Biasanya 2-3 minit untuk first deploy.

---

## 🆘 Support

Ada masalah? Create issue di GitHub repository anda.
