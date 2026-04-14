# FROM python:3.12-slim-bookworm
#
# WORKDIR /app
#
# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Copy the rest of the app
# COPY . .
# COPY config.yaml ./config.yaml
#
#
# # Set environment variables
# #ENV FLASK_APP=app.py
# #ENV FLASK_RUN_HOST=0.0.0.0
#
# # Expose Flask port
# EXPOSE 5000
#
# # Start the app
# CMD ["python", "webconfig.py"]


FROM python:3.12-slim-bookworm

WORKDIR /app

# --- Install curl & cloudflared ---
RUN apt-get update && apt-get install -y curl && \
    curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /usr/local/bin/cloudflared && \
    chmod +x /usr/local/bin/cloudflared && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Install Python dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy application code ---
COPY . .
COPY config.yaml ./config.yaml

# --- Expose your Python app port ---
EXPOSE 5000

# --- Copy and prepare startup script ---
COPY start.sh /start.sh
RUN chmod +x /start.sh

# --- Default command ---
CMD ["/start.sh"]
