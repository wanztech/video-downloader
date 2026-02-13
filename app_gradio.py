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
    ### 📹 Maklumat Video
    **Tajuk:** {info['title']}  
    **Tempoh:** {info['duration']}  
    **Saluran:** {info['uploader']}
    """
    return info['thumbnail'], details

def process_download(url, quality, audio_fmt, custom_name, embed_subs, embed_thumb, progress=gr.Progress()):
    """Wrapper for downloading video"""
    if not url:
        return None, "⚠️ Sila masukkan URL."
    
    progress(0, desc="Starting download...")
    
    try:
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
            return None, f"❌ Ralat: {error}"
        
        if not file_path or not os.path.exists(file_path):
            return None, "❌ Ralat: Fail tidak dijumpai selepas muat turun."
            
        return file_path, "✅ Download Selesai!"
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None, f"❌ Ralat Kritikal: {str(e)}"

# Custom CSS
css = """
.container { max-width: 900px; margin: auto; padding-top: 20px; }
.header { text-align: center; margin-bottom: 30px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
.header h1 { font-size: 2.5em; font-weight: bold; color: #6b46c1; margin-bottom: 10px; }
.header p { font-size: 1.1em; color: #666; }
.footer { text-align: center; margin-top: 40px; color: #888; font-size: 0.9em; border-top: 1px solid #eee; padding-top: 20px; }
.gr-button-primary { background: linear-gradient(90deg, #6b46c1 0%, #805ad5 100%); border: none; color: white; }
.gr-box { border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
"""

# Modern Theme
theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="indigo",
    neutral_hue="slate",
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_600",
    block_shadow="*shadow_drop_lg",
    block_title_text_weight="600"
)

with gr.Blocks(theme=theme, css=css, title="Universal Video Downloader Pro") as app:
    
    with gr.Column(elem_classes="container"):
        
        # Header
        gr.Markdown(
            """
            <div class="header">
                <h1>🎬 Universal Video Downloader Pro</h1>
                <p>Muat turun video berkualiti tinggi dengan mudah & pantas!</p>
            </div>
            """
        )
        
        # Input Section
        with gr.Group():
            with gr.Row(variant="panel"):
                url_input = gr.Textbox(
                    label="Pautan Video", 
                    placeholder="Tampal URL di sini (YouTube, Facebook, TikTok, dll...)", 
                    scale=4,
                    show_label=False,
                    container=False,
                    autofocus=True
                )
                analyze_btn = gr.Button("🔍 Analisis", variant="primary", scale=1, min_width=120)

        # Output Preview Section
        with gr.Row(visible=True, variant="panel", equal_height=True):
            with gr.Column(scale=1):
                thumb_output = gr.Image(label="Thumbnail", show_download_button=False, interactive=False, height=200)
            with gr.Column(scale=2):
                details_output = gr.Markdown("### ℹ️ Sila masukkan URL dan tekan Analisis")

        # Settings Section
        with gr.Accordion("⚙️ Tetapan Lanjutan", open=False):
            with gr.Row():
                quality_dropdown = gr.Dropdown(
                    choices=['4K (2160p)', '2K (1440p)', '1080p', '720p', '480p', 'Audio Only'],
                    value='1080p',
                    label="Kualiti Video"
                )
                audio_fmt_dropdown = gr.Dropdown(
                    choices=['mp3', 'm4a', 'wav', 'flac'],
                    value='mp3',
                    label="Format Audio (Jika Audio Only)",
                    interactive=False
                )
            
            custom_name_input = gr.Textbox(label="Nama Fail (Optional)", placeholder="Contoh: video_latihan_01")
            
            with gr.Row():
                subs_check = gr.Checkbox(label="Sertakan Subtitle", value=True)
                thumb_check = gr.Checkbox(label="Embed Thumbnail", value=True)

        # Action Section
        with gr.Group():
            download_btn = gr.Button("🚀 Mula Muat Turun", variant="primary", size="lg")
            
        with gr.Row():
            status_output = gr.Textbox(label="Status Proses", interactive=False, show_label=True, scale=2)
            file_output = gr.File(label="Fail Siap", scale=1)

        # Footer
        gr.Markdown(
            """
            <div class="footer">
            Dikuasakan oleh <b>yt-dlp</b> & <b>FFmpeg</b> | Dibangunkan oleh <b>wanztech</b><br>
            ⚠️ Untuk tujuan pendidikan sahaja. Sila hormati hak cipta.
            </div>
            """
        )

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

if __name__ == "__main__":
    app.queue().launch()
