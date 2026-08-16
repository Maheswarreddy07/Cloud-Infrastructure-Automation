# Use an explicit, stable Python 3.11 image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency configuration files first
COPY requirements.txt .

# Install dependencies smoothly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose port 5000 for web traffic
EXPOSE 5000

# Run your application with Gunicorn binding to Render's dynamic port environment variable
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
