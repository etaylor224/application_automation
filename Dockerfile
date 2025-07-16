FROM python:3.12-slim-bookworm

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .
COPY config.yaml ./config.yaml


# Set environment variables
#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0

# Expose Flask port
EXPOSE 5000

# Start the app
CMD ["python", "webconfig.py"]
