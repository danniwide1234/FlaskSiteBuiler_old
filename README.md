# FlaskSiteBuilder

## Overview

**FlaskSiteBuilder** is a scalable and maintainable web application built with Flask. This template provides a structured approach to organizing Flask applications, ensuring a clean separation of concerns and ease of development.

## Project Structure

```
FlaskSiteBuilder/
│
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── validators.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── services.py
│   │   └── views.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── core/
│   │       └── index.html
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── script.js
│   │   ├── images/
│   │   └── fonts/
│   ├── __init__.py
│   ├── extensions.py
│   ├── routes.py
│   ├── config.py
│   └── utils.py
│
├── migrations/
│   └── ...
│
├── tests/
│   ├── test_auth.py
│   ├── test_core.py
│   └── conftest.py
│
├── instance/
│   └── config.py
│
├── config.py
├── README.md
├── requirements.txt
├── run.py
├── Dockerfile
└── .env
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- Virtualenv
- Docker (optional, for containerized setup)

### Installation Steps

1. **Clone the repository:**

```sh
git clone https://github.com/danniwide1234/FlaskSiteBuilder.git
cd FlaskSiteBuilder
```

2. **Set up a virtual environment:**

```sh
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```sh
pip install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file in the root directory and add the following environment variables:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///instance/flasksitebuilder.db
```

5. **Run database migrations:**

```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

6. **Run the application:**

```sh
flask run
```

The application will be available at `http://127.0.0.1:5000`.

### Running with Docker

1. **Build the Docker image:**

```sh
docker build -t flasksitebuilder .
```

2. **Run the Docker container:**

```sh
docker run -p 5000:5000 flasksitebuilder
```

The application will be available at `http://127.0.0.1:5000`.

## Project Structure Details

- **app/auth/**: Contains the authentication module with forms, models, views, and validators.
- **app/core/**: Contains the core application logic, including models, services, and views.
- **app/templates/**: HTML templates for the application.
- **app/static/**: Static files (CSS, JavaScript, images, fonts).
- **app/extensions.py**: Initialization of Flask extensions (e.g., SQLAlchemy, Flask-Migrate, Flask-Login).
- **app/routes.py**: Blueprint registration and route definitions.
- **app/config.py**: Application configuration.
- **app/utils.py**: Utility functions used throughout the application.
- **migrations/**: Database migration scripts.
- **tests/**: Unit tests for the application.
- **instance/**: Configuration files specific to the instance (e.g., database configurations).
- **config.py**: Main configuration file.
- **run.py**: Entry point for running the application.
- **Dockerfile**: Docker configuration for containerized deployment.
- **.env**: Environment variables.

## Running Tests

To run the tests, use the following command:

```sh
pytest
```

This will discover and run all the tests in the `tests/` directory.

## Author

This project was created by Daniel Egbuluese.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to update the tests and documentation as needed.

## Licence

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

f you have any questions, feel free to contact me at danniwide.1981@gmail.com or fidelismicheal12@gmail.com.

---

This `README.md` provides detailed information about the project setup, structure, and usage, ensuring that any new contributors have a comprehensive guide to work with.
