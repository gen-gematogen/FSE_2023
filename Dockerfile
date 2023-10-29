# Use the specified Ubuntu version as the base image
FROM ubuntu:23.04

copy . /app/

# Install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the Docker image
WORKDIR /app

# Copy the local project files to the Docker image
COPY . /app/

# Command to run the checker game
CMD ["python3", "main.py"]

