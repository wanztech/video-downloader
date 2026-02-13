import os
import subprocess
import re
import tempfile
import json
from pathlib import Path
import sys

# Website detection patterns
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
    # Windows extension check
    is_windows = sys.platform.startswith('win')
    ext = ".exe" if is_windows else ""
    
    # Check current directory
    if os.path.exists(f"{name}{ext}"):
        return os.path.abspath(f"{name}{ext}")
    
    # Check parent directory
    parent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"{name}{ext}")
    if os.path.exists(parent_path):
        return parent_path
        
    return name


def check_dependencies():
    """Check if yt-dlp and ffmpeg are available"""
    yt_dlp_path = get_executable_path('yt-dlp')
    ffmpeg_path = get_executable_path('ffmpeg')
    
    try:
        # Use --version for yt-dlp
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
        cmd = [yt_dlp_path, '--dump-json', '--no-playlist', '--force-ipv4', '--no-check-certificates', url]
        if yt_dlp_path == 'yt-dlp':
            cmd = [sys.executable, '-m', 'yt_dlp', '--dump-json', '--no-playlist', '--force-ipv4', '--no-check-certificates', url]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return None, result.stderr
        
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
    cmd = []
    
    # Check if we should use python -m yt_dlp
    if yt_dlp_path == 'yt-dlp':
        cmd.extend([sys.executable, '-m', 'yt_dlp'])
    else:
        cmd.append(yt_dlp_path)
        
    cmd.extend([
        '-f', fmt,
        '-o', output_path,
        '--merge-output-format', 'mp4',
        '--no-playlist',
        '--force-ipv4',  # Force IPv4 to avoid IPv6 DNS issues
        '--no-check-certificates', # Avoid SSL certificate issues
        '--socket-timeout', '30',
        '--extractor-args', 'generic:impersonate',
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ])
    
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
    
    # Add URL
    cmd.append(url)
    
    print(f"Executing command: {' '.join(cmd)}")
    
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
                    progress_callback(line)
        
        # Find downloaded file
        files = list(Path(temp_dir).glob('*'))
        if files:
            return str(files[0]), None
            
        full_error = "".join(output_log)
        return None, f"No file downloaded. Log: {full_error}"
        
    except Exception as e:
        return None, str(e)
