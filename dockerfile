# Use the slim version of the official python image
FROM python:slim

# Install tzdata package and setup MST timezone
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -fs /usr/share/zoneinfo/America/Denver /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

# Set Time Zone environment variable to America/Denver
ENV TZ=America/Chicago

# Set the working directory in the Docker container
WORKDIR /app

# Copy the requirements.txt file from local machine to the Docker container
COPY requirements.txt .

# Install the Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the local project directory to the Docker container
COPY . .

# Create a non-root user 'nonroot' for running the application
RUN adduser --disabled-password --gecos "" nonroot

# Switch to the nonroot user for security
USER nonroot

# Define the default command to be executed when the container starts
CMD [ "python", "./app.py" ]