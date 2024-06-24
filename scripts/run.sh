#!/bin/bash

# Function to print an error message and exit
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
    echo "Loaded environment variables from .env file."
else
    error_exit "Error: .env file not found."
fi

# Check if .flaskenv file exists and source it
if [ -f .flaskenv ]; then
    export $(cat .flaskenv | xargs)
    echo "Loaded environment variables from .flaskenv file."
else
    error_exit "Error: .flaskenv file not found."
fi

# Activate the virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Activated virtual environment."
else
    error_exit "Error: Virtual environment not found. Please create one using 'python -m venv venv'"
fi

# Install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Installed dependencies from requirements.txt."
else
    error_exit "Error: requirements.txt file not found."
fi

# Run database migrations
if flask db upgrade; then
    echo "Database migrations applied successfully."
else
    error_exit "Error: Failed to apply database migrations."
fi

# Run the Flask application
if flask run --host=0.0.0.0 --port=5000; then
    echo "Flask application is running on http://0.0.0.0:5000"
else
    error_exit "Error: Failed to start Flask application."
fi

