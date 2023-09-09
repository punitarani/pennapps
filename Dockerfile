# Use the official Python image from the DockerHub
FROM python:3.10-slim

# Ensure up-to-date system packages
RUN apt-get update && apt-get upgrade -y

# Install necessary Python libraries
RUN pip install pandas pyarrow

# Create a directory for our code
WORKDIR /app

# By default, run a Python shell (this can be changed based on your needs)
CMD ["python"]
