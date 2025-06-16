# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Allow Python to buffer stdout/stderr (for easier logs)
ENV PYTHONUNBUFFERED=1

# Install FFmpeg
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /usr/src/app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port
EXPOSE 8000

# Default entrypoint is overridden by docker-compose command
