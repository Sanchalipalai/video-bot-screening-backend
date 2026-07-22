# Railway Docker rebuild v2
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "uvicorn app:app --host 0.0.0.0 --port ${PORT}"