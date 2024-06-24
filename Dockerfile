# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    PORT=5000

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only requirements files to prevent extra cache invalidations
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port number
EXPOSE ${PORT}

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=${PORT}"]

