"""
Universal Video Downloader - Streamlit Web App
Created by wanztech
Powered by yt-dlp + ffmpeg
"""

import streamlit as st
import os
import core

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
    
    /* Hide Hugging Face Spaces Header & Footer */
    div[class*="flex items-center justify-between xl:min-w-0"] { display: none !important; }
    footer[class*="flex-none flex flex-col"] { display: none !important; }
    .footer { display: none !important; }
    
    /* AGGRESSIVE: Hide specific elements by class patterns found in source */
    div[class*="_profilePreview_"] { display: none !important; }
    div[class*="_link_"] { display: none !important; }
    img[data-testid="appCreatorAvatar"] { display: none !important; }
    
    /* Hide the specific Streamlit SVG Logo */
    svg[viewBox="0 0 303 165"] { display: none !important; }
    div:has(> svg[viewBox="0 0 303 165"]) { display: none !important; }
    
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
    ytdlp_version, ffmpeg_available = core.check_dependencies()
    
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
        site_info = core.detect_website(url)
        
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
        
        info, error = core.get_video_info(url)
        
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
        
        file_path, error = core.download_video(url, quality, embed_subs, embed_thumb, audio_fmt, custom_name, update_progress)
        
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
