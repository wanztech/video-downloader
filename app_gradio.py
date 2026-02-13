import gradio as gr
import core
import os

def analyze_video(url):
    """Wrapper for analyzing video info"""
    if not url:
        return None, "Sila masukkan URL."
    
    info, error = core.get_video_info(url)
    
    if error:
        return None, f"Error: {error}"
    
    # Format output for display
    details = f"""
    **Title:** {info['title']}
    **Duration:** {info['duration']}
    **Uploader:** {info['uploader']}
    """
    return info['thumbnail'], details

def process_download(url, quality, audio_fmt, custom_name, embed_subs, embed_thumb, progress=gr.Progress()):
    """Wrapper for downloading video"""
    if not url:
        return None, "Sila masukkan URL."
    
    progress(0, desc="Starting download...")
    
    def progress_callback(line):
        # Simple parsing for progress bar
        if '[download]' in line and '%' in line:
            try:
                percent_str = line.split('%')[0].split()[-1]
                percent = float(percent_str)
                progress(percent / 100, desc=f"Downloading: {percent}%")
            except:
                pass
    
    file_path, error = core.download_video(
        url, quality, embed_subs, embed_thumb, audio_fmt, custom_name, progress_callback
    )
    
    if error:
        return None, f"Error: {error}"
    
    return file_path, "✅ Download Selesai!"

# Custom CSS
css = """
.container { max-width: 800px; margin: auto; }
.footer { text-align: center; margin-top: 20px; color: #666; }
"""

with gr.Blocks(css=css, title="Universal Video Downloader") as app:
    gr.Markdown(
        """
        # 🎬 Universal Video Downloader
        Powered by yt-dlp + ffmpeg | Created by wanztech
        """
    )
    
    with gr.Row():
        url_input = gr.Textbox(label="URL Video", placeholder="https://www.youtube.com/watch?v=...", scale=4)
        analyze_btn = gr.Button("🔍 Analisis", scale=1)
    
    with gr.Row(visible=True) as info_row:
        thumb_output = gr.Image(label="Thumbnail", height=200, show_download_button=False)
        details_output = gr.Markdown(label="Video Details")
    
    with gr.Accordion("⚙️ Tetapan Download", open=True):
        with gr.Row():
            quality_dropdown = gr.Dropdown(
                choices=['4K (2160p)', '2K (1440p)', '1080p', '720p', '480p', 'Audio Only'],
                value='1080p',
                label="Kualiti"
            )
            audio_fmt_dropdown = gr.Dropdown(
                choices=['mp3', 'm4a', 'wav', 'flac'],
                value='mp3',
                label="Format Audio (Jika Audio Only)",
                interactive=True
            )
        
        custom_name_input = gr.Textbox(label="Nama Fail (Optional)", placeholder="Biarkan kosong untuk default...")
        
        with gr.Row():
            subs_check = gr.Checkbox(label="Download Subtitle", value=True)
            thumb_check = gr.Checkbox(label="Embed Thumbnail", value=True)

    download_btn = gr.Button("🚀 Mula Download", variant="primary", size="lg")
    
    status_output = gr.Textbox(label="Status", interactive=False)
    file_output = gr.File(label="File Downloaded")
    
    # Event Handlers
    def update_audio_state(quality):
        if quality == 'Audio Only':
            return gr.update(interactive=True)
        return gr.update(interactive=False)

    quality_dropdown.change(update_audio_state, inputs=[quality_dropdown], outputs=[audio_fmt_dropdown])
    
    analyze_btn.click(
        analyze_video,
        inputs=[url_input],
        outputs=[thumb_output, details_output]
    )
    
    download_btn.click(
        process_download,
        inputs=[url_input, quality_dropdown, audio_fmt_dropdown, custom_name_input, subs_check, thumb_check],
        outputs=[file_output, status_output]
    )
    
    gr.Markdown(
        """
        ---
        <div class="footer">
        ✨ Penafian: Alat ini untuk tujuan pembelajaran & arkib peribadi sahaja.<br>
        Sila hormati hak cipta & sokong content creator! ❤️
        </div>
        """
    )

if __name__ == "__main__":
    app.queue().launch()
