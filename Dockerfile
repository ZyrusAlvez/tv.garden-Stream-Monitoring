# Use official Playwright image with Python + all browser deps
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run the scraper
CMD ["python", "main.py"]
