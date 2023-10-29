# Use the specified Ubuntu version as the base image
FROM ubuntu:23.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3.11-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the Docker image
WORKDIR /app

# Copy the local project files to the Docker image
COPY . /app/

# Create a virtual environment
RUN python3 -m venv venv

# Grant execute permissions to test.sh
RUN chmod +x /app/test.sh

# Activate the virtual environment and install packages
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Command to run the checker game
# CMD ["./venv/bin/python3", "main.py - "]
