FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install youtube_transcript_api

COPY . .

CMD ["python", "app.py"]
