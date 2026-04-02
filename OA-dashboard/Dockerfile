FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app.py .
COPY templates/ templates/
COPY static/ static/

EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]