FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Render uses this port
EXPOSE $PORT

# Run with Gunicorn (much more stable on Render)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
