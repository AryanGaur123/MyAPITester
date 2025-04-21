# Simple API Tester

A Django web application that allows users to interact with RESTful APIs through a clean, intuitive web interface.

## Features

- Make API requests with different HTTP methods (GET, POST, PUT, DELETE)
- Add custom headers to your requests
- Send JSON request bodies
- View formatted JSON responses
- See response status codes and headers
- Save request history to PostgreSQL database
- Cache recent responses with Redis for faster loading

## Tech Stack

- Python
- Django (web framework)
- PostgreSQL (database for request history)
- Redis (caching)
- Bootstrap 5 (frontend styling)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd SimpleAPITester
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database in `simple_api_tester/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api_tester',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Create the PostgreSQL database:
```bash
createdb api_tester
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the development server:
```bash
python manage.py runserver
```

8. Access the application at http://localhost:8000/

## Usage

1. Enter the API URL you want to test
2. Select the HTTP method (GET, POST, PUT, DELETE)
3. Add any required headers (one per line in the format `Key: Value`)
4. For POST and PUT requests, add a JSON request body
5. Click "Send Request" to make the API call
6. View the formatted response with status code, headers, and body
7. Check your request history in the table below

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
