FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# ffmpeg: required for yt-dlp to merge video+audio
# curl: required for healthcheck
# git: required for some python package installations
# iputils-ping & dnsutils: for network troubleshooting
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    iputils-ping \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (Hugging Face requirement for security, but we give permissions)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements first to cache dependencies
COPY --chown=user requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=user . .

# Expose port 7860 (Hugging Face default port)
EXPOSE 7860

# Command to run the application on port 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
