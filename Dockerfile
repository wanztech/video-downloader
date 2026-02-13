FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# ffmpeg: required for yt-dlp to merge video+audio
# curl: required for healthcheck
# git: required for some python package installations
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to cache dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000 (Standard for Koyeb/Cloud services)
EXPOSE 8000

# Healthcheck to ensure app is running
HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health || exit 1

# Run Streamlit on port 8000
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
