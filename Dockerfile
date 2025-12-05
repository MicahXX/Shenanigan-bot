# Use a stable Python version
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot
COPY . .

# Start your bot
CMD ["python", "bot.py"]