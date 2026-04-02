FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8090

# Production server (instead of python app.py)
CMD ["gunicorn", "-b", "0.0.0.0:8090", "app:app"]