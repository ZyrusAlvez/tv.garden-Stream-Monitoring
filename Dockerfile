FROM mcr.microsoft.com/playwright/python:v1.43.1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
