# 🚀 Panduan Deploy ke Streamlit Cloud (Step-by-Step)

## Prerequisite
Anda perlukan **GitHub account**. Jika belum ada:
1. Pergi ke https://github.com
2. Klik "Sign up"
3. Isi email, password, username
4. Verify email

---

## Langkah 1: Create GitHub Repository

### 1.1 Login ke GitHub
Pergi ke https://github.com dan login

### 1.2 Create New Repository
1. Klik button **"+"** (atas kanan) → **"New repository"**

![New Repo](https://docs.github.com/assets/cb-33027/mw-1440/images/help/repository/repo-create.webp)

### 1.3 Isi Maklumat
- **Repository name:** `video-downloader`
- **Description:** (optional) `Universal Video Downloader`
- **Visibility:** Pilih **Public** (wajib untuk free Streamlit)
- **Jangan** tick "Add a README file"

### 1.4 Klik "Create repository"

---

## Langkah 2: Upload Fail

### 2.1 Di page repository baru anda, klik **"uploading an existing file"**

### 2.2 Upload 3 fail ini
Drag & drop fail-fail ini dari folder `streamlit-downloader/`:
- `app.py`
- `requirements.txt`
- `README.md`

### 2.3 Commit
- Scroll bawah
- Klik **"Commit changes"**

---

## Langkah 3: Deploy ke Streamlit Cloud

### 3.1 Pergi ke Streamlit Cloud
Buka https://share.streamlit.io

### 3.2 Sign in dengan GitHub
1. Klik **"Sign in with GitHub"**
2. Authorize Streamlit

### 3.3 Create New App
1. Klik **"New app"** (button hijau)
2. Isi:
   - **Repository:** Pilih `video-downloader`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (optional):** Biarkan kosong (auto-generate)

### 3.4 Deploy!
Klik **"Deploy!"** button di bawah

---

## Langkah 4: Tunggu Build

- Tunggu **2-5 minit** untuk proses build
- Anda akan nampak log scrolling
- Bila selesai, website akan auto-load

---

## Langkah 5: Website Live! 🎉

Website anda sekarang live di:
```
https://video-downloader-<username>.streamlit.app
```

Contoh: `https://video-downloader-wanztech.streamlit.app`

---

## ❓ Troubleshooting

### Error: "Module not found"
Pastikan `requirements.txt` ada dan betul:
```
streamlit>=1.28.0
yt-dlp>=2023.11.16
```

### Error: "ffmpeg not found"
Streamlit Cloud dah ada ffmpeg pre-installed. Jika masih error, tambah dalam `packages.txt`:
```
ffmpeg
```

### Website sleep/first load slow
Ini normal untuk free tier. Website akan "sleep" jika tak ada visitor 7 hari. First load ambil 30-60 saat untuk "wake up".

---

## 📱 Share Website Anda

Setelah live, share link dengan kawan-kawan:
```
https://video-downloader-<username>.streamlit.app
```

---

## 🔄 Update Code

Kalau nak update code:
1. Edit fail di GitHub (atau upload baru)
2. Streamlit Cloud akan auto-redeploy!

---

## 🆘 Perlu Bantuan?

Jika ada error, check:
1. Streamlit Cloud logs (klik app name → "Logs")
2. Pastikan semua 3 fail di-upload
3. Pastikan repository adalah **Public**

Good luck! 🍀
