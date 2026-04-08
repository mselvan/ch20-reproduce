# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5005 available to the world outside this container
EXPOSE 5005

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Default command (can be overridden in docker-compose or Jenkins)
CMD ["python", "run_swift.py"]
