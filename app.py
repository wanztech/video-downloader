"""
Universal Video Downloader - Streamlit Web App
Created by wanztech
Powered by yt-dlp + ffmpeg
"""

import streamlit as st
import subprocess
import os
import tempfile
import re
import time
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Universal Video Downloader",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .category-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .anime { background-color: #8B5CF6; color: white; }
    .youtube { background-color: #FF0000; color: white; }
    .social { background-color: #1DA1F2; color: white; }
    .dailymotion { background-color: #0066DC; color: white; }
    .bilibili { background-color: #00A1D6; color: white; }
    .movie { background-color: #F59E0B; color: white; }
    .drama { background-color: #10B981; color: white; }
    .unknown { background-color: #EF4444; color: white; }
    .stProgress > div > div > div > div {
        background-color: #8B5CF6;
    }
    
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Hide Profile Preview - target by substring and attribute */
    div[class*="_profilePreview_"] { display: none !important; }
    img[data-testid="appCreatorAvatar"] { display: none !important; }
    
    /* Hide Logo/Link - target by specific SVG content and substring */
    div[class*="_link_"]:has(svg) { display: none !important; }
    div:has(> svg[viewBox="0 0 303 165"]) { display: none !important; }
    
    /* Additional Streamlit Cloud UI hiding */
    .viewerBadge_container__1QSob { display: none !important; }
    [data-testid="stHeader"] { visibility: hidden !important; }
    
    /* Custom Button Styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    /* Analysis Button (Secondary) */
    .stButton > button[kind="secondary"] {
        border: 2px solid #8B5CF6;
        color: #8B5CF6;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #8B5CF6;
        color: white;
        border-color: #8B5CF6;
        transform: scale(1.02);
    }
    
    /* Download Button (Primary) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #EF4444 0%, #F59E0B 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 14px 0 rgba(239, 68, 68, 0.39);
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #DC2626 0%, #D97706 100%);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.23);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Website detection patterns (same as batch script)
SITES = {
    'anime': [
        (r'gogoanime|anitaku|gogoanimehd', 'GogoAnime', 'https://gogoanimehd.to/'),
        (r'animepahe', 'AnimePahe', 'https://animepahe.ru/'),
        (r'9animetv|aniwave', '9Anime/AniWave', 'https://9animetv.to/'),
        (r'zoro|aniwatch|hianime', 'HiAnime', 'https://hianime.to/'),
    ],
    'youtube': [
        (r'youtube\.com|youtu\.be', 'YouTube', 'https://www.youtube.com/'),
    ],
    'dailymotion': [
        (r'dailymotion\.com|dai\.ly', 'Dailymotion', 'https://www.dailymotion.com/'),
    ],
    'bilibili': [
        (r'bilibili\.com|bilibili\.tv', 'Bilibili', 'https://www.bilibili.com/'),
    ],
    'social': [
        (r'facebook\.com|fb\.watch', 'Facebook', 'https://www.facebook.com/'),
        (r'instagram\.com', 'Instagram', 'https://www.instagram.com/'),
        (r'tiktok\.com', 'TikTok', 'https://www.tiktok.com/'),
        (r'twitter\.com|x\.com', 'Twitter/X', 'https://twitter.com/'),
    ],
    'movie': [
        (r'fmovies', 'FMovies', 'https://fmoviesz.to/'),
        (r'solarmovie', 'SolarMovie', 'https://solarmovie.pe/'),
        (r'123movies', '123Movies', 'https://123movies.ai/'),
        (r'putlocker', 'Putlocker', 'https://putlocker.pe/'),
    ],
    'drama': [
        (r'dramacool|asianc|watchasian', 'Dramacool', 'https://dramacool.pa/'),
        (r'kissasian', 'KissAsian', 'https://kissasian.lu/'),
        (r'myasiantv', 'MyAsianTV', 'https://myasiantv.ac/'),
        (r'viewasian', 'ViewAsian', 'https://viewasian.co/'),
    ]
}

# Video host patterns for smart headers
VIDEO_HOSTS = [
    'haildrop', 'vidstream', 'filemoon', 'vizcloud', 'simpleimage',
    'rainveil', 'fogtwist', 'lightning', 'sunshine', 'sunburst',
    'gogocdn', 'kwik', 'megacloud', 'vidcloud', 'fembed', 'mixdrop', 'mycloud'
]


def detect_website(url):
    """Detect website category and return info"""
    for category, sites in SITES.items():
        for pattern, name, referer in sites:
            if re.search(pattern, url, re.IGNORECASE):
                return {'category': category, 'name': name, 'referer': referer}
    return {'category': 'unknown', 'name': 'Unknown', 'referer': ''}


def get_video_host_referer(url):
    """Get appropriate referer for video hosts"""
    for host in VIDEO_HOSTS:
        if host in url.lower():
            if 'kwik' in url.lower():
                return 'https://animepahe.ru/'
            elif 'gogocdn' in url.lower():
                return 'https://gogoanimehd.to/'
            elif 'fembed' in url.lower():
                return 'https://dramacool.pa/'
            return 'https://9animetv.to/'
    return None


def get_executable_path(name):
    """Get path to executable, checking local dirs first"""
    # Check current directory
    if os.path.exists(f"{name}.exe"):
        return os.path.abspath(f"{name}.exe")
    
    # Check parent directory
    parent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"{name}.exe")
    if os.path.exists(parent_path):
        return parent_path
        
    return name

def check_dependencies():
    """Check if yt-dlp and ffmpeg are available"""
    yt_dlp_path = get_executable_path('yt-dlp')
    ffmpeg_path = get_executable_path('ffmpeg')
    
    try:
        result = subprocess.run([yt_dlp_path, '--version'], capture_output=True, text=True)
        ytdlp_version = result.stdout.strip()
    except:
        ytdlp_version = None
    
    try:
        # Check ffmpeg
        if ffmpeg_path != 'ffmpeg':
            # If we found a local ffmpeg, it's definitely available
            ffmpeg_available = True
        else:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            ffmpeg_available = True
    except:
        ffmpeg_available = False
    
    return ytdlp_version, ffmpeg_available


def get_video_info(url):
    """Get video metadata using yt-dlp"""
    yt_dlp_path = get_executable_path('yt-dlp')
    try:
        cmd = [yt_dlp_path, '--dump-json', '--no-playlist', url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return None, result.stderr
        
        import json
        info = json.loads(result.stdout)
        
        return {
            'title': info.get('title', 'Unknown'),
            'thumbnail': info.get('thumbnail', ''),
            'duration': info.get('duration_string', ''),
            'uploader': info.get('uploader', ''),
            'formats': ['1080p', '720p', '480p', 'Audio Only']
        }, None
    except Exception as e:
        return None, str(e)


def download_video(url, quality, embed_subs=False, embed_thumb=False, audio_format='mp3', custom_filename=None, progress_callback=None):
    """Download video using yt-dlp"""
    yt_dlp_path = get_executable_path('yt-dlp')
    ffmpeg_path = get_executable_path('ffmpeg')
    
    temp_dir = tempfile.mkdtemp()
    
    # Handle custom filename
    if custom_filename:
        # Sanitize filename
        custom_filename = re.sub(r'[\\/*?:"<>|]', "", custom_filename)
        output_template = f"{custom_filename}.%(ext)s"
    else:
        output_template = '%(title)s.%(ext)s'
        
    output_path = os.path.join(temp_dir, output_template)
    
    # Clean URL - remove list parameter to avoid playlist issues
    url = re.sub(r'&list=[^&]*', '', url)
    
    # Validate YouTube URL
    youtube_match = re.search(r'v=([\w-]{11})', url)
    if youtube_match:
        video_id = youtube_match.group(1)
        if len(video_id) < 11:
            return None, f"Invalid YouTube ID: '{video_id}' (length: {len(video_id)}). YouTube IDs must be 11 characters long."
    
    # Build quality format
    if '4K' in quality:
        fmt = 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'
    elif '2K' in quality:
        fmt = 'bestvideo[height<=1440]+bestaudio/best[height<=1440]'
    elif quality == '1080p':
        fmt = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif quality == '720p':
        fmt = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    elif quality == '480p':
        fmt = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
    elif quality == 'Audio Only':
        fmt = 'bestaudio/best'
    else:
        fmt = 'bestvideo+bestaudio/best'
    
    # Build command
    cmd = [
        yt_dlp_path,
        '-f', fmt,
        '-o', output_path,
        '--merge-output-format', 'mp4',
        '--no-playlist',
        '--extractor-args', 'generic:impersonate',
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    # Force mp4 extension for video downloads unless custom filename is used
    if not custom_filename and quality != 'Audio Only':
        cmd.extend(['--remux-video', 'mp4'])
    
    # Add Subtitles
    if embed_subs:
        cmd.extend(['--embed-subs', '--sub-langs', 'all', '--write-subs'])
        
    # Add Thumbnail
    if embed_thumb:
        cmd.extend(['--embed-thumbnail'])
    
    # Check for cookies file
    cookies_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cookies.txt')
    if os.path.exists(cookies_path):
        cmd.extend(['--cookies', cookies_path])
    
    # Add ffmpeg location if needed
    if ffmpeg_path != 'ffmpeg':
        cmd.extend(['--ffmpeg-location', os.path.dirname(ffmpeg_path)])
    
    # Add audio-only options
    if quality == 'Audio Only':
        cmd.extend(['-x', '--audio-format', audio_format])
    
    # Add smart headers for video hosts
    referer = get_video_host_referer(url)
    if referer:
        cmd.extend(['--referer', referer])
        cmd.extend(['--add-header', f'Origin: {referer.rstrip("/")}'])
    
    # Add ffmpeg location if needed
    cmd.append(url)
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Monitor progress
        output_log = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                output_log.append(line)
                if progress_callback:
                    # Parse progress from yt-dlp output
                    if '[download]' in line and '%' in line:
                        progress_callback(line)
        
        # Find downloaded file
        files = list(Path(temp_dir).glob('*'))
        if files:
            return str(files[0]), None
            
        full_error = "".join(output_log)
        return None, f"No file downloaded. Log: {full_error}"
        
    except Exception as e:
        return None, str(e)


# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Universal Video Downloader</h1>
        <p>Powered by yt-dlp + ffmpeg | Created by wanztech</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check dependencies
    ytdlp_version, ffmpeg_available = check_dependencies()
    
    if not ytdlp_version:
        st.error("❌ yt-dlp tidak dijumpai! Sila install dahulu.")
        st.code("pip install yt-dlp", language="bash")
        return
    
    if not ffmpeg_available:
        st.warning("⚠️ ffmpeg tidak dijumpai. Video 1080p+ mungkin tiada audio.")
    
    # URL Input
    url = st.text_input(
        "📎 Paste URL Video di sini:",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Support YouTube, streaming sites, dan banyak lagi"
    )
    
    # Auto-detect website
    if url:
        site_info = detect_website(url)
        
        category_colors = {
            'anime': 'anime',
            'youtube': 'youtube',                                           
            'dailymotion': 'dailymotion',
            'bilibili': 'bilibili',
            'social': 'social',
            'movie': 'movie', 
            'drama': 'drama',
            'unknown': 'unknown'
        }
        
        st.markdown(f"""
        <span class="category-badge {category_colors[site_info['category']]}">
            {site_info['category'].upper()}: {site_info['name']}
        </span>
        """, unsafe_allow_html=True)
    
    # Quality Selection
    col_qual1, col_qual2 = st.columns([2, 1])
    
    with col_qual1:
        quality = st.selectbox(
            "🎯 Pilih Kualiti:",
            ['4K (2160p)', '2K (1440p)', '1080p', '720p', '480p', 'Audio Only'],
            help="4K/2K = Ultra HD, 1080p = Full HD, 720p = HD"
        )
    
    with col_qual2:
        audio_fmt = 'mp3'
        if quality == 'Audio Only':
            audio_fmt = st.selectbox(
                "🎵 Format Audio:",
                ['mp3', 'm4a', 'wav', 'flac'],
                help="Pilih format audio yang dikehendaki"
            )
        else:
            st.selectbox("🎵 Format Audio:", ['-'], disabled=True)
            
    # Custom Filename
    custom_name = st.text_input(
        "📝 Nama Fail (Optional):",
        placeholder="Biarkan kosong untuk guna nama asal video...",
        help="Masukkan nama fail baru jika mahu (tak perlu letak .mp4/.mp3)"
    )
    
    # Advanced Options
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        embed_subs = st.checkbox("📝 Download Subtitle (Softsubs)", value=True, help="Download dan masukkan subtitle ke dalam video (jika ada)")
    with col_opt2:
        embed_thumb = st.checkbox("🖼️ Embed Thumbnail", value=True, help="Letak gambar cover pada video/lagu")
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        analyze_btn = st.button("🔍 Analisis Video", use_container_width=True)
    
    with col2:
        download_btn = st.button("🚀 Mula Download", use_container_width=True, type="primary")
    
    # Progress placeholder
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Analyze button action
    if analyze_btn and url:
        status_placeholder.info("🔄 Sedang mendapatkan info video...")
        
        info, error = get_video_info(url)
        
        if info:
            status_placeholder.empty()
            
            # Show video info
            if info['thumbnail']:
                st.image(info['thumbnail'], width=320)
            
            st.markdown(f"**📺 Title:** {info['title']}")
            st.markdown(f"**⏱️ Duration:** {info['duration']}")
            if info['uploader']:
                st.markdown(f"**👤 Uploader:** {info['uploader']}")
            
            st.success("✅ Video berjaya dianalisis! Klik Download untuk mula.")
        else:
            status_placeholder.error(f"❌ Gagal dapatkan info: {error}")
    
    # Download button action
    if download_btn and url:
        progress_bar = progress_placeholder.progress(0)
        status_text = status_placeholder.empty()
        
        def update_progress(line):
            # Simple progress parsing
            status_text.text(line.strip())
        
        status_text.info("🔄 Sedang download... Sila tunggu.")
        
        file_path, error = download_video(url, quality, embed_subs, embed_thumb, audio_fmt, custom_name, update_progress)
        
        if file_path:
            progress_bar.progress(100)
            status_text.success("✅ Download selesai!")
            
            # Read file and offer download
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            file_name = os.path.basename(file_path)
            
            st.download_button(
                label=f"📥 Download {file_name}",
                data=file_data,
                file_name=file_name,
                mime='video/mp4' if quality != 'Audio Only' else 'audio/mpeg',
                use_container_width=True,
                type="primary"
            )
            
            # Cleanup
            try:
                os.remove(file_path)
                os.rmdir(os.path.dirname(file_path))
            except:
                pass
        else:
            progress_bar.empty()
            status_text.error(f"❌ Download gagal: {error}")
    
    # Footer
    with st.expander("ℹ️ Lihat senarai website yang disokong"):
        st.markdown("""
        **Platform Video Utama:**
        - ✅ YouTube, Dailymotion, Bilibili, Vimeo
        
        **Media Sosial:**
        - ✅ Facebook, Instagram, TikTok, Twitter/X, Reddit, Pinterest
        
        **Anime:**
        - 🎌 GogoAnime, HiAnime
        - ⚠️ AnimePahe, 9Anime/AniWave (Mungkin tidak stabil - 403 Forbidden)
        
        **Drama & Movies:**
        - 🎬 Dramacool, KissAsian, FMovies, 123Movies
        
        *Dan beribu lagi website yang disupport oleh yt-dlp!*
        """)
        
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #4b5563; font-size: 0.9rem; padding: 25px; background: linear-gradient(145deg, #f3f4f6, #e5e7eb); border-radius: 15px; margin-top: 30px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); border: 1px solid #e5e7eb;">
        <p style="text-align: center; margin-bottom: 12px; font-weight: 500;">✨ <b>Penafian:</b> Alat ini dibangunkan untuk tujuan pembelajaran & arkib peribadi sahaja.</p>
        <p style="text-align: center; margin-bottom: 0; color: #6b7280;">Sila hormati hak cipta & sokong <i>content creator</i> dengan melanggan saluran rasmi mereka! ❤️</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
