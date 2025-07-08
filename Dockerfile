FROM mcr.microsoft.com/playwright/python:v1.48.0-focal

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
