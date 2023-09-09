# Use the official Python image from the DockerHub
FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install packages
COPY requirements.txt /requirements.txt

# Install necessary Python libraries and clean up in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    pip install --no-cache-dir -r /requirements.txt

# Copy project files to the working directory
COPY .env .
COPY config.py .
COPY mlbot/ .

# Load the environment variables from .env file and run Python
CMD export $(grep -v '^#' .env | xargs) && python
