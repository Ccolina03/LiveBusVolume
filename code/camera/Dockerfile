FROM python:3.12-slim

# Install system dependencies including the missing GLib package
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    librdkafka-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app

CMD ["python", "video_producer.py", "--produce"]
