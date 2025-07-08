FROM mcr.microsoft.com/playwright/python:focal

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
