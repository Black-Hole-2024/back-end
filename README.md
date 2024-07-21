
# Sign Language Recognition Backend

## Project Overview

This project is a backend system for a Sign Language Recognition application. The backend is built using Flask and Flask-SQLAlchemy to manage and process the sign language data. The primary goal is to provide an API that can handle sign language data, process it, and interface with a frontend application to provide real-time translations.

## Features

- **User Management**: Create, read, update, and delete user data.
- **Sign Language Data Processing**: Handle the storage and processing of sign language data.
- **API Endpoints**: Provide RESTful API endpoints for interacting with the frontend application.
- **Database Management**: Use SQLAlchemy for database operations, supporting SQLite.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **Flask-SQLAlchemy**: An extension for Flask that adds support for SQLAlchemy, a SQL toolkit and Object-Relational Mapping (ORM) system for Python.
- **SQLite**: A C library that provides a lightweight, disk-based database.

## Project Structure

```
├── app.py
├── config.py
├── requirements.txt
├── instance
│   └── config.py
├── models.py
├── user
│   ├── __init__.py
│   └── user_routes.py
├── admin
│   └── (admin related files)
├── both
│   └── (common files)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sign-language-recognition-backend.git
   cd sign-language-recognition-backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

### Configuration

Configuration settings can be adjusted in the `config.py` file located in the `instance` directory. This file includes settings for the database URI and other Flask configurations.

### Running the Application

1. **Run the Flask development server**:
   ```bash
   flask run
   ```
   By default, the application will be available at `http://127.0.0.1:5000/`.

### API Endpoints

#### User Management

- **Create a User**: `POST /api/users`
- **Get User**: `GET /api/users/<id>`
- **Update User**: `PUT /api/users/<id>`
- **Delete User**: `DELETE /api/users/<id>`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Flask Documentation: [Flask](https://flask.palletsprojects.com/)
- Flask-SQLAlchemy Documentation: [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- SQLite Documentation: [SQLite](https://www.sqlite.org/docs.html)

---

