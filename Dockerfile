# Use a slim official Python base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY main.py .

# The tool is a CLI; arguments are passed at runtime
ENTRYPOINT ["python", "main.py"]

# Default arguments (override at runtime, e.g. --ranges "1-3,4-7")
CMD ["--help"]
