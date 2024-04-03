FROM python:3.8-slim

WORKDIR /app

COPY flask-app/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]