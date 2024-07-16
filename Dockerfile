# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Copy the rest of the application code into the container
COPY . /app/

# Copy the requirements file into the container
COPY requirements.txt /app/

COPY aps_failure_training_set1.csv /app
# Set the working directory in the container
WORKDIR /app


# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Expose the port that the app runs on
EXPOSE 8080

# Specify the command to run the application
CMD ["python", "sensor/main.py"]
