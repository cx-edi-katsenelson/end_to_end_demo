FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY gunicorn_config.py .

EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
