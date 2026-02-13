# 🚀 Panduan Deploy ke Koyeb (High Performance & Less Cold Start)

Koyeb adalah platform cloud yang bagus sebab dia ada **Free Tier** yang laju dan support **Docker**.

---

## Langkah 1: Push Code ke GitHub (Wajib)

Koyeb akan tarik code terus dari GitHub awak.

1.  Login ke **GitHub**.
2.  Create **New Repository** (nama: `video-downloader`).
3.  Upload fail-fail ini ke dalam repo tersebut:
    *   `app.py`
    *   `core.py` (jika ada)
    *   `requirements.txt`
    *   `Dockerfile` (Sangat penting! Ini yang bagitahu Koyeb cara run app)
    *   `.gitignore` (optional)
4.  Commit changes.

---

## Langkah 2: Setup Koyeb

1.  Pergi ke [Koyeb.com](https://www.koyeb.com/) dan **Sign Up** (Boleh guna GitHub login).
2.  Lepas login, klik **"Create App"**.
3.  Pilih **"GitHub"** sebagai deployment method.
4.  Cari dan pilih repository `video-downloader` yang awak baru buat tadi.

---

## Langkah 3: Configure Service

Koyeb akan auto-detect `Dockerfile` dalam repo awak.

1.  **Builder:** Pastikan dia pilih `Dockerfile`.
2.  **Instance Type:** Pilih **Free** (Nano) -> `512MB RAM, 0.1 vCPU`.
3.  **App Name:** Boleh letak apa-apa (contoh: `my-downloader`).
4.  **Environment Variables:** (Tak perlu set apa-apa buat masa ni).
5.  Klik **"Deploy"**.

---

## Langkah 4: Tunggu & Test

1.  Koyeb akan ambil masa sikit (2-5 minit) untuk:
    *   Download Docker image base.
    *   Install Python & dependencies.
    *   Install FFmpeg.
    *   Start server.
2.  Bila status jadi **"Healthy"** (Hijau), dia akan bagi satu URL (contoh: `https://my-downloader-org.koyeb.app`).
3.  Klik link tu dan test download video!

---

## 💡 Tips Koyeb

*   **Cold Start:** Koyeb jauh lebih laju "bangun" berbanding Streamlit Cloud.
*   **Health Check:** Saya dah setkan `HEALTHCHECK` dalam Dockerfile, jadi Koyeb tahu bila app awak "sakit" dan akan auto-restart kalau perlu.
*   **Limit:** Free tier Koyeb ada limit penggunaan sebulan, tapi selalunya cukup untuk personal use.
