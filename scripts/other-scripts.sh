#!/bin/bash

# Function to print an error message and exit
function error_exit {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1" 1>&2
    exit 1
}

# Function to print an informational message
function info {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1"
}

# Activate the virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    info "Activated virtual environment."
else
    error_exit "Virtual environment not found. Please create one using 'python -m venv venv'."
fi

# Load environment variables from .flaskenv
if [ -f ".flaskenv" ]; then
    export $(grep -v '^#' .flaskenv | xargs)
    info "Loaded environment variables from .flaskenv."
else
    error_exit ".flaskenv file not found. Please ensure it exists in the project root."
fi

# Function to perform database backup
function backup_database {
    if [ -z "$SQLALCHEMY_DATABASE_URI" ]; then
        error_exit "SQLALCHEMY_DATABASE_URI is not set in the environment variables."
    fi

    BACKUP_DIR="backups"
    BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
    mkdir -p $BACKUP_DIR
    sqlite3 ${SQLALCHEMY_DATABASE_URI#sqlite:///} .dump > $BACKUP_FILE
    if [ $? -eq 0 ]; then
        info "Database backup created successfully: $BACKUP_FILE"
    else
        error_exit "Failed to create database backup."
    fi
}

# Function to run tests
function run_tests {
    if pytest; then
        info "All tests passed successfully."
    else
        error_exit "Some tests failed. Please check the test output for details."
    fi
}

# Function to clean up the project environment
function clean_environment {
    find . -type d -name '__pycache__' -exec rm -r {} + && info "Removed __pycache__ directories."
    find . -type f -name '*.pyc' -delete && info "Deleted .pyc files."
    info "Project environment cleaned successfully."
}

# Function to show usage
function show_usage {
    echo "Usage: $0 {backup|test|clean|help}"
    echo "  backup:    Create a backup of the database"
    echo "  test:      Run the test suite"
    echo "  clean:     Clean up the project environment"
    echo "  help:      Display this help message"
}

# Main script execution
case "$1" in
    backup)
        backup_database
        ;;
    test)
        run_tests
        ;;
    clean)
        clean_environment
        ;;
    help|*)
        show_usage
        ;;
esac

# Deactivate the virtual environment
deactivate
info "Virtual environment deactivated."

