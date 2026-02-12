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
    .movie { background-color: #F59E0B; color: white; }
    .drama { background-color: #10B981; color: white; }
    .unknown { background-color: #EF4444; color: white; }
    .stProgress > div > div > div > div {
        background-color: #8B5CF6;
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


def check_dependencies():
    """Check if yt-dlp and ffmpeg are available"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
        ytdlp_version = result.stdout.strip()
    except:
        ytdlp_version = None
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        ffmpeg_available = True
    except:
        ffmpeg_available = False
    
    return ytdlp_version, ffmpeg_available


def get_video_info(url):
    """Get video metadata using yt-dlp"""
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-playlist', url]
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


def download_video(url, quality, progress_callback=None):
    """Download video using yt-dlp"""
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, '%(title)s.%(ext)s')
    
    # Clean URL - remove list parameter to avoid playlist issues
    url = re.sub(r'&list=[^&]*', '', url)
    
    # Validate YouTube URL
    youtube_match = re.search(r'v=([\w-]{11})', url)
    if youtube_match:
        video_id = youtube_match.group(1)
        if len(video_id) < 11:
            return None, f"Invalid YouTube ID: '{video_id}' (length: {len(video_id)}). YouTube IDs must be 11 characters long."
    
    # Build quality format
    if quality == '1080p':
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
        'yt-dlp',
        '-f', fmt,
        '-o', output_path,
        '--merge-output-format', 'mp4',
        '--no-playlist',
        '--extractor-args', 'generic:impersonate'
    ]
    
    # Add audio-only options
    if quality == 'Audio Only':
        cmd.extend(['-x', '--audio-format', 'mp3'])
    
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
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor progress
        while True:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break
            if line and progress_callback:
                # Parse progress from yt-dlp output
                if '[download]' in line and '%' in line:
                    progress_callback(line)
        
        # Find downloaded file
        files = list(Path(temp_dir).glob('*'))
        if files:
            return str(files[0]), None
        return None, "No file downloaded"
        
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
        placeholder="https://youtube.com/watch?v=... atau https://9animetv.to/...",
        help="Support YouTube, streaming sites, dan banyak lagi"
    )
    
    # Auto-detect website
    if url:
        site_info = detect_website(url)
        
        category_colors = {
            'anime': 'anime',
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
    quality = st.selectbox(
        "🎯 Pilih Kualiti:",
        ['1080p', '720p', '480p', 'Audio Only'],
        help="1080p = Full HD, 720p = HD, 480p = SD (paling laju)"
    )
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        analyze_btn = st.button("🔍 Analisis Video", use_container_width=True)
    
    with col2:
        download_btn = st.button("⬇️ Download", use_container_width=True, type="primary")
    
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
        
        file_path, error = download_video(url, quality, update_progress)
        
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
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.85rem;">
        <p>⚠️ Website ini untuk tujuan pendidikan sahaja.</p>
        <p>Support content creators dengan subscribe channel mereka!</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
